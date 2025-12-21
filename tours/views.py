from django.shortcuts import render
from .models import Tour, Contract, Client
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ClientForm, ContractForm
import csv
from django.http import HttpResponse

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})


@login_required
def dashboard(request):
    contracts = Contract.objects.all().order_by('-contract_date')[:10]
    clients = Client.objects.all().order_by('-id')[:10]

    context = {
        'contracts': contracts,
        'clients': clients
    }
    return render(request, 'tours/dashboard.html', context)


@login_required
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ClientForm()

    return render(request, 'tours/add_client.html', {'form': form})


@login_required
def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.manager = request.user
            contract.save()
            return redirect('dashboard')
    else:
        form = ContractForm()

    return render(request, 'tours/add_contract.html', {'form': form})

@login_required
def export_clients_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['ID', 'Имя', 'Фамилия', 'Email', 'Телефон'])

    clients = Client.objects.all()
    for client in clients:
        writer.writerow([client.id, client.first_name, client.last_name, client.email, client.phone_number])

    return response
from django.shortcuts import render
from .models import Tour, Contract, Client, EmployeeProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ClientForm, ContractForm
import csv
from django.http import HttpResponse
from .forms import ClientForm, ContractForm, TourForm # <-- Добавьте TourForm
from django.shortcuts import render, get_object_or_404
import json
from django.http import JsonResponse

def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})


@login_required
def dashboard(request):
    contracts = Contract.objects.all().order_by('-contract_date')[:10]
    clients = Client.objects.all().order_by('-id')[:10]


    try:
        profile = request.user.employeeprofile
    except EmployeeProfile.DoesNotExist:
        profile = None

    context = {
        'contracts': contracts,
        'clients': clients,
        'profile': profile,
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

    context = {
        'form': form,
        'title': 'Новый клиент',
        'button_text': 'Сохранить клиента'
    }
    return render(request, 'tours/generic_form.html', context)


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


    context = {
        'form': form,
        'title': 'Новый договор',
        'button_text': 'Сохранить договор'
    }
    return render(request, 'tours/generic_form.html', context)

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



@login_required
def add_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourForm()

    context = {
        'form': form,
        'title': 'Новый тур',
        'button_text': 'Сохранить тур'
    }
    return render(request, 'tours/generic_form.html', context)


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    reviews = tour.reviews.all().order_by('-created_at')

    context = {
        'tour': tour,
        'reviews': reviews
    }

    return render(request, 'tours/tour_detail.html', context)


@login_required
def export_contracts_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contracts.csv"'

    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response, delimiter=';')

    writer.writerow([
        'ID Договора',
        'Дата заключения',
        'Статус',
        'Клиент',
        'Телефон клиента',
        'Тур',
        'Дата начала тура',
        'Менеджер',
        'Итоговая цена',
    ])

    contracts = Contract.objects.all().select_related('client', 'tour', 'manager')
    for contract in contracts:
        writer.writerow([
            contract.id,
            contract.contract_date.strftime('%Y-%m-%d'),
            contract.get_status_display(),
            contract.client,
            contract.client.phone_number,
            contract.tour.title,
            contract.tour.start_date,
            contract.manager.username,
            contract.total_price,
        ])

    return response


@login_required
def login_redirect_view(request):
    if request.user.is_superuser:
        return redirect('/admin/')

    elif request.user.is_staff:
        return redirect('dashboard')

    else:
        return redirect('tour_list')



@login_required
def export_clients_to_json(request):
    clients = Client.objects.all()

    clients_data = list(clients.values('id', 'first_name', 'last_name', 'email', 'phone_number'))

    response = HttpResponse(
        json.dumps(clients_data, ensure_ascii=False, indent=4),  # Преобразуем в JSON-строку
        content_type="application/json; charset=utf-8",
    )
    response['Content-Disposition'] = 'attachment; filename="clients.json"'

    return response


@login_required
def export_contracts_to_json(request):
    contracts = Contract.objects.all().select_related('client', 'tour', 'manager')

    contracts_data = []
    for contract in contracts:
        contracts_data.append({
            'id': contract.id,
            'contract_date': contract.contract_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': contract.get_status_display(),
            'total_price': float(contract.total_price),
            'client': {
                'id': contract.client.id,
                'full_name': str(contract.client),
            },
            'tour': {
                'id': contract.tour.id,
                'title': contract.tour.title,
            },
            'manager': {
                'id': contract.manager.id,
                'username': contract.manager.username,
            }
        })

    response = HttpResponse(
        json.dumps(contracts_data, ensure_ascii=False, indent=4),
        content_type="application/json; charset=utf-8",
    )
    response['Content-Disposition'] = 'attachment; filename="contracts.json"'

    return response
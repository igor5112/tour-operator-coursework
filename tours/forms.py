# tours/forms.py (новый файл)
from django import forms
from .models import Client
from .models import Client, Contract, Tour


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number'] #

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['tour', 'client', 'total_price', 'status']

class TourForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['title', 'description', 'price', 'start_date', 'end_date', 'hotel']
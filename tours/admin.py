
from django.contrib import admin
from .models import Country, City, Hotel, Tour,  Transport, Review, ClientDocument, Insurance


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Tour)


from .models import EmployeeProfile, Client, Contract, Payment, Transport, Review


admin.site.register(EmployeeProfile)
admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(Transport)
admin.site.register(Review)
admin.site.register(ClientDocument)
admin.site.register(Insurance)
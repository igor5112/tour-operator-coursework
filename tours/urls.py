# tours/urls.py (это новый файл)
from django.urls import path
from . import views # импортируем файл views из текущей папки

urlpatterns = [
    # Когда пользователь заходит на главную страницу,
    # вызывай функцию tour_list из файла views.py
    path('', views.tour_list, name='tour_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

# tours/urls.py
urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/add/', views.add_client, name='add_client'), # <-- ДОБАВЬТЕ ЭТУ СТРОКУ
    path('contracts/add/', views.add_contract, name='add_contract'),
    path('export/clients/csv/', views.export_clients_to_csv, name='export_clients_csv'),
    path('tours/add/', views.add_tour, name='add_tour'),
]
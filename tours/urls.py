from django.urls import path
from . import views
urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clients/add/', views.add_client, name='add_client'),
    path('contracts/add/', views.add_contract, name='add_contract'),
    path('export/clients/csv/', views.export_clients_to_csv, name='export_clients_csv'),
    path('tours/add/', views.add_tour, name='add_tour'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('export/contracts/csv/', views.export_contracts_to_csv, name='export_contracts_csv'),
    path('login_redirect/', views.login_redirect_view, name='login_redirect'),
    path('export/clients/json/', views.export_clients_to_json, name='export_clients_json'),
    path('export/contracts/json/', views.export_contracts_to_json, name='export_contracts_json')
]
# tour_project/urls.py
from django.contrib import admin
from django.urls import path, include # <-- Добавьте include

# tour_project/urls.py
# ... существующие импорты
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # <-- ДОБАВЬТЕ ЭТУ СТРОКУ
    path('', include('tours.urls')),

]


# tours/models.py
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название страны")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название города")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities", verbose_name="Страна")
    def __str__(self):
        return f"{self.name} ({self.country.name})"
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

class Hotel(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название отеля")
    stars = models.IntegerField(verbose_name="Количество звезд")
    description = models.TextField(verbose_name="Описание")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="hotels", verbose_name="Город")
    def __str__(self):
        return f"{self.name} - {self.stars}*"
    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"

class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    description = models.TextField(verbose_name="Описание тура")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="tours", verbose_name="Отель")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"


# tours/models.py (добавление в конец файла)

from django.contrib.auth.models import User, Group


# Расширяем стандартного пользователя, чтобы добавить должность
class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    position = models.CharField(max_length=100, verbose_name="Должность")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.position})"

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Contract(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'Активен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    manager = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Менеджер")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Статус")
    contract_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заключения")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая цена")

    def __str__(self):
        return f"Договор №{self.id} с {self.client} на тур '{self.tour.title}'"

    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"


class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="payments", verbose_name="Договор")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")

    def __str__(self):
        return f"Платеж на {self.amount} по договору №{self.contract.id}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


# tours/models.py (добавление в конец файла)

class Transport(models.Model):
    TRANSPORT_CHOICES = [
        ('plane', 'Авиаперелет'),
        ('bus', 'Автобус'),
        ('train', 'Поезд'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="transport_options", verbose_name="Тур")
    type = models.CharField(max_length=10, choices=TRANSPORT_CHOICES, verbose_name="Тип транспорта")
    description = models.CharField(max_length=255, verbose_name="Описание (номер рейса, маршрут)")
    departure_time = models.DateTimeField(verbose_name="Время отправления")
    arrival_time = models.DateTimeField(verbose_name="Время прибытия")

    def __str__(self):
        return f"{self.get_type_display()} для тура '{self.tour.title}'"

    class Meta:
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорт"


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Нормально'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews", verbose_name="Тур")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Отзыв от {self.client} на тур '{self.tour.title}'"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
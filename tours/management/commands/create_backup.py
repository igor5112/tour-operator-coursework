# tours/management/commands/create_backup.py
import os
import shutil
import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Создает резервную копию БД SQLite и загружает ее на Яндекс.Диск.'

    def upload_to_yadisk(self, file_path):
        self.stdout.write(self.style.NOTICE('Начинаем загрузку на Яндекс.Диск...'))

        token = settings.YADISK_TOKEN
        app_folder = settings.YADISK_APP_FOLDER
        file_name = os.path.basename(file_path)
        yadisk_path = f'app:/{app_folder}/{file_name}'

        headers = {'Authorization': f'OAuth {token}'}
        params = {'path': yadisk_path, 'overwrite': 'true'}
        try:
            # Сначала создаем папку на Диске. Если она уже есть, API вернет ошибку, но мы ее проигнорируем.
            requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=headers,
                         params={'path': f'app:/{app_folder}'})

            # Теперь получаем ссылку на загрузку
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers,
                                    params=params)
            response.raise_for_status()
            upload_url = response.json().get('href')

            if not upload_url:
                self.stdout.write(self.style.ERROR('Не удалось получить URL для загрузки.'))
                return

            with open(file_path, 'rb') as f:
                upload_response = requests.put(upload_url, data=f)
                upload_response.raise_for_status()

            self.stdout.write(
                self.style.SUCCESS(f'Файл успешно загружен на Яндекс.Диск в папку: "Приложения/{app_folder}"'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при работе с API Яндекс.Диска: {e}'))
            if e.response:
                self.stdout.write(self.style.ERROR(f'Ответ сервера: {e.response.text}'))

    def handle(self, *args, **options):
        # ... остальная часть handle без изменений ...
        self.stdout.write(self.style.SUCCESS('Начинаем процесс резервного копирования...'))
        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file_path = os.path.join(backup_dir, f'backup_{timestamp}.sqlite3')

        try:
            shutil.copy(db_path, backup_file_path)
            self.stdout.write(self.style.SUCCESS(f'Локальная резервная копия успешно создана: {backup_file_path}'))
            self.upload_to_yadisk(backup_file_path)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла непредвиденная ошибка: {e}'))
import os
import yadisk

token = os.environ.get("YANDEX_DISK_TOKEN")
if not token:
    print("YANDEX_DISK_TOKEN не задан.")
    raise SystemExit(1)

# Проверка на не-ASCII символы
if any(ord(ch) > 127 for ch in token):
    print("Ошибка: токен содержит не-ASCII символы. Установите корректный OAuth-токен.")
    raise SystemExit(1)

y = yadisk.YaDisk(token=token)
print("check_token:", y.check_token())

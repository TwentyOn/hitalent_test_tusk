from core.celery import app
from django.core.mail import send_mail


@app.task
def send_activation_key(email, activation_key):
    send_mail(
        'Сервис прокси-доступа',
        'Здравствуйте!\n\n'
        f'Ваш новый ключ активации: {activation_key}\n\n'
        'Желаем приятного использования!',
        'proxyservice@domen.ru',
        [email]
    )

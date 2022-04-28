from django.core.mail import send_mail


def send_activation_email(code, email):
    link = f'Перейдите по ссылке чтобы активировать ваш аккаунт: http://localhost:8000/api/v1/user/activate/{code}'

    send_mail(
        'Hello!',
        link,
        'isalikharov@gmail.com',
        [email]
    )
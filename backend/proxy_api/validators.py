from django.core.exceptions import ValidationError


def protocol_validator(value):
    allowed_protocols = ('socks5', 'http', 'https')
    if value not in allowed_protocols:
        raise ValidationError(f'Некорректный протокол. Выберите один из: {", ".join(allowed_protocols)}')

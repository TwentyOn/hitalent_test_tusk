from django.apps import AppConfig
from django.db.models.signals import post_migrate


def initial_vm_records(sender, **kwargs):
    from .models import VirtualMachine
    if not VirtualMachine.objects.exists():
        VirtualMachine.objects.create(name='proxy1', host='203.236.197.76', port=8080, protocol='http')
        VirtualMachine.objects.create(name='proxy2', host='186.174.48.132', port=8080, protocol='https')
        VirtualMachine.objects.create(name='proxy3', host='209.191.114.209', port=8080, protocol='socks5')


class ProxyApiConfig(AppConfig):
    name = 'proxy_api'

    def ready(self):
        post_migrate.connect(initial_vm_records, sender=self)

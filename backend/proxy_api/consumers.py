import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import sync_to_async
from .models import VirtualMachine


class ProxyConnection(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope['user']
            self.vm = await sync_to_async(VirtualMachine.objects.get)(current_user=self.scope['user'])

            await self.accept()
            await sync_to_async(self.user.deactivate_key)()
            self.conn_info_task = asyncio.create_task(self.send_status())

        except VirtualMachine.DoesNotExist:
            await self.close(code=4000, reason='Нет зарезервированной VMS')

    async def receive(self, text_data=None, bytes_data=None):
        print("server says client message received: ", text_data)
        await self.send("Server sends Welcome")

    async def disconnect(self, code):
        if hasattr(self, 'conn_info_task'):
            self.conn_info_task.cancel()
        if hasattr(self, 'vm'):
            await sync_to_async(self.vm.release)()

    async def send_status(self):
        """
        Переодическая отправка статуса
        """
        status = {}
        while True:
            await sync_to_async(self.vm.refresh_from_db)(
                fields=['is_active', 'current_user_id']
            )
            if not self.vm.is_active:
                status['status'] = 'disconnected'
                status['detail'] = 'VPS остановлена'
            elif not self.vm.current_user_id == self.user.id:

                status['status'] = 'disconnected'
                status['detail'] = 'Доступ к VMS закрыт'
            else:
                status['status'] = 'connected'
                status['detail'] = 'всё в порядке'

            await self.send(json.dumps(status))
            await asyncio.sleep(5)

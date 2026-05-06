import json
import logging
from urllib.parse import urlparse

import websocket
from PyQt6.QtCore import QObject, pyqtSignal

from settings import BASE_URL, WEB_SOCKET_PATH

logger = logging.getLogger(__name__)


class WebSocketWorker(QObject):
    finished = pyqtSignal(bool)
    is_connect = pyqtSignal(bool)
    status_msg = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.ws = None

    def run(self):
        try:
            self.status_msg.emit('Соединение...')
            host = urlparse(BASE_URL).netloc
            path = WEB_SOCKET_PATH.replace('{user_id}', str(self.user_id))
            # websocket.enableTrace(True)
            self.ws = websocket.WebSocketApp(
                f'ws://{host}{path}',
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.run_forever()
        except Exception as err:
            self.status_msg('Отключено')
            self.error.emit(f'Ошибка соединения {str(err)}')

    def stop(self):
        try:
            if self.ws:
                self.ws.close()
                self.finished.emit(True)
        except Exception as err:
            logger.error(err, exc_info=True)

    def on_message(self, ws, message):
        try:
            status = json.loads(message)
            self.status_msg.emit(
                f'Статус: {status.get("status")}\n'
                f'Детали: {status.get("detail")}'
            )
        except Exception as err:
            logger.error(err, exc_info=True)

    def on_error(self, ws, error):
        logger.error(error)

    def on_close(self, ws, close_status_code, close_msg):
        self.status_msg.emit('Отключено')
        self.is_connect.emit(False)
        self.stop()
        logger.info("### closed ###")

    def on_open(self, ws):
        self.status_msg.emit('Подключено')
        self.is_connect.emit(True)
        logger.info("Opened connection")

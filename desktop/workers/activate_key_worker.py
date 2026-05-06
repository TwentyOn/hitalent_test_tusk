import logging

from PyQt6.QtCore import QObject, pyqtSignal
import requests

from settings import BASE_URL, ACTIVATE_KEY_PATH

logger = logging.getLogger(__name__)

class KeyActivateWorker(QObject):
    conn_data = pyqtSignal(dict)
    finished = pyqtSignal(bool)
    status_msg = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, activation_key):
        super().__init__()
        self.activation_key = activation_key

    def run(self):
        self.status_msg.emit('Проверка ключа...')

        try:
            response = requests.post(
                f'{BASE_URL}{ACTIVATE_KEY_PATH}',
                {'activation_key': self.activation_key},
                timeout=5,
            )
            response.raise_for_status()
            self.conn_data.emit(response.json())
        except requests.exceptions.HTTPError as err:
            if response.status_code == 400:
                detail = response.json()
                if detail:
                    detail = detail.popitem()
                    detail = map(lambda i: i.pop(0) if isinstance(i, list) else i, detail)
                    detail = ': '.join(detail)
                else:
                    detail = f'Ошибка запроса. Статус: {response.status_code}'

                self.status_msg.emit('Отключено')
                self.error.emit(detail)
            else:
                self.error.emit(f'Ошибка активации ключа: {err}')
                self.status_msg.emit('Отключено')

        except requests.exceptions.ConnectionError as err:
            self.error.emit('Сервер недоступен')
            self.status_msg.emit('Отключено')

        except Exception as err:
            logger.error(err, exc_info=True)

        finally:
            self.finished.emit(True)

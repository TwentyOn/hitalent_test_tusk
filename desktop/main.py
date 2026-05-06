import sys
import logging

from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QThread, QObject

from workers.websocket_client_worker import WebSocketWorker
from workers.activate_key_worker import KeyActivateWorker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProxyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Прокси сервис")
        self.setFixedSize(500, 400)
        self.setup_ui()

        self.ws_client: None | QObject = None
        self.ws_thread: None | QThread = None

        self.act_key_worker: None | QObject = None
        self.act_key_thread: None | QThread = None

    def setup_ui(self):
        # Центральный виджет
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Заголовок
        title = QLabel("Добро пожаловать")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title")
        layout.addWidget(title)

        # Поле ввода
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Введите ваш ключ...")
        self.input_field.setObjectName("input")
        layout.addWidget(self.input_field)

        # Кнопки
        self.conn_button = QPushButton("Подключиться")
        self.conn_button.setObjectName("btn")
        self.close_btn = QPushButton('Отключится')
        self.close_btn.setObjectName('btn')
        self.close_btn.setVisible(False)
        layout.addWidget(self.conn_button)
        layout.addWidget(self.close_btn)

        # Статус бар для сообщений
        self.status_label = QLabel("Готов к подключению")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("status")
        layout.addWidget(self.status_label)

        # Применяем стили
        self.apply_styles()

        # Подключаем события
        self.conn_button.clicked.connect(self.on_connect)
        self.close_btn.clicked.connect(self.on_disconnect)

    def apply_styles(self):
        """Применяем CSS стили"""
        try:
            with open('styles.qss', 'r', encoding='utf-8') as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            logger.error('Ошибка применения стилей', exc_info=True)

    def on_connect(self):
        """
        Слот для сигнала нажатия кнопки соединения
        """
        try:
            activation_key = self.input_field.text()

            if not activation_key:
                QMessageBox.information(self, 'Внимание', 'Введите ключ активации')
                return

            self.conn_button.setEnabled(False)
            self.act_key_worker = KeyActivateWorker(activation_key)
            self.act_key_thread = QThread()
            self.act_key_worker.moveToThread(self.act_key_thread)

            self.act_key_thread.started.connect(self.act_key_worker.run)
            self.act_key_worker.finished.connect(self.act_key_thread.quit)
            self.act_key_worker.finished.connect(self.act_key_worker.deleteLater)
            self.act_key_thread.finished.connect(self.act_key_thread.deleteLater)

            self.act_key_worker.conn_data.connect(self.on_get_conn_data)
            self.act_key_worker.status_msg.connect(self.on_change_status)
            self.act_key_worker.error.connect(self.on_error)
            self.act_key_worker.finished.connect(self.on_finish_check_key)

            self.act_key_thread.start()

        except Exception as err:
            logger.error('Ошибка соединения', exc_info=True)

    def on_get_conn_data(self, conn_params: dict):
        """
        Слот для обработки сигнала получения данных соединения
        """
        try:
            self.ws_client = WebSocketWorker(conn_params['user_id'])
            self.ws_thread = QThread()
            self.ws_client.moveToThread(self.ws_thread)

            # слоты и сигналы
            self.ws_thread.started.connect(self.ws_client.run)
            self.ws_client.finished.connect(self.ws_thread.quit)
            self.ws_client.finished.connect(self.ws_client.deleteLater)
            self.ws_thread.finished.connect(self.ws_thread.deleteLater)

            self.ws_client.is_connect.connect(self.connection_change)
            self.ws_client.status_msg.connect(self.on_change_status)
            self.ws_client.error.connect(self.on_error)

            self.ws_thread.start()
        except Exception as err:
            logger.error('Ошибка соединения Web Socket', exc_info=True)

    def on_disconnect(self):
        """
        Слот для сигнала нажатия кнопки отсоединения
        :return:
        """

        try:
            if self.ws_client:
                self.ws_client.stop()
        except Exception as err:
            logger.error('Ошибка закрытия соединения', exc_info=True)

    def on_change_status(self, status_msg: str):
        """
        Слот для сигнала изменения status_label
        """
        try:
            self.status_label.setText(status_msg)
        except Exception as err:
            logger.error('', exc_info=True)

    def on_error(self, error_msg: str):
        """
        Слот для сигнала ошибки - обрабатывает ошибки в потоках
        """
        try:
            QMessageBox.critical(self, 'Ошибка', error_msg)
        except Exception as err:
            logger.error('', exc_info=True)

    def connection_change(self, is_conn: bool):
        """
        Слот для сигнала изменения статуса соединения
        (соединен / несоединен) и измененя интерфейса
        """
        try:
            if is_conn:
                self.conn_button.setVisible(False)
                self.close_btn.setVisible(True)
                self.status_label.setText('Подключено')
            else:
                self.conn_button.setVisible(True)
                self.close_btn.setVisible(False)
                self.status_label.setText('Отключено')
        except Exception as err:
            logger.error('', exc_info=True)

    def on_finish_check_key(self, finish):
        """
        Слот для сигнала завершения проверки ключа
        """
        self.conn_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProxyWindow()
    window.show()
    sys.exit(app.exec())

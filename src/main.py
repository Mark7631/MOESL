import sys
import getpass
import socket
from dataclasses import dataclass

from PySide6.QtCore import QCoreApplication

from PySide6.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow
from handlers import CmdHandler


@dataclass
class ShellData:
    """Класс содержит информацию для консоли(графического интерфейса)"""
    user: str
    machine: str
    path: str = "~"

    @property
    def get_cmd_promt(self):
        """Возращает стандартную строку приглошения как в bash"""
        return f"{self.user}@{self.machine}:{self.path}"

    @property
    def get_window_title(self):
        """Возвращает заголовок окна на основе реальных данных ОС"""
        return f"Эмулятор - [{self.user}@{self.machine}]"


class App(QMainWindow, Ui_MainWindow):
    """Класс инициализации графического интерфейса"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data = ShellData(
            user=getpass.getuser(),
            machine=socket.gethostname())

        self.cmd_handler = CmdHandler()

        self._init_ui()
        self._connect_events()

    def _init_ui(self):
        """Замена стандартного текста на актуальный"""
        self.setWindowTitle(self.data.get_window_title)
        self.cmd_promt.setText(self.data.get_cmd_promt)

    def _connect_events(self):
        """Подключение функций для взаимодействия с пользователем"""
        self.cmd_line.returnPressed.connect(self._enter)
        self.enter_btn.clicked.connect(self._enter)

    def _enter(self):
        """Обрабатывает данные по нажатию кнопки или Enter"""
        cmd_result = self.cmd_handler.process(self.cmd_line.text())
        match cmd_result.type:
            case "text_only":
                self.out_window.append(self._get_standart_out(cmd_result.text))
            case "error":
                self.out_window.append(self._get_standart_out(cmd_result.text))
            case "exit":
                exit_app()
            case _:
                self.out_window.append("internal unknown error\n")

        self.cmd_line.setText("")

    def _get_standart_out(self, text):
        """Возвращает строку приглошения и данные введеные пользователем"""
        return f"{self.cmd_promt.text()} {self.cmd_line.text()}\n{text}"


def exit_app():
    QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

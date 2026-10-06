import sys
import getpass
import socket
import argparse
import csv
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from PySide6.QtCore import QCoreApplication

from PySide6.QtWidgets import QApplication, QMainWindow

from design import Ui_MainWindow
from handlers import CmdHandler, ScriptHandler


@dataclass
class ShellData:
    """Класс содержит информацию для программы"""
    user: str = getpass.getuser()
    machine: str = socket.gethostname()
    path: str = "~"
    vfs_path: str = "."
    cmd_promt: str = f"{user}@{machine}:{path}"
    log_path: str = "./logs.csv"
    strt_scr_path: str | None = None

    @property
    def get_cmd_promt(self):
        """Возращает стандартную строку приглошения как в bash"""
        return f"{self.user}@{self.machine}:{self.path}"

    @property
    def get_window_title(self):
        """Возвращает заголовок окна на основе реальных данных ОС"""
        return f"Эмулятор - [{self.user}@{self.machine}]"


def program_args():
    """Обрабатывает аргументы запуска приложения"""
    parser = argparse.ArgumentParser()

    parser.add_argument("--vfs-path", required=True)
    parser.add_argument("--cmd-promt", required=False)
    parser.add_argument("--log-path", required=False)
    parser.add_argument("--strt-scr-path", required=False)

    return parser.parse_args()


def init_shell_data():
    """Инициализирует данные для программы"""
    args = program_args()
    data = ShellData(vfs_path=args.vfs_path)
    if args.cmd_promt is not None:
        data.cmd_promt = args.cmd_promt
    if args.log_path is not None:
        try:
            Path(args.log_path)
        except (TypeError, ValueError):
            print("Invalid argument --log-path", ValueError)
            exit()
        if not args.log_path.lower().endswith(".csv"):
            print("Invalid format of log file, not .csv")
            exit()
        data.log_path = args.log_path
    if args.strt_scr_path is not None:
        try:
            file_path = Path(args.strt_scr_path)
            if not file_path.is_file():
                print("Script file doesn't exist at written path")
                exit()
        except (TypeError, ValueError):
            print("Invalid argument --strt-scr-path", ValueError)
            exit()
        data.strt_scr_path = args.strt_scr_path
    return data


class App(QMainWindow, Ui_MainWindow):
    """Класс инициализации графического интерфейса"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.data = init_shell_data()
        self.log_path = Path(self.data.log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        self.cmd_handler = CmdHandler()

        self._init_ui()
        self._connect_events()

        if self.data.strt_scr_path is not None:
            self.script_handler = ScriptHandler()
            self._strt_scr_run()

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
        self._log([datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  self.cmd_line.text()])
        cmd_result = self.cmd_handler.process(self.cmd_line.text())
        print(cmd_result)
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

    def _log(self, data: list[str]):
        """Сохраняет логи о командах в файл"""
        with self.log_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def _strt_scr_run(self):
        """Функция для выполнения стартовых скриптов"""
        file_path = Path(self.data.strt_scr_path)

        with file_path.open("r", encoding="utf-8") as file:
            for line in file:
                cmd = self.script_handler.process(line.strip())
                if isinstance(cmd, ValueError):
                    self.cmd_line.setText(line.strip())
                    self._enter()
                elif cmd != "":
                    self.cmd_line.setText(cmd)
                    self._enter()


def exit_app():
    QCoreApplication.quit()


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

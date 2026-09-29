import shlex

from dataclasses import dataclass


@dataclass
class CmdResult:
    """Класс для представленния результата обработанной комманды"""
    type: str
    text: str = ""


class CmdHandler():
    def process(self, cmd) -> CmdResult:
        """Контролирует процесс обработки команды"""
        try:
            parsed_cmd = self._parse(cmd)
        except ValueError as err:
            return CmdResult("error", str(err))

        if not parsed_cmd:
            return CmdResult("text_only")
        return self._handle(self, parsed_cmd)

    @staticmethod
    def _parse(cmd):
        """Разбивает строку команды с учётом кавычек"""
        parsed_args = shlex.split(cmd)
        return parsed_args

    @staticmethod
    def _handle(self, parsed_args: list[str]):
        """Основной обработчик разбитой команды"""
        cmd_name = parsed_args[0]
        match cmd_name:
            case "cd":
                output = CmdResult("text_only", " ".join(parsed_args))
                return output
            case "ls":
                output = CmdResult("text_only", " ".join(parsed_args))
                return output
            case "exit":
                output = CmdResult("exit", "")
                return output
            case _:
                output = CmdResult("error", self._get_unkwn_cmd_err(cmd_name))
                return output

    @staticmethod
    def _get_unkwn_cmd_err(cmd_name):
        """Возвращает форматированную строку ошибки о неизвестной комманде"""
        return f"Command \'{cmd_name}\' not found"

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
        return self._handle(parsed_cmd)

    def _parse(self, cmd):
        """Разбивает строку команды с учётом кавычек"""
        parsed_args = shlex.split(cmd)
        return parsed_args

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

    def _get_unkwn_cmd_err(self, cmd_name):
        """Возвращает форматированную строку ошибки о неизвестной комманде"""
        return f"Command \'{cmd_name}\' not found"


class ScriptHandler:
    def process(self, line):
        """Контролирует процесс обработки команды из скрипта"""
        try:
            parsed_line = self._parse(line)
        except ValueError as err:
            return err

        if parsed_line == []:
            return ""
        return self._handle(parsed_line)

    def _parse(self, line):
        """Разбивает строку команды с учётом кавычек"""
        parsed_args = shlex.split(line)
        return parsed_args

    def _handle(self, parsed_args: list[str]):
        """Обрабатывает комманду с учётом кавычек"""
        for i in range(0, len(parsed_args)):
            if " " in parsed_args[i]:
                parsed_args[i] = "\"" + parsed_args[i] + "\""
        out_s = ""
        if parsed_args[0] != "#":
            out_s += parsed_args[0]
        else:
            return ""
        
        for i in range(1, len(parsed_args)):
            if parsed_args[i] == "#":
                return out_s
            out_s += f" {parsed_args[i]}"
        return out_s

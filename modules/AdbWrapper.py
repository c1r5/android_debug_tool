import subprocess


class Adb:
    _arguments: list = ["adb"]

    def __init__(self):
        ...

    @staticmethod
    def add_argument(*kwargs) -> None:
        Adb._arguments.extend(list(kwargs))

    @staticmethod
    def get_arguments() -> list:
        return Adb._arguments

    @staticmethod
    def run_command() -> subprocess.CompletedProcess:
        cmd = subprocess.run(
            Adb.get_arguments(),
            capture_output=True
        )

        Adb._arguments = Adb._arguments[0:1]

        return cmd


class AdbShell (Adb):
    _arguments = ["adb", "shell"]

    def __init__(self):
        super().__init__()
        ...

    @staticmethod
    def add_argument(*kwargs) -> None:
        AdbShell._arguments.extend(list(kwargs))

    @staticmethod
    def get_arguments() -> list:
        return AdbShell._arguments

    @staticmethod
    def run_command() -> subprocess.CompletedProcess:
        cmd = subprocess.run(
            AdbShell.get_arguments(),
            capture_output=True
        )

        AdbShell._arguments = AdbShell._arguments[0:2]

        return cmd



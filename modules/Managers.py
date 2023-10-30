from modules.AdbWrapper import AdbShell
from time import sleep


class ProcessManager(AdbShell):
    def __init__(self, package_name: str):
        super().__init__()
        self.package_name = package_name
        ...

    @staticmethod
    def pidof(package_name) -> str:
        AdbShell.add_argument("pidof", package_name)
        result = AdbShell.run_command().stdout.decode().strip()
        return result

    def run(self) -> str:
        AdbShell.run_command()

        AdbShell.add_argument("monkey", "-p", self.package_name)
        AdbShell.add_argument("-c", "android.intent.category.LAUNCHER 1")

        print("[+] Running process...")

        AdbShell.run_command()

        sleep(1)

        return ProcessManager.pidof(self.package_name)


class PackageManager(AdbShell):
    def __init__(self, package_name: str):
        super().__init__()
        self.packageId = package_name

    def clear(self) -> None:
        self.add_argument("pm", "clear", self.packageId)
        cmd = self.run_command()

        if cmd.stdout.decode().strip().lower() == "success":
            return
        else:
            raise Exception("error_at_app_clearing")

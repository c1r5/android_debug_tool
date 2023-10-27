from modules.AdbWrapper import Adb, PackageManager, AdbShell
from time import sleep

class StaticAnalysis:
    def __init__(self, target: str, port: int, persistent: int = 1):
        self.target = target
        self.port = port
        self.pm = PackageManager(target)
        self.persist_debug = persistent
        ...

    def run(self) -> None:
        print(f"[+] Clearing {self.target}...")
        self.pm.clear()

        print("[+] Setting app to debug mode...")

        AdbShell.add_argument("am", "set-debug-app", "-w")
        AdbShell.add_argument(self.target)

        AdbShell.run_command()

        print("[+] Starting app....")

        AdbShell.add_argument("monkey", "-p", self.target)
        AdbShell.add_argument("-c", "android.intent.category.LAUNCHER 1")

        AdbShell.run_command()

        print("[+] Setting up JDWP connection...")

        sleep(1)

        app_pid = self.pm.pidof(self.target)

        Adb.add_argument("forward")
        Adb.add_argument(f"tcp:{str(self.port)}")
        Adb.add_argument(f"jdwp:{app_pid}")

        Adb.run_command()

        input('Press enter to stop debugging...')

        self.pm.clear()

        AdbShell.add_argument("am", "clear-debug-app", self.target)
        AdbShell.run_command()
        Adb.add_argument("forward", "--remove-all")

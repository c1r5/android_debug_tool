from modules.AdbWrapper import Adb, PackageManager, AdbShell
from time import sleep


class StaticAnalysis:
    def __init__(self, target: str, port: int):
        self.target = target
        self.port = port
        self.pm = PackageManager(target)

    def reset(self) -> None:
        print(f"[+] Clearing all...")

        self.pm.clear()

        print("[+] Turning off app debug mode...")
        AdbShell.add_argument("am", "clear-debug-app", self.target)
        AdbShell.run_command()
        Adb.add_argument("forward", "--remove-all")

        Adb.run_command()

    def run(self) -> None:
        self.reset()

        AdbShell.add_argument("am", "set-debug-app", "-w")
        AdbShell.add_argument(self.target)

        print("[+] Setting app to debug mode...")
        AdbShell.run_command()

        AdbShell.add_argument("monkey", "-p", self.target)
        AdbShell.add_argument("-c", "android.intent.category.LAUNCHER 1")

        print("[+] Starting app....")
        AdbShell.run_command()

        sleep(1)

        app_pid = self.pm.pidof(self.target)

        Adb.add_argument(
            "forward",
            f"tcp:{str(self.port)}",
            f"jdwp:{app_pid}"
        )

        print("[+] Setting up JDWP binding...")

        cmd = Adb.run_command()
        if cmd.returncode == 0:
            input('[+] Press enter to stop debugging...')
            self.reset()
        else:
            print("[+] Error at JDWP Binding...")

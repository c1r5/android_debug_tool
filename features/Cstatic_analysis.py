from modules.AdbWrapper import Adb, AdbShell
from modules.Managers import PackageManager, ProcessManager
from argparse import Namespace
from modules.FridaLoader import FridaScriptLoader


class StaticAnalysis:
    def __init__(self, arguments: Namespace):
        self.target = arguments.target
        self.port = arguments.port
        self.script = arguments.script

        self.pm = PackageManager(arguments.target)
        self.ps = ProcessManager(arguments.target)
        self.frida = FridaScriptLoader(arguments.target)

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

        if not self.script:
            self.ps.run()
        else:
            self.frida.add_script(self.script)
            self.frida.run()

        app_pid = self.ps.pidof(self.target)

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

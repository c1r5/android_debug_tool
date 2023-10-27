from modules.argument_handler import app_arguments
from modules.checklist import check_adb
from modules.AdbWrapper import AdbShell, Adb
from features.Cstatic_analysis import StaticAnalysis
from tabulate import tabulate
import frida


def main():
    check_adb_return: dict = check_adb()

    # Check if adb check is success if not returns reason
    if not check_adb_return.get("success"):
        return print(f'[-] adb check error because {check_adb_return.get("reason")}')

    arguments = app_arguments()
    match arguments.subcommand:
        case "static":
            static_mode = StaticAnalysis(arguments.target, arguments.port)
            static_mode.run()
        case "package":
            if not arguments.list_packages:
                device = frida.get_usb_device()
                processes = device.enumerate_applications()
                table = list(
                    map(
                        lambda x: [x.name, x.identifier, x.pid if x.pid != 0 else "-"],
                        processes
                    )
                )
                print(tabulate(table, headers=["Name", "Package", "PID"]))
                ...
        case _:
            raise Exception("anything_here")


if __name__ == '__main__':
    main()

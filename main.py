from modules.argument_handler import app_arguments
from modules.checklist import check_adb
from features.Cstatic_analysis import StaticAnalysis
from tabulate import tabulate
from multiprocessing import freeze_support
import frida


def main():
    check_adb_return: dict = check_adb()

    # Check if adb check is success if not returns reason
    if not check_adb_return.get("success"):
        return print(f'[-] adb check error because {check_adb_return.get("reason")}')

    arguments = app_arguments()
    match arguments.subcommand:
        case "static":
            static_mode = StaticAnalysis(arguments)
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
            print("[-] Command not found!")
            print("Use: adt --help")


if __name__ == '__main__':
    freeze_support()
    main()

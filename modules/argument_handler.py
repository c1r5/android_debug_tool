import argparse


def app_arguments():
    parser = argparse.ArgumentParser(
        prog="adt",
        description="Android application analysis tool to turn easy analysis settings"
    )
    # Arguments for package utils feature
    subparsers = parser.add_subparsers(dest="subcommand")
    # create a static mode call command
    static_mode_subcmd = subparsers.add_parser("static")

    # set target package Eg. adt static -t com.example
    static_mode_subcmd.add_argument(
        "-t",
        "--target",
        metavar="com.example"
    )

    # (Optional) set debugger jvm port Eg. adt static -p 8000 default: 8000
    static_mode_subcmd.add_argument(
        "-p",
        "--port",
        metavar="8000",
        default=8000,
        type=int,
        help="(Optional) Jdwp bind port set to debugger Eg. Android Studio / Intellij IDEA"
    )

    parsed = parser.parse_args()

    return parsed

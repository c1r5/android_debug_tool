import subprocess


check_result: dict = {
    "success": False,
    "reason": ""
}


# check if adb exists or device is connected to
def check_adb() -> dict:

    command = subprocess.run(
        [
            "adb",
            "devices"
        ], capture_output=True
    )

    formatted_output = list(filter(lambda s: len(s) > 0, command.stdout.decode().split('\n')))

    if command.stdout and len(formatted_output) == 2:
        check_result["success"] = True
        check_result["reason"] = "ok"
    elif len(formatted_output) == 1:
        check_result["reason"] = "device not found"
    else:
        print(len(formatted_output))

        check_result["reason"] = "adb not found"

    return check_result


def check_screen_state():
    ...

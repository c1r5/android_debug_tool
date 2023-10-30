import frida
import time


class FridaScriptLoader:
    _scripts: list = []
    _processes: list = []
    _device = frida.get_usb_device()

    def __init__(self, package_name: str):
        if package_name:
            self.add_process(package_name)
        ...

    @staticmethod
    def add_script(path_to_script: str) -> None:
        with open(path_to_script, mode='r', encoding='utf8') as script:
            FridaScriptLoader._scripts.append(script.read())

    @staticmethod
    def add_process(package_name: str) -> None:
        FridaScriptLoader._processes.append(package_name)

    @staticmethod
    def run() -> None:
        print("[+] Running process...")
        psid = FridaScriptLoader._device.spawn(FridaScriptLoader._processes)
        time.sleep(1)
        FridaScriptLoader._device.resume(psid)
        session = FridaScriptLoader._device.attach(psid)
        script = session.create_script('\n'.join(FridaScriptLoader._scripts))
        script.load()


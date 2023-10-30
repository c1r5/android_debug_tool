import time
import os
import sys
from modules.Managers import ProcessManager
import frida

f = open(os.devnull, 'w')
sys.stdout = f

package_name = "br.com.brb.digitalflamengo"

device = frida.get_usb_device()

psid = device.spawn([
    package_name
])

time.sleep(1)

device.resume(psid)

session = device.attach(psid)

script = session.create_script(open("../f1.js").read())

script.load()

input()

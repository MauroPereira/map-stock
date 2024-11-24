# Mensaje dinámico
import os
import time

if os.name == "posix":
    var = "clear"
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
    var = "cls"

time.sleep(2)

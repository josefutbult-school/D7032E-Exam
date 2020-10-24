from telnetlib import Telnet
from Networking.adress import IP, PORT

# Why make it harder than this?
with Telnet(IP, PORT) as tn:
    tn.interact()

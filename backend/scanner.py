from scapy.all import ARP, Ether, srp
from mac_vendor_lookup import MacLookup
from db import upsert_device

mac_lookup = MacLookup()

def get_vendor(mac):
    try:
        return mac_lookup.lookup(mac)
    except Exception:
        return "Unknown"

def scan_network(ip_range="192.168.50.0/24"):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        vendor = get_vendor(received.hwsrc)
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc,
            "vendor": vendor
        })
        upsert_device(received.hwsrc, received.psrc, vendor)

    return devices

if __name__ == "__main__":
    found = scan_network()
    print(f"Found {len(found)} devices:")
    for d in found:
        print(f"  {d['ip']:<15} {d['mac']:<20} {d['vendor']}")

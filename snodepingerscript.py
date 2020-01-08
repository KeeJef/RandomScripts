import requests 
import json 
import time
import platform    # For getting the operating system name
import subprocess  # For executing a shell command

_zalpha = ['y', 'b', 'n', 'd', 'r', 'f', 'g', '8',
           'e', 'j', 'k', 'm', 'c', 'p', 'q', 'x',
           'o', 't', '1', 'u', 'w', 'i', 's', 'z',
           'a', '3', '4', '5', 'h', '7', '6', '9']


def zb32_encode(buf):
    s = str()
    bits = 0
    l = len(buf)
    idx = 0
    tmp = buf[idx]
    while bits > 0 or idx < l:
        if bits < 5:
            if idx < l:
                tmp <<= 8
                tmp |= buf[idx] & 0xff
                idx += 1
                bits += 8
            else:
                tmp <<= 5 - bits
                bits = 5
        bits -= 5
        s += _zalpha[(tmp >> bits) & 0x1f]
    return s

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '4', host]

    return subprocess.call(command) == 0

headers = {'Content-Type': 'application/json',}
data = '{"jsonrpc":"2.0","id":"0","method":"get_service_nodes", \"params\": {\"service_node_pubkeys\": []}}'
response = requests.post('http://imaginary.stream:38157/json_rpc', headers=headers,  data=data)
response = response.content.decode('utf-8')
response = json.loads(response)
response = response['result']

counter = 0
routersreachable = 0

print("got " + str(len(response['service_node_states'])) + " routers")

while len(response['service_node_states']) != counter:

    snversion =  response['service_node_states'][counter]['service_node_version'][0]

    if (response['service_node_states'][counter]['active'] == False) or (snversion != 6):
        counter += 1 
        continue

    time.sleep(60) 

    snEDkey = response['service_node_states'][counter]['pubkey_ed25519']
    lokiaddress = zb32_encode(bytes.fromhex(snEDkey)) + ".snode"
    print("checking " + lokiaddress + " number " + str(counter) + " router")
    pingresponse = ping(lokiaddress)

    if pingresponse:
        
        print("got successful response")
        routersreachable += 1
        pass

    counter += 1 
    
    pass

print('there was ' + str(routersreachable) + ' out of a total of ' + str(len(response['service_node_states'])))

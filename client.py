import time
import sys, requests
import json

def redirectToLeader(server_address, message):
    type = message["type"] 
    while True: 
        if type == "get":
            try:
                response = requests.get(server_address, json=message, timeout=1)
            except Exception as e:
                return e
        else:
            try:
                response = requests.put(server_address, json=message, timeout=1)
            except Exception as e:
                return e 
        if response.status_code == 200 and "payload" in response.json():
            payload = response.json()["payload"]
            if "message" in payload:
                server_address = payload["message"] + "/request"
            else:
                break
        else:
            break 
    return response.json()
def put(addr, key, value, broker_id, broker_host, broker_port, security_protocol, rack_id, method):
    server_address = addr + "/request"
    payload = {'key': key, 'value': value, "brokerId": broker_id, "brokerHost": broker_host,"brokerPort": broker_port,"securityProtocol": security_protocol,"method": method,"rackId": rack_id }
    message = {"type": "put", "payload": payload}
    print(redirectToLeader(server_address, message))


def get(addr, key):
    server_address = addr + "/request"
    payload = {'key': key}
    message = {"type": "get", "payload": payload}
    print(redirectToLeader(server_address, message))
def generate_metadata(broker_id, broker_host, broker_port, security_protocol, rack_id,method):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    metadata = {
        "type": "metadata",
        "name": "RegistrationChangeBrokerRecord",
        "fields": {
            "brokerId": broker_id,   
            "brokerHost": broker_host,   
            "brokerPort": broker_port,   
            "securityProtocol": security_protocol,   
            "method": method,   
            "rackId": rack_id,   
            "epoch": 0   
        },
        "timestamp": timestamp
    }
    return metadata

def load_metadata(filename):
    try:
        with open(filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}

def dump_metadata(metadata):
    filename = "client_metadata.json"
    
    with open(filename, 'a') as json_file:
        json.dump(metadata, json_file, indent = 4)

if __name__ == "__main__":
    if len(sys.argv) == 8:
        addr = sys.argv[1]
        broker_id = int(sys.argv[2])
        broker_host = sys.argv[3]
        broker_port = sys.argv[4]
        security_protocol = sys.argv[5]
        rack_id = sys.argv[6]
        key = sys.argv[7]
        method='get'
        metadata = generate_metadata(broker_id, broker_host, broker_port, security_protocol, rack_id, method)
        
        print(metadata)
        dump_metadata(metadata)
        get(addr, key, )
    elif len(sys.argv) == 9:
        addr = sys.argv[1]
        broker_id = int(sys.argv[2])
        broker_host = sys.argv[3]
        broker_port = sys.argv[4]
        security_protocol = sys.argv[5]
        rack_id = sys.argv[6]
        key = sys.argv[7]
        val = sys.argv[8]
        method='put'
        metadata = generate_metadata(broker_id, broker_host, broker_port, security_protocol, rack_id, method)
        print(metadata)
        dump_metadata(metadata)
        put(addr, key, val, broker_id, broker_host, broker_port, security_protocol, rack_id, method)
    else:
        print("PUT usage: python3 client.py address 'key' 'value'")
        print("GET usage: python3 client.py address 'key'")
        print("Format: address: http://ip:port")

from raftnode import Node
from raftnode import FOLLOWER, LEADER
from flask import Flask, request, jsonify
import sys
import logging
import time
import json
import random
import string
app = Flask(__name__)
@app.route("/request", methods=['GET'])
def value_get():
    payload = request.json["payload"]
    print(payload)

    reply = {"code": 'fail', 'payload': payload}
    if n.status == LEADER:
        result = n.handle_get(payload)
        if result:
            reply = {"code": "success", "payload": result}

            
    elif n.status == FOLLOWER:
        reply["payload"]["message"] = n.leader
    return jsonify(reply)


@app.route("/vote_req", methods=['POST'])
def vote_req():
    term = request.json["term"]
    commitIdx = request.json["commitIdx"]
    staged = request.json["staged"]
    choice, term = n.decide_vote(term, commitIdx, staged)
    message = {"choice": choice, "term": term}
    return jsonify(message)


@app.route("/request", methods=['PUT'])
def value_put():
    payload = request.json["payload"]
    reply = {"code": 'fail'}
    brokerId=payload['brokerId']
    brokerHost=payload['brokerHost']
    brokerPort=payload['brokerPort']
    securityProtocol=payload['securityProtocol']
    method=payload['method']  
    value=payload['value']
       
    
    
    print(brokerHost, brokerId)
    if n.status == LEADER:
        result = n.handle_put(payload)
        if result:
            reply = {"code": "success"}
            metadata = generate_metadata(brokerId, brokerHost, brokerPort, securityProtocol, method, n.status)
            dump_metadata(metadata)
            random_string = generate_random_string(10)
            m2=gen_met(random_string, value)
            dump_meta2(m2)

    elif n.status == FOLLOWER:
        payload["message"] = n.leader
        reply["payload"] = payload
    return jsonify(reply)

@app.route("/heartbeat", methods=['POST'])
def heartbeat():
    term, commitIdx = n.heartbeat_follower(request.json)
    message = {"term": term, "commitIdx": commitIdx}
    return jsonify(message)

log = logging.getLogger('werkzeug')
log.disabled = True

def generate_random_string(length):
    characters = string.ascii_letters + string.digits  # includes letters (both cases) and digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def gen_met(random_string, value):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    metadata = {
        "type": "metadata",
        "name": "TopicRecord",
        "fields": {
            "topicUUID": random_string,   
            "name": value 
        },
        "timestamp": timestamp
    }
    return metadata

def generate_metadata(broker_id, broker_host, broker_port, security_protocol, method, status):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    metadata = {
        "type": "metadata",
        "name": "RegisterBrokerRecord",
        "fields": {
            "brokerId": broker_id,   
            "brokerHost": broker_host,   
            "brokerPort": broker_port,   
            "securityProtocol": security_protocol,   
            "method": method,
            "brokerStatus":status
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
    filename = "server_metadata.json"
    
    with open(filename, 'a') as json_file:
        json.dump(metadata, json_file, indent = 4)
def dump_meta2(m2):
    filename = "topicRecord_metadata.json"
    
    with open(filename, 'a') as json_file:
        json.dump(m2, json_file, indent = 4)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        index = int(sys.argv[1])
        portfile = sys.argv[2]
        ports = []
        with open(portfile) as f:
            for ip in f:
                ports.append(ip.strip())
        mip = ports.pop(index)

        http, host, port = mip.split(':')
        n = Node(ports, mip)
        app.run(host="0.0.0.0", port=int(port), debug=False)
    else:
        print("bruh")

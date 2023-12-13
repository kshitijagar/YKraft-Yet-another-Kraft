# RR-Team-63-YAKt-Yet-Another-KRaft-
Repo for RR-Team 63-YAKt (Yet Another KRaft)
# Distributed Key-Value Store with Raft Consensus Algorithm

This is a simple implementation of a distributed key-value store using the Raft consensus algorithm. The system consists of three components:

1. **Node**: Represents a server in the distributed system. It handles Raft protocol, leader election, and key-value operations.

2. **Client**: Interacts with the distributed system by making requests to the server. It supports both 'get' and 'put' operations.

3. **Server**: Implements a Flask-based web server to handle client requests, participate in the Raft consensus algorithm, and maintain metadata storage.

## Files

- `node.py`: Implementation of the Node class that represents a server in the distributed system.

- `client.py`: Client implementation for making 'get' and 'put' requests to the distributed system.

- `server.py`: Flask-based server that handles client requests, participates in Raft consensus, and maintains metadata storage.

## Metadata Storage

The system maintains metadata records such as `RegisterBrokerRecord` and `TopicRecord`. Metadata is stored in a key-value format, resembling the specified structure.

## Usage

### Starting a Server

```bash
python server.py <index> <ip_list_file>
<index>: Index of the server in the IP list.
<ip_list_file>: File containing a list of IP addresses.
Running a Client
Get Request
bash
Copy code
python client.py <address> <broker_id> <broker_host> <broker_port> <security_protocol> <rack_id> <key>
Put Request
bash
Copy code
python client.py <address> <broker_id> <broker_host> <broker_port> <security_protocol> <rack_id> <key> <value>
<address>: Server address in the format http://ip:port.
Metadata Generation
bash
Copy code
python client.py <address> <broker_id> <broker_host> <broker_port> <security_protocol> <rack_id> <key>
Metadata Storage
Metadata records are stored in a file named metadata.json.

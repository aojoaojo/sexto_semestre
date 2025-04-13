server_connections = [
    {
        "id": 1,
        "command": "ssh lista-05-cs-aesestrutura555@74.235.160.126",
        "password": "rb8bd"
    },
    {
        "id": 2,
        "command": "ssh lista-05-cs-aeschavedarodada654@74.235.160.126",
        "password": "cjn6w"
    },
    {
        "id": 3,
        "command": "ssh lista-05-cs-aeschavedarodada654@74.235.160.126",
        "password": "6hdqz"
    },
    {
        "id": 4,
        "command": "ssh lista-05-cs-aesdifusao502@74.235.160.126",
        "password": "nyw1v"
    },
    {
        "id": 5,
        "command": "ssh lista-05-cs-finalmenteaes452@74.235.160.126",
        "password": "sefxy"
    },
    {
        "id": 6,
        "command": "ssh lista-05-cs-aesuso328@74.235.160.126",
        "password": "bxwc3"
    },
    {
        "id": 7,
        "command": "ssh lista-05-cs-desaes336@74.235.160.126",
        "password": "atcdd"
    },
    {
        "id": 8,
        "command": "ssh lista-05-cs-modos1232@74.235.160.126",
        "password": "orr5y"
    },
    {
        "id": 9,
        "command": "ssh lista-05-cs-modos2620@74.235.160.126",
        "password": "ham1v"
    },
    {
        "id": 10,
        "command": "ssh lista-05-cs-modos3327@74.235.160.126",
        "password": "prhk4"
    }
]

import sys
import os

if len(sys.argv) != 2:
    print("Usage: python conexao_servers.py <server_id>")
    sys.exit(1)

server_id = int(sys.argv[1])

server = next((s for s in server_connections if s["id"] == server_id), None)

if not server:
    print(f"Server with ID {server_id} not found.")
    sys.exit(1)

print(f"Connecting to server ID {server_id}...")
os.system(f"sshpass -p {server['password']} {server['command']}")
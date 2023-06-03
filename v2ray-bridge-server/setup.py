#!/usr/bin/python3

import uuid
import json
import secrets
from pathlib import Path
import os 

# LOAD CONFIG FILE

path = Path(__file__).parent
file = open(str(path.joinpath('v2ray/config/config.json')), 'r', encoding='utf-8')
config = json.load(file)

# LOAD DOCKER-COMPOSE FILE

docker_compose_file = open(str(path.joinpath('../docs/docker-compose-ptunnel-bridge-sample.yml')), 'r', encoding='utf-8')

# INPUT: PTUNNEl

upstreamIP = ''
ptunnel_verification = input("Do you want to use PTunnel? (y/n): \n")
if ptunnel_verification.lower() == 'y' or ptunnel_verification.lower() == 'yes':
    ptunnel_pass = input("Password for ptunnel: (Leave empty to generate a random one)\n")
    if(ptunnel_pass == ''):
        ptunnel_pass = secrets.token_hex(16)
        print(ptunnel_pass)
    upstreamIP = '10.71.71.1'
    ptunnel_upstreamIP = ''
elif ptunnel_verification.lower() != 'n' and ptunnel_verification.lower() != 'no':
    print('Invalid input. Exiting...')
    exit(1)

# INPUT: UPSTREAM-IP

defaultUpstreamIP = config['outbounds'][0]['settings']['vnext'][0]['address']
if defaultUpstreamIP == '<UPSTREAM-IP>':
    message = "Upstream IP:\n"
else:
    message = f"Upstream IP: (Leave empty to use `{defaultUpstreamIP}`)\n"

if upstreamIP != '10.71.71.1':
    upstreamIP = input(message)
else:
    ptunnel_upstreamIP = input(message)
    defaultUpstreamIP = ptunnel_upstreamIP
if upstreamIP != '':
    config['outbounds'][0]['settings']['vnext'][0]['address'] = upstreamIP

# INPUT: UPSTREAM-UUID

defaultUpstreamUUID = config['outbounds'][0]['settings']['vnext'][0]['users'][0]['id']
if defaultUpstreamUUID == '<UPSTREAM-UUID>':
    message = "Upstream UUID:\n"
else:
    message = f"Upstream UUID: (Leave empty to use `{defaultUpstreamUUID}`)\n"

upstreamUUID = input(message)
if upstreamUUID != '':
    config['outbounds'][0]['settings']['vnext'][0]['users'][0]['id'] = upstreamUUID

# CONFIGURE INBOUNDS

for i, inbound in enumerate(config['inbounds']):
    if inbound['protocol'] == 'vmess':
        defaultUUID = inbound['settings']['clients'][0]['id']
        if defaultUUID == '<BRIDGE-UUID>':
            message = "Bridge UUID: (Leave empty to generate a random one)\n"
        else:
            message = f"Bridge UUID: (Leave empty to use `{defaultUUID}`)\n"

        bridgeUUID = input(message)
        if bridgeUUID == "":
            if defaultUUID == '<BRIDGE-UUID>':
                bridgeUUID = str(uuid.uuid4())
                print(bridgeUUID)
            else:
                bridgeUUID = defaultUUID

        config['inbounds'][i]['settings']['clients'][0]['id'] = bridgeUUID

    if inbound['protocol'] == 'shadowsocks':
        defaultPassword = inbound['settings']['password']
        if defaultPassword == '<SHADOWSOCKS-PASSWORD>':
            message = "Shadowsocks Password: (Leave empty to generate a random one)\n"
        else:
            message = f"Shadowsocks Password: (Leave empty to use `{defaultPassword}`)\n"

        bridgePassword = input(message)
        if bridgePassword == "":
            if defaultPassword == '<SHADOWSOCKS-PASSWORD>':
                bridgePassword = secrets.token_urlsafe(16)
                print(bridgePassword)
            else:
                bridgePassword = defaultPassword

        config['inbounds'][i]['settings']['password'] = bridgePassword

# SAVE CONFIG FILE

content = json.dumps(config, indent=2)
open(str(path.joinpath('v2ray/config/config.json')), 'w', encoding='utf-8').write(content)

# CREATE DOCKER-COMPOSE FILE

docker_compose_content = docker_compose_file.read()
if(upstreamIP != '10.71.71.1'):
    docker_compose_content = docker_compose_content.split("hans")[0]
else:
    command = ["hans.sh", "-u", "nobody", "-d", "hans", "-v", "-f", "-c", ptunnel_upstreamIP, "-p", ptunnel_pass, "-qi", "-m", "1450"]
    docker_compose_content += "\n    command: {}".format(command)

filename = 'docker-compose.yml'
if os.path.isfile(filename):
    # If the file exists, open it and overwrite its contents with the new content
    with open(filename, "w") as f:
        f.write(docker_compose_content)
else:
    # If the file doesn't exist, create it and write the new content to it
    with open(filename, "x") as f:
        f.write(docker_compose_content)

# PRINT OUT RESULT

print('Done!')


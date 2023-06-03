#!/usr/bin/python3

import uuid
import json
from pathlib import Path
import secrets
import os 

# LOAD CONFIG FILE

path = Path(__file__).parent.joinpath('v2ray/config/config.json')
file = open(str(path), 'r', encoding='utf-8')
config = json.load(file)

# LOAD DOCKER-COMPOSE FILE

docker_compose_file = open(str(Path(__file__).parent.joinpath('../docs/docker-compose-ptunnel-upstream-sample.yml')), 'r', encoding='utf-8')

# INPUT: PTUNNEl

ptunnel_pass = None
ptunnel_verification = input("Do you want to use PTunnel? (y/n): \n")
if ptunnel_verification.lower() == 'y' or ptunnel_verification.lower() == 'yes':
    ptunnel_pass = input('Password for ptunnel: (Leave empty to generate a random one)\nDo not include "(" or ")" in password\n')
    if(ptunnel_pass == ''):
        ptunnel_pass = secrets.token_hex(16)
        print(ptunnel_pass)
elif ptunnel_verification.lower() != 'n' and ptunnel_verification.lower() != 'no':
    print('Invalid input. Exiting...')
    exit(1)

# INPUT: UPSTREAM UUID

defaultUUID = config['inbounds'][0]['settings']['clients'][0]['id']
if defaultUUID == '<UPSTREAM-UUID>':
    message = "Upstream UUID: (Leave empty to generate a random one)\n"
else:
    message = f"Upstream UUID: (Leave empty to use `{defaultUUID}`)\n"

upstreamUUID = input(message)
if upstreamUUID == '':
    if defaultUUID == '<UPSTREAM-UUID>':
        upstreamUUID = str(uuid.uuid4())
    else:
        upstreamUUID = defaultUUID

config['inbounds'][0]['settings']['clients'][0]['id'] = upstreamUUID

# SAVE CONFIG FILE

content = json.dumps(config, indent=2)
open(str(path), 'w', encoding='utf-8').write(content)

# CREATE DOCKER-COMPOSE FILE

docker_compose_content = docker_compose_file.read()
if(ptunnel_pass == None):
    docker_compose_content = docker_compose_content.split("hans")[0]
else:
    command = ["hans.sh", "-m", "1450", "-s", "10.71.71.0", "-p", ptunnel_pass, "-f", "-r", "-u", "nobody", "-d", "hans"]
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
print('Upstream UUID:')
print(upstreamUUID)
print('\nDone!')


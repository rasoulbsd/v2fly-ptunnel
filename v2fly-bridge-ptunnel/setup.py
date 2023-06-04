#!/usr/bin/python3

import json
from pathlib import Path

# LOAD CONFIG FILE

path = Path(__file__).parent
docker_compose_file = open(str(path.joinpath('docker-compose.yml')), 'r', encoding='utf-8')
docker_compose_contents = docker_compose_file.read()

docker_compose_contents_splitted = docker_compose_contents.split("\n")
line_count = 0
for line in docker_compose_contents_splitted:
    if line.find("command:") != -1:
        command_line = line
        break
    line_count += 1

credentials_file = open(str(path.joinpath('../credentials.json')), 'r', encoding='utf-8')
credentials = json.load(credentials_file)

# INPUT: UPSTREAM-IP

upstream_ip = credentials['UPSTREAM_IP']
command_line = command_line.replace("<upstream_ip>", upstream_ip)

# Ptunnel Password: READ FROM ENVIRONMENT VARIABLE

ptunnel_password = credentials['PTUNNEL_PASSWORD']
command_line = command_line.replace("<ptunnel_password>", ptunnel_password)

# SAVE DOCKER-COMPOSE FILE

docker_compose_contents_splitted[line_count] = command_line
docker_compose_contents = "\n".join(docker_compose_contents_splitted)

open(str(path.joinpath('docker-compose.yml')), 'w', encoding='utf-8').write(docker_compose_contents)

# PRINT OUT RESULT

print('Done!')

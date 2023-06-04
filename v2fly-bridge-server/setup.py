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

# PRINT OUT RESULT

print('Done!')


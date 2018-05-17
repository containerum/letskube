import os
import requests
import time
import json
import configparser

def create_droplets(token, tag, ssh_keys):
    url = "https://api.digitalocean.com/v2/droplets"
    headers = {"Authorization": "Bearer {}".format(token)}
    data = {"names":
            [
                "m1.train",
                "s1.train"
            ],
            "region": "nyc3",
            "size": "s-1vcpu-1gb",
            "image": "centos-7-x64",
            "ssh_keys": [ssh_keys],
            "backups": False,
            "ipv6": False,
            "user_data": None,
            "private_networking": True,
            "tags": ["travis-ci", tag]}
    r = requests.post(url, headers=headers, json=data)
    if 200 <= r.status_code < 300:
        print("droplets created")

def get_droplets(token, tag):
    url = "https://api.digitalocean.com/v2/droplets"
    headers = {"Authorization": "Bearer {}".format(token)}
    data = {"tag_name": tag}
    r = requests.get(url, headers=headers, params=data)
    return json.loads(r.text)

def wait_status(token, tag):
    start = time.time()
    counter = 0
    print("Wait active status")
    while time.time() < start + 120:
        counter += 1
        print("# {}".format(counter))
        droplets = get_droplets(token, tag)
        all_status = True
        for droplet in droplets["droplets"]:
            name_droplet = droplet["name"]
            status_droplet = droplet["status"]
            print(name_droplet, status_droplet)
            if status_droplet != "active":
                all_status = False
        if all_status:
            time.sleep(60) #wait loading
            break
        time.sleep(2)

def get_ip_for_droplets(token, tag):
    network = {}
    droplets = get_droplets(token, tag)
    for droplet in droplets["droplets"]:
        name_droplet = droplet["name"]
        network_droplet = droplet["networks"]["v4"]
        network[name_droplet] = {}
        for ip in droplet["networks"]["v4"]:
            type = ip["type"]
            ip_addr = ip["ip_address"]
            network[name_droplet][type] = ip_addr
    return network

def get_inventory(path=None):
    inventory = configparser.ConfigParser(allow_no_value=True, delimiters=('\t', ' '))
    if path:
        inventory.read(path)
    return inventory

def change_inventory(inventory, network):
    for droplet in network:
        node = droplet
        public_ip = network[droplet]['public']
        private_ip = network[droplet]['private']
        param = "ansible_user=root ansible_host={} ansible_port=22 private_ip={}".format(public_ip, private_ip)
        inventory.set("all", node, param)


def write_inventory(inventory, path=None):
    with open(path, 'w') as f:
        inventory.write(f)

def get_env():
    return os.environ['DO_TOKEN'], os.environ['TRAVIS_BUILD_ID'], os.environ['DO_SSH_KEYS']

if __name__ == "__main__":
    token, tag, ssh_keys = get_env()

    create_droplets(token, tag, ssh_keys)
    wait_status(token, tag)

    network = get_ip_for_droplets(token, tag)
    inventory = get_inventory(path="inventory")
    change_inventory(inventory, network)
    write_inventory(inventory, path="inventory")

#i just need some changes in file, don't pay attention on this d.t.

import os
import requests

def delete_droplets(token, tag):
    url = "https://api.digitalocean.com/v2/droplets"
    headers = {"Authorization": "Bearer {}".format(token)}
    data = {"tag_name": tag}
    r = requests.delete(url, headers=headers, params=data)
    if 200 <= r.status_code < 300:
        print("droplets deleted")


if __name__ == "__main__":
    token = os.environ['DO_TOKEN']
    tag = os.environ['TRAVIS_BUILD_ID']
    delete_droplets(token=token, tag=tag)
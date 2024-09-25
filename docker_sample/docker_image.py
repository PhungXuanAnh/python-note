import json

import docker

client = docker.from_env()

for image in client.images.list():
    # print(image.tags)
    # print(image.labels)
    print(image.attrs)
    break

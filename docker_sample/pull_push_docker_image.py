# pip install docker

import json

import docker
from docker.models.images import Image

client = docker.from_env()

# docker images -a | grep none | awk '{ print $3; }' | xargs docker rmi --force

# NOTE: change this based on your image version, using command: di | grep europe-docker.pkg | grep -v "none"
mapping_image_tag = {
    # "europe-docker.pkg.dev/viralize-143916/monetize/viralize-web:latest": "alexander1307xa/sh-web",
    "europe-docker.pkg.dev/viralize-143916/monetize/viralize-api:latest": "alexander1307xa/sh-api",
    # "europe-docker.pkg.dev/viralize-143916/monetize/ecg-sessionizer:latest": "alexander1307xa/sh-ss",
    # "europe-docker.pkg.dev/viralize-143916/monetize/pagetests:vvm": "alexander1307xa/sh-test",
    # "europe-docker.pkg.dev/viralize-143916/infra/druid-vm-importer:latest": "alexander1307xa/sh-druid1",
    # "europe-docker.pkg.dev/viralize-143916/monetize/vr-postgres:latest": "alexander1307xa/sh-db",
    # "europe-docker.pkg.dev/viralize-143916/monetize/druid:latest": "alexander1307xa/sh-druid",
    # "europe-docker.pkg.dev/viralize-143916/infra/kafka:2.12-2.3.0": "alexander1307xa/sh-kafka",
}


def list_old_amd64_docker_image() -> list[Image]:
    images = []
    print('List old amd64 docker images')
    for image in client.images.list():
        if image.tags and 'europe-docker.pkg.de' in image.tags[0]:
            images.append(image)
            print(image.tags[0])
    return images


def list_alexander1307xa_docker_image(arch) -> list[Image]:
    print(f'List new {arch} docker images')
    images = []
    for image in client.images.list():
        if image.tags and "alexander1307xa" in image.tags[0]:
            images.append(image)
            print(image.tags)
    return images


def _get_new_image_tag(image_name):
    for old, new in mapping_image_tag.items():
        if old == image_name:
            return new


def _get_old_image_tag(image_name):
    for old, new in mapping_image_tag.items():
        if new == image_name:
            return old


def rename_tag_docker_image(images: list[Image], arch):
    for image in images:
        old_tag = image.tags[0]
        new_tag = _get_new_image_tag(old_tag)
        # print(new_name, new_version)
        if new_tag:
            image.tag(new_tag + arch)
            client.images.remove(old_tag)


def revert_amd64_to_origin_docker_image_name(images: list[Image]):
    for image in images:
        new_tag = image.tags[0]
        new_name, _ = new_tag.split(":")
        old_tag = _get_old_image_tag(new_name[:-6])
        if old_tag:
            old_name, old_version = old_tag.split(":")
            # print(new_name, new_version)
            image.tag(old_name, old_version)
            client.images.remove(new_tag)


def push_image(images: list[Image]):
    for image in images:
        for tag in image.tags:
            print('Pushing: ', tag)
            resp = client.images.push(tag, stream=True, decode=True)
            for line in resp:
                print(line)

def pull_docker_image_arm64():
    for old, new in mapping_image_tag.items():
        print('Pulling: ', old)
        client.images.pull(old, platform='linux/arm64')

old_amd64_images = list_old_amd64_docker_image()
# rename_tag_docker_image(old_amd64_images, '-amd64')
# new_amd64_images = list_alexander1307xa_docker_image("amd64")
# # push_image(new_amd64_images)

# pull_docker_image_arm64()
# rename_tag_docker_image(old_amd64_images, "-arm64")
# new_arm64_images = list_alexander1307xa_docker_image("arm64")
# push_image(new_arm64_images)

# revert_amd64_to_origin_docker_image_name(new_amd64_images)
# list_old_amd64_docker_image()

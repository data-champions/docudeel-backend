#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examples/ references
# https://dutchcloudcommunity.nl/nieuws/wire/aws-news-blog-lightsail-containers-an-easy-way-to-run-your-containers-in-the-cloud/

# ci based workflow
# https://medium.com/generac-clean-energy/deploy-multi-container-service-on-aws-lightsail-c0e1b9de9726
# https://github.com/arch-inc/amazon-lightsail-containers-test/blob/master/.github/workflows/deploy.yml

Deploy a container image to lightsail.
Container config is made here on the fly to avoid hard-coding variables.

"""

import json
import os
import re
import subprocess
import sys
from time import sleep
from urllib import request


SLACK_URL = 'https://hooks.slack.com/services/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'  # noqa :E501


def run_bash(command: str) -> None:
    try:
        process = subprocess.run(command, shell=True,
                                 check=True, capture_output=True)
        out = process.stdout.decode("utf-8").strip()
    except Exception as e:
        print(e)
        out = None
    return out


def get_last_git_hash() -> str:
    return run_bash("git rev-parse --short HEAD")


def make_config(service_name: str,
                service_name_lightsail: str,
                config_fp: str) -> None:
    container_configs = {
        service_name: {
            "image": service_name_lightsail,
            "ports": {
                "5000": "HTTP"
            },
            # TODO
            # "environment": {
            #     "AWS_ACCESS_KEY_ID": os.environ['AWS_ACCESS_KEY_ID'],
            #     "AWS_SECRET_ACCESS_KEY": os.environ['AWS_SECRET_ACCESS_KEY']
            # }
        }
    }

    config = {
        "serviceName": service_name,
        "containers": container_configs,
        "publicEndpoint": {
            "containerName": service_name,
            "containerPort": 5000
        }
    }
    print(f'{config=}')
    with open(config_fp, 'w') as outfile:
        json.dump(config, outfile, indent=4)
    print(f'config created at {config_fp}')
    return None


def build_image(img_name_and_tag: str) -> None:
    build_img = f"""docker build . -t {img_name_and_tag}"""
    out = run_bash(build_img)
    # see if it works
    is_built = out.endswith(img_name_and_tag)
    if is_built:
        print(f'Docker build succesful with: \n{out}')
    else:
        print(f'Docker build failed with: \n{out}')
        sys.exit(1)
    return None


def create_service_if_not_exist(service_name: str,
                                size: str = 'nano') -> None:
    list_images = f"aws lightsail get-container-services --service-name {service_name}"
    out = run_bash(list_images)
    if out is not None:
        cmd = f"aws lightsail update-container-services --service-name {service_name} --power {size} --scale 1"
        print('service already exist... updating')
    else:
        print('service does not exist... creating')
        cmd = f"""aws lightsail create-container-service --service-name {service_name} --power {size} --scale 1"""
    out = run_bash(cmd)
    print(out)
    return None


def push_container_img(service_name, img_name_and_tag) -> str:
    push_image = f"""aws lightsail push-container-image --service-name {service_name} --label {service_name} --image {img_name_and_tag}"""
    out = run_bash(push_image)
    service_name_lightsail = [x for x in re.findall('"([^"]*)"', out)
                              if service_name in x]
    if not service_name_lightsail:
        print(out)
        raise RuntimeError(f'Container pushed does not have service name but has {service_name=}')
    service_name_lightsail = service_name_lightsail[0]
    return service_name_lightsail


def send_slack_message(message: str,
                       url: str = SLACK_URL) -> None:
    req = request.Request(url, method="POST")
    req.add_header('Content-Type', 'application/json')
    data = {
        "text": message
    }
    data = json.dumps(data)
    data = data.encode()
    r = request.urlopen(req, data=data)
    content = r.read()
    print(content)
    return None


def deploy_service(config_fp) -> None:
    deploy = f"""aws lightsail create-container-service-deployment --cli-input-json file://{config_fp}"""
    deploy_out = run_bash(deploy)
    if deploy_out is None:
        ci_url = 'https://app.circleci.com/pipelines/github/o-nexus-org/gui?filter=all'
        send_slack_message(f'lighstail deployment failed check {ci_url=}')
    print(f'{deploy_out=}')
    print('finished!')
    return None


if __name__ == '__main__':

    size = 'nano'
    service_name = 'docudeel-backend'
    git_hash = get_last_git_hash()
    img_name_and_tag = f"gui:{git_hash}"
    config_fp = run_bash('grep config.json .gitignore')

    build_image(img_name_and_tag=img_name_and_tag)
    create_service_if_not_exist(service_name=service_name,
                                size=size)
    service_name_lightsail = push_container_img(service_name, img_name_and_tag)

    make_config(service_name=service_name,
                service_name_lightsail=service_name_lightsail,
                config_fp=config_fp)

    deploy_service(config_fp=config_fp)
    # wait that the server is 100% up
    sleep(4.4 * 60)
    send_slack_message(f'deployment finished w/ {size=}!')

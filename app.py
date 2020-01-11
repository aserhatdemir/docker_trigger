from flask import Flask, request
from flask import abort
import json
import docker


app = Flask(__name__)


def docker_deploy(payload):
    log_payload(payload)
    repo_name, container_name, tag = get_docker_info(payload)
    client = docker.from_env()
    image = client.images.pull(f'{repo_name}:{tag}')
    if image:
        container = client.containers.run(f'{container_name}:{tag}', detach=True)
        if container:
            return "Container deployed"
    return None


def log_payload(payload):
    try:
        with open('payload.json', 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
            print("Payload is logged")
            return "Success"
    except IOError:
        print("Payload could not be logged to the file!!")
        return None


def get_docker_info(payload_data):
    repo = payload_data["repository"]
    push_data = payload_data["push_data"]
    return repo["repo_name"], repo["name"], push_data["tag"]


@app.route('/trigger', methods=['POST'])
def trigger_deploy():
    payload = request.get_json()
    result = docker_deploy(payload)
    if result:
        return result
    abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

from flask import Flask, request
from flask import abort
import json


app = Flask(__name__)


def deploy(payload):
    try:
        with open('payload.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)
        return True
    except OSError:
        return None


@app.route('/trigger', methods=['POST'])
def trigger_deploy():
    payload = request.get_json()
    result = deploy(payload)
    if result:
        return result
    abort(404)

if __name__ == '__main__':
    app.run()

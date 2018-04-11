from ansible_wrapper import PlaybookRunner
from flask import Flask, jsonify, abort, make_response, request
from os import environ

app = Flask(__name__)

# environ('GITHUB_API_KEY')
GITHUB_API_KEY = environ.get('GITHUB_API_KEY')
GITHUB_ORG = environ.get('GITHUB_ORG')
GITHUB_TEAM = environ.get('GITHUB_TEAM')


@app.route('/', methods=['POST'])
def refresh():
    runner = PlaybookRunner(
        playbook='fetch_keys.yml',
        extra_vars={
            "github_api_key": GITHUB_API_KEY,
            "github_org": GITHUB_ORG,
            "github_team": GITHUB_TEAM
        },
        verbosity=0
    )
    stats = runner.run()
    if stats is None:
        raise Exception("WUT")


if __name__ == '__main__':
    app.run(debug=True)

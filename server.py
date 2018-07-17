from flask import Flask, jsonify, abort, make_response
from os import environ

from ansible_wrapper import PlaybookRunner
from log import log
from distutils.util import strtobool
import logging

app = Flask(__name__)

# environ('GITHUB_API_KEY')
GITHUB_API_KEY = environ.get('GITHUB_API_KEY')
GITHUB_ORG = environ.get('GITHUB_ORG')
GITHUB_TEAM = environ.get('GITHUB_TEAM')
CHECK_MODE = strtobool(environ.get('CHECK_MODE', 'True'))

log.setLevel(logging.DEBUG)

log.debug("Starting")
log.debug("Github Org: {github_org}".format(github_org=GITHUB_ORG))
log.debug("Github Team: {github_team}".format(github_team=GITHUB_TEAM))
log.debug("Check mode: {check_mode}".format(check_mode=CHECK_MODE))


@app.route('/', methods=['POST'])
@app.route('/refresh-accesses', methods=['POST'])
def refresh():
    runner = PlaybookRunner(
        playbook='fetch_keys.yml',
        extra_vars={
            "github_api_key": GITHUB_API_KEY,
            "github_org": GITHUB_ORG,
            "github_team": GITHUB_TEAM
        },
        check_mode=CHECK_MODE,
        verbosity=5
    )
    try:
        runner.run()
    except Exception as e:
        print(e)
        abort(500, jsonify({'result': 'failed', 'error': str(e)}))
    return make_response(jsonify({'result': 'success'}))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

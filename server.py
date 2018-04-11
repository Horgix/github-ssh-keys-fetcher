from ansible_wrapper import PlaybookRunner
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def refresh():
    runner = PlaybookRunner(
        playbook='fetch_keys.yml',
        verbosity=0
    )
    stats = runner.run()
    if stats is None:
        raise Exception("WUT")


if __name__ == '__main__':
    app.run(debug=True)

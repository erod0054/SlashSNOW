from flask import Flask, request
from create_incident import create_incident
import get_user_id
import os

app = Flask(__name__)

@app.route('/ticket', methods=['POST'])
def ticket():
    token = request.form['token']
    if 'A7zfgcg4hXw49CkGDhlph4Sd' not in token:
        abort(403)
    slack_user = request.form['user_id']
    task_for = get_user_id.get_snow_uid(get_user_id.get_user_id(slack_user))
    short_desc = request.form['text']
    incident = create_incident(task_for, short_desc)
    return incident

@app.route('/test', methods=['GET', 'POST'])
def test():
    token = request.form['token']
    if '3tBQjvHmvHuJIzN8qYlQjnze' not in token:
        abort(403)
    user_info = request.form
    return repr(user_info)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

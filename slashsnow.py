from flask import Flask, request
from create_incident import create_incident
import get_user_id
import os
import yaml

app = Flask(__name__)

@app.route('/ticket', methods=['POST'])
def rackerex_ticket():

    conf_file = os.path.expanduser('~/snowconfig.yaml')
    with open(conf_file,'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        auth_token = str(cfg['rackerex']['auth'])

    token = request.form['token']
    if auth_token not in token:
        abort(403)
    slack_user = request.form['user_id']
    task_for = get_user_id.get_snow_uid(get_user_id.get_user_id(slack_user))
    short_desc = request.form['text']
    queue = 'Racker Experience'
    incident = create_incident(task_for, short_desc, queue)
    return incident

@app.route('/asops', methods=['POST'])
def asops_ticket():

    conf_file = os.path.expanduser('~/snowconfig.yaml')
    with open(conf_file,'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        auth_token = str(cfg['asops']['auth'])

    token = request.form['token']
    if auth_token not in token:
        abort(403)
    slack_user = request.form['user_id']
    task_for = get_user_id.get_snow_uid(get_user_id.get_user_id(slack_user))
    short_desc = request.form['text']
    queue = 'ASOPS'
    incident = create_incident(task_for, short_desc, queue)
    return incident

@app.route('/test', methods=['GET', 'POST'])
def test():

    conf_file = os.path.expanduser('~/snowconfig.yaml')
    with open(conf_file,'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        auth_token = str(cfg['test']['auth'])

    token = request.form['token']
    if auth_token not in token:
        abort(403)
    user_info = request.form
    return repr(user_info)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

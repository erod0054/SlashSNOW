import requests
import json
import base64
import yaml
import os
import argparse
from pprint import pprint as pp

conf_file = os.path.expanduser('~/snowconfig.yaml')
with open(conf_file,'r') as ymlfile:
    cfg = yaml.load(ymlfile)
    snow_user = str(cfg['production']['user'])
    snow_pwd = base64.b64decode(str(cfg['production']['passwd']))
    slack_token = str(cfg['production']['slack_token'])

def get_user_id(slack_userid):

    headers = {"Authorization": "Bearer " + slack_token, "Accept": "application/json"}
    url = 'https://api.slack.com/scim/v1/Users/{0}'.format(slack_userid)
    user_email = requests.get(url, headers=headers).json()['emails'][0]['value']
    return user_email

def get_snow_uid(user_email):
    # Set the request parameters
    url = 'https://rackspace.service-now.com/sys_user_list.do?JSON&sysparm_query=emailLIKE{0}'.format(user_email)
    headers = {"Accept":"application/json", "Content-Type":"application/json"}
    user_name = requests.get(url, auth=(snow_user, snow_pwd), headers=headers).json()['records'][0]['user_name']
    return user_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task_for")
    args = parser.parse_args()
    task_for = args.task_for
    
    print(get_snow_uid(get_user_id(task_for)))

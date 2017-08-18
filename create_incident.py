import requests
import json
import base64
import argparse
import yaml
import os
import sys
import calendar
import time
from ConfigParser import SafeConfigParser
from pprint import pprint as pp

def create_incident(task_for, short_desc, queue):

    time_now = int(time.time())
    #Import SNOW user credentials from config.yaml
    conf_file = os.path.expanduser('~/snowconfig.yaml')
    with open(conf_file,'r') as ymlfile:
        cfg = yaml.load(ymlfile)

        if 'Racker Experience' in queue:
            user = str(cfg['rackerex']['user'])
            pwd = base64.b64decode(str(cfg['rackerex']['passwd']))
            short_desc = short_desc
            opened_for = task_for
            category = 'inc_rackspace'
            sub_category = 'inc_change_service'
            sub_subcategory = 'inc_system_issue'
            assignment_group = 'Racker Experience'
            contact_type = 'Other'
            other = 'Slack ticket'
            urgency = '2'
            impact = '2'

        elif 'ASOPS' in queue:
            user = str(cfg['asops']['user'])
            pwd = base64.b64decode(str(cfg['asops']['passwd']))
            short_desc = short_desc
            opened_for = task_for
            category = 'inc_rackspace'
            sub_category = 'inc_nextgen'
            sub_subcategory = 'inc_operational'
            assignment_group = 'Automation Services Operations'
            contact_type = 'Other'
            other = 'Slack ticket'
            urgency = '1'
            impact = '2'

    log_file = 'log'
    with open(log_file,'r+') as f:
        existing = f.read().splitlines()
        #print existing
        for item in existing:
            if short_desc in item:
                incident_exists = 'It appears you already have an open incident, {0}, for this problem.  Try searching Service-Now to check the status.'.format(item[0:10])
                return incident_exists
                #print 'it is in existing'
                #sys.exit(0)
            else:
                #print 'Running create'
                pass

        # Set the request parameters
        url = 'https://rackspace.service-now.com/api/now/import/u_incident'

        # Set proper headers
        headers = {"Accept":"application/json", "Content-Type":"application/json"}

        # Add data
        data = {'short_description': short_desc, 'category': category, 'subcategory': sub_category, 'u_sub_subcategory': sub_subcategory, 'u_other': other, 'u_task_for': task_for, 'caller_id': task_for, 'assignment_group': assignment_group, 'contact_type': contact_type, 'urgency': urgency, 'impact': impact}
        data = json.dumps(data)

        # Do the HTTP request
        response = requests.post(url, auth=(user, pwd), headers=headers, data=data)

        # Check for HTTP codes other than 200
        if '20' not in str(response.status_code): 
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
            exit()

        time_now = int(time.time()) 
        r = response.json()
        incident_number = r['result'][0]['display_value']
        incident_link = 'https://rackspace.service-now.com/nav_to.do?uri=incident.do?sys_id={0}'.format(r['result'][0]['sys_id'])
        f.write('{0},{1},{2},{3}\n'.format(incident_number, task_for, short_desc, time_now))
        return '<{1}|{0}> has been created in Service-Now.  You are encouraged to add information and update the urgency at the link provided.'.format(incident_number, incident_link)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task_for")
    parser.add_argument("-d", "--short_desc")
    args = parser.parse_args()
    task_for = args.task_for
    short_desc = args.short_desc

    create_incident = create_incident(task_for, short_desc)
    if 'already' in create_incident:
        print(create_incident)
    else:
        print('Your incident for {0} has been created as {1}'.format(short_desc, create_incident))

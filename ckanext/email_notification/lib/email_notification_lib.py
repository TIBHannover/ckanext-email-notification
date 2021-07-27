# encoding: utf-8
import ckan.plugins.toolkit as toolkit
from datetime import datetime as _time
from sqlalchemy import true


class Helper():

    def get_new_users(time_delta):
        users = toolkit.get_action('user_list')({},{})
        new_users = []
        for user in users:        
            registration_delta = _time.now() - _time.strptime(user['created'], '%Y-%m-%dT%H:%M:%S.%f')
            if registration_delta.total_seconds() <= time_delta + 1:                
                temp = {}
                temp['name'] = user['name']                
                temp['email'] = user['email']            
                new_users.append(temp)

        return new_users
    

    def get_sysadmins_email():
        users = toolkit.get_action('user_list')({},{})
        sysadmins_emails = []        
        for user in users:
            if  user['sysadmin']:
                sysadmins_emails.append(user['email'])

        return sysadmins_emails
    

    def create_email_body(users_list):
        body = ""
        print(toolkit.config.get('ckan.site_url'))
        if 'test' in toolkit.config.get('ckan.site_url'):
            body += '---------This is Test Server---------- \n \n'
        body += "These users just registered in CKAN. Please add them to an organization and/or group. \n \n"
        for user in users_list:
            if user['name']:
                body += ('Username:  ' + user['name'] + '\n')
            if user['email']:
                body += ('Email:  ' + user['email'] + '\n')
                body += '----------- \n'

        return body
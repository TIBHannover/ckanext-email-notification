# encoding: utf-8
import ckan.plugins.toolkit as toolkit
from datetime import datetime as _time


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

    
    def get_users_without_organization():
        target_users = []        
        all_users = toolkit.get_action('user_list')({},{})
        for user in all_users:
            if not Helper.has_membership(user['id']):
                temp = {}
                temp['name'] = user['name']                
                temp['email'] = user['email']  
                target_users.append(temp)        

        return target_users

    
    def has_membership(user_id):
        params = {'all_fields' : 'True', 'include_users': 'True'}
        organizations = toolkit.get_action('organization_list')({},params)
        for org in organizations:
            for member in org['users']:
                if member['id'] == user_id:
                    return True
        
        return False


    def get_sysadmins_email():
        users = toolkit.get_action('user_list')({},{})
        sysadmins_emails = []        
        for user in users:
            if  user['sysadmin']:
                sysadmins_emails.append(user['email'])

        return sysadmins_emails
    

    def create_email_body(users_list, is_reminder=False):
        body = ""
        body = "----Email from CKAN ---- \n"
        if is_reminder:
            body += "These users do not have any ornaganization yet. \n \n"
        else:
            body += "These users just registered in CKAN. Please add them to an organization and/or group. \n \n"
            
        for user in users_list:
            if user['name']:
                body += ('Username:  ' + user['name'] + '\n')
            if user['email']:
                body += ('Email:  ' + user['email'] + '\n')
                body += '----------- \n'

        return body
    
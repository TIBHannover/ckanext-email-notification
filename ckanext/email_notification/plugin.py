import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.jobs as jobs
from flask import Blueprint
from datetime import datetime as _time

# time interval used for checking the new user(s) (past 2 minutues)
TIME_DELTA = 120

def get_new_users():
    users = toolkit.get_action('user_list')({},{})
    new_users = []
    for user in users:        
        registration_delta = _time.now() - _time.strptime(user['created'], '%Y-%m-%dT%H:%M:%S.%f')
        if registration_delta.total_seconds() <= TIME_DELTA + 1:                
            temp = {}
            temp['name'] = user['name']
            temp['fullname'] = user['fullname']
            temp['email'] = user['email']            
            new_users.append(temp)

    return new_users


def send_email_notification():
    new_users = get_new_users()
    subject = "Welcome to CKAN"
    body = "Hello, you just registered in a CKAN instance"
    for user in new_users:
        if user['email']:
            try:
                toolkit.mail_recipient(user['fullname'], user['email'], subject, body)
            except:
                return "False"
    
    return "True"



class EmailNotificationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'email_notification')

    #plugin Blueprint

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        blueprint.add_url_rule(
            u'/email_notification/user_reg',
            u'user_reg',
            send_email_notification,
            methods=['GET']
            )

        return blueprint
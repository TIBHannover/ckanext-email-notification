import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
from ckanext.email_notification.lib.email_notification_lib import Helper

# time interval used for checking the new user(s) (past 2 minutues)
TIME_DELTA = 120


def send_email_notification():
    new_users = Helper.get_new_users(TIME_DELTA)
    if len(new_users) == 0:
        return None

    sys_admins = Helper.get_sysadmins_email()
    subject = "New CKAN User"
    body = Helper.create_email_body(new_users)    
    for email in sys_admins:
        try:
            toolkit.mail_recipient('System Admin', email, subject, body)
        except:
            continue
    
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
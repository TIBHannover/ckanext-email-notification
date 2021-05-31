import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.jobs as jobs
from flask import Blueprint


def send_email_notification():
    users = toolkit.get_action('user_list')({},{})
    res = ""
    for user in users:
        res += (user['name'] + "\r\n")
    return res



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
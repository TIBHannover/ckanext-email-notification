import ckan.plugins as plugins
from flask import Blueprint
from ckanext.email_notification.controller.controllers import EmailController



class EmailNotificationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IBlueprint)

    #plugin Blueprint

    def get_blueprint(self):

        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        blueprint.add_url_rule(
            u'/email_notification/user_reg',
            u'user_reg',
            EmailController.send_email_notification,
            methods=['GET']
            )
        
        blueprint.add_url_rule(
            u'/email_notification/reminder_email',
            u'reminder_email',
            EmailController.send_reminder_email,
            methods=['GET']
            )

        return blueprint

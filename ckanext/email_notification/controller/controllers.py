# encoding: utf-8
from ckanext.email_notification.lib.email_notification_lib import Helper
import ckan.plugins.toolkit as toolkit



# time interval used for checking the new user(s) (past 2 minutues)
TIME_DELTA = 120

class EmailController():

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
 
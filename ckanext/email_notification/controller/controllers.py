# encoding: utf-8
from ckanext.email_notification.lib.email_notification_lib import Helper
import ckan.plugins.toolkit as toolkit
import logging


# time interval used for checking the new user(s) (past 2 minutues)
TIME_DELTA = 120
log = logging.getLogger(__name__)


class EmailController():

    @staticmethod
    def _check_sysadmin():
        try:
            toolkit.check_access('sysadmin', {'user': toolkit.g.user}, {})
        except toolkit.NotAuthorized:
            toolkit.abort(403, 'Need to be system administrator')

    @staticmethod
    def _send_to_sysadmins(subject, body):
        sent = False
        for email in Helper.get_sysadmins_email():
            try:
                toolkit.mail_recipient(
                    'System Admin', email, subject, body
                )
            except Exception:
                log.exception('Could not send notification email to %s', email)
            else:
                sent = True
        return sent

    @staticmethod
    def send_email_notification():
        EmailController._check_sysadmin()
        new_users = Helper.get_new_users(TIME_DELTA)
        if len(new_users) == 0:
            return 'no new user found.'

        subject = "New CKAN User"
        body = Helper.create_email_body(new_users)
        if not EmailController._send_to_sysadmins(subject, body):
            return "False"

        return "True"

    @staticmethod
    def send_reminder_email():
        EmailController._check_sysadmin()
        usernames = Helper.get_users_without_organization()
        if len(usernames) == 0:
            return 'no organization-less user found.'

        subject = "Reminder: User without Organization"
        body = Helper.create_email_body(usernames, is_reminder=True)
        if not EmailController._send_to_sysadmins(subject, body):
            return "False"

        return "True"

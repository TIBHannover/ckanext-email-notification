# ckanext-email-notification

A ckan extension for sending email notifications to system admins.

Included Plugin(s):

**email_notification**:
This plugin sends two types of emails:

_Registration Email_:  e-mail to system admins to inform them about the new user. 

_Reminder Email_: Reminds system admins about users without organization in ckan. 



## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
|  2.9 | Yes    |
| earlier | Not Tested |           |


## Installation

To install ckanext-email-notification:

1. Activate your CKAN virtual environment, for example:

        . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

        git clone https://github.com//ckanext-email-notification.git
        cd ckanext-email-notification
        pip install -e .
        pip install -r requirements.txt

3. Add `email-notification` to the `ckan.plugins` setting in your CKAN
    config file (by default the config file is located at
        `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Nginx on Ubuntu:

        sudo service nginx reload


## Config settings

_Registration Email_

This plugin checks the users (obtained via ckan API) creation date in the user table in ckan database and sends e-mail to users who registered in the past 2 minutue. 

Therefore, you need to set a job in the system cronjob list to call this plugin every 2 minutues. For instance:

    */2 * * * *  curl -H "Authorization:YOUR_API_KEY" http://localhost:5000/email_notification/user_reg

- *YOUR_API_KEY* is the ckan api key which you need to create.
- replace "http://localhost:5000/" with the target server. 

**NOTE**: If you like to change the 2 minutes time interval, you can change it in "controller/controllers.py", the variable "TIME_DELTA" (in seconds)

_Reminder Email_

You can set it on cronjob list to send this email in your desire time interval. for example, once a day at 16 p.m:

    0 16 * * *  curl -H "Authorization:YOUR_API_KEY" http://localhost:5000/email_notification/reminder_email`



## Developer installation

To install ckanext-email-notification for development, activate your CKAN virtualenv and
do:

    git clone https://github.com//ckanext-email-notification.git
    cd ckanext-email-notification
    python setup.py develop
    pip install -r dev-requirements.txt






# ckanext-email-notification

A ckan extension for sending email notifications to users.

Included Plugin(s):

**email_notification**:
This plugin sends user registration e-mail to users who register themselves in CKAN. 


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

This plugin checks the users (obtained via ckan API) creation date in the user table in ckan database and sends e-mail to users who registered in the past 2 minutue. 

Therefore, you need to set a job in the system cronjob list to call this plugin every 2 minutues. For instance:

    */2 * * * *  curl -H "Authorization:YOUR_API_KEY" http://localhost:5000/email_notification/user_reg

- *YOUR_API_KEY* is the ckan api key which you need to create.
- replace "http://localhost:5000/" with the target server. 

**NOTE**: If you like to change the 2 minutes time interval, you can change it in "plugin.py", the variable "TIME_DELTA" (in seconds)



## Developer installation

To install ckanext-email-notification for development, activate your CKAN virtualenv and
do:

    git clone https://github.com//ckanext-email-notification.git
    cd ckanext-email-notification
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini




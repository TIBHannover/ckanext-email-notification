"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import pytest

from ckan.plugins import toolkit
from ckanext.email_notification.controller.controllers import EmailController
from ckanext.email_notification.lib.email_notification_lib import Helper


@pytest.mark.ckan_config("ckan.plugins", "email_notification")
@pytest.mark.ckan_config("SECRET_KEY", "test_secret")
@pytest.mark.usefixtures("with_plugins")
def test_notification_endpoint_rejects_anonymous_users(app):
    response = app.get(
        toolkit.url_for("email_notification.user_reg"),
        status=403,
    )

    assert response.status_code == 403


def test_registration_notification_sends_to_each_sysadmin(monkeypatch):
    users = [{"name": "new-user", "email": "new@example.test"}]
    delivered = []
    monkeypatch.setattr(EmailController, "_check_sysadmin", lambda: None)
    monkeypatch.setattr(Helper, "get_new_users", lambda _delta: users)
    monkeypatch.setattr(
        Helper,
        "get_sysadmins_email",
        lambda: ["one@example.test", "two@example.test"],
    )
    monkeypatch.setattr(
        toolkit,
        "mail_recipient",
        lambda _name, email, subject, body: delivered.append(
            (email, subject, body)
        ),
    )

    assert EmailController.send_email_notification() == "True"
    assert [item[0] for item in delivered] == [
        "one@example.test",
        "two@example.test",
    ]
    assert all(item[1] == "New CKAN User" for item in delivered)
    assert "new-user" in delivered[0][2]


def test_notification_reports_when_all_deliveries_fail(monkeypatch):
    monkeypatch.setattr(EmailController, "_check_sysadmin", lambda: None)
    monkeypatch.setattr(
        Helper,
        "get_new_users",
        lambda _delta: [{"name": "new-user", "email": "new@example.test"}],
    )
    monkeypatch.setattr(
        Helper, "get_sysadmins_email", lambda: ["admin@example.test"]
    )

    def fail_delivery(*_args):
        raise RuntimeError("SMTP unavailable")

    monkeypatch.setattr(toolkit, "mail_recipient", fail_delivery)

    assert EmailController.send_email_notification() == "False"


def test_reminder_reports_when_no_users_need_an_organization(monkeypatch):
    monkeypatch.setattr(EmailController, "_check_sysadmin", lambda: None)
    monkeypatch.setattr(Helper, "get_users_without_organization", lambda: [])

    assert EmailController.send_reminder_email() == (
        "no organization-less user found."
    )

from flaskr import create_app, user, backend
from unittest.mock import patch
import pytest
"""Fixtures for testing the login functionality begin here."""


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'LOGIN_DISABLED': True,
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()


"""Tests for the login functionality begin here."""


def test_login_page(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Login" in resp.data


# Here, we are using parameters to run the same unit test but with different
# inputs. We will test all the different ways for login to fail.
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Need a username and password to login!'),
    ('a', '', b'Need a username and password to login!'),
    ('test', 'test', b'Username test does not exist!'),
    ('user', 'wrong', b'Invalid password for username test!'),
))
@patch('flaskr.backend.Backend.sign_in')
def test_login_failed(mock_sign_in, client, username, password, message):
    # side_effect allows use to raise exceptions when mocking
    # https://docs.python.org/3/library/unittest.mock.html#quick-guide
    mock_sign_in.side_effect = ValueError(message)
    resp = client.post("/login",
                       data={
                           "username": username,
                           "password": password
                       })
    assert resp.status_code == 200
    assert b"Login Failed" in resp.data
    assert message in resp.data


@patch('flaskr.backend.Backend.sign_in')
def test_login_successful(mock_sign_in, client):
    username = "Test User"
    password = "some password"
    mock_sign_in.return_value = user.User(username)
    resp = client.post("/login",
                       data={
                           "username": username,
                           "password": password
                       })
    assert resp.status_code == 200
    assert b"Login Successful" in resp.data
    assert b"Welcome Test User to my wiki!" in resp.data


def test_logout_successful(client):
    resp = client.get("/logout")
    assert resp.status_code == 200
    assert b"Logout Successful" in resp.data
    assert b"Logged out!" in resp.data


def test_signup_page(client):
    resp = client.get("/signup")
    assert resp.status_code == 200
    assert b"Sign Up" in resp.data


# Here, we are using parameters to run the same unit test but with different
# inputs. We will test all the different ways for signup to fail.
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Need a username and password to sign up'),
    ('a', '', b'Need a username and password to sign up'),
    ('user', 'password', b'Username user already exists!'),
))
@patch('flaskr.backend.Backend.sign_up')
def test_signup_failed(mock_sign_up, client, username, password, message):
    # side_effect allows use to raise exceptions when mocking
    # https://docs.python.org/3/library/unittest.mock.html#quick-guide
    mock_sign_up.side_effect = ValueError(message)
    resp = client.post("/signup",
                       data={
                           "username": username,
                           "password": password
                       })
    assert resp.status_code == 200
    assert b"Signup Failed" in resp.data
    assert message in resp.data


@patch('flaskr.backend.Backend.sign_up')
def test_signup_successful(mock_sign_up, client):
    username = "Test User"
    password = "some password"
    mock_sign_up.return_value = user.User(username)
    resp = client.post("/signup",
                       data={
                           "username": username,
                           "password": password
                       })
    assert resp.status_code == 200
    assert b"Signup Successful" in resp.data
    assert b"Successfully signed up!" in resp.data

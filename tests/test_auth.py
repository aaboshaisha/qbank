import pytest
from flask import g, session
from myapp.db import get_db

def test_register(client, app):
    # make sure u can get the register route
    assert client.get('/auth/register').status_code == 200
    # try sending data to it
    response = client.post('/auth/register', data={'email': 'test2@example.com', 
                                                   'password':'p', 
                                                   'password2':'a'})
    # ensure redirects to login
    assert response.headers['Location'] == '/auth/login'
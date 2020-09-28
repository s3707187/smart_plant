from backend_testing.setup_tests import *
    

# DEMONSTRATION METHOD, DELETE TODO
# def test_get_plants(client):
#     response = client.get('/plants')
#     print(response)

# login admin
# try login with bad password

# another: not admin, check claim?

# another: admin, check claim etc.


def test_login_fail(client):
    # login as admin with bad password
    details = {"username": TEST_ADMIN, "password": "bad_password"}
    response = client.post('/login', json=details)
    # check failed response code and no tokens
    assert response.status_code == 400
    assert "access_token" not in response.json
    assert "refresh_token" not in response.json

def test_login_fail_user(client):
    # login with nonexistent username
    details = {"username": "bad_user", "password": TEST_PASS}
    response = client.post('/login', json=details)
    # check failed response code and no tokens
    assert response.status_code == 400
    assert "access_token" not in response.json
    assert "refresh_token" not in response.json

def test_login_admin_success(client):
    # login as admin
    details = {"username": TEST_ADMIN, "password": TEST_PASS}
    response = client.post('/login', json=details)
    # check failed response code token
    assert response.status_code == 200
    assert "refresh_token" in response.json
    assert "access_token" in response.json


def test_login_user_success(client):
    details = {"username": TEST_USER_1, "password": TEST_PASS}
    response = client.post('/login', json=details)
    assert response.status_code == 200
    assert "refresh_token"  in response.json
    assert "access_token" in response.json




# delete user
# try not admin
# try admin, need to create one first

# update user
# try not admin or user
# try same user
# try admin
# not exists, exists


# fetch user
# try not admin or user
# try same user
# try admin
# not exists, exists

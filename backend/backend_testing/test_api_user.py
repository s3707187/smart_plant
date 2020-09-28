from backend_testing.setup_tests import *
from passlib.hash import pbkdf2_sha256
    

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
    # check success response code and tokens
    assert response.status_code == 200
    assert "refresh_token" in response.json
    assert "access_token" in response.json


def test_login_user_success(client):
    # successfully login as normal user
    details = {"username": TEST_USER_1, "password": TEST_PASS}
    response = client.post('/login', json=details)
    # check success response code and tokens
    assert response.status_code == 200
    assert "refresh_token"  in response.json
    assert "access_token" in response.json


def test_update_user_fail(client):
    # attempt to update the user when no permissions allowed
    hashed_pass = pbkdf2_sha256.hash(TEST_PASS)
    header = get_auth_header(client, TEST_USER_1, 'user')
    details = {"username": TEST_USER_2, "password": hashed_pass, "email": "magic@magic.com", "first_name": "John", "last_name": "Greenson"}
    response = client.post('/update_user_details', headers=header, json=details)
    assert response.status_code == 403

    # check the user was NOT changed via get_user_details call
    header_check = get_auth_header(client, TEST_USER_2, 'user')
    response_check = client.get('/get_user_details?user_to_query={}'.format(TEST_USER_2), headers=header_check)
    assert response_check.status_code == 200
    assert response_check.json["username"] == TEST_USER_2
    # password is NEVER returned!
    assert response_check.json["password"] == None
    assert response_check.json["email"] == "test2@test.com"
    assert response_check.json["first_name"] == "Test"
    assert response_check.json["last_name"] == "User2"

# delete user
# try not admin
# try admin, need to create one first



# fetch user
# try not admin or user
# try same user
# try admin
# not exists, exists

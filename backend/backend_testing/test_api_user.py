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


# update user
# try not admin or user *
# try same user *
# try admin *
# not exists, exists *

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
    assert response_check.json["last_name"] == "UserTwo"


def test_update_same_user(client):
    # attempt to update the user when no permissions allowed
    header = get_auth_header(client, TEST_USER_2, 'user')
    details = {"username": TEST_USER_2, "password": "", "email": "magic@magic.com", "first_name": "John", "last_name": "Greenson"}
    response = client.post('/update_user_details', headers=header, json=details)
    assert response.status_code == 201

    # check the user matches via get_user_details call
    response_check = client.get('/get_user_details?user_to_query={}'.format(TEST_USER_2), headers=header)
    assert response_check.status_code == 200
    assert response_check.json["username"] == TEST_USER_2
    # password is NEVER returned!
    assert response_check.json["password"] == None
    assert response_check.json["email"] == "magic@magic.com"
    assert response_check.json["first_name"] == "John"
    assert response_check.json["last_name"] == "Greenson"

    # need to do the same thing to make sure the details were actually changed,
    # and did not happen to already match the asserts,
    # and to revert back to original values.
    details = {"username": TEST_USER_2, "password": "", "email": "test2@test.com", "first_name": "Test", "last_name": "UserTwo"}
    response = client.post('/update_user_details', headers=header, json=details)
    assert response.status_code == 201

    # check the user matches via get_user_details call
    response_check = client.get('/get_user_details?user_to_query={}'.format(TEST_USER_2), headers=header)
    assert response_check.status_code == 200
    assert response_check.json["username"] == TEST_USER_2
    # password is NEVER returned!
    assert response_check.json["password"] == None
    assert response_check.json["email"] == "test2@test.com"
    assert response_check.json["first_name"] == "Test"
    assert response_check.json["last_name"] == "UserTwo"

def test_update_user_from_admin(client):
    # repeat of same_user test but with admin instead
    # attempt to update the user when no permissions allowed
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    details = {"username": TEST_USER_2, "password": "", "email": "magic@magic.com", "first_name": "John", "last_name": "Greenson"}
    response = client.post('/update_user_details', headers=header, json=details)
    assert response.status_code == 201

    # check the user matches via get_user_details call
    response_check = client.get('/get_user_details?user_to_query={}'.format(TEST_USER_2), headers=header)
    assert response_check.status_code == 200
    assert response_check.json["username"] == TEST_USER_2
    # password is NEVER returned!
    assert response_check.json["password"] == None
    assert response_check.json["email"] == "magic@magic.com"
    assert response_check.json["first_name"] == "John"
    assert response_check.json["last_name"] == "Greenson"

    # need to do the same thing to make sure the details were actually changed,
    # and did not happen to already match the asserts,
    # and to revert back to original values.
    details = {"username": TEST_USER_2, "password": "", "email": "test2@test.com", "first_name": "Test", "last_name": "UserTwo"}
    response = client.post('/update_user_details', headers=header, json=details)
    assert response.status_code == 201

    # check the user matches via get_user_details call
    response_check = client.get('/get_user_details?user_to_query={}'.format(TEST_USER_2), headers=header)
    assert response_check.status_code == 200
    assert response_check.json["username"] == TEST_USER_2
    # password is NEVER returned!
    assert response_check.json["password"] == None
    assert response_check.json["email"] == "test2@test.com"
    assert response_check.json["first_name"] == "Test"
    assert response_check.json["last_name"] == "UserTwo"


def test_update_user_nonexistent(client):
    # attempt to update the user when it does not exist
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    details = {"username": "nonexistent", "password": "", "email": "doesnot@matter.com", "first_name": "Anything", "last_name": "Goes"}
    response = client.post('/update_user_details', headers=header, json=details)
    assert response.status_code == 403

# delete user
# try not admin *
# try admin, need to create one first *
# exists *and not exists*

def test_delete_user_fail(client):
    # attempt to delete user when current one has no permission
    header = get_auth_header(client, TEST_USER_1, 'user')
    details = {"user_to_del": TEST_USER_2}
    response = client.post('/delete_user', headers=header, json=details)
    assert response.status_code == 403

    header_check = get_auth_header(client, TEST_ADMIN, 'admin')
    response_check = client.get('/get_user_details?user_to_query={}'.format(TEST_USER_2), headers=header_check)
    assert response_check.status_code == 200
    assert response_check.json["username"] == TEST_USER_2

def test_delete_user_not_exist(client):
    # attempt to delete user when it does not exist
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    details = {"user_to_del": "nonexistent"}
    response = client.post('/delete_user', headers=header, json=details)
    assert response.status_code == 403


def test_delete_user_success(client):
    # successfully delete user as admin
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    temp_user = "temp_user_111"

    details_create = {"username": temp_user, "first_name": "Test", "last_name": "Jones", "email": "court@jester.com", "password": "testpass"}
    response_create = client.post('/register', headers=header, json=details_create)
    assert response_create.status_code == 201

    response_check = client.get('/get_user_details?user_to_query={}'.format(temp_user), headers=header)
    assert response_check.status_code == 200
    assert response_check.json["username"] == temp_user
    # password is NEVER returned!
    assert response_check.json["password"] == None
    assert response_check.json["email"] == "court@jester.com"
    assert response_check.json["first_name"] == "Test"
    assert response_check.json["last_name"] == "Jones"

    details_delete = {"user_to_del": "temp_user_111"}
    response_delete = client.post('/delete_user', headers=header, json=details_delete)
    assert response_delete.status_code == 201

    response_check_delete = client.get('/get_user_details?user_to_query={}'.format(temp_user), headers=header)
    assert response_check_delete.status_code == 400



# fetch user:
# try not admin or user *
# try same user * - above
# try admin:
# not exists, *
# exists * - above

def test_get_user_details_fail(client):
    # test that attempting to get user details with no permissions fails
    header = get_auth_header(client, TEST_USER_2, 'admin')
    response_check = client.get('/get_user_details?user_to_query={}'.format(TEST_USER_1), headers=header)
    assert response_check.status_code == 400
    assert "username" not in response_check.json

def test_get_user_details_nonexistent(client):
    # test that attempting to get user details when user does not exist fails
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    response_check = client.get('/get_user_details?user_to_query={}'.format("nonexistent_user"), headers=header)
    assert response_check.status_code == 400
    assert "username" not in response_check.json


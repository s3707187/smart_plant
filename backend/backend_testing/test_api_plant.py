from backend_testing.setup_tests import *
from main import app

    
# get all plants
# try with not admin *
# try with admin *
# check len > whatever *
# check fields in each returned for each *

def test_user_plants(client):
    header = get_auth_header(client, TEST_USER_1, 'user')
    response = client.get('/get_users_plants', headers=header)
    assert response.status_code == 200
    assert len(response.json) >= 1
    for plant in response.json:
        assert plant['plant_id'] is not None
        assert plant['plant_name'] is not None
        assert plant['password'] is not None
        assert plant['plant_type'] is not None


def test_admin_plants(client):
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    response = client.get('/get_users_plants', headers=header)
    assert response.status_code == 200
    assert len(response.json) >= NUM_TEST_PLANTS
    for plant in response.json:
        assert plant['plant_id'] is not None
        assert plant['plant_name'] is not None
        assert plant['password'] is not None
        assert plant['plant_type'] is not None

def test_user_nonexistent(client):
    header = get_auth_header(client, 'rubbish', 'user')
    response = client.get('/get_users_plants', headers=header)
    assert response.status_code == 400

# update plant:
# try with not admin or owner
# try with user owner
# try with admin
# exists, not exists

def test_update_plant_fail(client):
    # fail to update the plant that you do not own
    header = get_auth_header(client, TEST_USER_1, 'user')
    details = {"plant_id": 2, "plant_name": "temp_name", "plant_type": "Flowering type"}
    response = client.post('/update_plant_details', headers=header, json=details)
    assert response.status_code == 403


def test_update_plant_from_owner(client):
    # successfully update the plant that you do own
    header = get_auth_header(client, TEST_USER_1, 'user')
    details = {"plant_id": 1, "plant_name": "temp_name", "plant_type": "Foliage type"}
    response = client.post('/update_plant_details', headers=header, json=details)
    assert response.status_code == 201

    response_check = client.get('/view_plant_details?plant_id={}'.format(1), headers=header)
    assert response_check.status_code == 200
    assert response_check.json["plant_id"] == 1
    assert response_check.json["plant_name"] == "temp_name"
    assert response_check.json["plant_type"] == "Foliage type"

    # update it back and check again
    details_new = {"plant_id": 1, "plant_name": "George_Keep", "plant_type": "Flowering type"}
    response = client.post('/update_plant_details', headers=header, json=details_new)
    assert response.status_code == 201

    response_check_new = client.get('/view_plant_details?plant_id={}'.format(1), headers=header)
    assert response_check_new.status_code == 200
    assert response_check_new.json["plant_id"] == 1
    assert response_check_new.json["plant_name"] == "George_Keep"
    assert response_check_new.json["plant_type"] == "Flowering type"
    assert response_check_new.json["password"] == "testpass"


def test_update_plant_from_admin(client):
    # successfully update a plant as admin
    # identical to from_owner test except for admin mode
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    details = {"plant_id": 1, "plant_name": "temp_name", "plant_type": "Foliage type"}
    response = client.post('/update_plant_details', headers=header, json=details)
    assert response.status_code == 201

    response_check = client.get('/view_plant_details?plant_id={}'.format(1), headers=header)
    assert response_check.status_code == 200
    assert response_check.json["plant_id"] == 1
    assert response_check.json["plant_name"] == "temp_name"
    assert response_check.json["plant_type"] == "Foliage type"

    # update it back and check again
    details_new = {"plant_id": 1, "plant_name": "George_Keep", "plant_type": "Flowering type"}
    response = client.post('/update_plant_details', headers=header, json=details_new)
    assert response.status_code == 201

    response_check_new = client.get('/view_plant_details?plant_id={}'.format(1), headers=header)
    assert response_check_new.status_code == 200
    assert response_check_new.json["plant_id"] == 1
    assert response_check_new.json["plant_name"] == "George_Keep"
    assert response_check_new.json["plant_type"] == "Flowering type"
    assert response_check_new.json["password"] == "testpass"

def test_update_plant_nonexistent(client):
    # fail update a nonexistent plant as admin
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    details = {"plant_id": 290357234, "plant_name": "temp_name", "plant_type": "Foliage type"}
    response = client.post('/update_plant_details', headers=header, json=details)
    assert response.status_code == 403

# delete plant:
# try with not admin *
# try with user owner *
# try with admin
# plant exists, not exists

def test_delete_plant_fail(client):
    # fail to update the plant that you do not own
    header = get_auth_header(client, TEST_USER_1, 'user')
    details = {"plant_id": 2}
    response = client.post('/delete_plant', headers=header, json=details)
    assert response.status_code == 403


def test_create_link_delete_plant_as_user(client):
    # create a plant, link it to test user 2, delete it as test user 2
    # must be combined as one test as no individual function is atomic
    header = get_auth_header(client, TEST_USER_2, 'user')
    details = {"plant_type": "Foliage type", "plant_name": "temp_plant_unique"}
    response = client.post('/register_plant', headers=header, json=details)
    assert response.status_code == 201

    response_check = client.get('/get_users_plants', headers=header)
    assert response_check.status_code == 200
    found_id = None
    for plant in response_check.json:
        if plant['plant_name'] == "temp_plant_unique":
            found_id = plant['plant_id']
    
    details_delete = {"plant_id": found_id}
    response_delete = client.post('/delete_plant', headers=header, json=details_delete)
    assert response_delete.status_code == 201

    response_check_deleted = client.get('/get_users_plants', headers=header)
    assert response_check_deleted.status_code == 200
    for plant in response_check_deleted.json:
        assert plant['plant_id'] != found_id

        
def test_delete_plant_as_admin(client):
    # create a plant, link it to test user 2, delete it as ADMIN
    # very similar to as_user test above, but with admin doing the deleting
    header_user = get_auth_header(client, TEST_USER_2, 'user')
    details = {"plant_type": "Foliage type", "plant_name": "temp_plant_unique"}
    response = client.post('/register_plant', headers=header_user, json=details)
    assert response.status_code == 201

    response_check = client.get('/get_users_plants', headers=header_user)
    assert response_check.status_code == 200
    found_id = None
    for plant in response_check.json:
        if plant['plant_name'] == "temp_plant_unique":
            found_id = plant['plant_id']
    
    header_admin = get_auth_header(client, TEST_ADMIN, 'admin')
    details_delete = {"plant_id": found_id}
    response_delete = client.post('/delete_plant', headers=header_admin, json=details_delete)
    assert response_delete.status_code == 201

    response_check_deleted = client.get('/get_users_plants', headers=header_user)
    assert response_check_deleted.status_code == 200
    for plant in response_check_deleted.json:
        assert plant['plant_id'] != found_id

def test_delete_plant_nonexistent(client):
    # test that deleting a nonexistent plant fails (as admin)
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    details_delete = {"plant_id": 987234986}
    response_delete = client.post('/delete_plant', headers=header, json=details_delete)
    assert response_delete.status_code == 403


# Test maintenance linking

def test_admin_allocate_deallocate_success(client):
    header = get_auth_header(client, TEST_ADMIN, 'admin')
    link_details = {
        "user_to_link" : TEST_ADMIN,
        "user_link_type" : "maintenance",
        "plant_id" : 1        
    }
    response = client.post('/add_plant_link', headers=header, json=link_details)
    assert response.status_code == 201

    response_check_plant = client.get('/view_plant_details?plant_id={}'.format(1), headers=header)
    assert response_check_plant.status_code == 200
    assert response_check_plant.json["maintainer"] == TEST_ADMIN

    delete_details = {
        "linked_user" : TEST_ADMIN,
        "link_type" : "maintenance",
        "plant_id" : 1        
    }
    response_delete_link = client.post('/remove_plant_link', headers=header, json=delete_details)
    assert response_delete_link.status_code == 201
    
    response_check_plant = client.get('/view_plant_details?plant_id={}'.format(1), headers=header)
    assert response_check_plant.status_code == 200
    assert response_check_plant.json["maintainer"] == None


def test_admin_allocate_wrong_link_type(client):
    pass

def test_allocate_user_fail(client):
    pass

def test_allocate_already_linked(client):
    pass

def test_link_admin_viewer_fail(client):
    pass


# Test notifications






from backend_testing.setup_tests import *
from main import app



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
    
# get all plants
# try with not admin
# try with admin
# check len > 0
# check fields in each returned for each


# delete plant:
# try with not admin
# try with user owner
# try with admin
# plant exists, not exists

# update plant:
# try with not admin
# try with user owner
# try with admin
# exists, not exists
from backend_testing.setup_tests import *

from flask_jwt_extended import create_access_token

TEST_USER_1_TOKEN = create_access_token('test_01', user_claims={"role": 'user'})
TEST_USER_2_TOKEN = create_access_token('test_02', user_claims={"role": 'user'})
TEST_ADMIN_TOKEN = create_access_token('test_admin', user_claims={"role": 'admin'})

def get_auth_header(token):
    auth_header = {
        'Authorization': 'Bearer {}'.format(token)
    }
    return auth_header

# DEMONSTRATION METHOD, DELETE TODO
def test_get_plants(client):
    response = client.get('/plants')
    print(response)

def test_get_all_plants_fail(client):
    header = get_auth_header(TEST_USER_1_TOKEN)
    response = client.get('')

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
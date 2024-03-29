import pytest

from flask_jwt_extended import create_access_token

from main import app
from main import USER, PASSWORD, HOST

# to run tests, CD to backend directory and run `python3 -m pytest`
# use -s option after `pytest` to show all print statement output

# used flask tutorial: https://flask.palletsprojects.com/en/1.1.x/testing/
# useful link for JWT authorisation mocking:
# https://stackoverflow.com/questions/46846762/flask-jwt-extended-fake-authorization-header-during-testing-pytest

# testing constants
TEST_DATABASE = "testing_smart_plant"
TEST_JWT_KEY = "testing1234"

TEST_USER_1 = 'test_01'
TEST_USER_2 = 'test_02'
TEST_ADMIN = 'test_admin'

NUM_TEST_PLANTS = 2
TEST_PASS = 'testpass'

@pytest.fixture
def client():
    # setup testing environment
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, TEST_DATABASE)
    app.config['JWT_SECRET_KEY'] = TEST_JWT_KEY
    with app.test_client() as client:
        yield client


def get_auth_header(client, identity, role):
    # need to temporarily simulate the request context inorder to create the
    # access token
    with app.test_request_context():
        token = create_access_token(identity, user_claims={"role": role})
    # make the header and return
    auth_header = {
        'Authorization': 'Bearer {}'.format(token)
    }
    return auth_header


# Testing Information

# DATABASE - testing_smart_plant contents expected:
# 
# Plant
# +----------+----------------+----------+-------------+--------------+
# | plant_id | plant_type     | password | plant_name  | plant_health |
# +----------+----------------+----------+-------------+--------------+
# |        1 | Flowering type | testpass | George_Keep | healthy      |
# |        2 | Cactus type    | testpass | Simon_Keep  | healthy      |
# |        3 | Foliage type   | testpass | Harry_Keep  | unhealthy    |
# +----------+----------------+----------+-------------+--------------+

# User
# +------------+-----------------------------------------------------------------------------------------+------------+-----------+--------------------+--------------+
# | username   | password                                                                                | first_name | last_name | email              | account_type |
# +------------+-----------------------------------------------------------------------------------------+------------+-----------+--------------------+--------------+
# | test_01    | $pbkdf2-sha256$29000$x9i7dy4FwJgTorS2FgLg3A$ZzjhJr3UCz8RkPijkx1lYralgsSF9M7RwjLCR4eUXoQ | Test       | User      | test@test.com      | user         |
# | test_02    | $pbkdf2-sha256$29000$x9i7dy4FwJgTorS2FgLg3A$ZzjhJr3UCz8RkPijkx1lYralgsSF9M7RwjLCR4eUXoQ | Test       | UserTwo   | test2@test.com     | user         |
# | test_admin | $pbkdf2-sha256$29000$x9i7dy4FwJgTorS2FgLg3A$ZzjhJr3UCz8RkPijkx1lYralgsSF9M7RwjLCR4eUXoQ | Test       | Admin     | test2@test.com     | admin        |
# | test_user  | $pbkdf2-sha256$29000$ZkwpBcDYuxeCECKEUEppTQ$c95vEVMJ3WBLy.wuDMaFax4DFLy0XM4oN3GVspiFFxk | test       | user      | test_user@test.com | user         |
# +------------+-----------------------------------------------------------------------------------------+------------+-----------+--------------------+--------------+
# NOTE: passwords are all 'testpass'

# Plant_link
# +----------+----------+---------------+
# | username | plant_id | user_type     |
# +----------+----------+---------------+
# | test_01  |        1 | plant_manager |
# | test_01  |        3 | plant_manager |
# +----------+----------+---------------+

# Plant_history
# +------------+----------+---------------------+-------------+----------+-------+----------+
# | history_id | plant_id | date_time           | temperature | humidity | light | moisture |
# +------------+----------+---------------------+-------------+----------+-------+----------+
# |          1 |        1 | 2020-09-28 03:35:26 |        0.35 |     0.55 |  0.33 |      0.6 |
# +------------+----------+---------------------+-------------+----------+-------+----------+

# Plant_type is identical to real database table


# Used to create new Plant_history table
# CREATE TABLE Plant_history (
#     history_id int NOT NULL AUTO_INCREMENT,
#     plant_id int NOT NULL,
#     date_time DATETIME NOT NULL,
#     temperature FLOAT NOT NULL,
#     humidity FLOAT NOT NULL,
#     light FLOAT NOT NULL,
#     moisture FLOAT NOT NULL,
#     PRIMARY KEY (history_id)
# );
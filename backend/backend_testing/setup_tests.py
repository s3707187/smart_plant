import pytest

from main import app
from main import USER, PASSWORD, HOST

# to run tests, CD to backend directory and run `python3 -m pytest`
# use -s option after `pytest` to show all print statement output

# used flask tutorial: https://flask.palletsprojects.com/en/1.1.x/testing/
# https://stackoverflow.com/questions/46846762/flask-jwt-extended-fake-authorization-header-during-testing-pytest

TEST_DATABASE = "testing_smart_plant"

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://{}:{}@{}/{}".format(USER, PASSWORD, HOST, TEST_DATABASE)

    with app.test_client() as client:
        yield client
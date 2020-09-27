from backend_testing.setup_tests import *
    

# DEMONSTRATION METHOD, DELETE TODO
def test_get_plants(client):
    response = client.get('/plants')
    print(response)


# save plant data
# get current list of histories length
# upload
# get new list length, check is 1 more
# get latest history (perhaps from view plant details), check is correct


# verify plant
# get a plant from database
# if none, create one
# get id and password
# check


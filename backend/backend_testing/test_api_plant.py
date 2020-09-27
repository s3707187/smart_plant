from backend_testing.setup_tests import *
    

# DEMONSTRATION METHOD, DELETE TODO
def test_get_plants(client):
    response = client.get('/plants')
    print(response)


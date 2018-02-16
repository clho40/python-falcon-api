from falcon import testing
import pytest
import app

data = {"tenant": "acme_test", "integration_type": "flight-information-system", "configuration": { "username": "acme_user", "password": "acme12345", "wsdl_urls": { "session_url": "https://session.manager.svc", "booking_url": "https://booking.manager.svc"}}}

@pytest.fixture()
def client():
    return testing.TestClient(app.create())

def test_post_config(client):
    result = client.simulate_post('/config',json=data)
    print(result)
    assert result.json[0] == data

def test_get_config(client):
    params = {"tenant":"acme_test","integration_type":"flight-information-system"}
    result = client.simulate_get('/config',params=params)
    assert result.json[0] == data

#def test_delete_config
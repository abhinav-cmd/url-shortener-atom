from urlshort import create_app

def test_shorten(client):
    response=client.get('/')
    assert b'Shorten' in response.data
def test_shortenzW(client):
    response=client.get('/')
    assert b'Shortenz' in response.data

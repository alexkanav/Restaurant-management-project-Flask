def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'homepage' in response.data


def test_admin_requires_authentication(client):
    response = client.get('/admin/order-processing', follow_redirects=True)
    assert response.status_code == 200
    assert b'login_page' in response.data


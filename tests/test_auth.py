from app.blueprints.admin.models import Staff


def test_login_form_display(client):
    """Test that the login form is rendered correctly."""

    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b'email' in response.data
    assert b'password' in response.data


def test_register_and_login_user(client):
    """Test registering a new user and logging in successfully."""

    # Register a new user
    register_response = client.post('/admin/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'Password',
        'confirm_password': 'Password',
    }, follow_redirects=True)

    assert register_response.status_code == 200
    assert b'login_page' in register_response.data

    # Verify the user is in the database
    user = Staff.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'testuser@example.com'

    # Login with the newly registered user
    login_response = client.post('/admin/login', data={
        'email': 'testuser@example.com',
        'password': 'Password',
    }, follow_redirects=True)

    assert login_response.status_code == 200
    assert b'dashboard' in login_response.data


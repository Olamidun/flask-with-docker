import json
import unittest
from project import db
from project.api.models import User

from project.tests.base import BaseTestCase

class TestUserService(BaseTestCase):
    """Tests for users service"""

    def test_users(self):
        """Ensure the /ping route returns a ping response"""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!',  data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database"""

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'micheal@mherman.org',
                    'password': 'admin1234'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('micheal@mherman.org was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])
    
    
    def test_add_user_invalid_json_keys(self):

        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
            '/users',
            data=json.dumps({'email': 'michael@mherman.org'}),
            content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
            '/users',
            data=json.dumps({
            'username': 'michael',
            'email': 'michael@mherman.org',
            'password': 'testing123'
            }),
            content_type='application/json',
            )
            response = self.client.post(
            '/users',
            data=json.dumps({
            'username': 'michael',
            'email': 'michael@mherman.org',
            'password': 'testing123'
            }),
            content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
            'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly"""
        user = User(username='michael', email='michael@mherman.org', password='testing1234')
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@mherman.org', data['data']['email'])
            self.assertIn('success', data['status'])
    
    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])
if __name__ == '__main__':
    unittest.main()
import unittest
from app import db, create_app
from app.models import User, Goal, Skill, SkillLog

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(username='test_user', email='test@example.com')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.username, 'test_user')
        self.assertEqual(self.user.email, 'test@example.com')

if __name__ == '__main__':
    unittest.main()

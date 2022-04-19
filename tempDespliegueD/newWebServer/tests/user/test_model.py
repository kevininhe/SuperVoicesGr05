import unittest
from project import db, create_app

class TestUserModel(unittest.TestCase):

    def setUp(self):
        admin._views = []
        rest_api.resources = []

        app = create_app()
        self.client = app.test_client()
        db.app = app
        db.create_all()
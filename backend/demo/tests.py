from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Note
import json

# See https://docs.djangoproject.com/en/2.1/topics/testing/tools/


def create_user_helper(username, password):
    user = User.objects.create_user(username=username, password=password)
    user.save()


def create_note_helper(content, username):
    user = User.objects.get(username=username)
    if not user:
        raise ValueError
    note = Note.objects.create(content=content, user=user)
    note.save()


def json_decode(resp):
    return json.loads(resp.content)


# A naive test, with some room for improvement.
class DemoTests(TestCase):
    def setUp(self):
        create_user_helper("taoky", "123456")
        create_user_helper("joe", "abcdefg")
        create_note_helper("It's so nice", "taoky")
        create_note_helper("hahaha", "taoky")
        create_note_helper("FLXG!", "joe")

    def test_register_and_login_normal(self):
        c = Client()
        res = c.post('/register', {"username": "aaa", "password": "666"})
        res = json_decode(res)
        self.assertEqual(res["code"], 0)
        self.assertEqual(res["msg"], "")

        res = c.post('/login', {"username": "aaa", "password": "666"})
        res = json_decode(res)
        self.assertEqual(res["code"], 0)
        self.assertEqual(res["msg"], "")

    def test_login_logout_normal(self):
        c = Client()
        res = c.post('/login', {"username": "taoky", "password": "123456"})

        res = json_decode(res)
        self.assertEqual(res["code"], 0)
        self.assertEqual(res["msg"], "")

        res = c.post("/logout")
        res = json_decode(res)
        self.assertEqual(res["code"], 0)
        self.assertEqual(res["msg"], "")

    def test_logout_without_login(self):
        c = Client()
        res = c.post("/logout")
        res = json_decode(res)
        self.assertEqual(res["code"], 4)

    def test_get_notes(self):
        c = Client()
        c.post('/login', {"username": "taoky", "password": "123456"})
        res = c.get('/get_notes')
        res = json_decode(res)
        self.assertEqual(res["code"], 0)
        self.assertEqual(res["msg"], "")
        self.assertEqual(res["items"][0]["content"], "It's so nice")
        self.assertEqual(res["items"][1]["content"], "hahaha")

    def test_add_notes(self):
        c = Client()
        c.post('/login', {"username": "joe", "password": "abcdefg"})
        res = c.post('/add_notes', {"content": "Naive!"})
        res = json_decode(res)
        self.assertEqual(res["code"], 0)
        self.assertEqual(res["msg"], "")
        res = c.get('/get_notes')
        res = json_decode(res)
        self.assertEqual(res["code"], 0)
        self.assertEqual(res["msg"], "")
        self.assertEqual(res["items"][1]["content"], "Naive!")

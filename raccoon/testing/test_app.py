from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import UsersInfo
from json import loads
import requests_mock

class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///')
        return app

    def setUp(self):
        db.create_all()
        for i in [
        {"uid":1, "user_info_key":"Physical_Data", "user_info_value":{"bloodType":"A","Gender":"Female","B":83,"W":56,"H":84,"Height":158,"Birthdate":"1978-05-27"}},
        {"uid":1, "user_info_key":"Educational_Data", "user_info_value":{"School":"Kirameki Private High School"}},
        {"uid":2, "user_info_key":"Physical_Data", "user_info_value":{"bloodType":"A","Gender":"Female","B":80,"W":59,"H":82,"Birthdate":"1979-02-03"}},
        {"uid":2, "user_info_key":"Educational_Data", "user_info_value":{"School":"Kirameki Private High School"}},
        {"uid":3, "user_info_key":"Physical_Data", "user_info_value":{"bloodType":"A","Gender":"Female","B":84,"W":58,"H":84,"Height":161,"Birthdate":"1979-02-03"}},
        {"uid":3, "user_info_key":"Educational_Data", "user_info_value":{"School":"Kirameki Private High School"}}
            ]:
            useradd = UsersInfo(user_id=i["uid"],user_info_key=i["user_info_key"],user_info_value=i["user_info_value"])
            db.session.add(useradd)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestGetAllInfo(TestBase):
    def test_get_all_info(self):
        response = self.client.get(url_for('dumpall'))
        strsponse = response.data.decode('utf-8')
        dictsponse = loads(strsponse)
        self.assert200(response)
        self.assertEqual("Kirameki Private High School",dictsponse[0]["user_info_value"]["School"])

class TestSearchUsersInfo(TestBase):
    def test_search_one_user(self):
        with requests_mock.Mocker() as lmnopreq:
            faketoken = "626dec4f-c87a-4e41-8f50-cedce221f5c7"
            lmnopreq.get('http://lmnop:5000/' + faketoken, text='{"expired":"False"}')
            response = self.client.post(
                url_for('getuser',user_id=1),
                json={"token":faketoken,"searchkey":"Physical_Data"},
            )
            dictresp = loads(response.text)
            self.assert200(response)
            self.assertEqual(83, dictresp[0]['user_info_value']['B'])
    
    def test_search_one_user_expired(self):
        with requests_mock.Mocker() as lmnopreq:
            faketoken = "626dec4f-c87a-4e41-8f50-cedce221f5c7"
            lmnopreq.get('http://lmnop:5000/' + faketoken, text='{"expired":"True"}')
            response = self.client.post(
                url_for('getuser',user_id=1),
                json={"token":faketoken,"searchkey":"Physical_Data"},
            )
            self.assert400(response)
            self.assertIn("Token has expired",response.text)

class TestAddInfo(TestBase):
    def test_add_with_valid_token(self):
        with requests_mock.Mocker() as lmnopreq:
            faketoken = "626dec4f-c87a-4e41-8f50-cedce221f5c7"
            lmnopreq.get('http://lmnop:5000/' + faketoken, text='{"expired":"False"}')
            response = self.client.post(
                url_for('addinfo',user_id=1),
                json={"token":faketoken,"user_info_key":"Test_Key","user_info_value":{"bloodType":"T","Gender":"T","B":5,"W":6,"H":7,"Height":100,"Birthdate":"1970-01-01"}}
            )
            responselist = self.client.post(
                url_for('getuser',user_id=1),
                json={"token":faketoken,"searchkey":"Test_Key"},
            )
            dictresp = loads(responselist.text)
            self.assert200(response)
            self.assertEqual(5, dictresp[0]['user_info_value']['B'])
            self.assertEqual("T", dictresp[0]['user_info_value']['bloodType'])


    def test_add_with_invalid_token(self):
        with requests_mock.Mocker() as lmnopreq:
            faketoken = "626dec4f-c87a-4e41-8f50-cedce221f5c7"
            lmnopreq.get('http://lmnop:5000/' + faketoken, text='{"expired":"True"}')
            response = self.client.post(
                url_for('addinfo',user_id=1),
                json={
                    "token":faketoken,
                    "user_info_key":"Test_Key",
                    "user_info_value":{
                        "bloodType":"T",
                        "Gender":"T",
                        "B":5,
                        "W":6,
                        "H":7,
                        "Height":100,
                        "Birthdate":"1970-01-01"
                        }
                    }

                )
            self.assert400(response)

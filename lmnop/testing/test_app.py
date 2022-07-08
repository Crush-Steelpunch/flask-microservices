from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.routes import gennewtoken
from application.models import Tokens
from unittest.mock import patch
from time import time, localtime
from datetime import datetime
from unittest.mock import patch
import requests_mock


class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///')
        return app

    def setUp(self):
        db.create_all()
        new_tok_dict = gennewtoken()
        newtoken = Tokens(user_id=1,
            user_token=new_tok_dict["new_token"],
            user_expiry=new_tok_dict["new_datetime"])
        db.session.add(newtoken)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
class TestToken(TestBase):
    def test_verify_token(self):
        tokenuuid = Tokens.query.filter(Tokens.user_id==1).first()
        response = self.client.get(url_for('verify',tok=tokenuuid.user_token))
        self.assert_200(response)
        self.assertIn(b"False",  response.data)
    
    def test_verify_token_not_exist(self):
        response = self.client.get(url_for('verify',tok="626dec4f-c87a-4e41-8f50-cedce221f5c7"))
        self.assert200(response)
        self.assertIn(b"True", response.data)

    def test_verify_token_time_expired(self):
        tokenuuid = Tokens.query.filter(Tokens.user_id==1).first()
        new_expiry = time() - 20
        tokenuuid.user_expiry = datetime.fromtimestamp(new_expiry)
        db.session.commit()
        response = self.client.get(url_for('verify',tok=tokenuuid.user_token))
        self.assert_200(response)
        self.assertIn(b"True",  response.data)
        
class TestGenToken(TestBase):
    def test_gen_new_token(self):
        with requests_mock.Mocker() as bingoreq:
            bingoreq.get('http://bingo:5000/uid/' + "2", text='[{"id":2,"user_first_name":"Jane","user_last_name":"Grandy","user_login_name":"janeg"}]')
            response = self.client.post(url_for('gentoken',uid="2"))
            self.assert200(response)
            self.assertIn(b'"expired":"False","token":"',response.data)
    
    def test_gen_no_user(self):
        with requests_mock.Mocker() as bingoreq:
            bingoreq.get('http://bingo:5000/uid/' + "2", text='[]')
            response = self.client.post(url_for('gentoken',uid="2"))
            self.assert400(response)
            self.assertIs(b'',response.data)

    def test_gen_update_user(self):
        with requests_mock.Mocker() as bingoreq:
            bingoreq.get('http://bingo:5000/uid/' + "1", text='[{"id":1,"user_first_name":"Jane","user_last_name":"Grandy","user_login_name":"janeg"}]')
            response = self.client.post(url_for('gentoken',uid="1"))
            self.assert200(response)
            self.assertIn(b'"expired":"False","token":"',response.data)
            tokenuuid = Tokens.query.filter(Tokens.user_id==1).first()
            self.assertIn(tokenuuid.user_token,response.data.decode('utf-8'))




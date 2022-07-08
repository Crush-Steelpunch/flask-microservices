from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Services
from datetime import datetime
from time import time
from json import loads


class TestBase(TestCase):
    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI='sqlite:///')
        return app

    def setUp(self):
        db.create_all()
        for i in [
            {"name":"bingo","checkin":1800}, 
            {"name":"lmnop","checkin":4000}, 
            {"name":"raccoon","checkin":300}]:
            new_expiry = time()-i["checkin"]
            servicecheckin = datetime.fromtimestamp(new_expiry)
            newservice = Services(
            service_name=i["name"], 
            service_url="http://"+i["name"]+":5000/", 
            service_last_checkin=servicecheckin)
            db.session.add(newservice)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class DumpData(TestBase):
    def test_dump_data(self):
        response = self.client.get(url_for('dump_data'))
        jresp = loads(response.text)
        self.assert200(response)
        self.assertEqual("bingo", jresp[2]["service_name"])

class QueryService(TestBase):
    def test_Query_service(self):
        response = self.client.get(url_for('query_service',servicename="bingo"))
        jresp = loads(response.text)
        self.assert200(response)
        self.assertEqual("bingo", jresp[0]["service_name"])

class AddService(TestBase):
    def test_add_service(self):
        response = self.client.post(
            url_for('reg_service'),
            json={"name":"test","url":"http://testurl:5000"}
            )
        self.assert200(response)
        responsecheckadd = self.client.get(url_for('query_service',servicename="test"))
        jsoned = loads(responsecheckadd.text)
        self.assertEqual("test",jsoned[0]["service_name"])

    def test_update_service(self):
        response = self.client.post(
            url_for('reg_service'),
            json={"name":"bingo","url":"http://bingo:5000"}
            )
        self.assert200(response)
        responsecheckadd = self.client.get(url_for('query_service',servicename="bingo"))

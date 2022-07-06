from application import db
from application.models import Users

db.drop_all()
db.create_all()

for i in [{"login":"bobr", "fname":"Bob","lname":"Robers"},{"login":"janeg", "fname":"Jane","lname":"Grandy"},{"login":"eriols", "fname":"Eriol","lname":"Saucepan"}]:
    useradd = Users(user_first_name=i["fname"],user_last_name=i["lname"],user_login_name=i["login"])
    db.session.add(useradd)
db.session.commit()

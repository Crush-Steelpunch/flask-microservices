from application import db
from application.models import Users

db.drop_all()
db.create_all()

for i in [{"login":"ShioriF", "fname":"Shiori","lname":"Fujisaki"},{"login":"MioK", "fname":"Mio","lname":"Kisaragi"},{"login":"YuinaH", "fname":"Yuina","lname":"Himoo"}]:
    useradd = Users(user_first_name=i["fname"],user_last_name=i["lname"],user_login_name=i["login"])
    db.session.add(useradd)
db.session.commit()

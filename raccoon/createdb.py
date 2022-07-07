from application import db
from application.models import UsersInfo

db.drop_all()
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


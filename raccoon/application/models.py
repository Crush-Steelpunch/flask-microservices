from application import db 

class UsersInfo(db.Model):
    __tablename__ = 'UserInfo'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_info_key = db.Column(db.String(60), nullable=False)
    user_info_value = db.Column(db.JSON, nullable=True)
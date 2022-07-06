from application import db 

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(30), nullable = False)
    user_last_name = db.Column(db.String(30), nullable = False)
    user_login_name = db.Column(db.String(30), unique = True, nullable = False )


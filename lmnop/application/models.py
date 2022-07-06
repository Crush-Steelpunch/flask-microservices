from application import db 

class Tokens(db.Model):
    __tablename__ = 'Tokens'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False, unique = True)
    user_token = db.Column(db.String(36), nullable = True)
    user_expiry = db.Column(db.DateTime, nullable = True)
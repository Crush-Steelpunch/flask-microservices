from application import db 

class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(30), nullable = False)
    service_url = db.Column(db.String(120), nullable = False)
    service_last_checkin = db.Column(db.DateTime, nullable = True )


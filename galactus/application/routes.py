from application import app, db
from application.models import Services
from flask import redirect, Response, jsonify, request
from datetime import datetime

def jsonify_services(query):
    iter = len(query) - 1
    return_services = []
    while iter > -1:
        return_services.append({"service_name": query[iter].service_name,
                                "service_url": query[iter].service_url,
                                "service_last_checkin": query[iter].service_last_checkin}
                               )
        iter = iter-1
    return return_services

@app.route('/', methods=['GET'])
def dump_data():
    service_list = db.session.query(Services).all()
    jsonedlist = jsonify_services(service_list)
    return jsonify(jsonedlist)

@app.route('/<servicename>',methods=['GET'])
def query_service(servicename):
    serviceresult = db.session.query(Services).filter(Services.service_name==servicename).all()
    jsonedlist = jsonify_services(serviceresult)
    return jsonify(jsonedlist)

@app.route('/register',methods=['POST'])
def reg_service():
    service_add = request.get_json() # Expecting { "name": "servicename": url:"serviceurl"}
    checkexists = query_service(service_add["name"])
    if checkexists.data == b'[]\n':
        addservice = Services(service_name=service_add["name"],service_url=service_add["url"],service_last_checkin=datetime.now())
        db.session.add(addservice)
    else: 
        updateservice = db.session.query(Services).filter(Services.service_name==service_add["name"]).first()
        updateservice.service_last_checkin = datetime.now()
    db.session.commit()
    return Response()
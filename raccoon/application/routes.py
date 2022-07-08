from application import app, db
from application.models import UsersInfo
from flask import redirect, Response, jsonify, request
import requests
from json import loads
import pdb


def jsonify_userinfo(query):
    iter = len(query) - 1
    return_userinfo = []
    while iter > -1:
        return_userinfo.append({"user_id": query[iter].user_id,
                                "user_info_key": query[iter].user_info_key,
                                "user_info_value": query[iter].user_info_value}
                               )
        iter = iter-1
    return return_userinfo


def token_verify(tokenin):
    response = requests.get('http://lmnop:5000/' + tokenin)
    jresp = loads(response.text)
    if jresp["expired"] == "False":
        return False
    else:
        return True


@app.route('/', methods=['GET'])
def dumpall():
    UserDump = UsersInfo.query.all()
    jsonedDump = jsonify_userinfo(UserDump)
    return jsonify(jsonedDump)


@app.route('/<user_id>', methods=['POST'])
def getuser(user_id):
    # expecting { "token":"uuid","searchkey":"searchterm"}
    datain = request.get_json()
    verified_token = token_verify(datain["token"])
    if not verified_token:
        UsersInfo_query_result = UsersInfo.query.filter(
            UsersInfo.user_id == user_id,
            UsersInfo.user_info_key.like(datain["searchkey"])).all()
        backinfo = jsonify_userinfo(UsersInfo_query_result)
        return jsonify(backinfo)
    else:
        return Response("Token has expired", status=400)


@app.route('/addinfo/<user_id>', methods=['POST'])
def addinfo(user_id):
    # expecting { "token":"uuid", "user_info_key":"keyname","user_info_value":"{json data}"}
    datain = request.get_json()
    verified_token = token_verify(datain["token"])
    if not verified_token:
        adddata = UsersInfo(
            user_id=user_id, user_info_key=datain["user_info_key"], user_info_value=datain["user_info_value"])
        db.session.add(adddata)
        db.session.commit()
        return Response()
    else:
        return Response("Token has expired", status=400)


@app.route('/delinfo/<user_id>', methods=['DELETE'])
def delinfo(user_id):
    # expecting { "token":"uuid", "searchkey":"keyname"}
    datain = request.get_json()
    verified_token = token_verify(datain["token"])
    if not verified_token:
        delldata =  UsersInfo.query.filter(
            UsersInfo.user_id == user_id,
            UsersInfo.user_info_key.like(datain["searchkey"])).first()
        db.session.delete(delldata)
        db.session.commit()
        return Response()
    else:
        return Response("Token has expired", status=400)

@app.route('/purgeinfo/<user_id>', methods=['DELETE'])
def purgeinfo(user_id):
    confirm = request.get_json()
    verified_token = token_verify(confirm["token"])
    if not verified_token:
        if confirm['yes-i-really-really-mean-it'] == "purge-this-user-info-i-will-be-responsible-for-the-consequences":
            db.session.query(UsersInfo).filter(
                UsersInfo.user_id == user_id
            ).delete()
            db.session.commit()
            return Response()
        else:
            return Response("Invalid Request",status=400)
    else:
        return Response("Token Expired",status=400)

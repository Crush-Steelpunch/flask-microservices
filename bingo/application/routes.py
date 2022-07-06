from application import app,db
from application.models import Users
from flask import redirect, Response, jsonify, request
import sys
# Function to turn querys into json artifacts
def jsonify_user(query):
    iter = len(query) -1
    return_users = []
    while iter > -1:
        return_users.append({"id":query[iter].id,
        "user_first_name":query[iter].user_first_name,
        "user_last_name":query[iter].user_last_name,
        "user_login_name":query[iter].user_login_name}
        )
        iter = iter-1
    return return_users

# list all users. This is totally not an security issue 
# if it's firewalled

@app.route('/', methods = ['GET'])
def base():
    users = Users.query.all()
    jsoned_users = jsonify_user(users)
    return jsonify(jsoned_users)

# return list of users on a partial match
@app.route('/search/<searchstring>', methods = ['GET'])
def search(searchstring):
    finduser = Users.query.filter(Users.user_login_name.like('%' + searchstring + '%')).all()
    jsoned_users = jsonify_user(finduser)
    return jsonify(jsoned_users)

# add users
@app.route('/adduser', methods = ['POST'])
def useradd():
    userinfo = request.get_json()
    for i in ['fname','lname','login']:
            if not i in  userinfo.keys():
               return Response('expected format "{ "fname":"<name>","lname":"<name>","login":"<login>" }"',status=400)

    uservals = Users(user_first_name=userinfo["fname"],user_last_name=userinfo["lname"],user_login_name=userinfo["login"])
    db.session.add(uservals)
    db.session.commit()
    return Response()

# delete users
@app.route('/deluser/<uid>',methods = ['DELETE'])
def deluser(uid):
    confirm = request.get_json()
    if confirm['yes-i-really-really-mean-it'] == "delete-this-user-i-will-be-responsible-for-the-consiquences":
        usertodel = Users.query.filter(Users.id==uid).first()
        db.session.delete(usertodel)
        db.session.commit()
        return Response()
    else:
        return Response("Failed Validation", status=400)

from application import app,db
from application.models import Tokens
from flask import redirect, Response, jsonify, request
from time import time, localtime
from datetime import datetime
from uuid import uuid4
import requests
import sys

def tokenexpiredcheck(uidcheck):
    # Does a token exist in the db?
    if uidcheck is None:
        return True
    else: 
        # has it expired?
        if uidcheck.user_expiry.strftime( '$s' ) < str(time()):
            return False
    return True

def gennewtoken():
    new_token = str(uuid4())
    new_expiry = time()+3600
    new_datetime = datetime.fromtimestamp(new_expiry)
    return {"new_token":new_token,"new_datetime":new_datetime}


@app.route('/<tok>', methods = ['GET'])
def verify(tok):
    tokenquery = Tokens.query.filter(Tokens.user_token==tok).first()
#    breakpoint()
    tokenexpiredstatus = tokenexpiredcheck(tokenquery)
    if tokenexpiredstatus:
        return jsonify({"expired":"True"})
    else:
        return jsonify({"expired":"False"})



@app.route('/reqtoken/<uid>', methods = ['POST'])
def gentoken(uid):
    response = requests.get('http://bingo:5000/uid/' + uid)
    respjson = response.json()
    if respjson[0].id is None:
        return Response(status=400)
    tokenquery = Tokens.query.filter(Tokens.user_id==uid).first()
    if tokenquery is None:
        new_tok_dict = gennewtoken()
        newtoken = Tokens(user_id=uid,
            user_token=new_tok_dict["new_token"],
            user_expiry=new_tok_dict["new_datetime"])
        db.session.add(newtoken)
        db.session.commit()
        return jsonify({"expired":"False","token":new_tok_dict["new_token"]})
    else:
        new_tok_dict = gennewtoken()
        tokenquery.user_token = new_tok_dict["new_token"]
        tokenquery.user_expiry = new_tok_dict["new_datetime"]
        db.session.commit()
        return jsonify({"expired":"False","token":new_tok_dict["new_token"]})





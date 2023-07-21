from flask import render_template, jsonify, request, make_response
from service import app, db
from service.brain import *
import json
from flask_cors import CORS, cross_origin

@app.route('/', methods=['GET'])
def home():
    return jsonify("Health Check API v.0.1, developed for AAC")

@app.route('/add', methods=['POST'])
def add():
    req = request.get_json()
    doc_id = req['doc_id']
    doctor = json.loads(str(get_doc(doc_id)))
    if doctor != "No":
        if doctor["password"] == req['password']:
            patient_info = {
                "name" : req['name'],
                "age" : req['age'],
                "gender" : req['gender'],
                "problems" : req['problems'],
                "diagnosis" : req['diagnosis'],
                "conditions" : req['conditions'],
                "identity" : req['identity'],
                "description" : req['description'],
                "medicines": req['medicines'],
                "status": req['status'],
                "doctor": req['doctor'],
                "info": req['info'],
                "time": time_cal(),
                "hash": hash_gen_engine()
            }
            result = add_to_db(patient_info)
            return patient_info 
        else:
            return "Incorrect Doctor Password"
    elif doctor == "No":
        return f"No Doctor with gov_id {doc_id} found!"

@app.route('/signin', methods=['POST'])
def signin():
    req = request.get_json()
    doctor = json.loads(str(get_doc(req['doc_id'])))
    if doctor != "No":
        if doctor["password"] == req['password']:
            response = make_response(jsonify(doctor))
            response.set_cookie("last_hash", "fail")
            response._status_code = 200
            response.content_type = "application/json"
            return response
    else:
        return make_response(jsonify("404"))

@app.route('/get/<hash>')
def get(hash):
    req = request.get_json()
    doc_id = req['doc_id']
    doctor = json.loads(str(get_doc(doc_id)))
    if doctor != "No":
        if doctor["password"] == req['password']:
            patient_info = get_db(hash)
            if patient_info != "No":
                key = patient_info.key
                final_info = decrypt_formater(patient_info, key)
                return jsonify((final_info))
            else:
                error_response = jsonify(f"No Patient Information with Hash {hash} available")
                return error_response
        else:
            return "Incorrect Doctor Password"
    elif doctor == "No":
        return f"No Doctor with gov_id {doc_id} found!"
    
@app.route('/status/<hash>/<status>')
def status(hash, status="In Process"):
    patient_info = get_db(hash)
    if patient_info != "No":
        patient_info.status = status
        db.session.commit()
        return "Made Changes"
    else:
        error_response = make_response(jsonify(f"No Patient Information with Hash {hash} available"))
        error_response._status_code = 404
        error_response.set_cookie("last_hash", "fail")
        return error_response

@app.route("/change", methods=['POST'])
def change():
    hash = request.values.get('hash')
    to_change = request.values.get('to_change')
    change = request.values.get('change')
    patient_info = get_db(hash)
    if patient_info != "No":
        setattr(patient_info, to_change, change)
        db.session.commit()
        return str(patient_info)
    else:
        error_response = make_response(
            jsonify(f"No Patient Information with Hash {hash} available"))
        error_response._status_code = 404
        error_response.set_cookie("last_hash", "fail")
        return error_response
    
@app.route('/delete', methods = ['POST'])
def delete():
    hash = request.values.get('hash')
    if hash != None:
        result = del_db(hash)
        return result
    else:
        return "No Hash Provided"

def replace_comma(content):
    import re
    censor_node = re.compile("(')")
    censored = censor_node.sub('"', content)
    return censored

@app.route("/all", methods=["POST"])
def all():
    password = request.args.get("password")
    if password == os.environ.get("PASSWORD"):
        content = Bin.query.all()
        result = []
        for stuff in content:
            key = stuff.key
            final_info = decrypt_formater(stuff, key)
            result.append(final_info)
        return str(replace_comma(str(result)))
    else:
        return "You don't have a password to access this!"
    
@app.route("/search", methods=["POST"])
def search():
    query = request.get_json()['query']
    results = []
    found = False
    response = Bin.query.all()
    for stuff in response:
        if query in str(stuff).lower():
            key = stuff.key
            results.append(decrypt_formater(stuff, key))
            found = True
    if found:
        return jsonify(results)
    else:
        return "No Results found"
@app.route("/search/<query>", methods=["GET"])
def searchquery(query):
    query = query.lower()
    results = []
    found = False
    response = Bin.query.all()
    for stuff in response:
        if query in str(stuff).lower():
            key = stuff.key
            results.append(decrypt_formater(stuff, key))
            found = True
    if found:
        return jsonify(results)
    else:
        return "No Results found"

# Helper Functions

@app.route("/joke", methods=["GET"])
def joke():
    return ran_joke()


@app.route("/fact", methods=["GET"])
def fact():
    return ran_fact()


@app.route("/tiny", methods=["POST"])
def tiny():
    url = request.values.get("url")
    return tinyurl(url)


# @cross_origin(supports_credentials=True)
@app.route("/quote", methods=["GET"])
def quote():
    return ran_quote()

from flask import render_template, jsonify, request, make_response
from service import app, db
from service.brain import *
import json
from flask_cors import CORS, cross_origin

@app.route('/', methods=['GET'])
def home():
    return jsonify("Health Check API v.0.1, developed independently by 'So Called Engineers'")

@app.route('/add', methods=['POST'])
def add():
    doc_id = request.values.get('doc_id')
    doctor = json.loads(str(get_doc(doc_id)))
    if doctor != "No":
        if doctor["password"] == request.values.get('password'):
            patient_info = {
                "name" : request.values.get("name"),
                "age" : request.values.get("age"),
                "gender" : request.values.get("gender"),
                "problems" : str(request.values.get("problems")),
                "diagnosis" : request.values.get("diagnosis"),
                "conditions" : str(request.values.get("conditions")),
                "identity" : request.values.get("identity"),
                "description" : request.values.get("description"),
                "medicines": request.values.get("medicines"),
                "status": request.values.get("status"),
                "doctor": request.values.get("doctor"),
                "info": str(f'[{request.values.get("phone")}, {request.values.get("email")}, {request.values.get("address")}]'),
                "time": time_cal(),
                "hash": hash_gen_engine()
            }
            result = add_to_db(patient_info)
            return patient_info 
        else:
            return "Incorrect Doctor Password"
    elif doctor == "No":
        return f"No Doctor with gov_id {doc_id} found!"

@app.route('/get/<hash>')
def get(hash):
    doc_id = request.values.get('doc_id')
    doctor = json.loads(str(get_doc(doc_id)))
    if doctor != "No":
        if doctor["password"] == request.values.get('password'):
            patient_info = get_db(hash)
            identity = request.values.get('identity')
            if patient_info != "No":
                key = patient_info.key
                final_info = decrypt_formater(patient_info, key)
                response = make_response(jsonify(final_info))
                response.set_cookie("last_hash", hash)
                response._status_code = 200
                response.calculate_content_length()
                response.content_type = "application/json"
                if identity == decrypt(patient_info.identity, patient_info.key):
                    return response
                else:
                    return "Wrong Identity ID"
            else:
                error_response = make_response(jsonify(f"No Patient Information with Hash {hash} available"))
                error_response._status_code = 404
                error_response.set_cookie("last_hash", "fail")
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

@app.route('/ai/<reason>', methods = ['POST'])
def ai(reason="treatment"):
    import openai
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    model_engine = "text-davinci-003"
    problems = str(request.values.get('problems')).split((", "))
    temp_text = ""
    for problem in problems:
        temp_text = temp_text + "and " + problem
    prompt =f"""You are a doctor. Return just three effective {reason} in the 
    form of a json that is not consulting with another doctor if a patient has {temp_text}.
constraints: Don't provide any pretext or post text. Just directly write the solution
and donot tell me that you are a medical professional. Just give me an answer. Don't include anything like
answer: or Answer: or result:. Just give a good formatted json. Name the first treatment as first and second treatment as second.
    """
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    result = completion["choices"][0]
    return jsonify(json.loads(result["text"]))

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
    query = request.values.get("query")
    results = []
    found = False
    response = Bin.query.all()
    for stuff in response:
        if query in str(stuff):
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

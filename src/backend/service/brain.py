import base64
from service.models import Bin, Doctors
import random
import string
from datetime import datetime, date
from service import app, db
import json
import requests
from base64 import b64encode, b64decode
import hashlib
import os
from cryptography.fernet import Fernet


def hash_gen_engine():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    whole = lower + upper + digits
    hash_string = random.sample(whole, 8)
    hash = "".join(hash_string)
    return hash


def otp_gen_engine():
    digits = string.digits
    whole = digits
    otp_string = random.sample(whole, 6)
    otp = "".join(otp_string)
    return otp


def censor(content):
    import re
    censor_node = re.compile(
        '([Ff][Uu]*[Cc]*[Kk]|[Ss]+[Ee]+[Xx]|[Dd]+[Ii]*[Cc]*[Kk]|[Pp][Us][Us][Yy]|[Pp][Oo]+[Rr]+[Nn])')
    censored = censor_node.sub("*CENSORED*", content)
    return censored


def time_cal():
    current_t = datetime.now()
    current_date = str(date.today())
    current_t_f = current_t.strftime("%H:%M:%S")
    time_date = (f'{current_t_f} {current_date}')
    return time_date


def key_gen():
    key = Fernet.generate_key()
    return key


def encrypt(content, key):
    # print(key.encode())
    fernet = Fernet(key)
    encrypted_content = fernet.encrypt(content.encode())
    return encrypted_content.decode()


def decrypt(content, key):
    # print(bytes(key, encoding='utf8').decode())
    # print(key.encode())
    fernet = Fernet(key.encode())
    decrypted_content = (fernet.decrypt(content.encode())).decode()
    return decrypted_content

def add_to_db(patient):
    key = Fernet.generate_key().decode()
    patient_info = Bin(
        name=patient["name"], age=patient["age"], gender=patient["gender"],
        problems=encrypt(patient["problems"], key), diagnosis=encrypt(patient["diagnosis"], key),
        description=encrypt(patient["description"], key), status=patient["status"],
        contact=encrypt(patient["info"], key),
        key=key,
        doctor=patient["doctor"], time=patient["time"],
        identity=encrypt(patient["identity"], key),
        conditions=encrypt(patient["conditions"], key), medicines=encrypt(patient["medicines"], key),
        hash=patient["hash"])
    db.session.add(patient_info)
    db.session.commit()
    return patient_info


def doc_add(doc):
    doc_info = Doctors(name=doc["name"], gender=doc["gender"], hash=hash_gen_engine(
    ), password=doc["password"], privs=doc["privs"], gov_id=doc["gov_id"])
    db.session.add(doc_info)
    db.session.commit()
    return doc_info


def doc_all():
    debug_content = Doctors.query.all()
    return debug_content


def get_db(hash):
    patient = Bin.query.filter_by(hash=hash).first()
    if patient == None:
        return "No"
    else:
        return patient


def get_doc(hash):
    doctor = Doctors.query.filter_by(hash=hash).first()
    if doctor == None:
        return "No"
    else:
        return doctor


def del_db(hash):
    content = Bin.query.filter_by(hash=hash).first()
    if content == None:
        return f"No Entry with hash {hash}"
    else:
        Bin.query.filter_by(hash=hash).delete()
        db.session.commit()
        return "Deleted Entry"


def ran_quote():
    try:
        quotes_page = json.loads(requests.get(
            "https://api.quotable.io/random").content)
        quote_list = [quotes_page["content"], quotes_page["author"]]
        return quote_list
    except:
        quote_list = ["Never give up!", "EveryOne in The World!"]


def ran_fact():
    fact_page = json.loads(requests.get(
        "https://useless-facts.sameerkumar.website/api").content)
    fact = fact_page["data"]
    return fact


def tinyurl(url):
    tinyurl_page = str(requests.get(
        f'https://tinyurl.com/api-create.php?url={url}').content).replace("b'", "").replace("'", "")
    return tinyurl_page


def decrypt_formater(content, key):
    final_info = {
        "name": content.name,
        "age": content.age,
        "gender": content.gender,
        "problems": decrypt(content.problems, key),
        "diagnosis": decrypt(content.diagnosis, key),
        "description": decrypt(content.description, key),
        "status": content.status,
        "contact": decrypt(content.contact, key),
        "doctor": content.doctor,
        "time": content.time,
        "identity": decrypt(content.identity, key),
        "conditions": decrypt(content.conditions, key),
        "medicines": decrypt(content.medicines, key),
        "hash": content.hash
    }
    return final_info


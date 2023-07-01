from service import app, db

class Bin(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=80))
    age = db.Column(db.String(length=8), nullable=True)
    gender = db.Column(db.Text())
    hash = db.Column(db.Text())
    problems = db.Column(db.Text())
    diagnosis = db.Column(db.Text())
    description = db.Column(db.Text())
    status = db.Column(db.Text())
    contact = db.Column(db.String())
    identity = db.Column(db.String())
    key = db.Column(db.UnicodeText())
    doctor = db.Column(db.String())
    conditions = db.Column(db.Text())
    medicines = db.Column(db.Text())
    time = db.Column(db.String())

    def __init__(self, name, hash, identity, age, gender, problems, diagnosis, description, status, contact , key, doctor, conditions, medicines, time):
        self.name = name
        self.age = age
        self.gender = gender
        self.problems = problems
        self.identity = identity
        self.diagnosis = diagnosis
        self.description = description
        self.status = status
        self.key = key
        self.contact = contact
        self.doctor = doctor
        self.time = time
        self.conditions = conditions
        self.medicines = medicines
        self.hash = hash

    def __repr__(self):
        import json
        result = {
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "problems": self.problems,
            "diagnosis": self.diagnosis,
            "medicines": self.medicines,
            "description": self.description,
            "status": self.status,
            "contact": self.contact,
            "doctor": self.doctor,
            "time": self.time,
            "conditions": self.conditions,
            "hash": self.hash
        }
        return json.dumps(result)

class Doctors(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=80))
    gender = db.Column(db.Text())
    hash = db.Column(db.Text())
    password = db.Column(db.Text())
    privs = db.Column(db.Text())
    gov_id = db.Column(db.Text())

    def __init__(self, name, gender, hash, password, privs, gov_id):
        self.name = name
        self.gender = gender
        self.hash = hash
        self.password = password
        self.privs = privs
        self.gov_id = gov_id
    
    def __repr__(self):
        import json
        result = {
            "name": self.name,
            "gender": self.gender,
            "hash": self.hash,
            "password": self.password,
            "privs": self.password,
            "gov_id": self.gov_id
        }
        return json.dumps(result)
    
db.create_all()
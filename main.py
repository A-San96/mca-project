from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from database import SessionLocal,engine
from passlib.context import CryptContext
from pydantic import parse_obj_as
from datetime import timedelta

from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi_mail.email_utils import DefaultChecker

import models
import schemas
import meet

tags_metadata = [
    {
        "name": "Classes",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
    },
    {
        "name": "Matières",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        
    },
    {
        "name": "Professeurs",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        
    },
    {
        "name": "Etudiants",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        
    }
]

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conf = ConnectionConfig(
    MAIL_USERNAME = " etudiant@projectesp.sn ",
    MAIL_PASSWORD = "ProjectESP",
    MAIL_FROM = " etudiant@projectesp.sn ",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    TEMPLATE_FOLDER='./email '
)




app = FastAPI(
    title="Google Meet Course Analyzer API",
    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit",
    version="0.1.0",
    openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Management of authentication
SECRET = "24523862eb1ead13af04778bb8147ed58af9a9008b244029"
manager = LoginManager(SECRET, token_url='/auth/token')

fake_db = {'johndoe@email.com': {'password': 'passer123'}}

@manager.user_loader
def load_user(email: str):  # get user in the database
    user = fake_db.get(email)
    return user

# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/auth/token')
def login( data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email), expires=timedelta(hours=2)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

#########################################################

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def get_subjects_of_teacher(profId, db):
    statement = 'SELECT prof_matiere.idMatiere, matiere.nom FROM prof_matiere '
    statement +='INNER JOIN matiere ON prof_matiere.idMatiere = matiere.idMatiere ' 
    statement += 'WHERE prof_matiere.idProf = '+str(profId)+';'
    # list of tuples
    result = db.execute(statement)
    myresult = []
    for row in result:
        myresult.append(dict(row))
    matieres = parse_obj_as(List[schemas.Matiere],myresult)

    return matieres

def get_class_of_student(etudiantId, db):
    statement = 'SELECT Etudiant.idClasse, Classe.nomClasse FROM Etudiant '
    statement +='INNER JOIN Classe ON Etudiant.idClasse = Classe.idClasse '
    statement += 'WHERE Etudiant.idEtudiant = '+str(etudiantId)+';'
    result = db.execute(statement)

    return result


############ Route for make operation in Classes ##########

@app.get('/api/classes',response_model=List[schemas.Classe],tags=["Classes"])
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(models.Classe).all()
    return classes

@app.get('/api/classe/{classeId}',response_model=schemas.Classe,tags=["Classes"])
def get_class(classeId: int,db: Session = Depends(get_db)):
    my_class = db.query(models.Classe).filter(models.Classe.idClasse==classeId).first()
    return my_class

@app.post('/api/classe',tags=["Classes"])
def create_classe(classe: schemas.ClasseIn,db: Session = Depends(get_db), user=Depends(manager)):
    myclasse = models.Classe(nomClasse = classe.nomClasse)
    db.add(myclasse)
    db.commit()
    return {'msg':'Classe créée'}

############ Route for make operation in Subjects ##########

@app.get('/api/matiere',response_model=List[schemas.Matiere], tags=["Matières"])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Matiere).all()
    return subjects

@app.get('/api/matiere/{matiereId}',response_model=schemas.Matiere,tags=["Matières"])
def get_subject(matiereId: int,db: Session = Depends(get_db)):
    my_subject = db.query(models.Matiere).filter(models.Matiere.idMatiere == matiereId).first()
    return my_subject

@app.post('/api/matiere',tags=["Matières"])
def create_subject(matiere: schemas.MatiereIn,db: Session = Depends(get_db), user=Depends(manager)):
    ma_matiere = models.Matiere(nom = matiere.nom)
    db.add(ma_matiere)
    db.commit()
    return {'msg':'Matiere créée'}

############ Route for make operation in Teachers ##########

@app.get('/api/professeurs',response_model=List[schemas.Professeur], tags=["Professeurs"])
def get_teachers(db: Session = Depends(get_db)):
    profs = db.query(models.Professeur).all()
    for i in range(len(profs)):
        profs[i].matiere = get_subjects_of_teacher(profs[i].idProf, db)
    
    return profs

@app.get('/api/professeur/{profId}',response_model=schemas.Professeur,tags=["Professeurs"])
def get_subject(profId: int,db: Session = Depends(get_db)):
    my_teacher = db.query(models.Professeur).filter(models.Professeur.idProf == profId).first()
    my_teacher.matiere= get_subjects_of_teacher(profId, db)

    return my_teacher

@app.post('/api/professeur', tags=["Professeurs"])
def create_teacher(prof: schemas.ProfesseurIn,db: Session = Depends(get_db), user=Depends(manager)):
    mon_prof = models.Professeur(prenom=prof.prenom,nom=prof.nom,email=prof.email,password_hash=get_password_hash(prof.password))
    db.add(mon_prof)
    db.commit()
    return {'msg':'Professeur créée'}

#Table d'association Prof_matiere
@app.post('/api/professeur-matiere', tags=["Professeurs"])
def attribute_subject(data: schemas.ProfMatiereIn,db: Session = Depends(get_db)):
    teacher_exists = db.query(exists().where(models.Professeur.idProf == data.idProf)).scalar()
    subject_exists = db.query(exists().where(models.Matiere.idMatiere == data.idMatiere)).scalar()
    if teacher_exists and subject_exists:
        query = models.t_prof_matiere.insert().values(idProf = data.idProf, idMatiere = data.idMatiere)
        db.execute(query)
        db.commit()
        return {'msg':'Attribution faite'}
    else :
        return {'msg':'Matiere ou Prof inexistant'}


############ Route for make operation in Student ##########
@app.get('/api/etudiants',response_model=List[schemas.Etudiant], tags=["Etudiants"])
def get_students(db: Session = Depends(get_db)):
    statement = 'SELECT  idEtudiant, prenom, nom, email FROM Etudiant;'
    students = db.execute(statement)
    mylist =[]
    for row in students:
        mylist.append(dict(row))
    print(mylist)
    for i in range(len(mylist)):
        result = get_class_of_student(mylist[i]['idEtudiant'],db)
        for row in result:
            mylist[i]['classe'] = dict(row)

    return parse_obj_as(List[schemas.Etudiant],mylist)

@app.get('/api/etudiant/{etudiantId}',response_model=schemas.Etudiant, tags=["Etudiants"])
def get_student(etudiantId: int,db: Session = Depends(get_db)):
    statement = 'SELECT  idEtudiant, prenom, nom, email FROM Etudiant where idEtudiant ='+str(etudiantId)+';'
    student = db.execute(statement)
    for row in student:
        my_student = dict(row)
    result = get_class_of_student(etudiantId,db)
    for row in result:
        my_student['classe'] = dict(row)

    return parse_obj_as(schemas.Etudiant,my_student)

################## Route for get meet data #############

@app.get('/api/meet')
def get_meet_data():
    return meet.meet_data('EAXKQBDIGW')

@app.get('/api/evolution_note')
def get_evolution_note():
    return {'labels': ['1ère', '2ème', '3ème', '4ème', '5ème', '6ème', '7ème'], 'datasets': [{'label': 'Langage C', 'data': [9, 17, 13, 10, 12, 19, 14], 'fill': False}, {'label': 'Proba et Stat', 'fill': False, 'data': [10, 15, 9, 17, 10, 13, 7]}]}

############ Route evaluation note form #########
@app.post("/email")
async def send_evalution_form(email: schemas.EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=email.dict().get("body"),
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="evaluation_email_template.html") 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
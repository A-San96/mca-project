from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from database import SessionLocal,engine
from passlib.context import CryptContext
from pydantic import parse_obj_as


#from schemas import City
import models
import schemas

models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        
    }
]


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

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def get_subjects_by_teacher_id(prof_id, db):
    statement = 'SELECT prof_matiere.idMatiere, matiere.nom FROM prof_matiere '
    statement +='INNER JOIN matiere ON prof_matiere.idMatiere = matiere.idMatiere ' 
    statement += 'WHERE prof_matiere.idProf = '+str(prof_id)+';'
    # list of tuples
    result = db.execute(statement)
    myresult = []
    for row in result:
        myresult.append(dict(row))
    matieres = parse_obj_as(List[schemas.Matiere],myresult)

    return matieres


############ Route for make operation in Classes ##########

@app.get('/api/classes',response_model=List[schemas.Classe],tags=["Classes"])
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(models.Classe).all()
    return classes

@app.get('/api/classes/{class_id}',response_model=schemas.Classe,tags=["Classes"])
def get_class(class_id: int,db: Session = Depends(get_db)):
    my_class = db.query(models.Classe).filter(models.Classe.idClasse==class_id).first()
    return my_class

@app.post('/api/classes',tags=["Classes"])
def create_classe(classe: schemas.ClasseIn,db: Session = Depends(get_db)):
    myclasse = models.Classe(nomClasse = classe.nomClasse)
    db.add(myclasse)
    db.commit()
    return {'msg':'Classe créée'}

############ Route for make operation in Subjects ##########

@app.get('/api/matieres',response_model=List[schemas.Matiere], tags=["Matières"])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Matiere).all()
    return subjects

@app.get('/api/matieres/{matiere_id}',response_model=schemas.Matiere,tags=["Matières"])
def get_subject(matiere_id: int,db: Session = Depends(get_db)):
    my_subject = db.query(models.Matiere).filter(models.Matiere.idMatiere == matiere_id).first()
    return my_subject

@app.post('/api/matieres',tags=["Matières"])
def create_subject(matiere: schemas.MatiereIn,db: Session = Depends(get_db)):
    ma_matiere = models.Matiere(nom = matiere.nom)
    db.add(ma_matiere)
    db.commit()
    return {'msg':'Matiere créée'}

############ Route for make operation in Teachers ##########

@app.get('/api/professeurs',response_model=List[schemas.Professeur], tags=["Professeurs"])
def get_teachers(db: Session = Depends(get_db)):
    profs = db.query(models.Professeur).all()
    for i in range(len(profs)):
        profs[i].matiere = get_subjects_by_teacher_id(profs[i].idProf, db)
    
    return profs

@app.get('/api/professeurs/{prof_id}',response_model=schemas.Professeur,tags=["Professeurs"])
def get_subject(prof_id: int,db: Session = Depends(get_db)):
    my_teacher = db.query(models.Professeur).filter(models.Professeur.idProf == prof_id).first()
    my_teacher.matiere= get_subjects_by_teacher_id(prof_id, db)

    return my_teacher

@app.post('/api/professeurs', tags=["Professeurs"])
def create_teacher(prof: schemas.ProfesseurIn,db: Session = Depends(get_db)):
    mon_prof = models.Professeur(prenom=prof.prenom,nom=prof.nom,email=prof.email,password_hash=get_password_hash(prof.password))
    db.add(mon_prof)
    db.commit()
    return {'msg':'Professeur créée'}
#Table d'association Prof_matiere
@app.post('/api/professeur/matiere', tags=["Professeurs"])
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
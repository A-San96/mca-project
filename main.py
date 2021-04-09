from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal,engine
from passlib.context import CryptContext

#from schemas import City
import models
import schemas

models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

dbase = [
  {
    "name": "Dakar",
    "timezone": "Senegal/Dakar"
  },
  {
    "name": "Ziguinchor",
    "timezone": "Senegal/Ziguinchor"
  },
  {
    "name": "Thies",
    "timezone": "Senegal/Thies"
  }
]


app = FastAPI(title="Google Meet Analyzer API")

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


@app.get('/api/classes',response_model=List[schemas.Classe])
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(models.Classe).all()
    return classes

@app.post('/api/classes')
def create_classe(classe: schemas.ClasseIn,db: Session = Depends(get_db)):
    myclasse = models.Classe(nomClasse = classe.nomClasse)
    db.add(myclasse)
    db.commit()
    return {'msg':'Classe créée'}

@app.get('/api/matieres',response_model=List[schemas.Matiere])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Matiere).all()
    return subjects

@app.post('/api/matieres')
def create_subject(matiere: schemas.MatiereIn,db: Session = Depends(get_db)):
    ma_matiere = models.Matiere(nom = matiere.nom)
    db.add(ma_matiere)
    db.commit()
    return {'msg':'Matiere créée'}

@app.get('/api/professeurs',response_model=List[schemas.Professeur])
def get_teachers(db: Session = Depends(get_db)):
    profs = db.query(models.Professeur).all()
    return profs

@app.post('/api/professeurs')
def create_teacher(prof: schemas.ProfesseurIn,db: Session = Depends(get_db)):
    mon_prof = models.Professeur(prenom=prof.prenom,nom=prof.nom,email=prof.email,password_hash=get_password_hash(prof.password))
    db.add(mon_prof)
    db.commit()
    return {'msg':'Professeur créée'}


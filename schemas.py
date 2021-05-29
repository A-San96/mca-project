from typing import List, Dict, Any
from pydantic import BaseModel, EmailStr



class Classe(BaseModel):
    idClasse: int
    nomClasse: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': 
                {
                    'idClasse': 1,
                    'nomClasse': 'Licence 3 GLSI'
                },
                
        }


class ClasseIn(BaseModel):
    nomClasse: str

    class Config:
        orm_mode = True



class Matiere(BaseModel):
    idMatiere: int
    nom: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': 
                {
                    'idMatiere': 1,
                    'nom': 'SGBD Avancés'
                },
                
        }

class MatiereIn(BaseModel):
    nom: str

    class Config:
        orm_mode = True


class Professeur(BaseModel):
    idProf: int 
    prenom: str 
    nom: str 
    email: str
    matiere : List[Matiere]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': 
                {
                    'idProf': 2,
                    'prenom': 'Jane',
                    'nom': 'Doe',
                    'email': 'jane.doe@mail.net',
                    "matiere": [
                        {
                        "idMatiere": 1,
                        "nom": "Génie Logiciel"
                        },
                        {
                        "idMatiere": 2,
                        "nom": "POO Avancée"
                        },
                        {
                        "idMatiere": 3,
                        "nom": "SGBD"
                        }
                    ]
                }
                
        }

class ProfesseurIn(BaseModel):
    prenom: str 
    nom: str 
    email: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': 
                {
                    'prenom': 'John',
                    'nom': 'Doe',
                    'email': 'john.doe@mail.net',
                    'password' : 'qwerty123'
                },
                
        }

class ProfMatiereIn(BaseModel):
    ## Peut-on utiliser l'email et le nom de la matiere pour faire simple ??
    idProf: int
    idMatiere: int

    class Config:
        orm_mode = True


class Etudiant(BaseModel):
    idEtudiant: int
    prenom:str
    nom: str
    email: str
    classe: Classe

    class Config:
        schema_extra = {
                'example': 
                    {
                        "idEtudiant": 1,
                        "prenom": "Assane",
                        "nom": "Diatta",
                        "email": "a.diatta@email.com",
                        "classe": {
                            "idClasse": 1,
                            "nomClasse": "L3GLSI"
                        }
                    }
                    
            }

class EtudiantIn(BaseModel):
    prenom:str
    nom: str
    email: str
    idClasse: int

    class Config:
        orm_mode = True

class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]



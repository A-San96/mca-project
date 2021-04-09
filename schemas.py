from pydantic import BaseModel



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

class MatiereIn(BaseModel):
    nom: str

    class Config:
        orm_mode = True


class Professeur(BaseModel):
    idProf: int 
    prenom: str 
    nom: str 
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': 
                {
                    'idProf': 2,
                    'prenom': 'Mohamed',
                    'nom': 'Diop',
                    'email': 'mohamed.diop@esp.sn'
                },
                
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


# coding: utf-8
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from database import Base

metadata = Base.metadata

class Administrateur(Base):
    __tablename__ = 'administrateur'

    id = Column(Integer, primary_key=True)
    login = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)


class Classe(Base):
    __tablename__ = 'classe'

    idClasse = Column(Integer, primary_key=True)
    nomClasse = Column(String(50), nullable=False)


class Matiere(Base):
    __tablename__ = 'matiere'

    idMatiere = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False, unique=True)

    professeur = relationship('Professeur', secondary='prof_matiere')


class Professeur(Base):
    __tablename__ = 'professeur'

    idProf = Column(Integer, primary_key=True)
    prenom = Column(String(100), nullable=False)
    nom = Column(String(100), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)


class Etudiant(Base):
    __tablename__ = 'etudiant'

    idEtudiant = Column(Integer, primary_key=True)
    prenom = Column(String(100), nullable=False)
    nom = Column(String(100), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    idClasse = Column(ForeignKey('classe.idClasse'), nullable=False, index=True)

    classe = relationship('Classe')


t_prof_matiere = Table(
    'prof_matiere', metadata,
    Column('idProf', ForeignKey('professeur.idProf'), primary_key=True, nullable=False),
    Column('idMatiere', ForeignKey('matiere.idMatiere'), primary_key=True, nullable=False, index=True)
)


class Seance(Base):
    __tablename__ = 'seance'

    idSeance = Column(Integer, primary_key=True)
    dateDebut = Column(Date, nullable=False)
    dateFin = Column(Date, nullable=False)
    etatPartage = Column(TINYINT(1), nullable=False)
    noteSeance = Column(Float)
    idProf = Column(ForeignKey('professeur.idProf'), nullable=False, index=True)
    idClasse = Column(ForeignKey('classe.idClasse'), nullable=False, index=True)

    classe = relationship('Classe')
    professeur = relationship('Professeur')


class Evaluation(Base):
    __tablename__ = 'evaluation'

    idEvaluation = Column(Integer, primary_key=True)
    note = Column(Float, nullable=False)
    idEtudiant = Column(ForeignKey('etudiant.idEtudiant'), nullable=False, index=True)
    idSeance = Column(ForeignKey('seance.idSeance'), nullable=False, index=True)

    etudiant = relationship('Etudiant')
    seance = relationship('Seance')


class Presence(Base):
    __tablename__ = 'presence'

    idPresence = Column(Integer, primary_key=True)
    idEtudiant = Column(ForeignKey('etudiant.idEtudiant'), nullable=False, index=True)
    idSeance = Column(ForeignKey('seance.idSeance'), nullable=False, index=True)
    nbrConnexion = Column(Integer, nullable=False)
    nbrDeconnexion = Column(Integer, nullable=False)
    dureeConnexion = Column(Integer, nullable=False)
    typeTerminal = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)

    etudiant = relationship('Etudiant')
    seance = relationship('Seance')

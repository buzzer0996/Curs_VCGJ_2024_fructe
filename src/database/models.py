import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# Configurarea bazei de date
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app):
    """
    Binds a Flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    """
    Drops the database tables and starts fresh
    Can be used to initialize a clean database
    """
    db.drop_all()
    db.create_all()

class Fruct(db.Model):
    """
    A persistent fruit entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'fruct'  # Asigură-te că ai definit numele tabelului

    id = Column(Integer, primary_key=True)  # Poți elimina .with_variant dacă nu folosești variante
    title = Column(String(80), unique=True)
    color = Column(String(20), nullable=False)
    parts = Column(Integer, nullable=False)
    description = Column(String)  # Descrierea fructului

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'color': self.color,
            'parts': self.parts,
            'description': self.description
        }

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'color': self.color,
            'parts': self.parts,
            'description': self.description
        }

    def insert(self):
        """
        Inserts a new model into the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes a model from the database
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """
        Updates a model in the database
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


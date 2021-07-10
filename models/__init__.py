from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Paciente(db.Model):
    __tablename__ = 'pacientes'    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    
     
    def __init__(self, name, email, senha):
        self.public_id
        self.name = name
        self.email = email
        self.senha = senha
        
        
    def json(self):
        return{'name': self.name, 'email': self.email,
               'id_publico': self.public_id}
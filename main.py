#from flask import Flask, request
from blueprints.pacientes_endpoints import blueprint,app as pacientes_endpoints,app
from models import db as db



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
        
    
    
    
    



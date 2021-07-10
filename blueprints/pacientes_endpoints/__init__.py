from flask import Flask, Blueprint, request, jsonify, make_response
import uuid  # para id publico
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Paciente 
# imports para pyJwt
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
app.config['SECRET_KEY'] = 'thisissecret'

def token_requerid(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt é passado no request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # retorna 401 se o token não for passado
        if not token:
            return jsonify({'message': 'faltando passar o token'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            usuario_atual = Paciente.query\
                .filter_by(public_id=data['public_id'])\
                .first()
            
        except:
            return jsonify({
                'message': 'Token inválido'
            }), 401
        return f(usuario_atual, *args, **kwargs)
    
    return decorated
    
            

@blueprint.route('/pacientes', methods=['GET'])
@token_requerid
def listar_paciente(usuario_atual):
    
    if request.method == "GET":
        pacientes = Paciente.query.all()
        output = []
        for paciente in pacientes:
            output.append({
                'public_id': paciente.public_id,
                'name': paciente.name,
                'email': paciente.email
            })
        
        return jsonify({'pacientes': output})

@blueprint.route('/paciente/login', methods=['POST'])
def login():
    
    auth = request.form
  
    if not auth or not auth.get('email') or not auth.get('senha'):
        # returns 401 if any email or / and senha is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )
  
    paciente = Paciente.query\
        .filter_by(email=auth.get('email'))\
        .first()
  
    if not paciente:
        # returns 401 if paciente does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="paciente does not exist !!"'}
        )
  
    if check_password_hash(paciente.senha, auth.get('senha')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': paciente.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
    # returns 403 if senha is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong senha !!"'}
    )        

            
@blueprint.route('/paciente/cadastro', methods=['POST'])    
def cadastra_paciente():
    data = request.form
  
    # gets name, email e senha
    name, email = data.get('name'), data.get('email')
    senha = data.get('senha')
  
    # checking for existing paciente
       paciente = Paciente.query\
        .filter_by(email=email)\
        .first()
    if not paciente:
        # database ORM object
        paciente = Paciente(
            #public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            senha=generate_password_hash(senha)
            
        )
        # insert paciente
        db.session.add(paciente)
        db.session.commit()
  
        return make_response('Cadastrado com sucesso.', 201)
    else:
       
        return make_response('Paciente existente', 202)



"""
@blueprint.route('/paciente/<id>', methods=['PUT'])
def update_paciente(id):
    data = request.get_json()
    paciente = Paciente.query.filter_by(id=id).first()
    if paciente:
        paciente.name = data["name"]
        paciente.email = data["email"]
        paciente.senha = data["senha"]
        
    if not paciente:
        return jsonify({"message": 'paciente não encontrado pelo id'})
    db.session.add(paciente)
    db.session.commit()
    return paciente.json()


@blueprint.route('/paciente/<id>', methods=['DELETE'])
def delete_paciente(id):
    paciente = Paciente.query.filter_by(id=id).first()
    if not paciente:
        return jsonify({'message': 'paciente não encontrado'})
    db.session.delete(paciente)
    db.session.commit()
    return jsonify({'message': 'paciente deletado com sucesso'})"""


app.register_blueprint(blueprint)
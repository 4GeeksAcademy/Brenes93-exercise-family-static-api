"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET']) #devuelve todos los miembros de la familia Jackson.
def get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members() #obtener los miembros.
    if members is None:
        return jsonify({
            "error": "Fallo del servidor"
        }), 500
    if members == []:
        return jsonify({"msg":"miembros no encontrados"}),404 #Si no hay miembros error 404
    response_body = {"self._members": members}


    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET']) #obtener miembro segun id
def get_member(member_id): #creamos parametro para buscar un miembro

    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({
            "error": "Fallo del servidor"
        }), 500
    if member == []:
        return jsonify({"msg":"miembro no encontrado"}),404
    response_body = {"self._members": member}


    return jsonify(response_body), 200    

@app.route('/members', methods=['POST']) #Añadir un miebro 
def add_member():
    data = request.get_json()  # obtenr datos enviados en formato JSON

    if not data:
        return jsonify({"error": "Faltan datos"}), 400

    # Crear un nuevo miembro con los datos recibidos
    new_member = {
        "id": jackson_family._generate_id(),
        "first_name": data.get("first_name"),
        "last_name": jackson_family.last_name,
        "age": data.get("age"),
        "lucky_numbers": data.get("lucky_numbers")
    }

    # Añadimos el miembro a la familia
    jackson_family.add_member(new_member)

    # Respondemos con el miembro agregado
    return jsonify(new_member), 200

@app.route('/members/<int:member_id>', methods=['DELETE']) # eliminamos un miembro por su id
def delete_member(member_id):
    
    member = jackson_family.delete_member(member_id)
    
    if member is None:
        #error inesperado
        return jsonify({"error": "Erro en el servidor"}), 500
    elif member:
        # miembro eliminado con exito
        return jsonify({"done": True}), 200
    else:
        # Si no se encuentra al miembro
        return jsonify({"error": "Member not found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


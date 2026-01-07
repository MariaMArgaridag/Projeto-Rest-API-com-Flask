
#novo
from flask import Blueprint, request, jsonify
from app.service.defense_mechanism_service import DefenseMechanismService
from app.repository.defense_mechanism_repository import DefenseMechanismRepository
from app.database import db
from app.utils import generate_public_id

# Blueprint: tudo o que estiver aqui começa com /defense_mechanisms
defense_mechanism_bp = Blueprint(
    "defense_mechanisms",
    __name__,
    url_prefix="/defense_mechanisms"
)

# Liga Camada 1 -> Camada 2 (service) -> Camada 3 (repository)
service = DefenseMechanismService(DefenseMechanismRepository(db))


def _format_response(data):
    """Transforma Id em public_id na resposta"""
    if data is None:
        return data
    
    # Se for uma lista, processa cada item
    if isinstance(data, list):
        result = []
        for item in data:
            if isinstance(item, dict):
                item_copy = dict(item)  # Faz uma cópia
                # Trata tanto 'id' quanto 'Id' (case-insensitive)
                if 'Id' in item_copy:
                    item_copy['public_id'] = generate_public_id(item_copy['Id'])
                    del item_copy['Id']
                elif 'id' in item_copy:
                    item_copy['public_id'] = generate_public_id(item_copy['id'])
                    del item_copy['id']
                result.append(item_copy)
            else:
                result.append(item)
        return result
    
    # Se for um dicionário, processa o item
    if isinstance(data, dict):
        data_copy = dict(data)  # Faz uma cópia
        # Trata tanto 'id' quanto 'Id' (case-insensitive)
        if 'Id' in data_copy:
            data_copy['public_id'] = generate_public_id(data_copy['Id'])
            del data_copy['Id']
        elif 'id' in data_copy:
            data_copy['public_id'] = generate_public_id(data_copy['id'])
            del data_copy['id']
        return data_copy
    
    return data


@defense_mechanism_bp.post("/")
def create_defense_mechanism():
    """
    Cria um novo mecanismo de defesa
    ---
    tags:
      - Defense Mechanisms
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - mechanism
          properties:
            mechanism:
              type: string
              example: Firewall
    responses:
      201:
        description: Mecanismo criado
      400:
        description: Dados inválidos
    """
    data = request.json or {}

    mechanism = data.get("mechanism")

    if not mechanism or not isinstance(mechanism, str):
        return jsonify({"error": "Mechanism invalid"}), 400

    created = service.create(mechanism)
    return jsonify(_format_response(created)), 201


@defense_mechanism_bp.get("/")
def list_defense_mechanisms():
    """
    Lista todos os mecanismos de defesa
    ---
    tags:
      - Defense Mechanisms
    responses:
      200:
        description: Lista de mecanismos de defesa
    """
    return jsonify(_format_response(service.list())), 200



@defense_mechanism_bp.get("/<id>")
def get_by_id_defense_mechanism(id):
    """
    Obtém um mecanismo de defesa pelo ID (int) ou public_id (hash)
    ---
    tags:
      - Defense Mechanisms
    parameters:
      - in: path
        name: id
        required: true
        type: string
        example: 1 ou hash
    responses:
      200:
        description: Mecanismo encontrado
      404:
        description: Não encontrado
    """
    result = None
    try:
        int_id = int(id)
        result = service.get_by_id(int_id)
    except ValueError:
        all_items = service.list()
        for item in all_items:
            real_id = item.get('Id') or item.get('id')
            if real_id and generate_public_id(real_id) == id:
                result = item
                break
    if result is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(_format_response(result)), 200


@defense_mechanism_bp.put("/<int:id>")
def update_defense_mechanism(id):
    """
    Atualiza um mecanismo de defesa pelo ID
    ---
    tags:
      - Defense Mechanisms
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - mechanism
          properties:
            mechanism:
              type: string
              example: VPN
    responses:
      200:
        description: Mecanismo atualizado
      400:
        description: Dados inválidos
      404:
        description: Não encontrado
    """
    data = request.json or {}
    mechanism = data.get("mechanism")

    if not mechanism or not isinstance(mechanism, str):
        return jsonify({"error": "Mechanism invalid"}), 400

    result = service.update(id, mechanism)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(_format_response(result)), 200


@defense_mechanism_bp.delete("/<int:id>")
def delete_defense_mechanism(id):
    """
    Apaga um mecanismo de defesa pelo ID
    ---
    tags:
      - Defense Mechanisms
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        example: 1
    responses:
      204:
        description: Apagado com sucesso
      404:
        description: Não encontrado
      409:
        description: Não pode ser apagado (FK)
    """
    result = service.delete(id)

    if result is False:
        return jsonify({"error": "Not found"}), 404

    if result == "FK":
        return jsonify({"error": "It cannot be deleted"}), 409

    return "", 204

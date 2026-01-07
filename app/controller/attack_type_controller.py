

#novo codigo 

from flask import Blueprint, request, jsonify
from app.service.attack_type_service import AttackTypeService
from app.repository.attack_type_repository import AttackTypeRepository
from app.database import db
from app.utils import generate_public_id

# Blueprint: tudo o que estiver aqui vai começar com /attack_types
attack_type_bp = Blueprint("attack_types", __name__, url_prefix="/attack_types")

# Liga Camada 1 -> Camada 2 (service) -> Camada 3 (repository)
service = AttackTypeService(AttackTypeRepository(db))


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


@attack_type_bp.post("/")
def create_attack_type():
    """
    Cria um novo tipo de ataque
    ---
    tags:
      - Attack Types
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - type
          properties:
            type:
              type: string
              example: DDoS
    responses:
      201:
        description: Tipo de ataque criado
      400:
        description: Dados inválidos
    """
    data = request.json or {}

    # Evitar usar "type" como variável (é nome reservado do Python)
    attack_type_name = data.get("type")

    # Validação simples (Camada 1): tem de existir e ser string
    if not attack_type_name or not isinstance(attack_type_name, str):
        return jsonify({"error": "Invalid type"}), 400

    created = service.create(attack_type_name)
    return jsonify(_format_response(created)), 201


@attack_type_bp.get("/")
def list_attack_types():
    """
    Lista todos os tipos de ataque
    ---
    tags:
      - Attack Types
    responses:
      200:
        description: Lista de tipos de ataque
    """
    results = service.list()
    return jsonify(_format_response(results)), 200



@attack_type_bp.get("/<id>")
def get_by_id_attack_type(id):
    """
    Obtém um tipo de ataque pelo ID (int) ou public_id (hash)
    ---
    tags:
      - Attack Types
    parameters:
      - in: path
        name: id
        required: true
        type: string
        example: 1 ou hash
    responses:
      200:
        description: Tipo de ataque encontrado
      404:
        description: Não encontrado
    """
    # Tenta buscar por id inteiro
    result = None
    try:
        int_id = int(id)
        result = service.get_by_id(int_id)
    except ValueError:
        # Não é inteiro, tenta buscar por public_id
        all_items = service.list()
        for item in all_items:
            # Suporta tanto 'Id' quanto 'id'
            real_id = item.get('Id') or item.get('id')
            if real_id and generate_public_id(real_id) == id:
                result = item
                break

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(_format_response(result)), 200


@attack_type_bp.put("/<int:id>")
def update_attack_type(id):
    """
    Atualiza um tipo de ataque pelo ID
    ---
    tags:
      - Attack Types
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
            - type
          properties:
            type:
              type: string
              example: Malware
    responses:
      200:
        description: Tipo de ataque atualizado
      400:
        description: Dados inválidos
      404:
        description: Não encontrado
    """
    data = request.json or {}
    attack_type_name = data.get("type")

    if not attack_type_name or not isinstance(attack_type_name, str):
        return jsonify({"error": "Invalid type"}), 400

    result = service.update(id, attack_type_name)

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(_format_response(result)), 200



@attack_type_bp.delete("/<id>")
def delete_attack_type(id):
    """
    Apaga um tipo de ataque pelo ID (int) ou public_id (hash)
    ---
    tags:
      - Attack Types
    parameters:
      - in: path
        name: id
        required: true
        type: string
        example: 1 ou hash
    responses:
      204:
        description: Apagado com sucesso
      404:
        description: Não encontrado
      409:
        description: Não pode ser apagado (FK)
    """
    real_id = None
    try:
        real_id = int(id)
    except ValueError:
        all_items = service.list()
        for item in all_items:
            item_id = item.get('Id') or item.get('id')
            if item_id and generate_public_id(item_id) == id:
                real_id = item_id
                break
    if real_id is None:
        return jsonify({"error": "Not found"}), 404
    result = service.delete(real_id)
    if result is False:
        return jsonify({"error": "Not found"}), 404
    if result == "FK":
        return jsonify({"error": "It cannot be deleted"}), 409
    return "", 204

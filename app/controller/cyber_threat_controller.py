


#novo código
from flask import Blueprint, request, jsonify
from app.service.cyber_threat_service import CyberThreatService
from app.repository.cyber_threat_repository import CyberThreatRepository
from app.database import db
from app.utils import generate_public_id

cyber_threat_bp = Blueprint("cyber_threats", __name__, url_prefix="/cyber_threats")
service = CyberThreatService(CyberThreatRepository(db))


def _format_response(data):
  """Transforma Id em public_id na resposta e remove Id dos objetos aninhados"""
  def clean_nested(obj):
    if isinstance(obj, dict):
      obj = dict(obj)
      # Remove Id de objetos aninhados
      if 'Id' in obj:
        del obj['Id']
      elif 'id' in obj:
        del obj['id']
      # Recursivo para outros níveis
      for k, v in obj.items():
        obj[k] = clean_nested(v)
      return obj
    elif isinstance(obj, list):
      return [clean_nested(i) for i in obj]
    return obj

  if data is None:
    return data

  # Se for uma lista, processa cada item
  if isinstance(data, list):
    result = []
    for item in data:
      if isinstance(item, dict):
        item_copy = dict(item)
        # public_id só no principal
        if 'Id' in item_copy:
          item_copy['public_id'] = generate_public_id(item_copy['Id'])
          del item_copy['Id']
        elif 'id' in item_copy:
          item_copy['public_id'] = generate_public_id(item_copy['id'])
          del item_copy['id']
        # Limpa objetos aninhados
        for k, v in item_copy.items():
          item_copy[k] = clean_nested(v)
        result.append(item_copy)
      else:
        result.append(item)
    return result

  # Se for um dicionário, processa o item
  if isinstance(data, dict):
    data_copy = dict(data)
    if 'Id' in data_copy:
      data_copy['public_id'] = generate_public_id(data_copy['Id'])
      del data_copy['Id']
    elif 'id' in data_copy:
      data_copy['public_id'] = generate_public_id(data_copy['id'])
      del data_copy['id']
    for k, v in data_copy.items():
      data_copy[k] = clean_nested(v)
    return data_copy

  return data


@cyber_threat_bp.post("/")
def create_cyber_threat():
    """
    Cria um novo incidente (cyber threat)
    ---
    tags:
      - Cyber Threats
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - country
            - year
            - attack_type
            - target_industry
            - financial_loss
            - affected_users
            - attack_source
            - security_vulnerability
            - defense_mechanism
            - resolution_time
          properties:
            country:
              type: string
              example: Portugal
            year:
              type: integer
              example: 2023
            attack_type:
              type: integer
              example: 4
            target_industry:
              type: integer
              example: 6
            financial_loss:
              type: number
              example: 12.5
            affected_users:
              type: integer
              example: 5000
            attack_source:
              type: integer
              example: 2
            security_vulnerability:
              type: integer
              example: 1
            defense_mechanism:
              type: integer
              example: 2
            resolution_time:
              type: integer
              example: 48
    responses:
      201:
        description: Incidente criado
      400:
        description: Dados inválidos
    """
    data = request.json or {}

    country = data.get("country")
    year = data.get("year")
    attack_type = data.get("attack_type")
    target_industry = data.get("target_industry")
    financial_loss = data.get("financial_loss")
    affected_users = data.get("affected_users")
    attack_source = data.get("attack_source")
    security_vulnerability = data.get("security_vulnerability")
    defense_mechanism = data.get("defense_mechanism")
    resolution_time = data.get("resolution_time")

    # Validações simples (Camada 1)
    if not country or not isinstance(country, str):
        return jsonify({"error": "Invalid country"}), 400
    if year is None or not isinstance(year, int):
        return jsonify({"error": "Invalid year"}), 400
    if attack_type is None or not isinstance(attack_type, int):
        return jsonify({"error": "Invalid attack_type"}), 400
    if target_industry is None or not isinstance(target_industry, int):
        return jsonify({"error": "Invalid target_industry"}), 400
    if financial_loss is None or not isinstance(financial_loss, (int, float)):
        return jsonify({"error": "Invalid financial_loss"}), 400
    if affected_users is None or not isinstance(affected_users, int):
        return jsonify({"error": "Invalid affected_users"}), 400
    if attack_source is None or not isinstance(attack_source, int):
        return jsonify({"error": "Invalid attack_source"}), 400
    if security_vulnerability is None or not isinstance(security_vulnerability, int):
        return jsonify({"error": "Invalid security_vulnerability"}), 400
    if defense_mechanism is None or not isinstance(defense_mechanism, int):
        return jsonify({"error": "Invalid defense_mechanism"}), 400
    if resolution_time is None or not isinstance(resolution_time, int):
        return jsonify({"error": "Invalid resolution_time"}), 400

    result = service.create(
        country, year, attack_type, target_industry, financial_loss,
        affected_users, attack_source, security_vulnerability,
        defense_mechanism, resolution_time
    )

    if result is None:
        return jsonify({"error": "Invalid parameters"}), 400

    return jsonify(_format_response(result)), 201


@cyber_threat_bp.get("/")
def list_cyber_threats():
    """
    Lista todos os incidentes (cyber threats)
    ---
    tags:
      - Cyber Threats
    responses:
      200:
        description: Lista de incidentes
    """
    return jsonify(_format_response(service.list())), 200



@cyber_threat_bp.get("/<id>")
def get_by_id_cyber_threat(id):
    """
    Obtém um incidente pelo ID (int) ou public_id (hash)
    ---
    tags:
      - Cyber Threats
    parameters:
      - in: path
        name: id
        required: true
        type: string
        example: 1 ou hash
    responses:
      200:
        description: Incidente encontrado
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


@cyber_threat_bp.put("/<int:id>")
def update_cyber_threat(id):
    """
    Atualiza um incidente pelo ID
    ---
    tags:
      - Cyber Threats
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
          properties:
            country:
              type: string
            year:
              type: integer
            attack_type:
              type: integer
            target_industry:
              type: integer
            financial_loss:
              type: number
            affected_users:
              type: integer
            attack_source:
              type: integer
            security_vulnerability:
              type: integer
            defense_mechanism:
              type: integer
            resolution_time:
              type: integer
    responses:
      200:
        description: Incidente atualizado
      404:
        description: Não encontrado
    """
    data = request.json or {}

    result = service.update(
        id=id,
        country=data.get("country"),
        year=data.get("year"),
        attack_type=data.get("attack_type"),
        target_industry=data.get("target_industry"),
        financial_loss=data.get("financial_loss"),
        affected_users=data.get("affected_users"),
        attack_source=data.get("attack_source"),
        security_vulnerability=data.get("security_vulnerability"),
        defense_mechanism=data.get("defense_mechanism"),
        resolution_time=data.get("resolution_time"),
    )

    if result is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(_format_response(result)), 200


@cyber_threat_bp.delete("/<int:id>")
def delete_cyber_threat(id):
    """
    Apaga um incidente pelo ID
    ---
    tags:
      - Cyber Threats
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
    """
    result = service.delete(id)

    if result is False:
        return jsonify({"error": "Not found"}), 404

    return "", 204


# ==========================================================
# ENDPOINTS DE ESTATÍSTICA (consultar dados estatísticos)
# ==========================================================


@cyber_threat_bp.get("/attack_types")
def attack_type_percentage():
    """
    Estatística: percentagem de incidentes por tipo de ataque
    ---
    tags:
      - Cyber Threats Stats
    responses:
      200:
        description: Percentagens por attack_type
    """
    stats = service.attack_type_percentage()
    for item in stats:
        if 'Id' in item:
            item['public_id'] = generate_public_id(item['Id'])
            del item['Id']
        elif 'id' in item:
            item['public_id'] = generate_public_id(item['id'])
            del item['id']
    return jsonify(stats), 200



@cyber_threat_bp.get("/defense_mechanism")
def defense_mechanism_percentage():
    """
    Estatística: percentagem de incidentes por mecanismo de defesa
    ---
    tags:
      - Cyber Threats Stats
    responses:
      200:
        description: Percentagens por defense_mechanism
    """
    stats = service.defense_mechanism_percentage()
    for item in stats:
        if 'Id' in item:
            item['public_id'] = generate_public_id(item['Id'])
            del item['Id']
        elif 'id' in item:
            item['public_id'] = generate_public_id(item['id'])
            del item['id']
    return jsonify(stats), 200



@cyber_threat_bp.get("/security_vulnerability")
def security_vulnerability_percentage():
    """
    Estatística: percentagem de incidentes por vulnerabilidade
    ---
    tags:
      - Cyber Threats Stats
    responses:
      200:
        description: Percentagens por security_vulnerability
    """
    stats = service.security_vulnerability_percentage()
    for item in stats:
        if 'Id' in item:
            item['public_id'] = generate_public_id(item['Id'])
            del item['Id']
        elif 'id' in item:
            item['public_id'] = generate_public_id(item['id'])
            del item['id']
    return jsonify(stats), 200



@cyber_threat_bp.get("/target_industry")
def target_industry_percentage():
    """
    Estatística: percentagem de incidentes por indústria alvo
    ---
    tags:
      - Cyber Threats Stats
    responses:
      200:
        description: Percentagens por target_industry
    """
    stats = service.target_industry_percentage()
    for item in stats:
        if 'Id' in item:
            item['public_id'] = generate_public_id(item['Id'])
            del item['Id']
        elif 'id' in item:
            item['public_id'] = generate_public_id(item['id'])
            del item['id']
    return jsonify(stats), 200

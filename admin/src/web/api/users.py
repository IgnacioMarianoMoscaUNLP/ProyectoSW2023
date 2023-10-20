from flask import Blueprint, jsonify, request
from web.helpers.apivalidations import requires_auth
from src.core.configuration import get_rows_per_page
from src.core import service_requests
from src.core.service_requests import get_request_detaile, get_state_by_id
api_user_bp = Blueprint("user_api", __name__, url_prefix="/api/me/")

@api_user_bp.get('/profile')
@requires_auth()
def get_user_profile(user):
    profile = {
        "name": user.name,
        "email": user.email,
        "id": user.id,
        "lastname": user.lastname,
        "username": user.username,
    }
    return jsonify(profile), 200

@api_user_bp.get('/requests/<int:service_request_id>')
@requires_auth()
def get_user_requests(user, service_request_id):
    if not service_request_id:
        return jsonify({"error": "Falta el id de la solicitud"}), 400
    service_request = get_request_detaile(service_request_id)
    if service_request is None:
        return jsonify({"error": "id de solicitud invalido"}), 400
    state = get_state_by_id(service_request.state_id)

    service_request_parsed = {
        "id": service_request.id,
        "name": service_request.name,
        "service_id": service_request.service_id,
        "observations": service_request.observations,
        "inserted_at": service_request.inserted_at,
        "state_name": state.name,
        "state_message": state.state_message,
    }
    
    return jsonify(service_request_parsed), 200


@api_user_bp.get('/requests')
@requires_auth()
def get_requests_paginated(user):
    params = request.args.to_dict()
    page = 1
    per_page = None
    try:
        if 'page' in params :
            page = int(params['page'])
        if 'per_page' in params:
            per_page = int(params['per_page'])
    except ValueError:
        return jsonify(error='Parametros Invalidos'), 400
    
    if not per_page:
        per_page = get_rows_per_page()

    paginated_requests = service_requests.list_requests_paged_by_user(page=page, per_page=per_page, user_id=user.id)
    total_count = len(service_requests.list_all_requests_by_user(user_id=user.id))
    final_list = []

    for req in paginated_requests:
        request_data = {
            "name": req.ServiceRequest.name,
            "creation_date": req.ServiceRequest.inserted_at,
            "close_date": req.ServiceRequest.closed_at,
            "status": req.service_state_alias.name,
            "observations": req.ServiceRequest.observations
        }
        final_list.append(request_data)


    response = {
        'data': final_list,
        'page': page,
        'per_page': per_page,
        'total': total_count
    }
    return jsonify(response), 200

@api_user_bp.post('/requests/<int:service_request_id>/notes')
@requires_auth()
def add_note_to_request(user, service_request_id):
    text = request.json["text"]
    if not text:
        return jsonify(error='Parametros Invalidos'), 400
    text_added = service_requests.create_message_request(service_request_id=service_request_id, user_id=user.id, msg_content=text)
    if text_added:
        return jsonify(), 200
    else:
        return jsonify(error='ID no encontrada'), 404
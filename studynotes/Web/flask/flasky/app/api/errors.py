from flask import Blueprint,jsonify
from . import api

# errorhandler
@api.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response

@api.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'server error'})
    response.status_code = 500
    return response


@api.app_errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

@api.app_errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response

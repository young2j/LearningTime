from flask import Blueprint
from flask import render_template,request,jsonify

errors = Blueprint('errors', __name__)


# errorhandler
@errors.app_errorhandler(404)
def page_not_found(e):
    # print('request.accept_mimetypes:',request.accept_mimetypes)
    if request.accept_mimetypes.accept_json and not \
       request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and not \
       request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'server error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500

@errors.app_errorhandler(403)
def forbidden(message):
    if request.accept_mimetypes.accept_json and not \
       request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden','message':message})
        response.status_code = 403
        return response
    return render_template('500.html'),403 #以500代替

@errors.app_errorhandler(401)
def unauthorized(message):
    if request.accept_mimetypes.accept_json and not \
       request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'unauthorized','message':message})
        response.status_code = 401
        return response
    return render_template('500.html'),401 #以500代替

 
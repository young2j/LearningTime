from flask import render_template, current_app
from flask_mail import Message

from app import mail


# def send_asnyc_email(current_app,msg):
#     with current_app.app_context():
#         mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg = Message(subject=current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[to])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    # thread = Thread(target=send_asnyc_email,args=[current_app,msg])
    # thread.start()
    # return thread
    with current_app.app_context():
        mail.send(msg)

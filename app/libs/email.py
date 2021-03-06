from threading import Thread
from flask import current_app, render_template
from app import mail
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_email(to, subject, template, **kwargs):
    # msg = Message('[]',
    #               sender='409968627@qq.com',
    #               body='Test',
    #               recipients=['409968627@qq.com'])
    msg = Message('[鱼书]'+' '+subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  body='Test',
                  recipients=[to]
                  )
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

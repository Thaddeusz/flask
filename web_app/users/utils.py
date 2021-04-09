import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from web_app import mail
from flask import current_app



def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # generates random name for pictures
    _, f_ext = os.path.splitext(form_picture.filename) # split filename and extension
    picture_fn = random_hex + f_ext # combine random and extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # creates a variable to store the pictures
    output_size = (125, 125) # sets avatar size, pixel
    i = Image.open(form_picture) # create object for Pillow to decrease size
    i.thumbnail(output_size) # creates new picture in Pillow
    i.save(picture_path) # saves picture to profile_pics
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset Request", sender="noreply@demo.com", recipients=[user.email])
    msg.body = f"To reset the password, click here: {url_for('users.reset_token', token=token, _external=True)}" # external means the link to be converted to URI
    mail.send(msg)

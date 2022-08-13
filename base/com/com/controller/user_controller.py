import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template, redirect, request, flash, url_for
from werkzeug.utils import secure_filename
from base import app
from base.com.controller.login_controller import admin_login_session
from base.com.dao.area_dao import AreaDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO

DATASET_FOLDER2 = 'base/static/adminResources/user_image/'
app.config['DATASET_FOLDER2'] = DATASET_FOLDER2


@app.route("/admin/view_user")
def admin_view_user():
    if admin_login_session() == 'admin':
        user_dao = UserDAO()
        user_vo_list = user_dao.view_user()
        print(user_vo_list)
        return render_template("admin/viewUser.html",user_vo_list = user_vo_list)
    else:
        return redirect(url_for('admin_logout_session'))

@app.route("/user/load_user")
def user_load_user():
    try:
        area_dao = AreaDAO()
        area_vo_list = area_dao.view_area()
        return render_template("user/addUser.html", area_vo_list=area_vo_list)
    except Exception as ex:
        print("in user_load_user route exception occured>>>>>>>>>>", ex)


@app.route("/user/insert_user", methods=["POST"])
def user_insert_user():
    try:
        login_dao = LoginDAO()
        login_vo = LoginVO()
        user_dao = UserDAO()
        user_vo = UserVO()

        login_username = request.form.get("loginUsername")
        user_firstname = request.form.get("userFirstname")
        user_lastname = request.form.get("userLastname")
        user_gender = request.form.get("userGender")
        user_contact = request.form.get("userContact")
        user_address = request.form.get("userAddress")
        user_area_id = request.form.get("userAreaId")

        user_image = request.files.get("userImage")
        user_image_filename = secure_filename(user_image.filename)
        user_image_filepath = os.path.join(app.config["DATASET_FOLDER2"])
        user_vo.user_image_filepath=user_image_filepath.replace("base", "..")+user_firstname+user_lastname+user_image_filename
        user_image.save(os.path.join(user_image_filepath, user_firstname+user_lastname+user_image_filename))
        print(user_vo.user_image_filepath)

        login_password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
        login_secretkey = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(32))
        print("in admin_insert_user login_secretkey>>>>>>>", login_secretkey)
        login_vo_list = login_dao.view_login()
        print("in admin_insert_user login_vo_list>>>>>>", login_vo_list)
        if len(login_vo_list) != 0:
            for i in login_vo_list:
                if i.login_secretkey == login_secretkey:
                    login_secretkey = ''.join(
                        (random.choice(string.ascii_letters + string.digits)) for x in range(32))
                if i.login_username == login_username:
                    error_message = "The username is already exists !"
                    flash(error_message)
                    return redirect("/user/load_user")

        sender = "healthcarechatbot2811@gmail.com"
        receiver = login_username
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "PYTHON PASSWORD"
        msg.attach(MIMEText(login_password, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, "HealthCareChatBot2811")
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()

        login_vo.login_username = login_username
        login_vo.login_password = login_password
        login_vo.login_role = "user"
        login_vo.login_status = "active"
        login_vo.login_secretkey = login_secretkey
        login_dao.insert_login(login_vo)

        user_vo.user_firstname = user_firstname
        user_vo.user_lastname = user_lastname
        user_vo.user_gender = user_gender
        user_vo.user_address = user_address
        user_vo.user_contact = user_contact
        user_vo.user_login_id = login_vo.login_id
        user_vo.user_area_id = user_area_id
        user_dao.insert_user(user_vo)
        return redirect('/')

    except Exception as ex:
        print("in user_insert_user route exception occured>>>>>>>>>>", ex)


@app.route("/user/account_details",methods=['GET'])
def user_account_details():
    if admin_login_session() == 'user':
        user_vo=UserVO()
        login_vo=LoginVO()
        login_dao=LoginDAO()
        user_dao=UserDAO()
        login_vo.login_username=request.args.get("loginUsername")
        login_vo.login_id=login_dao.find_login_id(login_vo)
        user_vo_list=user_dao.user_account_details(login_vo)
        print(user_vo_list)
        return render_template("user/accountDetails.html",user_vo_list=user_vo_list)
    else:
        return redirect(url_for('admin_logout_session'))

@app.route("/user/edit_details",methods=['POST'])
def user_edit_details():
    if admin_login_session() == 'user':
        user_vo=UserVO()
        user_dao=UserDAO()
        user_vo.user_id=request.form.get("userId")
        user_vo.user_firstname=request.form.get("firstName")
        user_vo.user_lastname=request.form.get("lastName")
        user_vo.user_address=request.form.get("address")
        user_vo.user_contact=request.form.get("contactNumber")
        user_vo.user_gender=request.form.get("userGender")
        user_dao.update_details(user_vo)
        return redirect("/user/load_dashboard")
    else:
        return redirect(url_for('admin_logout_session'))
import datetime
import random
import smtplib
import time
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template, redirect, request, url_for, make_response, session, flash, jsonify
from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO

global_loginvo_list = []
global_login_secretkey_set = {0}
otp_session_timeout_flag = False
sec = 60


@app.route('/', methods=['GET'])
def admin_load_login():
    try:
        return render_template('admin/login.html')
    except Exception as ex:
        print("admin_load_login route exception occured>>>>>>>>>>", ex)


@app.route("/admin/validate_login", methods=['POST'])
def admin_validate_login():
    try:
        global global_loginvo_list
        global global_login_secretkey_set

        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = request.form.get('loginUsername')
        login_vo.login_password = request.form.get('loginPassword')

        login_vo_list = login_dao.validate_login(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        print("in admin_validate_login login_list>>>>>>>>>>>", login_list)

        len_login_list = len(login_list)

        if len_login_list == 0:
            error_message = 'username or password is incorrect !'
            flash(error_message)
            return redirect(url_for('admin_load_login'))
        elif login_list[0]['login_status'] == 'inactive':
            error_message = 'You have been temporarily blocked by website admin !'
            flash(error_message)
            return redirect(url_for('admin_load_login'))
        else:
            for row1 in login_list:
                login_id = row1['login_id']
                login_username = row1['login_username']
                login_role = row1['login_role']
                login_secretkey = row1['login_secretkey']
                login_vo_dict = {
                    login_secretkey: {'login_username': login_username, 'login_role': login_role, 'login_id': login_id}}
                if len(global_loginvo_list) != 0:
                    for i in global_loginvo_list:
                        tempList = list(i.keys())
                        global_login_secretkey_set.add(tempList[0])
                    login_secretkey_list = list(global_login_secretkey_set)
                    if login_secretkey not in login_secretkey_list:
                        global_loginvo_list.append(login_vo_dict)
                else:
                    global_loginvo_list.append(login_vo_dict)
                if login_role == 'admin':
                    response = make_response(redirect(url_for('admin_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')
                    print("in admin_validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in admin_validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response
                elif login_role == 'user':
                    response = make_response(redirect(url_for('user_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')
                    print("in admin_validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in admin_validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response
                else:
                    return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_validate_login route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_dashboard', methods=['GET'])
def admin_load_dashboard():
    try:
        if admin_login_session() == 'admin':
            return render_template('admin/index.html')
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/user/load_dashboard', methods=['GET'])
def user_load_dashboard():
    try:
        if admin_login_session() == 'user':
            login_dao = LoginDAO()
            login_vo = LoginVO()
            login_vo.login_secretkey = request.cookies.get('login_secretkey')
            login_id = login_dao.find_login_id_secret(login_vo)
            user_dao = UserDAO()
            user_vo = UserVO()
            user_vo.user_login_id=login_id
            user_vo_list = user_dao.search_user(user_vo)
            session['profile_picture'] = user_vo_list[0].user_image_filepath
            session["name"]=user_vo_list[0].user_firstname+" "+user_vo_list[0].user_lastname
            return render_template('user/index.html')
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/admin/login_session', methods=["POST"])
def admin_login_session():
    try:
        session['datetime'] = str(datetime.datetime.now())
        global global_loginvo_list
        login_role_flag = ""

        login_secretkey = request.cookies.get('login_secretkey')
        print("in admin_login_session login_secretkey>>>>>>>>>", login_secretkey)

        if login_secretkey is None:
            admin_logout_session()
            return redirect('/')
        for i in global_loginvo_list:
            if login_secretkey in i.keys():
                if i[login_secretkey]['login_role'] == 'admin':
                    login_role_flag = "admin"
                elif i[login_secretkey]['login_role'] == 'user':
                    login_role_flag = "user"
        if login_role_flag != "":
            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")
        return login_role_flag

    except Exception as ex:
        print("admin_login_session route exception occured>>>>>>>>>>", ex)

@app.route("/admin/logout_session", methods=['GET'])
def admin_logout_session():
    try:
        global global_loginvo_list
        login_secretkey = request.cookies.get('login_secretkey')
        login_username = request.cookies.get('login_username')
        print("in admin_logout_session login_secretkey>>>>>>>>>", login_secretkey)
        print("in admin_logout_session login_username>>>>>>>>>", login_username)
        print("in admin_logout_session type of login_secretkey>>>>>>>>>", type(login_secretkey))
        print("in admin_logout_session type of login_username>>>>>>>>>", type(login_username))

        response = make_response(redirect('/'))
        if login_secretkey is not None and login_username is not None:
            response.set_cookie('login_secretkey', "", max_age=0)
            response.set_cookie('login_username', "", max_age=0)
            for i in global_loginvo_list:
                if login_secretkey in i.keys():
                    global_loginvo_list.remove(i)
                    print("in admin_logout_session global_loginvo_list>>>>>>>>>>>>>>>", global_loginvo_list)
                    session.clear()
                    break
        return response
    except Exception as ex:
        print("in admin_logout_session route exception occured>>>>>>>>>>", ex)

@app.route("/admin/block_user", methods=['GET'])
def admin_block_user():
    try:
        if admin_login_session() == 'admin':
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_id = request.args.get('loginId')
            login_vo.login_id = login_id
            login_vo.login_status = 'inactive'
            login_dao.update_login(login_vo)
            return redirect(url_for('admin_view_user'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_block_user route exception occured>>>>>>>>>>", ex)


@app.route("/admin/unblock_user", methods=['GET'])
def admin_unblock_user():
    try:
        if admin_login_session() == 'admin':

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_id = request.args.get('loginId')
            login_vo.login_id = login_id
            login_vo.login_status = 'active'
            login_dao.update_login(login_vo)
            return redirect(url_for('admin_view_user'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_unblock_user route exception occured>>>>>>>>>>", ex)

@app.route('/admin/load_update_password', methods=['GET'])
def admin_load_update_password():
    try:
        if admin_login_session() == "user":
            login_secretkey = request.cookies.get('login_secretkey')
            print("in admin_load_update_password login_secretkey>>>>>>>>>", login_secretkey)
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_secretkey = login_secretkey
            login_vo_list = login_dao.find_login_id_secret(login_vo)
            return render_template('user/updatePassword.html', login_vo_list=login_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_update_password route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_update_password', methods=['POST'])
def admin_insert_update_password():
    try:
        if admin_login_session() == "user":
            login_id = request.form.get('loginId')
            login_old_password = request.form.get("loginOldPassword")
            login_new_password = request.form.get("loginNewPassword")
            login_confirm_password = request.form.get("loginConfirmPassword")

            print("login_old_password>>>>>>>>>>", login_old_password)
            print("login_new_password>>>>>>>>>", login_new_password)
            print("login_confirm_password>>>>>>>>>", login_confirm_password)

            login_dao = LoginDAO()
            login_vo_one = LoginVO()

            login_vo_one.login_password = login_old_password
            login_vo_list = login_dao.login_validate_password(login_vo_one)
            login_list = [i.as_dict() for i in login_vo_list]
            print("in admin_insert_update_password login_list>>>>>>>>>>>", login_list)
            len_login_list = len(login_list)
            if len_login_list == 0:
                error_message = 'old password is incorrect !'
                flash(error_message)
                return redirect(url_for('admin_load_update_password'))
            else:
                if login_new_password == login_confirm_password:
                    login_vo_two = LoginVO()
                    login_vo_two.login_password = login_confirm_password
                    login_vo_two.login_id = login_id
                    login_dao.update_login(login_vo_two)
                    return admin_load_login()
                else:
                    error_message = 'new password and confirm password not matched !'
                    flash(error_message)
                    return redirect(url_for('admin_load_update_password'))
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_insert_update_password route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_forget_password', methods=['GET'])
def admin_load_forget_password():
    try:
        return render_template('admin/forgetPassword.html')
    except Exception as ex:
        print("admin_load_forget_password route exception occured>>>>>>>>>>", ex)


def generate_otp():
    global now
    now = time.time()
    otp = random.randint(1000, 9999)
    session['session_otp_number'] = otp

    sender = "healthcarechatbot2811@gmail.com"
    receiver = session['login_username']
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "OTP From Health Care Chat Bot"
    body = "Your OTP for Forget Password is {}\n\t Please Validate Within 60 Seconds.".format(otp)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "HealthCareChatBot2811")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


@app.route('/admin/validate_login_username', methods=['post'])
def admin_validate_login_username():
    try:
        login_username = request.form.get("loginUsername")

        login_dao = LoginDAO()
        login_vo = LoginVO()

        login_vo.login_username = login_username
        login_vo_list = login_dao.login_validate_username(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        print("in admin_validate_login_username login_list>>>>>>>>>>>", login_list)
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username is incorrect !'
            flash(error_message)
            return redirect(url_for('admin_load_forget_password'))
        else:
            session['login_id'] = login_vo_list[0].login_id
            session['login_username'] = login_vo_list[0].login_username
            generate_otp()
            return render_template("admin/otpPassword.html",var=sec)
    except Exception as ex:
        print("admin_validate_login_username route exception occured>>>>>>>>>>", ex)


# @app.route('/admin/validate_otp_number', methods=['POST'])
# def admin_validate_otp_number():
#     try:
#         later = time.time()
#         if int(later - now) < 60:
#             user_otp = int(request.form.get('otpNumber'))
#             session_otp = session['session_otp_number']
#             if user_otp == session_otp:
#                 return render_template("admin/resetPassword.html")
#             else:
#                 session.pop('session_otp_number')
#                 error_message = ' Invalid OTP ! Click On Resend OTP'
#                 flash(error_message)
#                 return redirect("/admin/load_otp_password")
#         else:
#             error_message = 'Session Time out! Click on Resend OTP'
#             flash(error_message)
#             return redirect("/admin/load_otp_password")
#     except Exception as ex:
#         print("admin_validate_otp_number route exception occured>>>>>>>>>>", ex)

@app.route('/admin/validate_otp_number', methods=['POST'])
def admin_validate_otp_number():
    global otp_session_timeout_flag
    global sec
    try:
        later = time.time()
        if otp_session_timeout_flag is False:
            if int(later - now) < 60:
                user_otp = int(request.form.get('otpNumber'))
                session_otp = session['session_otp_number']
                if user_otp == session_otp:
                    return render_template("admin/resetPassword.html")
                else:
                    print("seconds:",sec)
                    sec = request.form.get('seconds')
                    error_message = ' Invalid OTP ! Click On Resend OTP'
                    flash(error_message)
                    return render_template("admin/otpPassword.html", var=sec)
            else:
                otp_session_timeout_flag = True
                session.pop('session_otp_number')
                error_message = 'Session Time out! Click on Resend OTP'
                flash(error_message)
                return redirect("/admin/load_otp_password")
        else:
            error_message = 'Please Click on Resend OTP'
            flash(error_message)
            return redirect("/admin/load_otp_password")
    except Exception as ex:
        print("admin_validate_otp_number route exception occured>>>>>>>>>>", ex)

@app.route('/admin/load_otp_password')
def admin_load_otp_password():
    try:
        return render_template('admin/otpPassword.html',var=sec)
    except Exception as ex:
        print("in admin_resend_otp route exception occured>>>>>>>>>>", ex)


# @app.route('/admin/resend_otp')
# def admin_resend_otp():
#     try:
#         generate_otp()
#         return render_template('admin/otpPassword.html')
#     except Exception as ex:
#         print("in admin_resend_otp route exception occured>>>>>>>>>>", ex)

@app.route('/admin/resend_otp')
def admin_resend_otp():
    global otp_session_timeout_flag
    global sec
    try:
        generate_otp()
        sec = 60
        otp_session_timeout_flag = False
        return render_template('admin/otpPassword.html', var=sec)
    except Exception as ex:
        print("in admin_resend_otp route exception occured>>>>>>>>>>", ex)

@app.route('/admin/update_reset_password', methods=['POST'])
def admin_update_reset_password():
    try:
        new_password = request.form.get('newPassword')
        print("new_password>>>>>>>>>>>>>>", new_password)
        confirm_password = request.form.get('confirmPassword')
        print("confirm_password>>>>>>>>>>>", confirm_password)
        login_id = session['login_id']
        if new_password == confirm_password:
            login_vo = LoginVO()
            login_dao = LoginDAO()
            login_vo.login_password = confirm_password
            login_vo.login_id = login_id
            login_dao.update_password(login_vo)
            return redirect('/')
        else:
            error_message = 'Both Passwords Are Not Matched Please Enter Again !'
            flash(error_message)
            return redirect(url_for('admin_load_reset_password'))
    except Exception as ex:
        print("in admin_update_reset_password route exception occured>>>>>>>>>>", ex)

#ajex method
@app.route("/checkoldpassword",methods=['GET'])
def admin():
    username=request.args.get("loginId")
    password=request.args.get("oldPassword")
    print(username,password)
    return jsonify("passwors wrong")

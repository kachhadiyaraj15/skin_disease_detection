import datetime
from flask import render_template, redirect, request
from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.complain_dao import ComplainDAO
from base.com.dao.login_dao import LoginDAO
from base.com.vo.complain_vo import ComplainVO
from base.com.vo.login_vo import LoginVO

@app.route("/admin/view_complain")
def admin_view_complain():
    try:
        if admin_login_session() == 'admin':
            complain_dao = ComplainDAO()
            complain_vo_list = complain_dao.admin_view_complain()
            return render_template("admin/viewComplain.html", complain_vo_list=complain_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_view_complain route exception occured>>>>>>>>>>", ex)


@app.route("/admin/load_complain_reply")  # give the reply of complain
def admin_load_complain_reply():
    try:
        if admin_login_session() == 'admin':
            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            complain_id = request.args.get("complainId")
            complain_vo.complain_id = complain_id
            complain_vo_list = complain_dao.insert_complain_reply(complain_vo)  # fetch the complain data
            print("complain_vo_list>>>>>", complain_vo_list)
            return render_template("admin/replyComplain.html", complain_vo_list=complain_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_reply_complain route exception occured>>>>>>>>>>", ex)


@app.route("/admin/insert_complain_reply", methods=['POST'])
def admin_insert_complain_reply():
    try:
        if admin_login_session() == 'admin':
            complain_id = request.form.get("complainId")  # id from reply page for data update
            complain_reply_description = request.form.get("complainReplyDescription")  # data from reply page

            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            complain_reply_date = datetime.datetime.now()
            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            complain_vo.complain_id = complain_id
            complain_vo.complain_to_login_id = login_id
            complain_vo.complain_reply_datetime = complain_reply_date
            complain_vo.complain_reply_description = complain_reply_description
            complain_vo.complain_status = "Replied"
            complain_dao.update_complain(complain_vo)
            return redirect("/admin/view_complain")
        else:
            return admin_logout_session()

    except Exception as ex:
        print("in admin_update_complain route exception occured>>>>>>>>>>", ex)


@app.route("/admin/delete_complain")
def admin_delete_complain():
    try:
        if admin_login_session() == 'admin':
            complain_vo = ComplainVO()
            complain_dao = ComplainDAO()
            complain_vo.complain_id = request.args.get("complainId")
            complain_dao.delete_complain(complain_vo)
            return redirect("/admin/view_complain")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in admin_delete_complain route exception occured>>>>>>>>>>", ex)


@app.route("/user/view_complain")
def user_view_complain():
    global admin_login_username
    try:
        if admin_login_session() == 'user':
            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            user_login_id = login_dao.find_login_id(login_vo)
            complain_vo.complain_from_login_id = user_login_id
            complain_vo_updated_list = []
            complain_vo_list = complain_dao.user_view_complain()
            print("complain_vo_list=", complain_vo_list)
            if len(complain_vo_list) != 0:
                for index in range(len(complain_vo_list)):
                    if user_login_id == complain_vo_list[index][1].complain_from_login_id:
                        complain_vo_updated_list.append(complain_vo_list[index])
                if len(complain_vo_updated_list) == 0:
                    return render_template("user/addComplain.html", complain_vo_updated_list=None)
                else:
                    admin_login_username = None
                    for index in range(len(complain_vo_updated_list)):
                        if complain_vo_updated_list[index][1].complain_to_login_id is not None:
                            admin_login_id = complain_vo_updated_list[index][1].complain_to_login_id
                            admin_login_vo = LoginVO()
                            admin_login_vo.login_id = admin_login_id
                            admin_login_username = login_dao.find_login_username(admin_login_vo)
                    return render_template("user/addComplain.html", complain_vo_updated_list=complain_vo_updated_list,
                                           admin_login_username=admin_login_username)
            else:
                return render_template("user/addComplain.html", complain_vo_updated_list=None)
        else:
            return admin_logout_session()

    except Exception as ex:
        print("in user_view_complain route exception occured>>>>>>>>>>", ex)


@app.route("/user/insert_complain", methods=['POST'])
def user_insert_complain():
    try:
        if admin_login_session() == 'user':
            complain_subject = request.form.get("userComplainType")
            complain_description = request.form.get("userComplainDescription")

            complain_dao = ComplainDAO()
            complain_vo = ComplainVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            complain_date = datetime.datetime.now()
            complain_status = "Pending"
            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            complain_vo.complain_subject = complain_subject
            complain_vo.complain_description = complain_description
            complain_vo.complain_datetime = complain_date
            complain_vo.complain_status = complain_status
            complain_vo.complain_from_login_id = login_id
            complain_dao.insert_complain(complain_vo)
            return redirect("/user/view_complain")
        else:
            return admin_logout_session()

    except Exception as ex:
        print("in user_insert_complain route exception occured>>>>>>>>>>", ex)

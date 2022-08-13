import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, redirect, url_for, render_template, session

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.appointment_dao import AppointmentDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.specialist_dao import SpecialistDAO
from base.com.vo.appointment_vo import AppointmentVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.specialist_vo import SpecialistVO
from base.com.dao.classification_dao import ClassificationDAO
from base.com.vo.classification_vo import ClassificationVO

global_loginvo_list = []
otp_session_timeout_flag = False


@app.route("/admin/view_appointment")
def admin_view_appointment():
    try:
        if admin_login_session() == 'admin':
            appointment_dao = AppointmentDAO()
            appointment_vo_list = appointment_dao.admin_view_appointment()
            return render_template("admin/viewAppointment.html", appointment_vo_list=appointment_vo_list)
        else:
            return admin_logout_session()

    except Exception as ex:
        print("admin_view_appointment route exception occured>>>>>>", ex)


def generate_user_appointment(login_username, specialist_vo_list, appointment_date, appointment_time):
    global now
    now = time.time()

    sender = "healthcarechatbot2811@gmail.com"
    receiver = str(login_username)
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Appointment confirmation From Health Care Chat Bot"
    body = "Your appoinment detail \n Specialist Name: {} \n Specialist Contact No.:{} \n Specialist Mail ID:{} \n Appointment Date: {}\n Appointment Time:{}".format(
        specialist_vo_list[0][0].specialist_name, specialist_vo_list[0][0].specialist_contact,
        specialist_vo_list[0][0].specialist_email, appointment_date, appointment_time)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "HealthCareChatBot2811")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


def generate_specialist_appointment(login_username, specialist_vo_list, appointment_date, appointment_time):
    global now
    now = time.time()

    sender = "healthcarechatbot2811@gmail.com"
    receiver = str(specialist_vo_list[0][0].specialist_email)
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Patient Appointment detail From Health Care Chat Bot"
    body = "Patient appoinment detail \n Patient Mail ID:{} \n Appointment Date: {}\n Appointment Time:{}".format(
        login_username, appointment_date, appointment_time)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "HealthCareChatBot2811")
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


@app.route("/user/insert_appointment", methods=["POST"])
def user_insert_appointment():
    try:
        if admin_login_session() == 'user':
            login_vo = LoginVO()
            login_dao = LoginDAO()
            appointment_vo = AppointmentVO()
            appointment_dao = AppointmentDAO()
            specialist_vo = SpecialistVO()
            specialist_dao = SpecialistDAO()
            classification_vo = ClassificationVO()
            classification_dao = ClassificationDAO()

            appointment_date = request.form.get("appointmentDate")
            appointment_time = request.form.get("appointmentTime")
            if appointment_time == '0':
                appointment_slot = "9:00 AM to 11:00 AM"
            elif appointment_time == '1':
                appointment_slot = "1:00 PM to 3:00 PM"
            elif appointment_time == '2':
                appointment_slot = "4:00 PM to 7:00 PM"
            else:
                appointment_slot = "8:00 PM to 10:00 PM"
            specialist_id = request.form.get("specialistId")
            classification_id = request.form.get("classificationId")
            session['classification_id'] = classification_id
            login_secretkey = request.cookies.get('login_secretkey')
            login_username = request.cookies.get('login_username')
            login_vo.login_secretkey = login_secretkey
            login_id = login_dao.find_login_id_secret(login_vo)

            specialist_vo.specialist_id = specialist_id
            specialist_vo_list = specialist_dao.user_appointment_specialist(specialist_vo)
            generate_user_appointment(login_username, specialist_vo_list, appointment_date, appointment_slot)
            generate_specialist_appointment(login_username, specialist_vo_list, appointment_date, appointment_slot)
            appointment_vo.appointment_date = appointment_date
            appointment_vo.appointment_time = appointment_time
            appointment_vo.appointment_specialist_id = specialist_id
            appointment_vo.appointment_classification_id = classification_id
            appointment_vo.appointment_user_id = login_id

            appointment_dao.insert_appoinment(appointment_vo)

            return redirect(url_for("user_view_appointment"))
        else:
            return admin_logout_session()

    except Exception as ex:
        print("user_insert_appointment route exception occured>>>>>>", ex)


@app.route("/user/view_appointment")
def user_view_appointment():
    try:
        if admin_login_session() == 'user':
            login_vo = LoginVO()
            login_dao = LoginDAO()
            appointment_vo = AppointmentVO()
            appointment_dao = AppointmentDAO()
            login_secretkey = request.cookies.get('login_secretkey')
            login_vo.login_secretkey = login_secretkey
            login_id = login_dao.find_login_id_secret(login_vo)
            appointment_vo.appointment_user_id = login_id
            appointment_vo_list = appointment_dao.user_search_appointment(appointment_vo)
            return render_template("user/viewAppointment.html", appointment_vo_list=appointment_vo_list)

        else:
            return admin_logout_session()

    except Exception as ex:
        print("user_insert_appointment route exception occured>>>>>>", ex)

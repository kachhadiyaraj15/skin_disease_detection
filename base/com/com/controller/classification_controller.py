import datetime
import os

from flask import render_template, redirect, request, url_for, flash
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_login_session
from base.com.controller.predictor import pridictor
from base.com.dao.classification_dao import ClassificationDAO
from base.com.dao.disease_dao import DiseaseDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.specialist_dao import SpecialistDAO
from base.com.vo.classification_vo import ClassificationVO
from base.com.vo.disease_vo import DiseaseVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.specialist_vo import SpecialistVO

DATASET_FOLDER = 'base/static/adminResources/input_image/'
app.config['DATASET_FOLDER'] = DATASET_FOLDER


@app.route("/user/load_image")
def user_load_image():
    try:
        if admin_login_session() == 'user':
            return render_template("user/addImage.html")
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("user_insert_image route exception occured>>>>>>", ex)


@app.route("/user/insert_image", methods=['POST'])
def user_insert_image():
    try:
        if admin_login_session() == 'user':
            login_secretkey = request.cookies.get('login_secretkey')
            login_username = request.cookies.get('login_username')

            classification_vo = ClassificationVO()
            classification_dao = ClassificationDAO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = login_username
            login_vo.login_secretkey = login_secretkey
            login_id = login_dao.find_login_id(login_vo)

            classification_vo.classification_datetime = datetime.datetime.now()
            classification_vo.classification_login_id = login_id
            disease_image = request.files.get("detectDisease")
            classification_vo.classification_input_filename = secure_filename(disease_image.filename)
            dataset_filepath = os.path.join(app.config["DATASET_FOLDER"])
            classification_vo.classification_input_filepath = dataset_filepath.replace("base", "..")
            disease_image.save(os.path.join(dataset_filepath, classification_vo.classification_input_filename))

            disease_vo = DiseaseVO()
            disease_dao = DiseaseDAO()
            disease_vo.disease_name = pridictor(dataset_filepath + classification_vo.classification_input_filename)
            print(disease_vo.disease_name)
            disease_vo_list = disease_dao.get_disease_pridictor(disease_vo)
            print(disease_vo_list)

            classification_vo.classification_detected_disease = disease_vo_list[0].disease_id
            classification_vo.classification_status = 'detected'
            classification_dao.insert_image(classification_vo)
            return redirect(url_for("user_view_image"))
        else:
            return redirect(url_for("admin_logout_session"))
    except Exception as ex:
        print("user_insert_image route exception occured>>>>>>", ex)


@app.route("/user/view_image", methods=['GET'])
def user_view_image():
    try:
        if admin_login_session() == 'user':
            login_secretkey = request.cookies.get('login_secretkey')
            login_username = request.cookies.get('login_username')
            login_vo = LoginVO()
            login_dao = LoginDAO()
            login_vo.login_username = login_username
            login_vo.login_secretkey = login_secretkey
            login_id = login_dao.find_login_id(login_vo)
            classification_dao = ClassificationDAO()
            classification_vo = ClassificationVO()
            classification_vo.classification_login_id = login_id
            classification_vo_list = classification_dao.view_disease_user(classification_vo)
            print(classification_vo_list)
            return render_template("user/viewImage.html", classification_vo_list=classification_vo_list)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("user_view_image route exception occured>>>>>>", ex)


@app.route("/user/delete_image", methods=["GET"])
def user_delete_image():
    try:
        if admin_login_session() == 'user':
            classification_vo = ClassificationVO()
            classification_dao = ClassificationDAO()
            classification_vo.classification_id = request.args.get("classificationId")
            classification_vo_list = classification_dao.delete_image(classification_vo)
            file_path = classification_vo_list.classification_input_filepath.replace("..",
                                                                                     "base") + classification_vo_list.classification_input_filename
            os.remove(file_path)
            return redirect(url_for("user_view_image"))

        elif admin_login_session() == 'admin':
            classification_vo = ClassificationVO()
            classification_dao = ClassificationDAO()
            classification_vo.classification_id = request.args.get("classificationId")
            classification_vo_list = classification_dao.delete_image(classification_vo)
            file_path = classification_vo_list.classification_input_filepath.replace("..",
                                                                                     "base") + classification_vo_list.classification_input_filename
            os.remove(file_path)
            return redirect("/admin/view_image")
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("user_delete_image route exception occured>>>>>>", ex)


@app.route("/user/suggest_details", methods=['GET'])
def user_suggest_details():
    try:
        if admin_login_session() == 'user':
            classification_vo = ClassificationVO()
            classification_dao = ClassificationDAO()
            classification_id = request.args.get("classificationId")
            classification_vo.classification_id = classification_id
            classification_vo_list = classification_dao.suggest_details(classification_vo)
            print(classification_vo_list)
            return render_template("user/suggestDetails.html", classification_vo_list=classification_vo_list,
                                   classification_id=classification_id)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        flash("Internal server error!")
        return render_template("user/error.html")


@app.route('/user/take_appointment', methods=['GET'])
def user_maintenance():
    try:
        if admin_login_session() == 'user':
            specialist_vo = SpecialistVO()
            specialist_dao = SpecialistDAO()
            specialist_id = request.args.get("specialistId")
            classification_id = request.args.get("classificationId")
            print("classification_id>>", classification_id)
            specialist_vo.specialist_id = specialist_id
            specialist_vo_list = specialist_dao.user_appointment_specialist(specialist_vo)
            print("specialist_vo_list>>>", specialist_vo_list)
            return render_template("user/addAppointment.html", specialist_vo_list=specialist_vo_list,classification_id = classification_id)
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("user_maintenance route exception occured>>>>>", ex)

from flask import render_template, redirect, request, flash
from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.area_dao import AreaDAO
from base.com.dao.disease_dao import DiseaseDAO
from base.com.dao.specialist_dao import SpecialistDAO
from base.com.vo.specialist_vo import SpecialistVO


@app.route("/admin/load_specialist")
def admin_load_specialist():
    try:
        if admin_login_session() == 'admin':
            area_dao = AreaDAO()
            area_vo_list = area_dao.view_area()
            disease_dao = DiseaseDAO()
            diease_vo_list = disease_dao.view_disease()
            return render_template("admin/addSpecialist.html", area_vo_list=area_vo_list, diease_vo_list=diease_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_specialist route exception occured>>>>>>", ex)


@app.route("/admin/insert_specialist", methods=["POST"])
def admin_insert_specialist():
    try:
        if admin_login_session() == 'admin':
            specialist_vo = SpecialistVO()
            specialist_dao = SpecialistDAO()
            specialist_vo.specialist_name = request.form.get("specialistName")
            specialist_vo.specialist_qualification = request.form.get("specialistQualification")
            specialist_vo.specialist_contact = request.form.get("specialistContact")
            specialist_vo.specialist_gender = request.form.get("specialistGender")
            specialist_vo.specialist_email = request.form.get("specialistEmail")
            specialist_vo.specialist_address = request.form.get("specialistAddress")
            specialist_vo.specialist_area_id = request.form.get("specialistPincode")
            specialist_vo.specialist_disease_id = request.form.get("specialistDisease")
            specialist_dao.add_specialist(specialist_vo)
            flash("Specialist added successfully")
            return redirect("/admin/view_specialist")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_specialist route exception occured>>>>>>", ex)


@app.route("/admin/view_specialist")
def admin_view_specialist():
    try:
        if admin_login_session() == 'admin':
            specialist_dao = SpecialistDAO()
            specialist_vo_list = specialist_dao.view_specialist()
            return render_template("admin/viewSpecialist.html", specialist_vo_list=specialist_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_specialist route exception occured>>>>>>", ex)


@app.route("/admin/edit_specialist")
def admin_edit_specialist():
    try:
        if admin_login_session() == 'admin':
            specialist_vo = SpecialistVO()
            specialist_dao = SpecialistDAO()
            specialist_vo.specialist_id = request.args.get("specialistId")
            specialist_edit_list = specialist_dao.edit_specialist(specialist_vo)
            area_dao = AreaDAO()
            area_vo_list = area_dao.view_area()
            disease_dao = DiseaseDAO()
            diease_vo_list = disease_dao.view_disease()
            return render_template("admin/editSpecialist.html", specialist_edit_list=specialist_edit_list,
                                   area_vo_list=area_vo_list, diease_vo_list=diease_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_specialist route exception occured>>>>>>", ex)


@app.route("/admin/delete_specialist")
def admin_delete_specialist():
    try:
        if admin_login_session() == 'admin':
            specialist_vo = SpecialistVO()
            specialist_dao = SpecialistDAO()
            specialist_vo.specialist_id = request.args.get("specialistId")
            specialist_dao.delete_specialist(specialist_vo)
            return redirect("/admin/view_specialist")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_specialist route exception occured>>>>>>", ex)


@app.route("/admin/update_specialist", methods=["POST"])
def admin_update_specialist():
    try:
        if admin_login_session() == 'admin':
            specialist_vo = SpecialistVO()
            specialist_dao = SpecialistDAO()
            specialist_vo.specialist_id = request.form.get("specialistId")
            specialist_vo.specialist_name = request.form.get("specialistName")
            specialist_vo.specialist_qualification = request.form.get("specialistQualification")
            specialist_vo.specialist_contact = int(request.form.get("specialistContact"))
            specialist_vo.specialist_gender = request.form.get("specialistGender")
            specialist_vo.specialist_email = request.form.get("specialistEmail")
            specialist_vo.specialist_address = request.form.get("specialistAddress")
            specialist_vo.specialist_area_id = request.form.get("specialistPincode")
            specialist_vo.specialist_disease_id = request.form.get("specialistDisease")
            specialist_dao.update_specialist(specialist_vo)
            return redirect("/admin/view_specialist")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_specialist route exception occured>>>>>>", ex)

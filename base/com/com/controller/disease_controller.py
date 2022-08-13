from flask import render_template, redirect, request, flash
from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.disease_dao import DiseaseDAO
from base.com.vo.disease_vo import DiseaseVO


@app.route("/admin/load_disease")
def admin_load_disease():
    try:
        if admin_login_session() == 'admin':
            return render_template("admin/addDisease.html")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_disease route exception occured>>>>>>", ex)


@app.route("/admin/insert_disease", methods=["POST"])
def admin_add_disease():
    try:
        if admin_login_session() == 'admin':
            disease_vo = DiseaseVO()
            disease_dao = DiseaseDAO()
            disease_vo.disease_name = request.form.get("diseaseName")
            disease_vo.disease_description = request.form.get("diseaseDescription")
            disease_dao.add_disease(disease_vo)
            flash("Disease added successfully")
            return redirect("/admin/view_disease")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_disease route exception occured>>>>>>", ex)


@app.route("/admin/view_disease")
def admin_view_disease():
    try:
        if admin_login_session() == 'admin':
            disease_dao = DiseaseDAO()
            disease_dao_list = disease_dao.view_disease()
            return render_template("admin/viewDisease.html", disease_dao_list=disease_dao_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_disease route exception occured>>>>>>", ex)


@app.route("/admin/delete_disease")
def admin_delete_disease():
    try:
        if admin_login_session() == 'admin':
            disease_vo = DiseaseVO()
            disease_dao = DiseaseDAO()
            disease_vo.disease_id = request.args.get("diseaseId")
            disease_dao.delete_disease(disease_vo)
            return redirect("/admin/view_disease")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_disease route exception occured>>>>>>", ex)


@app.route("/admin/edit_disease")
def admin_edit_disease():
    try:
        if admin_login_session() == 'admin':
            disease_vo = DiseaseVO()
            disease_dao = DiseaseDAO()
            disease_vo.disease_id = request.args.get("diseaseId")
            disease_vo_list = disease_dao.edit_disease(disease_vo)
            return render_template("admin/editDisease.html", disease_vo_list=disease_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_disease route exception occured>>>>>>", ex)


@app.route("/admin/update_disease", methods=["POST"])
def admin_update_disease():
    try:
        if admin_login_session() == 'admin':
            disease_vo = DiseaseVO()
            disease_dao = DiseaseDAO()
            disease_vo.disease_id = request.form.get("diseaseId")
            disease_vo.disease_name = request.form.get("diseaseName")
            disease_vo.disease_description = request.form.get("diseaseDescription")
            disease_dao.update_disease(disease_vo)
            return redirect("/admin/view_disease")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_disease route exception occured>>>>>>", ex)

from flask import render_template, redirect, request, flash
from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.area_dao import AreaDAO
from base.com.vo.area_vo import AreaVO


@app.route("/admin/load_area")
def admin_load_area():
    try:
        if admin_login_session() == 'admin':
            return render_template("admin/addArea.html")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_area route exception occured>>>>>>", ex)


@app.route("/admin/view_area")
def admin_view_area():
    try:
        if admin_login_session() == 'admin':
            area_dao = AreaDAO()
            area_vo_list = area_dao.view_area()
            return render_template("admin/viewArea.html", area_vo_list=area_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_area route exception occured>>>>>>", ex)


@app.route("/admin/insert_area", methods=["POST"])
def admin_add_area():
    try:
        if admin_login_session() == 'admin':
            area_vo = AreaVO()
            area_dao = AreaDAO()
            area_vo.area_name = request.form.get("areaName")
            area_vo.area_pincode = request.form.get("areaPincode")
            area_dao.insert_area(area_vo)
            flash("Area added successfully")
            return redirect('/admin/view_area')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_area route exception occured>>>>>>", ex)


@app.route("/admin/delete_area")
def admin_delete_area():
    try:
        if admin_login_session() == 'admin':
            area_vo = AreaVO()
            area_dao = AreaDAO()
            area_vo.area_id = request.args.get('areaId')
            area_dao.delete_area(area_vo)
            return redirect("/admin/view_area")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_area route exception occured>>>>>>", ex)


@app.route("/admin/edit_area")
def admin_edit_area():
    try:
        if admin_login_session() == 'admin':
            area_vo = AreaVO()
            area_dao = AreaDAO()
            area_vo.area_id = request.args.get("areaId")
            area_vo_edit_list = area_dao.edit_area(area_vo)
            return render_template("admin/editArea.html", area_vo_list=area_vo_edit_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_edit_area route exception occured>>>>>>", ex)


@app.route("/admin/update_area", methods=["POST"])
def admin_update_area():
    try:
        if admin_login_session() == 'admin':
            area_vo = AreaVO()
            area_dao = AreaDAO()
            area_vo.area_id = request.form.get("areaId")
            area_vo.area_name = request.form.get("areaName")
            area_vo.area_pincode = request.form.get("areaPincode")
            area_dao.update_area(area_vo)
            return redirect("/admin/view_area")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_update_area route exception occured>>>>>>", ex)

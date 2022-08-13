import datetime
import os
from flask import render_template, redirect, request
from werkzeug.utils import secure_filename
from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.dataset_dao import DatasetDAO
from base.com.dao.disease_dao import DiseaseDAO
from base.com.vo.dataset_vo import DatasetVO

DATASET_FOLDER = 'base/static/adminResources/dataset/'
app.config['DATASET_FOLDER1'] = DATASET_FOLDER


@app.route("/admin/load_dataset")
def admin_load_dataset():
    try:
        if admin_login_session() == 'admin':
            disease_dao = DiseaseDAO()
            disease_vo_list = disease_dao.view_disease()
            return render_template("admin/addDataset.html", disease_vo_list=disease_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_dataset route exception occured>>>>>>", ex)

@app.route("/admin/add_dataset", methods=['post'])
def admin_add_dataset():
    try:
        if admin_login_session() == 'admin':
            dataset_dao = DatasetDAO()
            dataset_vo = DatasetVO()
            disease_name = request.form.get("diseaseName")
            disease_image = request.files.get("diseaseImage")
            datset_filename = secure_filename(disease_image.filename)
            dataset_filepath = os.path.join(app.config["DATASET_FOLDER1"])
            dataset_vo.dataset_disease_id = disease_name
            dataset_vo.dataset_filename = datset_filename
            dataset_vo.dataset_filepath = dataset_filepath.replace("base", "..")
            dataset_vo.dataset_datetime = datetime.datetime.now()
            disease_image.save(os.path.join(dataset_filepath, datset_filename))
            dataset_dao.insert_dataset(dataset_vo)
            return redirect("/admin/view_dataset")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_add_dataset route exception occured>>>>>>", ex)

@app.route("/admin/view_dataset")
def admin_view_dataset():
    try:
        if admin_login_session() == 'admin':
            datset_dao = DatasetDAO()
            dataset_vo_list = datset_dao.view_dataset()
            return render_template("admin/viewDataset.html", dataset_vo_list=dataset_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_dataset route exception occured>>>>>>", ex)


@app.route("/admin/delete_dataset")
def admin_delete_dataset():
    try:
        if admin_login_session() == 'admin':
            dataset_dao = DatasetDAO()
            dataset_vo = DatasetVO()
            dataset_vo.dataset_id = request.args.get("datasetId")
            dataset_vo_list = dataset_dao.delete_dataset(dataset_vo)
            file_path = dataset_vo_list.dataset_filepath.replace("..", "base") + dataset_vo_list.dataset_filename
            os.remove(file_path)
            return redirect("/admin/view_dataset")
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_delete_dataset route exception occured>>>>>>", ex)

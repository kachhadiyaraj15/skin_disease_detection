from flask import render_template, redirect, url_for, request
from base import app
from base.com.controller.login_controller import admin_login_session
from base.com.dao.classification_dao import ClassificationDAO

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/admin/view_image")
def admin_view_image():
    if admin_login_session() == 'admin':
        classification_dao = ClassificationDAO()
        classification_vo_list = classification_dao.view_disease_admin()
        print(classification_vo_list)
        return render_template("admin/viewImage.html",classification_vo_list=classification_vo_list)
    else:
        return redirect(url_for('admin_logout_session'))


# @app.route("/admin/server_shutdown")
# def Stop():
#     if admin_login_session() == 'admin':
#         func=request.environ.get('werkzeug.server.shutdown')
#         if func is None:
#             raise RuntimeError("not running with werkzeug server")
#         func()
#         return render_template("admin/server.html")
#     else:
#         return redirect(url_for('admin_logout_session'))


@app.route('/aboutus')
def aboutus():
    return render_template('user/aboutus.html')
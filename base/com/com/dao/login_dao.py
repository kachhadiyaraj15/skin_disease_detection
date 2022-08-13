from base import db
from base.com.vo.login_vo import LoginVO


class LoginDAO:
    def insert_login(self, login_vo):
        db.session.add(login_vo)
        db.session.commit()

    def view_login(self):
        login_vo_list = LoginVO.query.all()
        return login_vo_list

    def validate_login(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_username=login_vo.login_username,
                                                login_password=login_vo.login_password)
        return login_vo_list

    def update_login(self, login_vo):
        db.session.merge(login_vo)
        db.session.commit()

    def find_login_id(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_username=login_vo.login_username).all()
        login_id = login_vo_list[0].login_id
        return login_id

    def find_login_username(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_id=login_vo.login_id).all()
        login_username = login_vo_list[0].login_username
        return login_username

    def login_validate_username(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_username=login_vo.login_username).all()
        return login_vo_list

    def update_password(self, login_vo):
        db.session.merge(login_vo)
        db.session.commit()

    def block_user(self, login_vo):
        db.session.merge(login_vo)
        db.session.commit()

    def unblock_user(self, login_vo):
        db.session.merge(login_vo)
        db.session.commit()

    def login_validate_password(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_password=login_vo.login_password).all()
        print("login_vo_list in dao>>>>>>>>>>>>>>>>", login_vo_list)
        return login_vo_list

    def find_login_id_secret(self, login_vo):
        login_vo_list = LoginVO.query.filter_by(login_secretkey=login_vo.login_secretkey).all()
        login_id = login_vo_list[0].login_id
        return login_id





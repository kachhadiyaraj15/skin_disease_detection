from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.login_vo import LoginVO

from base.com.vo.user_vo import UserVO


class UserDAO():
    def insert_user(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()

    def search_user(self, user_vo):
        user_vo_list = UserVO.query.filter_by(user_login_id=user_vo.user_login_id).all()
        return user_vo_list

    def view_user(self):
        user_vo_list=db.session.query(LoginVO, AreaVO, UserVO).filter(
            LoginVO.login_id == UserVO.user_login_id).filter(
            AreaVO.area_id == UserVO.user_area_id).all()
        return user_vo_list

    def user_account_details(self,login_vo):
        user_vo_list = UserVO.query.filter_by(user_login_id=login_vo.login_id).all()
        return user_vo_list

    def update_details(self,user_vo):
        db.session.merge(user_vo)
        db.session.commit()



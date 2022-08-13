from base import db
from base.com.vo.complain_vo import ComplainVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO


class ComplainDAO:
    def insert_complain(self, complain_vo):  # user insert the complain
        db.session.add(complain_vo)
        db.session.commit()

    def user_view_complain(self):
        complain_vo_list = db.session.query(LoginVO, ComplainVO, UserVO) \
            .filter(LoginVO.login_id == ComplainVO.complain_from_login_id, ComplainVO.complain_from_login_id==UserVO.user_login_id) \
            .all()
        return complain_vo_list


    def admin_view_complain(self):
        complain_vo_list = db.session.query(ComplainVO, LoginVO) \
            .join(LoginVO, ComplainVO.complain_from_login_id == LoginVO.login_id) \
            .all()
        return complain_vo_list


    def delete_complain(self, complain_vo):  # admin delete the complain
        complain_vo_delete = ComplainVO.query.get(complain_vo.complain_id)
        db.session.delete(complain_vo_delete)
        db.session.commit()


    def insert_complain_reply(self, complain_vo):  # admin give the reply of complain ,fetch the complain data
        complain_vo_list = ComplainVO.query.get(complain_vo.complain_id)
        return complain_vo_list


    def update_complain(self, complain_vo):  # update data into complain table
        db.session.merge(complain_vo)
        db.session.commit()

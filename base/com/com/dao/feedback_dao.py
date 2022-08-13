from base import db
from base.com.vo.feedback_vo import FeedbackVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO


class FeedbackDAO:
    def insert_feedback(self, feedback_vo):
        db.session.add(feedback_vo)
        db.session.commit()

    def user_view_feedback(self):
        feedback_vo_list = db.session.query(LoginVO, FeedbackVO, UserVO) \
            .filter(LoginVO.login_id == FeedbackVO.feedback_login_id,FeedbackVO.feedback_login_id==UserVO.user_login_id) \
            .all()
        return feedback_vo_list

    def admin_view_feedback(self):
        feedback_vo_list = db.session.query(FeedbackVO, LoginVO) \
            .join(LoginVO, FeedbackVO.feedback_login_id == LoginVO.login_id) \
            .all()
        print("feedback_vo_list>>>>>",feedback_vo_list)
        return feedback_vo_list

    def delete_feedback(self, feedback_vo):
        feedback_vo_delete = FeedbackVO.query.get(feedback_vo.feedback_id)
        db.session.delete(feedback_vo_delete)
        db.session.commit()

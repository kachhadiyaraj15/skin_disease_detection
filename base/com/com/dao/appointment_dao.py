from base import db
from base.com.vo.appointment_vo import AppointmentVO
from base.com.vo.classification_vo import ClassificationVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.specialist_vo import SpecialistVO


class AppointmentDAO:
    def insert_appoinment(self, appointment_vo):
        db.session.add(appointment_vo)
        db.session.commit()

    def user_search_appointment(self, appointment_vo):
        appointment_vo_list = db.session.query(AppointmentVO, SpecialistVO, LoginVO, ClassificationVO).filter_by(
            appointment_user_id=appointment_vo.appointment_user_id) \
            .filter(AppointmentVO.appointment_user_id == LoginVO.login_id,
                    AppointmentVO.appointment_specialist_id == SpecialistVO.specialist_id,
                    AppointmentVO.appointment_classification_id == ClassificationVO.classification_id).all()
        print("appointment_vo_list>>>>>>>>>>>", appointment_vo_list)
        return appointment_vo_list

    def admin_view_appointment(self):
        appointment_vo_list = db.session.query(AppointmentVO, SpecialistVO, LoginVO, ClassificationVO)\
            .join(LoginVO,AppointmentVO.appointment_user_id == LoginVO.login_id) \
            .join(SpecialistVO, AppointmentVO.appointment_specialist_id == SpecialistVO.specialist_id) \
            .join(ClassificationVO, AppointmentVO.appointment_classification_id == ClassificationVO.classification_id) \
            .all()
        return appointment_vo_list

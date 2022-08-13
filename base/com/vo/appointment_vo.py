from base import db
from base.com.vo.classification_vo import ClassificationVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.specialist_vo import SpecialistVO


class AppointmentVO(db.Model):
    __tablename__ = "appointment_table"
    appointment_id = db.Column("appointment_id", db.Integer, primary_key=True, autoincrement=True)
    appointment_date = db.Column("appointment_date", db.Date, nullable=False)
    appointment_time = db.Column("appointment_time", db.String(20), nullable=False)
    appointment_specialist_id = db.Column("appointment_specialist_id", db.Integer,
                                          db.ForeignKey(SpecialistVO.specialist_id))
    appointment_user_id = db.Column("appointment_user_id", db.Integer, db.ForeignKey(LoginVO.login_id))
    appointment_classification_id = db.Column("appointment_classification_id", db.Integer,
                                              db.ForeignKey(ClassificationVO.classification_id))

    def as_dict(self):
        return {
            "appointment_id": self.appointment_id,
            "appointment_date": self.appointment_date,
            "appointment_time": self.appointment_time,
            "appointment_specialist_id": self.appointment_specialist_id,
            "appointment_user_id": self.appointment_user_id,
            "appointment_classification_id": self.appointment_classification_id
        }


db.create_all()

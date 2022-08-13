from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.disease_vo import DiseaseVO


class SpecialistVO(db.Model):
    __tablename__ = 'specialist_table'
    specialist_id = db.Column("specialist_id", db.Integer, primary_key=True, autoincrement=True)
    specialist_name = db.Column("specialist_name", db.String(255), nullable=False)
    specialist_qualification = db.Column("specialist_qualification", db.String(255), nullable=False)
    specialist_contact = db.Column("specialist_contact", db.Numeric, nullable=False)
    specialist_gender = db.Column('specialist_gender', db.String(6), nullable=False)
    specialist_email = db.Column("specialist_email", db.String(255), nullable=False)
    specialist_address = db.Column("specialist_address", db.String(255), nullable=False)
    specialist_area_id = db.Column('specialist_area_id', db.Integer, db.ForeignKey(AreaVO.area_id))
    specialist_disease_id = db.Column('specialist_disease_id', db.Integer, db.ForeignKey(DiseaseVO.disease_id))

    def as_dict(self):
        return {
            "specialist_id": self.specialist_id,
            "specialist_name": self.specialist_name,
            "specialist_qualification": self.specialist_qualification,
            "specialist_contact": self.specialist_contact,
            "specialist_gender": self.specialist_gender,
            "specialist_email": self.specialist_email,
            "specialist_address": self.specialist_address,
            "specialist_area_id": self.specialist_area_id,
            "specialist_disease_id": self.specialist_disease_id
        }


db.create_all()

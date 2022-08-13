from base import db
from base.com.vo.disease_vo import DiseaseVO
from base.com.vo.login_vo import LoginVO


class ClassificationVO(db.Model):
    __tablename__ = "classification_table"
    classification_id = db.Column("classification_id", db.Integer, primary_key=True, autoincrement=True)
    classification_datetime = db.Column("classification_datetime",db.DateTime,nullable=False)
    classification_input_filename = db.Column("classification_input_filename",db.String(255),nullable=False)
    classification_input_filepath = db.Column("classification_input_filepath",db.String(255),nullable=False)
    classification_status = db.Column("classification_status",db.String(10),nullable=False)
    classification_login_id = db.Column('classification_login_id', db.Integer, db.ForeignKey(LoginVO.login_id))
    classification_detected_disease = db.Column("classification_detected_disease", db.Integer, db.ForeignKey(DiseaseVO.disease_id))

    def as_dict(self):
        return {
            "classification_id":self.classification_id,
            "classification_datetime":self.classification_datetime,
            "classification_input_filename":self.classification_input_filename,
            "classification_input_filepath":self.classification_input_filepath,
            "classification_status":self.classification_status,
            "classification_detected_disease":self.classification_detected_disease,
            "classification_login_id":self.classification_login_id
            }

db.create_all()

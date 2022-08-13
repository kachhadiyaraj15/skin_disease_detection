from base import db
from base.com.vo.disease_vo import DiseaseVO


class DatasetVO(db.Model):
    __tablename__ = "dataset_table"
    dataset_id = db.Column('dataset_id', db.Integer, primary_key=True, autoincrement=True)
    dataset_disease_id = db.Column("dataset_disease_id", db.Integer, db.ForeignKey(DiseaseVO.disease_id))
    dataset_filename = db.Column("disease_filename", db.String(255), nullable=False)
    dataset_filepath = db.Column("disease_filepath", db.String(255), nullable=False)
    dataset_datetime = db.Column("dataset_datetime", db.DATETIME)

    def as_dict(self):
        return {
            "dataset_id": self.dataset_id,
            "dataset_disease_id": self.dataset_disease_id,
            "dataset_filename": self.dataset_filename,
            "dataset_filepath": self.dataset_filepath
        }


db.create_all()

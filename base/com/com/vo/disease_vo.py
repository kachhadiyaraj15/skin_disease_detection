from base import db


class DiseaseVO(db.Model):
    __tablename__ = "disease_table"
    disease_id = db.Column("disease_id", db.Integer, primary_key=True, autoincrement=True)
    disease_name = db.Column("disease_name", db.String(255), nullable=False)
    disease_description = db.Column("disease_description", db.String(2000), nullable=False)

    def as_dict(self):
        return {
            "disease_id": self.disease_id,
            "disease_name": self.disease_name,
            "disease_description": self.disease_description
        }


db.create_all()

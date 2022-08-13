from base import db
from base.com.vo.disease_vo import DiseaseVO


class DiseaseDAO():
    def add_disease(self, disease_vo):
        db.session.add(disease_vo)
        db.session.commit()

    def view_disease(self):
        disease_dao_list = DiseaseVO.query.all()
        return disease_dao_list

    def delete_disease(self, disease_vo):
        disease_vo_list = DiseaseVO.query.get(disease_vo.disease_id)
        db.session.delete(disease_vo_list)
        db.session.commit()

    def edit_disease(self, disease_vo):
        disease_vo_edit = DiseaseVO.query.filter_by(disease_id=disease_vo.disease_id).all()
        return disease_vo_edit

    def update_disease(self, disease_vo):
        db.session.merge(disease_vo)
        db.session.commit()

    def get_disease_pridictor(self,disease_vo):
        disease_vo_list = DiseaseVO.query.filter_by(disease_name=disease_vo.disease_name).all()
        return disease_vo_list
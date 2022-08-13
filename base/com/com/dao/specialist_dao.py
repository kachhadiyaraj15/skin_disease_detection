from base import db
from base.com.vo.area_vo import AreaVO
from base.com.vo.disease_vo import DiseaseVO
from base.com.vo.specialist_vo import SpecialistVO


class SpecialistDAO():
    def add_specialist(self, specialist_vo):
        db.session.add(specialist_vo)
        db.session.commit()

    def view_specialist(self):
        specialist_vo_list = db.session.query(AreaVO, DiseaseVO, SpecialistVO).filter(
            AreaVO.area_id == SpecialistVO.specialist_area_id).filter(
            DiseaseVO.disease_id == SpecialistVO.specialist_disease_id).all()
        return specialist_vo_list

    def delete_specialist(self, specialist_vo):
        specialist_vo_list = SpecialistVO.query.get(specialist_vo.specialist_id)
        db.session.delete(specialist_vo_list)
        db.session.commit()

    def edit_specialist(self, specialist_vo):
        specialist_vo_edit = SpecialistVO.query.filter_by(specialist_id=specialist_vo.specialist_id).all()
        return specialist_vo_edit

    def update_specialist(self, specialist_vo):
        db.session.merge(specialist_vo)
        db.session.commit()

    def user_appointment_specialist(self, specialist_vo):
        specialist_vo_list = db.session.query(SpecialistVO,AreaVO, DiseaseVO).filter_by(
            specialist_id=specialist_vo.specialist_id).filter(
            AreaVO.area_id == SpecialistVO.specialist_area_id).filter(
            DiseaseVO.disease_id == SpecialistVO.specialist_disease_id).all()
        print("specialist_vo_list user_appointment_specialist>>>>>>>",specialist_vo_list)
        return specialist_vo_list

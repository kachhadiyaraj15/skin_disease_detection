from base import db
from base.com.vo.classification_vo import ClassificationVO
from base.com.vo.disease_vo import DiseaseVO
from base.com.vo.login_vo import LoginVO
from base.com.vo.specialist_vo import SpecialistVO
from base.com.vo.user_vo import UserVO


class ClassificationDAO:
    def insert_image(self, classification_vo):
        db.session.add(classification_vo)
        db.session.commit()

    def view_disease_user(self,classification_vo):
        classification_vo_list = ClassificationVO.query.filter_by(classification_login_id=classification_vo.classification_login_id).all()
        return classification_vo_list

    def view_disease_admin(self):
        classification_vo=db.session.query(LoginVO, ClassificationVO,DiseaseVO).filter(
            LoginVO.login_id == ClassificationVO.classification_login_id,ClassificationVO.classification_detected_disease==DiseaseVO.disease_id).all()
        return classification_vo

    def delete_image(self,classification_vo):
        classification_vo_list=ClassificationVO.query.get(classification_vo.classification_id)
        db.session.delete(classification_vo_list)
        db.session.commit()
        return classification_vo_list

    def suggest_details(self,classification_vo):
        temp = ClassificationVO.query.get(classification_vo.classification_id)

        classification_vo_list = db.session.query(ClassificationVO, DiseaseVO, SpecialistVO).filter(
            ClassificationVO.classification_id == temp.classification_id).filter(
            temp.classification_detected_disease == DiseaseVO.disease_id).filter(
            temp.classification_detected_disease == SpecialistVO.specialist_disease_id).all()

        return classification_vo_list
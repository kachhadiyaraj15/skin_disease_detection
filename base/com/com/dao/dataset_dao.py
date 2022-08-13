from base import db
from base.com.vo.dataset_vo import DatasetVO
from base.com.vo.disease_vo import DiseaseVO


class DatasetDAO:
    def insert_dataset(self, dataset_vo):
        db.session.add(dataset_vo)
        db.session.commit()

    def view_dataset(self):
        dataset_vo_list = (db.session.query(DiseaseVO, DatasetVO).filter(
            DatasetVO.dataset_disease_id == DiseaseVO.disease_id).all())
        return dataset_vo_list

    def delete_dataset(self, dataset_vo):
        product_vo_list = DatasetVO.query.get(dataset_vo.dataset_id)
        db.session.delete(product_vo_list)
        db.session.commit()
        return product_vo_list

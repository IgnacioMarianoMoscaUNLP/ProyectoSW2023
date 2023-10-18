from src.core.database import db
from src.core.services.service import Service
from src.core.configuration import get_rows_per_page

def list_service_paged(page):
    per_page = get_rows_per_page()
    return Service.query.paginate(page=page, per_page=per_page, error_out=False)

def get_service(service_id):
    return Service.query.get(service_id)

def create_service(**kwargs):
    service = Service(**kwargs)
    db.session.add(service)
    db.session.commit()
    return service

def delete_service(service_id):
    service = Service.query.get(service_id)
    db.session.delete(service)
    db.session.commit()
    return service

def update_service(service_id, **kwargs):
    service = Service.query.get(service_id)
    for key, value in kwargs.items():
        setattr(service, key, value)
    db.session.commit()
    return service

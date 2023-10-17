from src.core.configuration import get_rows_per_page
from src.core.database import db
from src.core.institutions.institution import Institution
from sqlalchemy import or_

def list_institutions():
    """Devuelve una lista de todas las instituciones

    Returns:
        list: lista de instituciones
    """
    return Institution.query.all()

def get_user_institutions(selected_institution=-1):
    """Returns user institutions, if he has a selected institution it should be sorted to appear first on the list

    Args:
        selected_institution (int, optional): If other value than -1 then there is a selected institution. Defaults to -1.

    Returns:
        list(Institution): Return a list of institutions
    """
    _institutions = Institution.query.all() ## hay que ser que sean las del usuario TO DO
    if selected_institution != -1:
        _institutions.sort(key=lambda institution: (institution.id != selected_institution, institution.id))
    return _institutions

def list_institutions_paged(page):
    """Devuelve una lista de instituciones paginada y ordenada por id ascendentemente
   
     Args:
        page (int): numero de pagina
    
    Returns:
        list: lista de instituciones
    """
    per_page = get_rows_per_page()
    query = Institution.query.order_by(Institution.id.asc())
    return query.paginate(page=page, per_page=per_page, error_out=False)

def create_institution(**kwargs):
    """Crea una institucion

    Returns:
        Institution: institucion creada
    """
    try:
        institution = Institution(**kwargs)
        db.session.add(institution)
        db.session.commit()
        return institution
    except Exception as e:
        print(e)
        return None

def institution_exists(name):
    """Comprueba si existe una institucion con el nombre pasado por parametro

    Args:
        name (str): nombre de la institucion
    Returns:
        bool: True si existe, False en caso contrario
    """
    return Institution.query.filter_by(name=name).first() is not None

def get_institution_by_id(id):
    return Institution.query.filter_by(id=id).first()

def update_institution(id, **kwargs):
    """Actualiza una institucion

    Args:
        id (int): id de la institucion
        **kwargs: parametros a actualizar

    Returns:
        Institution: institucion actualizada
    """
    try:
        institution = get_institution_by_id(id)
        if institution is None:
            return None
        for key, value in kwargs.items():
            setattr(institution, key, value)
        db.session.commit()
        return institution
    except Exception as e:
        print(e)
        return None

def delete_institution(id):
    """Elimina una institucion

    Args:
        id (int): id de la institucion

    Returns:
        Institution: institucion eliminada
    """
    try:
        institution = get_institution_by_id(id)
        if institution is None:
            return None
        db.session.delete(institution)
        db.session.commit()
        return institution
    except Exception as e:
        print(e)
        return None
from src.core.database import db
from src.core.institutions import Institution
from src.core.model.model import User,Rol,RolUsuario,RolPermiso,Permiso
from sqlalchemy.orm import joinedload


def create_rol(**kwargs):
    rol = Rol(**kwargs)
    db.session.add(rol)
    db.session.commit()
    return rol

def create_permission(**kwargs):
    permission = Permiso(**kwargs)
    db.session.add(permission)
    db.session.commit()
    return permission

def create_rol_permission(**kwargs):
    kwargs["role_id"] = get_role_id_by_name(kwargs["role_id"])
    kwargs["permission_id"] = get_permission_id_by_name(kwargs["permission_id"])
    permission_role = RolPermiso(**kwargs)
    db.session.add(permission_role)
    db.session.commit()
    return permission_role
    
        
def create_rol_usuario(**kwargs):
    """
    Aca supone que se elige el rol por nombre
    entonces se obtiene el id del rol, para que quede en la tabla rol de usuario 
    """
    kwargs["role_id"] = get_role_id_by_name(kwargs["role_id"])
    user_role = RolUsuario(**kwargs)
    db.session.add(user_role)
    db.session.commit()
    return user_role

def get_rol_usuario(institution_id, user_id, role_id):
    role_id = get_role_id_by_name(role_id)
    user_role = (
        db.session.query(RolUsuario)
        .filter(RolUsuario.user_id == user_id)
        .filter(RolUsuario.institution_id == institution_id)
        .filter(RolUsuario.role_id == role_id)
        .all()
    )
    return user_role

def delete_permission(permission_id):
    permission = Permiso.query.get(permission_id)
    if permission:
        db.session.delete(permission)
        db.session.commit()
        return True
    return False

def delete_rol_permission(role_id, permission_id):
    role_permission = RolPermiso.query.filter_by(role_id=role_id, permission_id=permission_id).first()
    if role_permission:
        db.session.delete(role_permission)
        db.session.commit()
        return True
    return False

def delete_rol_usuario(user_id,institution_id, role_id):
    user_role = RolUsuario.query.filter_by(user_id=user_id, institution_id=institution_id, role_id=role_id).first()
    print("user role")
    print(user_role)
    if user_role:
        db.session.delete(user_role)
        db.session.commit()
        return True
    return False




##Esto para identificar los roles por nombre y no por id
def get_role_id_by_name(role_name):
    print(role_name)
    rol = Rol.query.filter_by(name=role_name).first()
    return rol.id 

###retorna name id del permiso segun name
def get_permission_id_by_name(permission_name):
    permission = Permiso.query.filter_by(name=permission_name).first()
    return permission.id

def is_superadmin(user_id):
    role = (
        db.session.query(Permiso.name)
        .join(RolUsuario, RolUsuario.role_id == 3)
        .filter(RolUsuario.user_id == user_id)
        .all()
    )
    if role:
        return True
    else:
        return False
    
def is_institution_owner(user_id, institution_id):
    owner = (
        db.session.query(Permiso.name)
        .join(RolUsuario, RolUsuario.role_id == 1)
        .filter(RolUsuario.user_id == user_id)
        .filter(RolUsuario.institution_id == institution_id)
        .all()
    )
    if owner:
        return True
    else:
        return False
    
def list_institutions_owned_by_user(user_id):
    """Retorna las instituciones donde el user es dueño

    Args:
        user_id (int): user id

    Returns:
        list(Institutions)
    """
    print(user_id)
    institutions = (
        db.session.query(Institution)
        .join(RolUsuario, RolUsuario.role_id == 1)
        .filter(RolUsuario.user_id == user_id)
        .filter(Institution.id == RolUsuario.institution_id)
        .all()
    )
    print(institutions)
    return institutions

def list_permissions_by_user_id(user_id):
    """
        Listar los permisos en general de un usuario
        Puede ser usada como base para hacer peticion de permisos segun el modulo
    """
    permissions = (
        db.session.query(Permiso.name)
        .join(RolPermiso, RolPermiso.permission_id == Permiso.id)
        .join(RolUsuario, RolUsuario.role_id == RolPermiso.role_id)
        .filter(RolUsuario.user_id == user_id)
        .all()
    )

    # Extraer los nombres de los permisos de la consulta
    permission_names = [permission.name for permission in permissions]
    return permission_names

def list_Permissions_By_User_Id_In_Institution(user_id,institution_id):
    """
        Obtener los permisos de un usuario en una institucion especifica
    """
    permissions = (
        db.session.query(Permiso.name)
        .join(RolPermiso, RolPermiso.permission_id == Permiso.id)
        .join(RolUsuario, RolUsuario.role_id == RolPermiso.role_id)
        .filter(RolUsuario.user_id == user_id)
        .filter(RolUsuario.institution_id == institution_id)
        .all()
    )

    # Extraer los nombres de los permisos de la consulta
    permission_names = [permission.name for permission in permissions]

    return permission_names


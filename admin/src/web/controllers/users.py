from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.web.helpers.auth import login_required
from src.core import auth
user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.get('/')
#@login_required
def home():
    """"Muestra un listado de los usuarios si el usuario esta logeado"""
    page = request.args.get('page', type=int, default=1)
    only_blocked = request.args.get('blocked',default=None)
    if only_blocked == "False":
        only_blocked = False
    elif only_blocked == "True":
        only_blocked = True
    else:
        only_blocked = None
    users = auth.list_users_paged(page,only_blocked)
    return render_template("users/index.html", users=users, page=page, blocked=only_blocked)

@user_bp.route('/update_user_status/<int:user_id>') ## TO DO--> Proteger para superADMIN
def update_user_status(user_id):
    user = auth.change_user_status(user_id=user_id)
    if not user:
        flash("No se puede cambiar el estado de ese usuario", "error")
    return redirect(url_for('user.home'))

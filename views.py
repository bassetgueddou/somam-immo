import os
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import Property, Project, Message
from forms import LoginForm, PropertyForm, ProjectForm

main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)

# --- Public pages ---
@main_bp.route('/')
def index():
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    properties = Property.query.order_by(Property.created_at.desc()).limit(6).all()
    return render_template('index.html', projects=projects, properties=properties)

@main_bp.route('/projets')
def projects():
    q = request.args.get("q", "")
    query = Project.query
    if q:
        like = f"%{q}%"
        query = query.filter((Project.name.ilike(like)) | (Project.description.ilike(like)) | (Project.status.ilike(like)))
    items = query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', items=items, q=q)

@main_bp.route('/immobilier')
def properties_page():
    city = request.args.get("ville", "")
    max_price = request.args.get("prix_max", type=float)
    query = Property.query
    if city:
        query = query.filter(Property.city.ilike(f"%{city}%"))
    if max_price is not None:
        query = query.filter(Property.price <= max_price)
    items = query.order_by(Property.created_at.desc()).all()
    return render_template('properties.html', items=items, city=city, max_price=max_price)

@main_bp.route('/bien/<int:item_id>')
def property_detail(item_id):
    item = Property.query.get_or_404(item_id)
    return render_template('property_detail.html', item=item)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        body = request.form.get('message')
        if not (name and email and subject and body):
            flash('Tous les champs sont obligatoires.', 'danger')
        else:
            msg = Message(name=name, email=email, subject=subject, body=body)
            db.session.add(msg)
            db.session.commit()
            flash('Message envoyé avec succès. Merci !', 'success')
            return redirect(url_for('main.contact'))
    return render_template('contact.html')

@main_bp.route('/a-propos')
def about():
    return render_template('about.html')

# --- Simple admin auth ---
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Veuillez vous connecter en tant qu'admin.", "warning")
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return wrapper

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username == os.environ.get('ADMIN_USERNAME', 'admin') and password == os.environ.get('ADMIN_PASSWORD', 'admin123'):
            session['is_admin'] = True
            flash('Connecté.', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Identifiants invalides.', 'danger')
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('Déconnecté.', 'info')
    return redirect(url_for('main.index'))

@admin_bp.route('/')
@login_required
def dashboard():
    stats = {
        'properties': Property.query.count(),
        'projects': Project.query.count(),
        'messages': Message.query.count(),
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/projets', methods=['GET', 'POST'])
@login_required
def manage_projects():
    form = ProjectForm()
    if form.validate_on_submit():
        p = Project(
            name=form.name.data,
            status=form.status.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            image_url=form.image_url.data or None
        )
        db.session.add(p)
        db.session.commit()
        flash('Projet ajouté.', 'success')
        return redirect(url_for('admin.manage_projects'))
    items = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/manage_projects.html', form=form, items=items)

@admin_bp.route('/projets/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_project(item_id):
    p = Project.query.get_or_404(item_id)
    db.session.delete(p)
    db.session.commit()
    flash('Projet supprimé.', 'info')
    return redirect(url_for('admin.manage_projects'))

@admin_bp.route('/biens', methods=['GET', 'POST'])
@login_required
def manage_properties():
    form = PropertyForm()
    if form.validate_on_submit():
        b = Property(
            title=form.title.data,
            description=form.description.data,
            city=form.city.data,
            price=form.price.data,
            surface=form.surface.data,
            rooms=form.rooms.data,
            image_url=form.image_url.data or None
        )
        db.session.add(b)
        db.session.commit()
        flash('Bien ajouté.', 'success')
        return redirect(url_for('admin.manage_properties'))
    items = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('admin/manage_properties.html', form=form, items=items)

@admin_bp.route('/biens/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_property(item_id):
    b = Property.query.get_or_404(item_id)
    db.session.delete(b)
    db.session.commit()
    flash('Bien supprimé.', 'info')
    return redirect(url_for('admin.manage_properties'))

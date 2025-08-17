from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, DateField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Connexion")

class PropertyForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired(), Length(max=120)])
    description = TextAreaField("Description", validators=[DataRequired()])
    city = StringField("Ville", validators=[DataRequired()])
    price = FloatField("Prix (DA)", validators=[DataRequired(), NumberRange(min=0)])
    surface = FloatField("Surface (m²)", validators=[DataRequired(), NumberRange(min=0)])
    rooms = IntegerField("Pièces", validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField("URL image", validators=[Optional(), Length(max=255)])

class ProjectForm(FlaskForm):
    name = StringField("Nom du projet", validators=[DataRequired(), Length(max=120)])
    status = StringField("Statut", validators=[DataRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[DataRequired()])
    start_date = DateField("Début", validators=[Optional()])
    end_date = DateField("Fin", validators=[Optional()])
    image_url = StringField("URL image", validators=[Optional(), Length(max=255)])

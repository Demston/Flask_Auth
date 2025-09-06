from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class LoginForm(FlaskForm):
    """Форма для авторизации"""
    name = StringField('Логин', [validators.InputRequired()])
    psw = PasswordField('Пароль', [validators.InputRequired()])


class RegForm(FlaskForm):
    """Форма для регистрации"""
    name = StringField('Логин', [validators.InputRequired()])
    psw = PasswordField('Пароль', validators=[
        validators.DataRequired(),
        validators.Length(min=8, message='Пароль должен быть не менее 8 символов'),
        validators.Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)',
               message='Пароль должен содержать цифры и буквы в разных регистрах')
    ])

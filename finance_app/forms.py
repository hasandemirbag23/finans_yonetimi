from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from finance_app.models.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')

class RegistrationForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifreyi Doğrula', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Kayıt Ol')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Bu kullanıcı adı zaten kullanılıyor. Lütfen başka bir kullanıcı adı seçin.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu email adresi zaten kullanılıyor. Lütfen başka bir email adresi seçin.')

class IncomeForm(FlaskForm):
    amount = FloatField('Miktar', validators=[DataRequired()])
    description = TextAreaField('Açıklama')
    category = SelectField('Kategori', choices=[
        ('maaş', 'Maaş'),
        ('yan_gelir', 'Yan Gelir'),
        ('yatırım_geliri', 'Yatırım Geliri'),
        ('hediye', 'Hediye'),
        ('diğer', 'Diğer')
    ], validators=[DataRequired()])
    date = DateField('Tarih', validators=[DataRequired()])
    submit = SubmitField('Gelir Ekle')

class ExpenseForm(FlaskForm):
    amount = FloatField('Miktar', validators=[DataRequired()])
    description = TextAreaField('Açıklama')
    category = SelectField('Kategori', choices=[
        ('yiyecek', 'Yiyecek'),
        ('kira', 'Kira'),
        ('faturalar', 'Faturalar'),
        ('ulaşım', 'Ulaşım'),
        ('eğlence', 'Eğlence'),
        ('sağlık', 'Sağlık'),
        ('alışveriş', 'Alışveriş'),
        ('diğer', 'Diğer')
    ], validators=[DataRequired()])
    date = DateField('Tarih', validators=[DataRequired()])
    submit = SubmitField('Gider Ekle')

class BudgetForm(FlaskForm):
    category = SelectField('Kategori', choices=[
        ('yiyecek', 'Yiyecek'),
        ('kira', 'Kira'),
        ('faturalar', 'Faturalar'),
        ('ulaşım', 'Ulaşım'),
        ('eğlence', 'Eğlence'),
        ('sağlık', 'Sağlık'),
        ('alışveriş', 'Alışveriş'),
        ('diğer', 'Diğer')
    ], validators=[DataRequired()])
    amount = FloatField('Miktar', validators=[DataRequired()])
    month = SelectField('Ay', choices=[
        (1, 'Ocak'), (2, 'Şubat'), (3, 'Mart'), (4, 'Nisan'),
        (5, 'Mayıs'), (6, 'Haziran'), (7, 'Temmuz'), (8, 'Ağustos'),
        (9, 'Eylül'), (10, 'Ekim'), (11, 'Kasım'), (12, 'Aralık')
    ], coerce=int, validators=[DataRequired()])
    year = SelectField('Yıl', choices=[(2023, '2023'), (2024, '2024'), (2025, '2025')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Bütçe Oluştur') 
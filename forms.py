from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired
# the names of the fields may need to change
class AddCompanyForm(Form):
    company_id = IntegerField()
    name = StringField('name', validators=[DataRequired()])
    revenue = IntegerField('revenue')

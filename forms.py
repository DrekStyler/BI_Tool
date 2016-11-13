from flask_wtf import Form
from wtforms import StringField, DataField, IntegerField, SelectField
from wtforms.validators import DataRequired
# the names of the fields may need to change
class AddTaskForm(Form)
    company_id = IntegerField()
    name = StringField('Company Name', validators=[DataRequired()])
    revenue = IntegerField('Revenue')

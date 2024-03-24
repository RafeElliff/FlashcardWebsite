from wtforms import Form, IntegerField, StringField, SubmitField, SelectField
class NewQuizForm(Form):
    Name = StringField('Name')
    Submit = SubmitField('Submit')

class NewTermsForm(Form):
    Side1 = StringField('Side 1 (Term)')
    Side2 = StringField('Side 2 (Definition)')
    Submit = SubmitField('Submit')

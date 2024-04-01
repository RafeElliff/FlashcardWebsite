from wtforms import Form, IntegerField, StringField, SubmitField, SelectField

def store_file_as_list_of_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines



class NewQuizForm(Form):
    Name = StringField('Name')
    Submit = SubmitField('Submit')

class NewTermsForm(Form):
    Side1 = StringField('Side 1 (Term)')
    Side2 = StringField('Side 2 (Definition)')
    Submit = SubmitField('Submit')

list_of_flashcard_sets = store_file_as_list_of_lines("list_of_flashcard_sets.txt")
class ChooseCardSet(Form):
    Choice = SelectField("Flashcard Set", choices=list_of_flashcard_sets)
    Submit = SubmitField('Submit')
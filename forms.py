from wtforms import Form, IntegerField, StringField, SubmitField, SelectField

def store_file_as_list_of_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines



class NewQuizForm(Form):
    Name = StringField('Name')
    Submit = SubmitField('Submit')

class NewTermsForm(Form):
    Term = StringField('Side 1 (Term)')
    Definition = StringField('Side 2 (Definition)')
    Submit = SubmitField('Submit')

list_of_flashcard_sets = store_file_as_list_of_lines("list_of_flashcard_sets.txt")
class ChooseCardSet(Form):
    Choice = SelectField("Flashcard Set", choices=list_of_flashcard_sets)
    Submit = SubmitField('Submit')

class ChooseQuizType(Form):
    Choice = SelectField("Quiz Type", choices=["Type in Answers", "Multiple Choice"])
    Submit = SubmitField('Submit')

class AnswerTypedQuestion(Form):
    Answer = StringField('Answer')
    Submit = SubmitField('Submit')

class ChangeForm(Form):
    Change = SelectField("Change Marking", choices = ["I was right", "I was wrong"])
    Submit = SubmitField('Submit')
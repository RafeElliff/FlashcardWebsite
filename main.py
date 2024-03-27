import json
from flask import Flask, request, render_template, redirect, url_for, flash, session
from forms import NewQuizForm, NewTermsForm


app = Flask(__name__)
app.secret_key = 'your_secret_key'

def save_to_file(item_to_save, filename):
    with open (filename, 'w') as file:
        file.write ("{")
    with open(filename, 'a') as file:
        list_of_lines = store_file_as_list(filename)
        for i in list_of_lines:
            json.dump(i, file)
            file.write('\n')
        file.write('}')


def append_to_list_of_sets(item_to_save, filename):
    with open(filename, 'w') as file:
        json.dump(item_to_save, file)
#
def load_last_line_of_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        last_dict = eval(last_line)
    return last_dict

def get_dictionary(filename):
    with open (filename, 'r') as file:
        file_value = file.read()
        string_of_sets = json.loads(file_value)
        return string_of_sets

def store_file_as_list(filename):
    with open (filename, 'r') as file:
        list_of_lines = file.readlines
        return list_of_lines

@app.route('/')
def initialise():
    return render_template("index.html")
@app.route('/QuizPage')
def QuizPage():
    return render_template("QuizPage.html")


# Code that initialises a new set of flashcards and gives it a name
@app.route('/NewQuiz', methods = ["GET", "POST"])
def NewQuiz():
    form = NewQuizForm(request.form)
    name = None

    if request.method == "POST":
        name = request.form.get("Name")
        dict_of_sets = get_dictionary("flashcard_sets.txt")
        dict_of_sets[name] = {"Number of cards": 0}
        save_to_file(name, "list_of_flashcard_sets.txt")

        save_to_file(dict_of_sets, "flashcard_sets.txt")
        # save_to_file("flashcard_sets.txt")
        return redirect(url_for('NewTerms'))


    return render_template("NewQuiz.html", form=form, Name=name)


# Code that adds new terms to the set of flashcards that was just named
@app.route('/NewTerms', methods = ["GET", "POST"])
def NewTerms():
    form = NewTermsForm(request.form)
    # current_dict = read_file("flashcard_sets.txt")
    # current_dict = current_dict[name]["Number of cards"]
    # side1 = request.form.get("Side1")
    # side2 = request.form.get("Side2")
    # if side1 is not None and side2 is not None:
    #     number_of_cards = number_of_cards + 1
    #     number_of_flashcard = f"Flashcard {number_of_cards}"
    #     flashcard = {"Number of cards": number_of_cards, number_of_flashcard: {"Side1": side1, "Side2": side2}}
    #     current_dict.update(flashcard)
    #     save_to_file(current_dict, "flashcard_sets.txt")
    return render_template("NewTerms.html", form=form)






if __name__ == "__main__":
    app.run(debug=True)







# Code plan
# List of dictionary names, website has menu to choose which set of flashcards you want to do


# Flashcard sets themselves
# Each set is a dictionary, each flashcard is a sub dictionary with 3 attributes - Side1, Side2, learn_score. Each set also has a name
# Automate production: first create a dictionary with a 'name' value. Assign the name input to the name value then allow input of the rest of the values, creating dictionaries with them as it happens

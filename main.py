import json
import random
from flask import Flask, request, render_template, redirect, url_for
from forms import NewQuizForm, NewTermsForm, ChooseCardSet, ChooseQuizType

app = Flask(__name__)


# Appends a given item to a given file on a new line
def save_to_file(item_to_save, filename):
    with open(filename, 'a') as file:
        file.write("\n")
        json.dump(item_to_save, file)


# Stores a file as a list of the lines in it
def store_file_as_list_of_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines


# Clears the contents of a file
def erase_file(filename):
    with open(filename, 'w') as file:
        file.close()


# Keeps all dictionaries that have previously been written to a file, then adds a new given one with proper formatting
def write_dict_to_file(new_set, filename):
    lines = store_file_as_list_of_lines(filename)
    flashcard_sets = lines[1:-1]
    with open(filename, 'w') as file:
        file.write("{")
        file.write("\n")
        for line in flashcard_sets:
            file.write(line)
        file.write(new_set + ",")
        file.write("\n")
        file.write("}")


# Loads a whole file and formats it as a dictionary
def load_whole_file_as_dict(filename):
    with open(filename, 'r') as file:
        file_string = file.read()
        file_dict = eval(file_string)
        return file_dict


# Unused function that loads a file as a dictionary
def load_last_line_of_file_as_dict(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-2].strip()
        last_dict = "{" + last_line + "}"
        last_dict = eval(last_dict)
    return last_dict


# Returns the last (real, ignoring closing brackets etc) line of the file
def load_last_line_of_file_as_str(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-2].strip()
        return last_line


# Replaces the most recent dictionary with a file
def update_dictionary(replacement_item, filename):
    list_of_lines = store_file_as_list_of_lines(filename)
    with open(filename, "w") as file:
        file.write("{")
        file.write("\n")
        lines_without_last_dict = list_of_lines[1:-2]
        for line in lines_without_last_dict:
            file.write(line)
        file.write(replacement_item + ",")
        file.write("\n")
        file.write("}")


# Writes the dictionary chosen in choose_quiz to a file, with each card on a new line
def get_flashcards_from_dict():
    with open("current_flashcard_set.txt", 'r') as file:
        dict_of_card_set = eval(file.read())
        del dict_of_card_set["Number of Cards"]
        str_of_dict = str(dict_of_card_set)
        list_of_cards = str_of_dict.split("}")
        list_of_cards = list_of_cards[:-2]
    with open("list_of_flashcards_in_current_set.txt", "a") as file:
        for card in list_of_cards:
            card = card + "}"
            if card[:2] == ", ":
                card = card[2:]
                card = "{" + card
            file.write(card + "\n")


@app.route('/')
def initialise():
    return render_template("index.html")


@app.route('/choose-quiz', methods=["GET", "POST"])
def choose_quiz():
    form = ChooseCardSet(request.form)
    choice = None

    if request.method == "POST":
        choice = str(request.form.get("Choice"))
        choice = choice.strip()
        whole_dict = load_whole_file_as_dict("flashcard_sets.txt")
        chosen_set = whole_dict[choice]
        save_to_file(chosen_set, "current_flashcard_set.txt")
        get_flashcards_from_dict()
        return redirect(url_for("quiz"))

    return render_template("choose-quiz.html", form=form)


@app.route('/new-quiz', methods=["GET", "POST"])
def new_quiz():
    form = NewQuizForm(request.form)
    name = None

    if request.method == "POST":
        name = request.form.get("Name")
        New_Flashcard_Set = "'" + name + "'" + ":{'Number of Cards': 0}"
        write_dict_to_file(New_Flashcard_Set, "flashcard_sets.txt")
        save_to_file(name, "list_of_flashcard_sets.txt")

        return redirect(url_for('new-terms'))

    return render_template("new-quiz.html", form=form, Name=name)


@app.route('/new-terms', methods=["GET", "POST"])
def new_terms():
    form = NewTermsForm(request.form)
    side1 = request.form.get("Side1")
    side2 = request.form.get("Side2")
    last_line_of_file = load_last_line_of_file_as_str("flashcard_sets.txt")
    list_of_elements = last_line_of_file.split("'")
    name = list_of_elements[1]
    whole_dict = load_whole_file_as_dict("flashcard_sets.txt")
    current_dict = whole_dict[name]
    number_of_cards = current_dict["Number of Cards"]
    if side1 is not None and side2 is not None:
        number_of_cards = number_of_cards + 1
        number_of_flashcard = f"Flashcard {number_of_cards}"
        flashcard = {
            str(number_of_flashcard): {
                'Side1': side1,
                'Side2': side2,
                'Learn Score': 0
            }
        }
        current_dict["Number of Cards"] = number_of_cards
        current_dict.update(flashcard)
        dict_as_str = str(current_dict)
        whole_dict_as_str = "'" + name + "'" + ":" + dict_as_str
        update_dictionary(whole_dict_as_str, "flashcard_sets.txt")
        return redirect(url_for("new-terms"))

    return render_template("new-terms.html", form=form)


@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    form = ChooseQuizType(request.form)
    choice = request.form.get("Choice")
    if choice == "Multiple Choice":
        return redirect(url_for("multiple-choice-quiz"))
    elif choice == "Type in Answers":
        return redirect(url_for("type-in-answers-quiz"))
    return render_template("quiz.html", form=form)


@app.route('/type-in-answers-quiz', methods=["GET", "POST"])
def type_in_answers_quiz():
    list_of_cards = store_file_as_list_of_lines("list_of_flashcards_in_current_set.txt")

    return render_template(("type-in-answers-quiz.html"))


@app.route('/multiple-choice-quiz', methods=["GET", "POST"])
def multiple_choice_quiz():
    return render_template(("multiple-choice-quiz.html"))


def clear_session_variables():
    erase_file("current_flashcard_set.txt")
    erase_file("list_of_flashcards_in_current_set.txt")


if __name__ == "__main__":
    clear_session_variables()
    app.run(debug=True)

# Code plan
# List of dictionary names, website has menu to choose which set of flashcards you want to do


# Flashcard sets themselves
# Each set is a dictionary, each flashcard is a sub dictionary with 3 attributes - Side1, Side2, learn_score. Each set also has a name
# Automate production: first create a dictionary with a 'name' value. Assign the name input to the name value then allow input of the rest of the values, creating dictionaries with them as it happens

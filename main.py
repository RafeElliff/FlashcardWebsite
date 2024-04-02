import json
from flask import Flask, request, render_template, redirect, url_for
from forms import NewQuizForm, NewTermsForm, ChooseCardSet, ChooseQuizType

app = Flask(__name__)


def save_to_file(item_to_save, filename):
    with open(filename, 'a') as file:
        file.write ("\n")
        json.dump(item_to_save, file)

def store_file_as_list_of_lines(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines

def write_dict_to_file(new_set, filename):
    lines = store_file_as_list_of_lines(filename)
    flashcard_sets = lines[1:-1]
    with open (filename, 'w') as file:
        file.write("{")
        file.write("\n")
        for line in flashcard_sets:
            file.write(line)
        file.write(new_set + ",")
        file.write("\n")
        file.write("}")

def load_whole_file_as_dict(filename):
    with open (filename, 'r') as file:
        file_string = file.read()
        file_dict = eval(file_string)
        return file_dict


def load_last_line_of_file_as_dict(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-2].strip()
        last_dict = "{" + last_line + "}"
        last_dict = eval(last_dict)
    return last_dict

def load_last_line_of_file_as_str(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-2].strip()
        return last_line

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

def write_name_of_set_to_file(name, filename):
    with open (filename, "a") as file:
        file.write(name)
        file.write("\n")

@app.route('/')
def initialise():
    return render_template("index.html")
@app.route('/ChooseQuiz', methods = ["GET", "POST"])
def ChooseQuiz():
    form = ChooseCardSet(request.form)
    choice = None

    if request.method == "POST":
        choice = str(request.form.get("Choice"))
        choice = choice.strip()
        whole_dict = load_whole_file_as_dict("flashcard_sets.txt")
        print (choice)
        print (whole_dict)
        chosen_set = whole_dict[choice]
        save_to_file(chosen_set, "current_flashcard_set.txt")
        print (chosen_set)
        return redirect(url_for("Quiz"))

    return render_template("ChooseQuiz.html", form=form)

@app.route('/NewQuiz', methods = ["GET", "POST"])
def NewQuiz():
    form = NewQuizForm(request.form)
    name = None

    if request.method == "POST":
        name = request.form.get("Name")
        New_Flashcard_Set = "'"+ name + "'" + ":{'Number of Cards': 0}"
        write_dict_to_file(New_Flashcard_Set, "flashcard_sets.txt")
        write_name_of_set_to_file(name, "list_of_flashcard_sets.txt")



        return redirect(url_for('NewTerms'))

    return render_template("NewQuiz.html", form=form, Name=name)

@app.route('/NewTerms', methods = ["GET", "POST"])
def NewTerms():
    form = NewTermsForm(request.form)
    side1 = request.form.get("Side1")
    side2 = request.form.get("Side2")
    last_line_of_file = load_last_line_of_file_as_str("flashcard_sets.txt")
    # print(last_line_of_file)
    list_of_elements = last_line_of_file.split("'")
    # print (list_of_elements)
    name = list_of_elements[1]
    # print (name)
    whole_dict = load_whole_file_as_dict("flashcard_sets.txt")
    current_dict = whole_dict[name]
    number_of_cards = current_dict["Number of Cards"]
    print (number_of_cards)
    if side1 is not None and side2 is not None:
        print (side1 + side2)
        number_of_cards = number_of_cards + 1
        number_of_flashcard = f"Flashcard {number_of_cards}"
        print (number_of_flashcard)
        flashcard = {
            str(number_of_flashcard): {
                'Side1': side1,
                'Side2': side2,
                'Learn Score': 0
            }
        }
        print(flashcard)
        current_dict["Number of Cards"] = number_of_cards
        current_dict.update(flashcard)
        dict_as_str = str(current_dict)
        whole_dict_as_str = "'" + name + "'" + ":" + dict_as_str
        update_dictionary(whole_dict_as_str, "flashcard_sets.txt")
        return redirect(url_for("NewTerms"))

    return render_template("NewTerms.html", form=form)

@app.route('/Quiz', methods = ["GET", "POST"])
def Quiz():
    form = ChooseQuizType(request.form)
    choice = request.form.get("Choice")
    if choice == "Multiple Choice":
        return redirect(url_for("MultipleChoiceQuiz"))
    elif choice == "Type In Answers":
        return redirect(url_for("TypeInAnswersQuiz"))
    return render_template("Quiz.html", form=form)

@app.route('/MultipleChoiceQuiz', methods = ["GET", "POST"])
def MultipleChoiceQuiz():
    return render_template(("MultipleChoiceQuiz.html"))

@app.route('/TypeInAnswersQuiz', methods=["GET", "POST"])
def TypeInAnswersQuiz():
    return render_template(("TypeInAnswersQuiz.html"))

if __name__ == "__main__":
    app.run(debug=True)







# Code plan
# List of dictionary names, website has menu to choose which set of flashcards you want to do


# Flashcard sets themselves
# Each set is a dictionary, each flashcard is a sub dictionary with 3 attributes - Side1, Side2, learn_score. Each set also has a name
# Automate production: first create a dictionary with a 'name' value. Assign the name input to the name value then allow input of the rest of the values, creating dictionaries with them as it happens

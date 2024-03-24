import json
from flask import Flask, request, render_template, redirect, url_for
from forms import NewQuizForm, NewTermsForm

app = Flask(__name__)
# def create_dictionary():
#     data = {'name': input("Enter name: ")}
#
#     terms = {}
#     term_counter = 1
#
#     while True:
#         term_key = f'term{term_counter}'
#         answer_key = f'answer{term_counter}'
#
#         term_value = input(f"Enter term for {term_key} (or 'done' to finish): ")
#         if term_value.lower() == 'done':
#             break
#
#         answer_value = input(f"Enter answer for {answer_key}: ")
#
#         terms[term_key] = {'term': term_value, 'answer': answer_value}
#         term_counter += 1
#
#     data.update(terms)
#     return data
#
def save_to_file(item_to_save, filename):
    with open(filename, 'a') as file:
        file.write('\n')
        json.dump(item_to_save, file)
#
def load_last_line_of_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        last_dict = eval(last_line)
    return last_dict
#
# def main():
#     filename = 'flashcard_sets.txt'
#
#     flashcard_sets = load_flashcard_sets(filename)
#
#     while True:
#         user_input = input("Do you want to create a new dictionary? (yes/no): ")
#         if user_input.lower() != 'yes':
#             break
#
#         dictionary = create_dictionary()
#         flashcard_sets.append(dictionary)
#         save_to_file(flashcard_sets, filename)
#         print("Dictionary saved successfully!")
#     for i in flashcard_sets:
#         print(i.get("name"))


@app.route('/')
def initialise():
    return render_template("index.html")
@app.route('/QuizPage')
def QuizPage():
    return render_template("QuizPage.html")

@app.route('/NewQuiz', methods = ["GET", "POST"])
def NewQuiz():
    form = NewQuizForm(request.form)
    name = None

    if request.method == "POST":
        name = request.form.get("Name")
        New_Flashcard_Set = {'name': name, "Number of cards": 0}
        save_to_file(New_Flashcard_Set, "flashcard_sets.txt")
        return redirect(url_for('NewTerms'))

    #     side1 = request.form.get("Side1")
    #     side2 = request.form.get("Side2")
    #     terms = {}
    #     if side1 is not None and side2 is not None:
    #         terms = {"Side 1": side1, "Side 2": side2}
    #         New_Flashcard_Set.update(terms)
    #     print(New_Flashcard_Set)
    return render_template("NewQuiz.html", form=form, Name=name)

@app.route('/NewTerms', methods = ["GET", "POST"])
def NewTerms():
    form = NewTermsForm(request.form)
    current_dict = load_last_line_of_file("flashcard_sets.txt")
    number_of_cards = current_dict["Number of cards"]
    side1 = request.form.get("Side1")
    side2 = request.form.get("Side2")
    if side1 is not None and side2 is not None:
        number_of_cards = number_of_cards + 1
        number_of_flashcard = f"Flashcard {number_of_cards}"
        flashcard = {"Number of cards": number_of_cards, number_of_flashcard: {"Side1": side1, "Side2": side2}}
        current_dict.update(flashcard)
        save_to_file(current_dict, "flashcard_sets.txt")
    return render_template("NewTerms.html", form=form)


# def NewQuiz():
#     form = NewQuizForm(request.form)
#     name = None
#     New_Flashcard_Set = None
#     if request.method == "POST":
#         if name is None:
#             name = request.form["Name"]
#         New_Flashcard_Set = {'name':name}
#     return render_template("NewQuiz.html", form=form, Name=name), New_Flashcard_Set
#
# @app.route('/MakeTerms', methods=["GET", "POST"])
# def MakeTerms():
#
#     form = MakeTermsForm(request.form)
#     side1 = None
#     side2 = None
#     if side1 and side2 != None:
#         side1 = request.form["Side1"]
#         side2 = request.form["Side2"]
#         terms = {"Side 1": side1, "Side2": side2}
#         New_Flashcard_Set.update(terms)
#
#     print(terms)






    # def create_dictionary():
    #     data = {'name': input("Enter name: ")}
    #
    #     terms = {}
    #     term_counter = 1
    #
    #     while True:
    #         term_key = f'term{term_counter}'
    #         answer_key = f'answer{term_counter}'
    #
    #         term_value = input(f"Enter term for {term_key} (or 'done' to finish): ")
    #         if term_value.lower() == 'done':
    #             break
    #
    #         answer_value = input(f"Enter answer for {answer_key}: ")
    #
    #         terms[term_key] = {'term': term_value, 'answer': answer_value}
    #         term_counter += 1
    #
    #     data.update(terms)




if __name__ == "__main__":
    app.run(debug=True)







# Code plan
# List of dictionary names, website has menu to choose which set of flashcards you want to do


# Flashcard sets themselves
# Each set is a dictionary, each flashcard is a sub dictionary with 3 attributes - Side1, Side2, learn_score. Each set also has a name
# Automate production: first create a dictionary with a 'name' value. Assign the name input to the name value then allow input of the rest of the values, creating dictionaries with them as it happens

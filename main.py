import json
import random
from flask import Flask, request, render_template, redirect, url_for
from forms import NewQuizForm, NewTermsForm, ChooseCardSet, ChooseQuizType, AnswerTypedQuestion, ChangeForm
import inspect


app = Flask(__name__)


#prints the line number of the code
def print_line_number():
    caller_frame = inspect.currentframe().f_back
    print(f"This is line {caller_frame.f_lineno}")

# Replaces everything in a file with a given item
def read_file(filename):
        with open (filename, 'r') as file:
            return file.read()
def overwrite_file(item_to_save, filename):
    with open (filename, 'w') as file:
        for item in item_to_save:
            file.write(str(item))
            file.write("\n")
# Appends a given item to a given file on a new line
def save_to_file(item_to_save, filename):
    with open(filename, 'a') as file:
        json.dump(item_to_save, file)
        file.write("\n")

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

# Returns the last (real, ignoring closing brackets etc) line of the file
def load_last_line_of_file_as_str(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        last_line = lines[-2].strip()
        return last_line


# Replaces the most recent dictionary with a different dictionary
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
            file.write(card + "}" + "\n")

@app.route('/')
def index():
    clear_session_variables()
    return render_template("index.html")


@app.route('/choose-quiz', methods=["GET", "POST"])
def choose_quiz():
    form = ChooseCardSet(request.form)
    choice = None

    if request.method == "POST":
        choice = str(request.form.get("Choice"))
        choice = choice.strip()
        choice = choice.strip("\n")
        whole_dict = load_whole_file_as_dict("flashcard_sets.txt")
        chosen_set = whole_dict[choice]
        save_to_file(chosen_set, "current_flashcard_set.txt")
        get_flashcards_from_dict()
        list_of_cards = store_file_as_list_of_lines("list_of_flashcards_in_current_set.txt")
        list_of_card_ids = []
        for item in range(0, len(list_of_cards)):
            list_of_card_ids.append(item)
        random.shuffle(list_of_card_ids)
        save_to_file(list_of_card_ids, "session_variables.txt")
        save_to_file(None, "session_variables.txt")
        save_to_file(None, "session_variables.txt")
        save_to_file(None, "session_variables.txt")
        save_to_file(choice.strip("\n"), "session_variables.txt")
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
        with open("list_of_flashcard_sets.txt", 'a') as file:
            file.write(name)
            file.write("\n")

        return redirect(url_for('new_terms'))

    return render_template("new-quiz.html", form=form, Name=name)


@app.route('/new-terms', methods=["GET", "POST"])
def new_terms():
    form = NewTermsForm(request.form)
    term = request.form.get("Term")
    definition = request.form.get("Definition")
    last_line_of_file = load_last_line_of_file_as_str("flashcard_sets.txt")
    list_of_elements = last_line_of_file.split("'")
    name = list_of_elements[1]
    whole_dict = load_whole_file_as_dict("flashcard_sets.txt")
    current_dict = whole_dict[name]
    number_of_cards = current_dict["Number of Cards"]
    if term is not None and definition is not None:
        number_of_cards = number_of_cards + 1
        number_of_flashcard = f"Flashcard_{number_of_cards}"
        flashcard = {
            str(number_of_flashcard): {
                'Term': term,
                'Definition': definition,
                'Learn Score': 0
            }
        }
        current_dict["Number of Cards"] = number_of_cards
        current_dict.update(flashcard)
        dict_as_str = str(current_dict)
        whole_dict_as_str = "'" + name + "'" + ":" + dict_as_str
        update_dictionary(whole_dict_as_str, "flashcard_sets.txt")
        return redirect(url_for("new_terms"))

    return render_template("new-terms.html", form=form)


@app.route('/quiz', methods=["GET", "POST"])
def quiz():
    form = ChooseQuizType(request.form)
    choice = request.form.get("Choice")
    if choice == "Multiple Choice":
        return redirect(url_for("multiple_choice_quiz"))
    elif choice == "Type in Answers":
        return redirect(url_for("type_in_answers_quiz"))
    return render_template("quiz.html", form=form)


@app.route('/type-in-answers-quiz', methods=["GET", "POST"])
def type_in_answers_quiz():
    answer_form = AnswerTypedQuestion(request.form)
    change_form = ChangeForm(request.form)
    term = None
    message = None
    card_to_change = None

    list_of_valid_ids = []
    list_of_cards = store_file_as_list_of_lines("list_of_flashcards_in_current_set.txt") # stores all the flashcards as items in a list

    list_of_lines = store_file_as_list_of_lines("session_variables.txt")
    list_of_lines = list_of_lines[:5]
    card_to_change_in_change_response = store_file_as_list_of_lines("changed_cards.txt")
    if card_to_change_in_change_response:
        card_to_change_in_change_response = card_to_change_in_change_response[-1]
    print_line_number()
    print(card_to_change_in_change_response)
    if list_of_lines[2].strip("\n") != 'null':
        card_to_change = list_of_lines[2].strip("\n")
    change = change_form.data.get("Change")
    if change == "I was right" and card_to_change_in_change_response:
        print_line_number()
        print(card_to_change_in_change_response)
        card_to_change_in_change_response = str(card_to_change_in_change_response).strip("[")
        card_to_change_in_change_response = card_to_change_in_change_response.strip("]")
        list_of_final_card_to_change = card_to_change_in_change_response.split(":", 1)
        print_line_number()
        print(list_of_final_card_to_change)
        card_to_change = list_of_final_card_to_change[1]
        final_card_to_change_in_change_response = card_to_change.strip()
        # final_card_to_change_in_change_response = final_card_to_change_in_change_response.
        final_card_to_change_in_change_response = final_card_to_change_in_change_response.rstrip('}\\n"')
        final_card_to_change_in_change_response = final_card_to_change_in_change_response + "}"
        print_line_number()
        print(final_card_to_change_in_change_response)
        final_card_to_change_in_change_response = eval(final_card_to_change_in_change_response)
        current_learn_score = int(list_of_lines[3])
        final_card_to_change_in_change_response["Learn Score"] = current_learn_score + 1
        final_card_to_change_in_change_response = list_of_final_card_to_change[0].strip('"') + ":" + str(final_card_to_change_in_change_response) + '}'
        print_line_number()
        print(final_card_to_change_in_change_response)
        with open("changed_cards.txt", 'a') as file:
            file.write(final_card_to_change_in_change_response)
            file.write("\n")

    if list_of_lines[2].strip("\n") != 'null':
        card_to_change = list_of_lines[2].strip("\n")


    list_of_flashcard_ids = eval(list_of_lines[0])
    if list_of_flashcard_ids:
        for num in list_of_flashcard_ids:
            card = list_of_cards[num]
            temp_list = card.split(":", 1)  # Split at the first colon only
            card = ":".join(temp_list[1:])
            final_card = card.strip()
            final_card = eval(final_card[:-1])  # Slice to remove the last character
            current_learn_score = final_card["Learn Score"]
            if current_learn_score < 4:
                list_of_valid_ids.append(num)
        for num in list_of_valid_ids:
            card = list_of_cards[num]
            list_of_lines[2] = card.strip("\n")
            temp_list = card.split(":", 1)  # Split at the first colon only
            card = ":".join(temp_list[1:])
            final_card = card.strip()
            final_card = eval(final_card[:-1])  # Slice to remove the last character
            current_learn_score = final_card["Learn Score"]
            if current_learn_score < 4:
                term = final_card["Term"]
                definition = list_of_lines[1]
                if card_to_change is not None:
                    temp_list_of_card_to_change = card_to_change.split(":", 1)
                    final_card_to_change = temp_list_of_card_to_change[1]
                    final_card_to_change = eval(final_card_to_change[:-1])
                    current_learn_score = final_card_to_change["Learn Score"]
                if definition is not None:
                    definition = definition.strip()
                next_definition = final_card["Definition"]
                if next_definition is not None:
                    next_definition = next_definition.strip()
                answer = answer_form.data.get("Answer")
                if answer is not None:
                    answer = answer.strip()

                if definition == answer:
                    message = "Correct"
                    final_learn_score = current_learn_score + 1
                elif answer is not None:
                    message = f"Wrong, answer is {definition}"
                    if current_learn_score > 0:
                        final_learn_score = current_learn_score - 1
                    else:
                        final_learn_score = current_learn_score
                else:
                    message = None
                    final_learn_score = current_learn_score

                if card_to_change is not None:
                    print_line_number()
                    print(final_card_to_change)
                    final_card_to_change["Learn Score"] = final_learn_score
                    temp_list_of_card_to_change[1] = str(final_card_to_change)
                    card_to_change = ":".join(temp_list_of_card_to_change)
                    card_to_change = card_to_change + "}"
                    with open ("changed_cards.txt", 'a') as file:
                        file.write(card_to_change)
                        file.write("\n")
                list_of_lines[0] = list_of_valid_ids[1:]
                list_of_lines[1] = next_definition
                list_of_lines[3] = current_learn_score

                answer_form.Answer.data = None
                change_form.Change.data = None
                print_line_number()
                print(list_of_lines)
                overwrite_file(list_of_lines, "session_variables.txt")
                return render_template("type-in-answers-quiz.html", answer_form=answer_form, term=term, message=message, change_form = change_form)



    elif not list_of_flashcard_ids and change == None:
        if card_to_change is not None:
            temp_list_of_card_to_change = card_to_change.split(":", 1)
            final_card_to_change = temp_list_of_card_to_change[1]
            final_card_to_change = eval(final_card_to_change[:-1])
            current_learn_score = final_card_to_change["Learn Score"]

        definition = list_of_lines[1]
        if definition is not None:
            definition = definition.strip()
        answer = answer_form.data.get("Answer")
        if answer is not None:
            answer = answer.strip()

        if definition == answer:
            message = "Correct"
            final_learn_score = current_learn_score + 1
        elif answer is not None:
            message = f"Wrong, answer is {definition}"
            if current_learn_score > 0:
                final_learn_score = current_learn_score - 1
            else:
                final_learn_score = current_learn_score
        else:
            message = None


        if card_to_change is not None:
            print_line_number()
            print(final_card_to_change)
            final_card_to_change["Learn Score"] = final_learn_score
            temp_list_of_card_to_change[1] = str(final_card_to_change)
            card_to_change = ":".join(temp_list_of_card_to_change)
            card_to_change = card_to_change + "}"
            print_line_number()
            print(card_to_change)
            with open("changed_cards.txt", 'a') as file:
                file.write(card_to_change)
                file.write("\n")

        answer_form.Answer.data = None
        change_form.Change.data = None
        return render_template("type-in-answers-quiz.html", answer_form=answer_form, term=term, message=message, change_form=change_form)
    elif not list_of_flashcard_ids and change != None:

        return render_template("type-in-answers-quiz.html", answer_form=answer_form, term=term, message=message, change_form = change_form)
    return render_template("type-in-answers-quiz.html", answer_form=answer_form, term=term, message=message, change_form=change_form)

@app.route('/save-progress')
def save_progress():
    card_sets = eval(read_file("flashcard_sets.txt").strip())
    changes = store_file_as_list_of_lines("changed_cards.txt")
    name_of_card_set = store_file_as_list_of_lines("session_variables.txt")[4]
    name_of_card_set = name_of_card_set.strip("\n")
    name_of_card_set = name_of_card_set.strip("'")
    print_line_number()
    print(card_sets)
    for change in changes:
        print_line_number()
        print(change)
        change = change.strip("\n")
        change = change[2:-1]
        parts_of_card = change.split(":", 1)
        name = parts_of_card[0]
        change = parts_of_card[1]
        name_of_card_set = name_of_card_set.strip('"')
        name = name.strip("'")
        change = change.strip('"')
        change = change.strip("'")
        print_line_number()
        print(change)
        change = eval(change)
        card_sets[name_of_card_set][name] = change
    print_line_number()
    print(card_sets)

    list_of_cards = (str(card_sets)).split("}}")
    print_line_number()
    print(list_of_cards)
    erase_file("current_flashcard_set.txt")
    erase_file("flashcard_sets.txt")
    with open("flashcard_sets.txt", 'a') as file:
        file.write("{")
        file.write("\n")
    for card in list_of_cards[:-1]:
        card = card.lstrip("{")
        card = card.lstrip(",")
        card = card.lstrip()
        card = (card.strip('"') + "}},")
        print_line_number()
        print(card)
        with open("flashcard_sets.txt", 'a') as file:
            file.write(card)
            file.write("\n")
    with open("flashcard_sets.txt", 'a') as file:
        file.write("}")



    clear_session_variables()
    return redirect(url_for("index"))

@app.route('/multiple-choice-quiz', methods=["GET", "POST"])
def multiple_choice_quiz():
    return render_template("multiple-choice-quiz.html")


def clear_session_variables():
    erase_file("current_flashcard_set.txt")
    erase_file("list_of_flashcards_in_current_set.txt")
    erase_file("session_variables.txt")
    erase_file("changed_cards.txt")


if __name__ == "__main__":
    app.run(debug=True)





import json

def create_dictionary():
    data = {'name': input("Enter name: ")}

    terms = {}
    term_counter = 1

    while True:
        term_key = f'term{term_counter}'
        answer_key = f'answer{term_counter}'

        term_value = input(f"Enter term for {term_key} (or 'done' to finish): ")
        if term_value.lower() == 'done':
            break

        answer_value = input(f"Enter answer for {answer_key}: ")

        terms[term_key] = {'term': term_value, 'answer': answer_value}
        term_counter += 1

    data.update(terms)
    return data

def save_to_file(flashcard_sets, filename):
    with open(filename, 'w') as file:
        json.dump(flashcard_sets, file)

def load_flashcard_sets(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return json.loads(content) if content else []
    except json.decoder.JSONDecodeError:
        return []

def main():
    filename = 'flashcard_sets.txt'

    flashcard_sets = load_flashcard_sets(filename)

    while True:
        user_input = input("Do you want to create a new dictionary? (yes/no): ")
        if user_input.lower() != 'yes':
            break

        dictionary = create_dictionary()
        flashcard_sets.append(dictionary)
        save_to_file(flashcard_sets, filename)
        print("Dictionary saved successfully!")
    for i in flashcard_sets:
        print (i.get("name"))

if __name__ == "__main__":
    main()








# Code plan
# List of dictionary names, website has menu to choose which set of flashcards you want to do


# Flashcard sets themselves
# Each set is a dictionary, each flashcard is a sub dictionary with 3 attributes - Side1, Side2, learn_score. Each set also has a name
# Automate production: first create a dictionary with a 'name' value. Assign the name input to the name value then allow input of the rest of the values, creating dictionaries with them as it happens

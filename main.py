# This is a sample Python script.
import json

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
Flashcards = "flashcard_sets.txt"
my_dict = {
    "Name": input("Name"),
    "Age": input("Age"),
    "Place": input("Place")
}

file = open("flashcard_sets.txt", "w")
json.dump(my_dict, file)

file = open("flashcard_sets.txt", "r")
dictionary = dict(json.load(file))
print (dictionary)
print (dictionary["Name"])

# import json
#
# # Writing dictionary to a file
# my_dict = {
#     'name': 'John',
#     'age': 25,
#     'city': 'New York'
# }
#
# file_path = "my_dict.txt"
# with open(file_path, 'w') as file:
#     json.dump(my_dict, file)
#
# # Reading dictionary from a file
# with open(file_path, 'r') as file:
#     # Use json.load() to parse the content into a dictionary
#     dict_from_file = json.load(file)
#
# print(dict_from_file["name"])








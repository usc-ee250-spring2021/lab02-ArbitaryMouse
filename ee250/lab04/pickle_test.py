import pickle

notes = []
# Part A
notes = pickle.load(open("notes.pickle","r+"))
# Part B
print(notes)
# Part C
addNotes = input("Please enter the content you want to add in your notes:")
notes += addNotes
# Part D
pickle.dump(notes,open("notes.pickle","r+"))
# TODO: Using the pickle module...

# A. If notes.pickle exists, read it in using pickle and assign the content to
#   the notes variable

# B. Print out notes

# C. Read in a string from the user using input() and append it to notes

# D. Save notes to notes.pickle


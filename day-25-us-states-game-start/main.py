from tkinter import messagebox

import pandas
import turtle
from PIL import Image

image_path = "blank_states_img.gif"
image = Image.open(image_path)
image_width = image.width
image_height = image.height

# #draw the screen to the size of the image
screen = turtle.Screen()
screen.title("U.S. States Game")
screen.setup(width=image_width, height=image_height)
screen.bgpic(image_path)

# #read the csv data and add the state names to a list
states_data = pandas.read_csv("50_states.csv")
states_list = states_data.state.to_list()

# #to write the states name on the screen
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()

# #get a list of x & y coordinates
states_x_coordinates = states_data['x'].to_list()
states_y_coordinates = states_data['y'].to_list()

states_coordinates = []

# #put the coordinates into a list of tuples to pull from
for number in range(len(states_list)):
    current = (states_x_coordinates[number], states_y_coordinates[number])
    states_coordinates.append(current)

inputs_list = []

game_is_on = True

while game_is_on:
    answer_state = screen.textinput(title=f"{len(inputs_list)}/50 States Correct",
                                    prompt="Whats another state's name?").title()
    # #check if the user answer is in the list of states and that the list of states length is still greater than 0
    if answer_state == "Exit":
        # #filter missing states to revise using list comprehension
        missing_states = [state for state in states_list if state not in inputs_list]
        # for state in states_list:
        #     if state not in inputs_list:
        #         missing_states.append(state)
        new_data = pandas.DataFrame(missing_states)
        new_data.to_csv("States_to_learn.csv")
        break
    if answer_state in states_list and len(states_list) > 0:
        # #use the users answer as the index for the states list
        index = states_list.index(answer_state)
        # #using the index, get the coordinates and writes the state name on the map
        writer.goto(states_coordinates[index])
        writer.write(answer_state)
        # #add the answer to the inputs list
        inputs_list.append(answer_state)
        # #remove the guessed state and its coordinates from their respective lists
        del states_list[index]
        del states_coordinates[index]
    # #if the states list == 0, game is over
    elif len(states_list) == 0:
        game_is_on = False
    # #if the answer is in the inputs list, duplicate answer message
    elif answer_state in inputs_list:
        messagebox.showinfo(title="Duplicate Guess", message=f"{answer_state} already guessed and is on the map.")
    # #if the guess is incorrect, inform the user
    else:
        messagebox.showinfo(title="Incorrect Guess", message=f"{answer_state} is not on the map.")
    # #outside the game loop, confirm game over to user
    if len(states_list) == 0:
        messagebox.showinfo(title="Map Complete", message="Well done, you completed the map!")

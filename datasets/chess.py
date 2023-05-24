import pyautogui
import keyboard
import time
# Set the size of the chess board
board_size = 8

# Set the size of each square
square_size = 100

# Set the starting position of the mouse
mouse_pos = (375, 225)
time.sleep(5)
# Move the mouse to the upper-left corner of the board
pyautogui.moveTo(mouse_pos[0], mouse_pos[1], duration=1)

# Loop through each square as the starting square
for start_row in range(board_size):
    for start_col in range(board_size):
        # Calculate the position of the starting square
        start_pos = (mouse_pos[0] + start_col * square_size, mouse_pos[1] + start_row * square_size)
        
        # Press the right mouse button at the starting square
        pyautogui.mouseDown(start_pos[0], start_pos[1], button='right')
        
        # Loop through each square as the ending square
        for end_row in range(board_size):
            for end_col in range(board_size):
                # Calculate the position of the ending square
                end_pos = (mouse_pos[0] + end_col * square_size, mouse_pos[1] + end_row * square_size)
                
                # Move the mouse to the ending square
                pyautogui.moveTo(end_pos[0], end_pos[1], duration=0.1)
                
                # Release the right mouse button at the ending square
                pyautogui.mouseUp(end_pos[0], end_pos[1], button='right')
                
                # Check if the 'Esc' key has been pressed
                if keyboard.is_pressed('Esc'):
                    # Stop the program if the 'Esc' key has been pressed
                    quit()
                    
        # Release the right mouse button at the starting square
        pyautogui.mouseUp(start_pos[0], start_pos[1], button='right')
import keyboard
import time
import win32api, win32con

# Set the coordinates of the center of the screen
screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
center_x, center_y = screen_width // 2, screen_height // 2
center_y -= 260
center_x -= 50

# Set initial pause state to False
paused = True

# Loop until the stop button is pressed
while True:
    # Check if the pause/resume button has been pressed
    if keyboard.is_pressed('p'):
        paused = not paused
        time.sleep(0.2)  # Wait to avoid registering multiple key presses
    # Only execute the loop if not paused
    if not paused:
        # Simulate pressing the "V" key
        keyboard.press('v')

        # Move the mouse to the center of the screen
        win32api.SetCursorPos((center_x, center_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, center_x, center_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, center_x, center_y, 0, 0)
        time.sleep(0.001) 
        # Release the "V" key
        keyboard.release('v')

        # Pause briefly to avoid overloading the system
        

    # Check if the stop button has been pressed
    if keyboard.is_pressed('o'):
        break

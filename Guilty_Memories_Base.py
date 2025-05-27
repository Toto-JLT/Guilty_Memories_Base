#Guilty Memories 
#Deadline: 26/06/2025
#Coded by: Toto :)


import pygame #Importing pygame library.
import random #Importing functions for random number generation.
import time #Importing time library for delays.
pygame.init() #Initialize the pygame library.

#Parameters, screen size and boxes specifications.
width, height = 780, 500
box_size = 100
target_size = 100
num_boxes = 9

#Display settings and title.
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Guilty Memories")

#Timer settings.
total_time = 60 #Time in seconds.

# --- LOADING ASSETS ---
#Fonts and text.
font = pygame.font.Font("DailyMemory-EBdl.ttf", 30)
big_font = pygame.font.Font("DailyMemory-EBdl.ttf", 80)
small_font = pygame.font.SysFont("courier new", 20)

#Images for background and menu.
background_img = pygame.image.load("background.jpg").convert()
menu_background_img = pygame.image.load("menu.jpg").convert()
background_img = pygame.transform.scale(background_img, (width, height))
menu_background_img = pygame.transform.scale(menu_background_img, (width, height))

# --- MENU SCREEN FUNCTION ---
def draw_text(surface, text, font, color, x, y):
    #Helper function to draw text on the screen.

    #Defining parameters for the text. 
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, rect)

#Function to display the menu screen.
def menu_screen():
    menu = True

    #Creating buttons for the menu.
    play_button = pygame.Rect(width//2 - 100, height//2 - 60, 200, 50)
    quit_button = pygame.Rect(width//2 - 100, height//2 + 20, 200, 50)
    
    #Main loop for the menu screen.
    #This loop will run until the user clicks the play or quit button.
    while menu:
        screen.blit(menu_background_img, (0, 0)) #Drawing the background image.

        #Drawing game title.
        draw_text(screen, "Guilty Memories", big_font, (255, 255, 255), width//2, height//2 - 120)

        #Drawing rectangles for buttons.
        pygame.draw.rect(screen, (0, 200, 0 ), play_button)
        pygame.draw.rect(screen, (200, 0, 0), quit_button)

        #Drawing text on buttons.
        draw_text(screen, "Play", font, (255, 255, 255), play_button.centerx, play_button.centery)
        draw_text(screen, "Quit", font, (255, 255, 255), quit_button.centerx, quit_button.centery)
        
        # --- EVENT HANDLING MENU ---
        #Checking for events in the menu.

    #Player clicks "X" button to close the window.
    pygame.display.update() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Window closed.")
            pygame.quit() 
            exit()
            
    #Detecting click on play button.
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_button.collidepoint(event.pos):
                print(f"Play button clicked!")
                menu = False 

                #Detecting click on quit button.   
        elif quit_button.collidepoint(event.pos):
            print(f"Quit button clicked!")
            pygame.quit()
            exit()

#Initialize the timer.
start_time = time.time() #store the start time of the game.

menu_screen() 

# --- GAME SETUP ---
#Opening empty lists for boxes and targets.
boxes = []
targets = []

#Generating random positions for boxes and targets.
for i in range(num_boxes):

    #Randomly generating x and y coordinates for boxes.
    x = random.randint(0, width - box_size)
    y = random.randint(0, height - box_size)

    #Creating box squares.
    box = pygame.Rect(x, y, box_size, box_size)
    boxes.append(box)

    #Randomly generating x and y coordinates for targets (3x3 grid).
    grid_x = (i % 3) * (width // 3) + (width // 6 - target_size // 2)
    grid_y = (i // 3) * (height // 3) + (height // 6 - target_size // 2)
    
    #Creating target rectangles.
    target = pygame.Rect(grid_x, grid_y, target_size, target_size)
    target = pygame.Rect(grid_x, grid_y, target_size, target_size)
    targets.append(target)

# Variable to keep track of dragging state.
active_box = None
offset_x = 0
offset_y = 0


# --- MAIN GAME LOOP ---
print("Game started, place the boxes on their targets!")
run = True
while run:  

    # Calculate and display the elapsed time.
    elapsed_seconds = int(time.time() - start_time)
    remaining_time = max(0, total_time - elapsed_seconds)

    screen.blit(background_img, (0, 0)) #Drawing the background image.

    #Drawing targets. (Outlined rectangles)
    for target in targets:
        pygame.draw.rect(screen, (128, 0, 128), target, 3)

    #Drawing boxes. (Filled rectangles)
    for box in boxes:
        pygame.draw.rect(screen, (255,192,203), box)

    #Draw the timer on the screen.
    timer_text = f"Time: {remaining_time}s"
    draw_text(screen, timer_text, small_font, (255, 255, 255), width - 80, 30)

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #Quits the game.

        #Detecting mouse button down.
        #If left mouse button is pressed, check if it collides with any box.
        #If it does, set it as the active box.
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, box in enumerate(boxes):
                if box.collidepoint(event.pos):
                    active_box = idx #Set the active box.

                    #Storing the offset to drag smoothly.
                    offset_x = box.x - event.pos[0]
                    offset_y = box.y - event.pos[1]

                    #Print control message.
                    print(f"Box {active_box + 1} grabbed!")
                    break

        #Detecting mouse motion.
        #If the left mouse button is pressed and a box is active, move it with the mouse.
        elif event.type == pygame.MOUSEMOTION and active_box is not None:
            #Move the active box with the mouse.
            boxes[active_box].x = event.pos[0] + offset_x
            boxes[active_box].y = event.pos[1] + offset_y

        #Detecting mouse button up.
        #If the left mouse button is released, check if the box is close to the target.
        #If it is, snap it to the target.
        elif event.type == pygame.MOUSEBUTTONUP and event.button ==1 and active_box is not None:

            #Print control message.
            print(f"Box {active_box + 1} released!")

            #Snap the box to the target if close enough.
            box = boxes[active_box]
            target = targets[active_box]
            if abs(box.centerx - target.centerx) < 20 and abs(box.centery - target.centery) < 20:
                box.center = target.center

                #Print control message.
                print(f"Box {active_box + 1} placed succesfully!")

            active_box = None

    pygame.display.update() #Update the display.

    # --- LOSE CONDITION CHECK ---
# --- RESETING GAME ---
#Clearing boxes and targets for a new game.
def reset_game():
    boxes.clear()
    targets.clear()

    for i in range(num_boxes):
        #Randomly generating x and y coordinates for boxes.
        x = random.randint(0, width - box_size)
        y = random.randint(0, height - box_size)
        box = pygame.Rect(x, y, box_size, box_size)
        boxes.append(box)

        #Randomly generating x and y coordinates for targets (3x3 grid).
        grid_x = (i % 3) * (width // 3) + (width // 6 - target_size // 2)
        grid_y = (i // 3) * (height // 3) + (height // 6 - target_size // 2)
        target = pygame.Rect(grid_x, grid_y, target_size, target_size)
        targets.append(target)
        
    #Reset active box and offsets.
    global active_box, offset_x, offset_y, start_time
    active_box = None
    offset_x = 0
    offset_y = 0

    print("Game restarted, place the boxes on their targets!")
    start_time = time.time()  # Reset the timer.

    # --- WIN CONDITION CHECK ---
    #Check if all boxes are on their targets.
    all_on_targets = all(
        box.center == target.center
        for box, target in zip(boxes, targets)
    )
    if all_on_targets:
        print("All boxes are on their targets!")

        #Return to menu screen.
        menu_screen()

    # End of reset_game function

    # --- MAIN GAME LOOP ---
print("Game started, place the boxes on their targets!")
run = True
while run:  

    # Calculate and display the elapsed time.
    elapsed_seconds = int(time.time() - start_time)
    remaining_time = max(0, total_time - elapsed_seconds)

    screen.blit(background_img, (0, 0)) #Drawing the background image.

    #Drawing targets. (Outlined rectangles)
    for target in targets:
        pygame.draw.rect(screen, (128, 0, 128), target, 3)

    #Drawing boxes. (Filled rectangles)
    for box in boxes:
        pygame.draw.rect(screen, (255,192,203), box)

    #Draw the timer on the screen.
    timer_text = f"Time: {remaining_time}s"
    draw_text(screen, timer_text, small_font, (255, 255, 255), width - 80, 30)

    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #Quits the game.

        #Detecting mouse button down.
        #If left mouse button is pressed, check if it collides with any box.
        #If it does, set it as the active box.
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, box in enumerate(boxes):
                if box.collidepoint(event.pos):
                    active_box = idx #Set the active box.

                    #Storing the offset to drag smoothly.
                    offset_x = box.x - event.pos[0]
                    offset_y = box.y - event.pos[1]

                    #Print control message.
                    print(f"Box {active_box + 1} grabbed!")
                    break

        #Detecting mouse motion.
        #If the left mouse button is pressed and a box is active, move it with the mouse.
        elif event.type == pygame.MOUSEMOTION and active_box is not None:
            #Move the active box with the mouse.
            boxes[active_box].x = event.pos[0] + offset_x
            boxes[active_box].y = event.pos[1] + offset_y

        #Detecting mouse button up.
        #If the left mouse button is released, check if the box is close to the target.
        #If it is, snap it to the target.
        elif event.type == pygame.MOUSEBUTTONUP and event.button ==1 and active_box is not None:

            #Print control message.
            print(f"Box {active_box + 1} released!")

            #Snap the box to the target if close enough.
            box = boxes[active_box]
            target = targets[active_box]
            if abs(box.centerx - target.centerx) < 20 and abs(box.centery - target.centery) < 20:
                box.center = target.center

                #Print control message.
                print(f"Box {active_box + 1} placed succesfully!")

            active_box = None

    pygame.display.update() #Update the display.

    # --- LOSE CONDITION CHECK ---
    if remaining_time <= 0:
        print("Time's up! You lost!")
        menu_screen()
        reset_game() 

pygame.quit() #End of the game.
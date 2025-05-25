#Guilty Memories 
#Deadline: 26/06/2025
#Coded by: Toto :)


import pygame #Importing pygame library.
import random #Importing functions for random number generation.
pygame.init() #Initialize the pygame library.

#Parameters, screen size and boxes specifications.
width, height = 780, 500
box_size = 100
target_size = 100
num_boxes = 9

#Display settings and title.
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Guilty Memories")

# --- MENU SCREEN FUNCTION ---
def draw_text(surface, text, size, color, x, y):
    #Helper function to draw text on the screen.

    #Defining parameters for the text. 
    font = pygame.font.SysFont(None, size)
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
        screen.fill((30, 30, 60)) #Filling the screen with a color (dark blue).

        #Drawing game title.
        draw_text(screen, "Guilty Memories", 60, (255, 255, 255), width//2, height//2 - 120)

        #Drawing rectangles for buttons.
        pygame.draw.rect(screen, (0, 200, 0 ), play_button)
        pygame.draw.rect(screen, (200, 0, 0), quit_button)

        #Drawing text on buttons.
        draw_text(screen, "Play", 40, (255, 255, 255), play_button.centerx, play_button.centery)
        draw_text(screen, "Quit", 40, (255, 255, 255), quit_button.centerx, quit_button.centery)
        
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

     #Filling the screen with a color (dark blue).
    screen.fill((0, 0, 30)) 

    #Drawing targets. (Outlined rectangles)
    for target in targets:
        pygame.draw.rect(screen, (128, 0, 128), target, 3)

    #Drawing boxes. (Filled rectangles)
    for box in boxes:
        pygame.draw.rect(screen, (255,192,203), box)

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

        # --- RESETING GAME ---
        #Clearing boxes and targets for a new game.
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
        active_box = None
        offset_x = 0
        offset_y = 0

        print("Game restarted, place the boxes on their targets!")

pygame.quit() #End of the game.
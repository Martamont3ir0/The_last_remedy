import pygame
from game import *
from config import *
from shed import *

def puzzle_game(screen):
    """
    puzzle that consists on a wire connection:
    the player connects wires to match nodes.
    parameters:
    -dragging_wire: tracks which wire the player is currently dragging.
    -dragging_offset: stores offset between the players click position and the wires position.
    - connections: list to track the connections between wires and nodes.
    """

    #configuration values to use
    colors= puzzle_colors
    wire_positions= puzzle_wire_positions.copy()
    node_positions= puzzle_node_positions

    #variables to track the players actions
    dragging_wire = None
    dragging_offset= (0,0)#used to make the dragging smooth
    connections= [None]* len(colors)


    running= True
    clock= pygame.time.Clock()

    while running:
        mouse_pos= pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                for i, (x, y) in enumerate(wire_positions):
                    if (x - 15 <= mouse_pos[0] <= x + 15) and (y - 15 <= mouse_pos[1] <= y + 15):
                        dragging_wire = i
                        dragging_offset = (mouse_pos[0] - x, mouse_pos[1] - y)

            if event.type==pygame.MOUSEBUTTONUP:
                if dragging_wire is not None:
                    for i, (x, y) in enumerate(node_positions):
                        if (x - 15 <= mouse_pos[0] <= x + 15) and (y - 15 <= mouse_pos[1] <= y + 15):
                            if connections[i] is None:  # Only connect if the node is not already connected
                                connections[i] = dragging_wire
                                break
                    dragging_wire = None

        #update dragging wire position:
        if dragging_wire is not None:
            wire_positions[dragging_wire] = (mouse_pos[0] - dragging_offset[0], mouse_pos[1] - dragging_offset[1])

        #check if the puzzle is solved
        solved= True
        for i, connection in enumerate(connections):
            if connection is None or connection!=i:
                solved= False
                break

        if solved:
            #puzzle is completed successfully
            print("Puzzle Solved!")
            return "shed" #proceed to the shed after solving the puzzle

        #draw the puzzle
        screen.fill((30,30,30))
        font= pygame.font.Font(None, 36)
        instructions = font.render("Connect the wires to the matching nodes!", True, (255, 255, 255))
        screen.blit(instructions, (50, 50))

        #draw wires
        for i, (x,y) in enumerate(wire_positions):
            pygame.draw.circle(screen, colors[i], (x,y), 15)
            if connections[i] is not None:
                node_x, node_y= node_positions[connections[i]]
                pygame.draw.line(screen, colors[i], (x, y), (node_x, node_y), 3)

        #dragging the wires
        if dragging_wire is not None:
            pygame.draw.line(screen, colors[dragging_wire], wire_positions[dragging_wire], mouse_pos, 3 )

        #draw nodes
        for i, (x, y) in enumerate(node_positions):
            pygame.draw.circle(screen, colors[i], (x, y), 15)
            if connections[i] is not None:
                wire_x, wire_y = wire_positions[connections[i]]
                pygame.draw.line(screen, colors[i], (x, y), (wire_x, wire_y), 3)

        pygame.display.flip()
        clock.tick(60)

def show_balloon(screen, background):
    # Constants
    balloon_start_y = -105
    balloon_start_x = 400
    # Load and scale the balloon image
    balloon_image = pygame.image.load('img/military_drop.png')
    balloon_image = pygame.transform.scale(balloon_image, (300, 300))
    balloon_rect = balloon_image.get_rect(center=(balloon_start_x, balloon_start_y))  # Center horizontally

    # Return the balloon image and rectangle
    return balloon_image, balloon_rect


def puzzle_message(background, player, selected_character, bg_width):
    screen = pygame.display.set_mode(resolution)
    balloon_image, balloon_rect = show_balloon(screen, background) #getting the values that were returned from the show_balloon function
    clock = pygame.time.Clock()
    balloon_speed = 9
    balloon_end_y = 437

    # add crate dropping sound
    pygame.mixer.music.load("audio/mixkit-bomb-drop-impact-2804.wav")
    pygame.mixer.music.play(0)  # Play music once
    balloon_dropped = False #State to check if the balloon has dropped

    # Main loop for the puzzle message
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Update the balloon's position
        if balloon_rect.centery < balloon_end_y: #Controlling when the y of balloon rect reaches the y position we want
            balloon_rect.y += balloon_speed # Move the balloon down
        else:
            balloon_dropped = True

        # Clear the screen
        screen.fill((0, 0, 0))  # Fill with black background
        screen.blit(background, (0, 0))

        # Draw the balloon
        screen.blit(balloon_image, balloon_rect)

        # Call the user_info function
        user_info(player, screen, False)

        # Update the display
        pygame.display.flip()
        clock.tick(30)  # Control the frame rate

        # Check for mouse button down event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if balloon_dropped and balloon_rect.collidepoint(event.pos):
                    shed(player, selected_character, bg_width)



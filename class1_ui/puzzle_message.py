import pygame
from game import *
from config import *
from shed import *
import random # For shuffling nodes
from class1_ui.interface import interface

def puzzle_game(screen):
    """
        Displays a wire-connecting puzzle where the player connects wires to shuffled nodes.

        The player must:
        - Drag and connect wires to their matching colored nodes.
        - Complete the puzzle within a 16-second timer.

        Key Features:
        - A timer at the top tracks the remaining time.
        - If the player matches wires incorrectly, the wire returns to its original position.
        - If the time runs out, a retry option is displayed to restart or exit.

        Args:
            screen (pygame.Surface): The game screen surface to render the puzzle.
            player:


        Returns:
            function shed if the puzzle is solved, or triggers a retry/reset if the timer runs out.
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Render game elements
        screen.fill(deep_black)
        # Add your puzzle game logic here

        # Apply brightness and sound
        apply_brightness_and_sound(screen)

        pygame.display.flip()

    def show_retry_prompt(screen):
        """
         Displays a retry prompt when the puzzle timer runs out.

         Args:
             screen (pygame.Surface): The game screen surface to display the prompt.

         Returns:
             str: "retry" to restart the puzzle, or "main" to return to the main menu.
         """
        font = pygame.font.Font(None, 48)
        prompt_text = font.render("Time's up! Want to try again?", True, (255, 255, 255))
        yes_button = pygame.Rect(width // 2 - 150, 400, 100, 50)
        no_button = pygame.Rect(width // 2 + 50, 400, 100, 50)

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button.collidepoint(mouse_pos):
                        interface()
                    if no_button.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()

            # Draw the prompt
            screen.fill(deep_black)
            screen.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, 300))

            # Draw buttons
            pygame.draw.rect(screen, (0, 255, 0), yes_button)  # Green for "Yes"
            pygame.draw.rect(screen, (255, 0, 0), no_button)  # Red for "No"

            # Draw button text
            yes_text = font.render("Yes", True, (0, 0, 0))
            no_text = font.render("No", True, (0, 0, 0))
            screen.blit(yes_text, (yes_button.centerx - yes_text.get_width() // 2, yes_button.centery - yes_text.get_height() // 2))
            screen.blit(no_text,(no_button.centerx - no_text.get_width() // 2, no_button.centery - no_text.get_height() // 2))

            # Apply brightness and sound settings dynamically
            apply_brightness_and_sound(screen)

            pygame.display.flip()

    # Configuration values
    colors = puzzle_colors
    wire_positions = puzzle_wire_positions.copy()
    node_positions = puzzle_node_positions.copy()

    # Shuffle the nodes for added difficulty
    random.shuffle(node_positions)

    # Variables to track player actions
    dragging_wire = None
    dragging_offset = (0, 0)  # Smooth dragging
    connections = [None] * len(colors)

    running = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()  # Timer start point
    time_limit = 30000  # 30 seconds in milliseconds
    puzzle_bg = pygame.image.load("img/cratebg.png")
    while running:


        screen.blit(puzzle_bg,(0,0))
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        remaining_time = max(0, time_limit - elapsed_time)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Start dragging wire
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (x, y) in enumerate(wire_positions):
                    if (x - 15 <= mouse_pos[0] <= x + 15) and (y - 15 <= mouse_pos[1] <= y + 15):
                        dragging_wire = i
                        dragging_offset = (mouse_pos[0] - x, mouse_pos[1] - y)

            # Drop the wire
            if event.type == pygame.MOUSEBUTTONUP:
                if dragging_wire is not None:
                    connected = False
                    for i, (x, y) in enumerate(node_positions):
                        # Check if the wire matches the correct color node
                        if (x - 15 <= mouse_pos[0] <= x + 15) and (y - 15 <= mouse_pos[1] <= y + 15):
                            if connections[i] is None and i == dragging_wire:  # Ensure it's the correct node
                                connections[i] = dragging_wire
                                connected = True
                                break

                    if not connected:
                        # Reset wire to its original position
                        wire_positions[dragging_wire] = puzzle_wire_positions[dragging_wire]

                    dragging_wire = None  # Reset dragging state

        # Check if the timer has run out
        if remaining_time == 0:
            show_retry_prompt(screen)

        # Check if the puzzle is solved
        solved = all(connections[i] == i for i in range(len(connections)))

        if solved:
            print("Puzzle Solved!")
            return "shed" #proceed to the shed after solving the puzzle


        # Display the timer
        timer_font = pygame.font.Font(None, 35)
        timer_text = timer_font.render(f"Time Left: {remaining_time // 1000}", True, white)
        timer_rect = timer_text.get_rect(center=(width // 2, 35 ))
        screen.blit(timer_text, timer_rect)

        # Draw wires
        for i, (x, y) in enumerate(wire_positions):
            pygame.draw.circle(screen, colors[i], (x, y), 15)
            if connections[i] is not None:
                node_x, node_y = node_positions[i]
                pygame.draw.line(screen, colors[i], (x, y), (node_x, node_y), 3)

        # Draw dragging wire
        if dragging_wire is not None:
            pygame.draw.line(screen, colors[dragging_wire], wire_positions[dragging_wire], mouse_pos, 3)

        # Draw nodes
        for i, (x, y) in enumerate(node_positions):
            pygame.draw.circle(screen, colors[i], (x, y), 15)


        #display of instructions
        font= pygame.font.Font(None, 33)
        instructions = font.render("To unlock the crate and get the map of The Wastes,", True, deep_black)
        instructions2 = font.render("connect the colors to prove you're not a ROBOT!",True, deep_black)
        instructions_rect = instructions.get_rect()
        instructions2_rect = instructions2.get_rect()
        instructions_rect.center = (width//2, 95)
        instructions2_rect.center = (width // 2, 135)


        screen.blit(instructions, instructions_rect)
        screen.blit(instructions2, instructions2_rect)

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        pygame.display.flip()
        clock.tick(60)

def show_balloon():
    """
    :return:
    """
    # Constants
    balloon_start_y = -105
    balloon_start_x = 400
    # Load and scale the balloon image
    balloon_image = pygame.image.load('img/military_drop.png')
    balloon_image = pygame.transform.scale(balloon_image, (300, 300))
    balloon_rect = balloon_image.get_rect(center=(balloon_start_x, balloon_start_y))  # Center horizontally

    # Return the balloon image and rectangle
    return balloon_image, balloon_rect


def puzzle_message(background, player):
    """

    :param background:
    :param player:
    :return:
    """
    screen = pygame.display.set_mode(resolution)
    balloon_image, balloon_rect = show_balloon() #getting the values that were returned from the show_balloon function
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

        # Apply brightness and sound settings dynamically
        apply_brightness_and_sound(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(30)  # Control the frame rate

        # Check for mouse button down event
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if balloon_dropped and balloon_rect.collidepoint(event.pos):
                    return "puzzle_game"




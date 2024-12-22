import pygame
import cv2


class FinalChoice:
    def __init__(self, screen, player):
        """
        Initializes the FinalChoice object with the screen and player data.

        :param screen: The screen surface where the choice UI and video will be displayed.
        :param player: The player object that contains character data like selected character type.
        """
        self.screen = screen
        self.character_type = player.selected_character  # Character type: "girl" or "boy"

        # Fonts for different UI elements (titles, options, subtext, etc.)
        self.font_title = pygame.font.Font(None, 80)
        self.font_options = pygame.font.Font(None, 48)
        self.font_subtext = pygame.font.Font(None, 40)
        self.font_discreet = pygame.font.Font(None, 32)  # Smaller font for discreet messages
        self.font_outcome = pygame.font.Font(None, 60)

        # The list of possible final choices presented to the player
        self.options = [
            "Option 1: Save humanity",
            "Option 2: Keep the elixir for yourself",
            "Option 3: Accept humanity’s fate",
        ]

        # Color scheme for each option (Green, Orange, Red)
        self.colors = [(0, 255, 0), (255, 165, 0), (255, 0, 0)]

        # Default selected option is the first one
        self.selected_index = 0

    def render_text_with_shadow(self, text, font, x, y, color, shadow_offset=2):
        """
        Renders text with a shadow effect to make the text visually more appealing.

        :param text: The text string to be displayed.
        :param font: The font to be used for rendering the text.
        :param x: The x-coordinate of the text position.
        :param y: The y-coordinate of the text position.
        :param color: The main color of the text.
        :param shadow_offset: The offset used to display the shadow text (default is 2 pixels).
        """
        # Create a shadow of the text (dark gray color)
        shadow = font.render(text, True, (50, 50, 50))
        # Draw the shadow with a small offset
        self.screen.blit(shadow, (x + shadow_offset, y + shadow_offset))

        # Create the main text with the desired color
        rendered_text = font.render(text, True, color)
        # Draw the main text on top of the shadow
        self.screen.blit(rendered_text, (x, y))

    def play_video(self, choice_index):
        """
        Plays a video based on the player's choice and character type.
        The video is displayed with a 90-degree clockwise rotation to fit the screen.

        :param choice_index: The index of the selected choice (0, 1, or 2) that determines the video to play.
        """
        # Mapping the character type and choice index to video file paths
        video_paths = {
            "girl": [
                "vid/little_girl.mp4",
                "vid/eye.mp4",
                "vid/dark_wind.mp4",
            ],
            "boy": [
                "vid/sunset.mp4",
                "vid/flowers.mp4",
                "vid/vela.mp4",
            ],
        }

        # Select the appropriate video based on character type and choice index
        video_path = video_paths.get(self.character_type, [""])[choice_index]

        # Open the video using OpenCV
        cap = cv2.VideoCapture(video_path)

        # Check if the video file was opened successfully
        if not cap.isOpened():
            print(f"Error: Cannot open video {video_path}")
            return

        # Set up the clock to control the playback speed
        clock = pygame.time.Clock()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Rotate the frame 90 degrees clockwise to match the screen orientation
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Resize the frame to fit the screen dimensions
            screen_width, screen_height = self.screen.get_size()
            frame_resized = cv2.resize(frame, (screen_width, screen_height))

            # Convert the frame from BGR to RGB for Pygame compatibility
            frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            # Convert the frame into a Pygame surface
            frame_resized = pygame.surfarray.make_surface(frame_resized)

            # Draw the resized frame on the screen
            self.screen.blit(frame_resized, (0, 0))

            # Update the display and control playback speed (30 frames per second)
            pygame.display.flip()
            clock.tick(30)

            # Handle quit events during video playback
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    exit()

        # Release the video capture object after playback
        cap.release()

    class FinalChoice:

        def display_choice_screen(self):
            """
            Displays the screen where the player can make a final choice.
            This screen includes a title, subtext, a flashing 'Press Enter twice' message,
            and the options for the player to select from.

            The player can use the UP and DOWN arrow keys to navigate between options,
            and the ENTER key to select an option.

            :return: The index of the option the player selected.
            """
            running = True
            press_twice_text = "Press Enter twice for good measure"
            show_press_twice = True
            press_twice_last_toggled = pygame.time.get_ticks()  # Time tracking for flashing effect

            while running:
                self.screen.fill((0, 0, 0))  # Clear the screen with black background

                # Render the title text and center it on the screen
                title_surface = self.font_title.render("Make your choice", True, (255, 255, 255))
                title_x = self.screen.get_width() // 2 - title_surface.get_width() // 2
                title_y = 50
                self.render_text_with_shadow("Make your choice", self.font_title, title_x, title_y, (255, 255, 255))

                # Render subtext below the title
                subtext = "Live with the consequences"
                subtext_surface = self.font_subtext.render(subtext, True, (255, 255, 255))
                subtext_x = self.screen.get_width() // 2 - subtext_surface.get_width() // 2
                subtext_y = 130
                self.render_text_with_shadow(subtext, self.font_subtext, subtext_x, subtext_y, (200, 200, 200))

                # Flash the "Press Enter twice" message at a set interval
                current_time = pygame.time.get_ticks()
                if current_time - press_twice_last_toggled > 500:
                    show_press_twice = not show_press_twice  # Toggle visibility
                    press_twice_last_toggled = current_time

                if show_press_twice:
                    press_twice_surface = self.font_discreet.render(press_twice_text, True, (150, 150, 150))
                    press_twice_x = self.screen.get_width() // 2 - press_twice_surface.get_width() // 2
                    press_twice_y = self.screen.get_height() - 50
                    self.screen.blit(press_twice_surface, (press_twice_x, press_twice_y))

                # Render the available options
                for i, option in enumerate(self.options):
                    x_pos = self.screen.get_width() // 2
                    y_pos = 220 + i * 100  # Position each option with some vertical spacing
                    option_surface = self.font_options.render(option, True, (255, 255, 255))
                    option_rect = option_surface.get_rect(center=(x_pos, y_pos))
                    pygame.draw.rect(self.screen, self.colors[i], option_rect.inflate(20, 20), 4)  # Option background

                    # Highlight the selected option
                    if i == self.selected_index:
                        pygame.draw.rect(self.screen, (255, 255, 255), option_rect.inflate(30, 30), 3)

                    self.render_text_with_shadow(option, self.font_options, option_rect.x, option_rect.y,
                                                 (255, 255, 255))

                pygame.display.flip()  # Update the screen

                # Event handling for user input (navigation and selection)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        # UP and DOWN arrow keys to navigate options
                        if event.key == pygame.K_UP:
                            self.selected_index = (self.selected_index - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_index = (self.selected_index + 1) % len(self.options)
                        # ENTER key to confirm selection
                        elif event.key == pygame.K_RETURN:
                            print(f"You selected: {self.options[self.selected_index]}")
                            running = False  # Exit the loop once a choice is made

            return self.selected_index  # Return the index of the selected option

        def display_outcome_screen(self, choice_index):
            """
            Displays the outcome of the player's final choice by playing the corresponding video.

            :param choice_index: The index of the player's selected option which determines the video played.
            """
            self.screen.fill((0, 0, 0))  # Fill screen with black before displaying video
            pygame.display.flip()  # Update screen to show black before video starts
            self.play_video(choice_index)  # Play the corresponding video based on choice
            self.display_final_end_screen()  # Show the final end screen after video finishes

        def display_final_end_screen(self):
            """
            Displays the final end screen with a visually appealing gradient background
            and a pulsating "Thank You for Playing" message before closing the game.
            """
            # Create a gradient background effect
            gradient_surface = pygame.Surface(self.screen.get_size())
            for i in range(self.screen.get_height()):
                # Generate a gradient from blue to red
                color = (i * 255 // self.screen.get_height(), 0, 255 - i * 255 // self.screen.get_height())
                pygame.draw.line(gradient_surface, color, (0, i), (self.screen.get_width(), i))

            # Create a fade-out effect on top of the gradient
            fade_surface = pygame.Surface(self.screen.get_size())
            fade_surface.fill((0, 0, 0))  # Black fade effect

            clock = pygame.time.Clock()
            for alpha in range(0, 256, 5):  # Gradual fade-in effect
                fade_surface.set_alpha(255 - alpha)  # Decrease transparency as the screen fades in
                self.screen.blit(gradient_surface, (0, 0))  # Draw the gradient
                self.screen.blit(fade_surface, (0, 0))  # Draw the fade effect

                # Display the pulsating "Thank You for Playing" text
                text = "Thank You for Playing"
                pulsate_size = 60 + (10 * pygame.time.get_ticks() % 1000 // 500)  # Pulsate the text size
                font = pygame.font.Font(None, pulsate_size)
                text_surface = font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
                self.screen.blit(text_surface, text_rect)

                pygame.display.flip()  # Update the screen
                clock.tick(30)  # Control frame rate

            pygame.time.wait(3000)  # Hold the final screen for 3 seconds before closing
            return "interface"  # Return a string indicating the game is ready for the interface to reload or quit



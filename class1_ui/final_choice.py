import pygame
import cv2

class FinalChoice:
    def _init_(self, screen, player):
        self.screen = screen
        self.character_type = player.selected_character  # Character type: "girl" or "boy"
        self.font_title = pygame.font.Font(None, 80)
        self.font_options = pygame.font.Font(None, 48)
        self.font_subtext = pygame.font.Font(None, 40)
        self.font_discreet = pygame.font.Font(None, 32)  # Smaller font for discreet messages
        self.font_outcome = pygame.font.Font(None, 60)
        self.options = [
            "Option 1: Save humanity",
            "Option 2: Keep the elixir for yourself",
            "Option 3: Accept humanity’s fate",
        ]
        self.colors = [(0, 255, 0), (255, 165, 0), (255, 0, 0)]
        self.selected_index = 0

    def render_text_with_shadow(self, text, font, x, y, color, shadow_offset=2):
        shadow = font.render(text, True, (50, 50, 50))
        self.screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))

    def play_video(self, choice_index):
        """
        Play a video based on the selected choice and character type.
        The video frames will be rotated 90 degrees clockwise.
        """
        # Map choices to video file paths
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

        # Select the appropriate video
        video_path = video_paths.get(self.character_type, [""])[choice_index]

        # OpenCV Video Playback
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Error: Cannot open video {video_path}")
            return

        clock = pygame.time.Clock()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Rotate the frame 90 degrees clockwise
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Resize the frame to stretch it to fit the screen
            screen_width, screen_height = self.screen.get_size()
            frame_resized = cv2.resize(frame, (screen_width, screen_height))

            # Convert frame to Pygame format
            frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            frame_resized = pygame.surfarray.make_surface(frame_resized)

            # Draw the resized (stretched) frame on the screen
            self.screen.blit(frame_resized, (0, 0))

            pygame.display.flip()
            clock.tick(30)  # Control playback speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    exit()

        cap.release()

    def display_choice_screen(self):
        running = True
        press_twice_text = "Press Enter twice for good measure"
        show_press_twice = True
        press_twice_last_toggled = pygame.time.get_ticks()

        while running:
            self.screen.fill((0, 0, 0))  # Clear the screen with black background

            title_surface = self.font_title.render("Make your choice", True, (255, 255, 255))
            title_x = self.screen.get_width() // 2 - title_surface.get_width() // 2
            title_y = 50
            self.render_text_with_shadow("Make your choice", self.font_title, title_x, title_y, (255, 255, 255))

            subtext = "Live with the consequences"
            subtext_surface = self.font_subtext.render(subtext, True, (255, 255, 255))
            subtext_x = self.screen.get_width() // 2 - subtext_surface.get_width() // 2
            subtext_y = 130
            self.render_text_with_shadow(subtext, self.font_subtext, subtext_x, subtext_y, (200, 200, 200))

            # Flash "Press Twice" Text
            current_time = pygame.time.get_ticks()
            if current_time - press_twice_last_toggled > 500:
                show_press_twice = not show_press_twice
                press_twice_last_toggled = current_time

            if show_press_twice:
                press_twice_surface = self.font_discreet.render(press_twice_text, True, (150, 150, 150))
                press_twice_x = self.screen.get_width() // 2 - press_twice_surface.get_width() // 2
                press_twice_y = self.screen.get_height() - 50
                self.screen.blit(press_twice_surface, (press_twice_x, press_twice_y))

            # Render the options
            for i, option in enumerate(self.options):
                x_pos = self.screen.get_width() // 2
                y_pos = 220 + i * 100
                option_surface = self.font_options.render(option, True, (255, 255, 255))
                option_rect = option_surface.get_rect(center=(x_pos, y_pos))
                pygame.draw.rect(self.screen, self.colors[i], option_rect.inflate(20, 20), 4)

                if i == self.selected_index:
                    pygame.draw.rect(self.screen, (255, 255, 255), option_rect.inflate(30, 30), 3)

                self.render_text_with_shadow(option, self.font_options, option_rect.x, option_rect.y, (255, 255, 255))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        print(f"You selected: {self.options[self.selected_index]}")
                        running = False  # This will allow the choice to register immediately

        return self.selected_index

    def display_outcome_screen(self, choice_index,interface_callback):
        self.screen.fill((0, 0, 0))  # Fill screen with black before displaying video
        pygame.display.flip()  # Update screen to show black before video
        self.play_video(choice_index)
        self.display_final_end_screen(interface_callback)

    def display_final_end_screen(self,interface_callback):
        """Show the final end screen with an appealing effect."""
        gradient_surface = pygame.Surface(self.screen.get_size())
        for i in range(self.screen.get_height()):
            color = (i * 255 // self.screen.get_height(), 0, 255 - i * 255 // self.screen.get_height())
            pygame.draw.line(gradient_surface, color, (0, i), (self.screen.get_width(), i))

        fade_surface = pygame.Surface(self.screen.get_size())
        fade_surface.fill((0, 0, 0))

        clock = pygame.time.Clock()
        for alpha in range(0, 256, 5):  # Gradual fade in
            fade_surface.set_alpha(255 - alpha)
            self.screen.blit(gradient_surface, (0, 0))
            self.screen.blit(fade_surface, (0, 0))

            text = "Thank You for Playing"
            pulsate_size = 60 + (10 * pygame.time.get_ticks() % 1000 // 500)
            font = pygame.font.Font(None, pulsate_size)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(30)

        pygame.time.wait(3000)  # Hold the final screen for 3 seconds
        interface_callback()


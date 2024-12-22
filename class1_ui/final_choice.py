import pygame
from config import *
class FinalChoice:
    def __init__(self, screen, player):
        self.screen = screen
        self.character_type = player.selected_character  # Character type: "girl" or "boy"
        self.font_title = pygame.font.Font(None, 80)  # Slightly larger, bolded title font
        self.font_options = pygame.font.Font(None, 48)  # Font for options
        self.font_subtext = pygame.font.Font(None, 40)  # Subtext font
        self.font_outcome = pygame.font.Font(None, 60)  # Font for outcome screens
        self.options = [
            "Option 1: Save humanity",
            "Option 2: Keep the elixir for yourself",
            "Option 3: Accept humanity’s fate",
        ]
        self.colors = [(0, 255, 0), (255, 165, 0), (255, 0, 0)]  # Green, Orange, Red for outlines
        self.selected_index = 0  # Track which option is selected

    def render_text_with_shadow(self, text, font, x, y, color, shadow_offset=2):
        """
        Renders text with a shadow for depth.
        """
        # Shadow text
        shadow = font.render(text, True, (50, 50, 50))  # Shadow is dark gray
        self.screen.blit(shadow, (x + shadow_offset, y + shadow_offset))

        # Main text
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))

    def display_choice_screen(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Black background

            # Render title with shadow
            title_surface = self.font_title.render("Make your choice", True, (255, 255, 255))
            title_x = self.screen.get_width() // 2 - title_surface.get_width() // 2
            title_y = 50
            self.render_text_with_shadow("Make your choice", self.font_title, title_x, title_y, (255, 255, 255))

            # Render subtitle with shadow
            subtext = "Live with the consequences"
            subtext_surface = self.font_subtext.render(subtext, True, (255, 255, 255))
            subtext_x = self.screen.get_width() // 2 - subtext_surface.get_width() // 2
            subtext_y = 130
            self.render_text_with_shadow(subtext, self.font_subtext, subtext_x, subtext_y, (200, 200, 200))

            # Display each option with outlined boxes
            for i, option in enumerate(self.options):
                x_pos = self.screen.get_width() // 2
                y_pos = 220 + i * 100

                # Render option text
                option_surface = self.font_options.render(option, True, (255, 255, 255))
                option_rect = option_surface.get_rect(center=(x_pos, y_pos))

                # Draw colored outline for each option
                pygame.draw.rect(self.screen, self.colors[i], option_rect.inflate(20, 20), 4)

                # Highlight the selected option with a glowing white outline
                if i == self.selected_index:
                    pygame.draw.rect(self.screen, (255, 255, 255), option_rect.inflate(30, 30), 3)

                # Render text with shadow for options
                self.render_text_with_shadow(option, self.font_options, option_rect.x, option_rect.y, (255, 255, 255))

            pygame.display.flip()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:  # Move selection up
                        self.selected_index = (self.selected_index - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:  # Move selection down
                        self.selected_index = (self.selected_index + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:  # Confirm selection
                        print(f"You selected: {self.options[self.selected_index]}")
                        running = False

        return self.selected_index  # Return the chosen option index

    def display_outcome_screen(self, choice_index):
        """
        Display a new screen based on the character type and selected choice.
        """
        outcomes = {
            "girl": [
                "You, the compassionate girl, chose to save humanity.",
                "The girl keeps the elixir, seeking immortality.",
                "The girl accepts humanity’s fate with grace.",
            ],
            "boy": [
                "You, the courageous boy, chose to save humanity.",
                "The boy hoards the elixir, thinking only of himself.",
                "The boy accepts humanity’s fate with resolve.",
            ],
        }
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Black background

            # Render outcome text
            outcome_text = outcomes.get(self.character_type, ["Unknown outcome"])[choice_index]
            outcome_surface = self.font_outcome.render(outcome_text, True, (255, 255, 255))
            outcome_x = self.screen.get_width() // 2 - outcome_surface.get_width() // 2
            outcome_y = self.screen.get_height() // 2 - outcome_surface.get_height() // 2
            self.render_text_with_shadow(outcome_text, self.font_outcome, outcome_x, outcome_y, (255, 255, 255))

            # Apply brightness and sound settings dynamically
            apply_brightness_and_sound(screen)

            pygame.display.flip()

            # Handle events (press any key to exit)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    running = False  # Exit the outcome screen







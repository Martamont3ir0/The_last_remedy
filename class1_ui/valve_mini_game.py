import pygame
from interactive_object import InteractiveObject
from config import *

class Valve(InteractiveObject):
    def __init__(self, target_pressure):
        super().__init__(140,380,'img/valve.png',True,(120,120))
        self.pressure = 50  # Starting pressure
        self.target_pressure = target_pressure

    def adjust_pressure(self, increase, amount):
        if increase:
            self.pressure = min(self.pressure + amount, 200)
        else:
            self.pressure = max(self.pressure - amount, 0)

    def is_puzzle_solved(self):
        return self.pressure == self.target_pressure


class ValveMiniGame:
    def __init__(self, valve, background_path):
        self.valve = valve
        try:
            self.background = pygame.image.load('img/valve_minigame.jpeg')
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            raise
        self.font = pygame.font.Font(None, 48)
        self.solved_time = None  # Track when the puzzle is solved

        # Set up the pressure bar dimensions and position
        self.bar_width = 200
        self.bar_height = 20
        self.bar_x = 260
        self.bar_y = 250
        self.adjustment_rate = 0.5  # Change rate of pressure

    def render_outlined_text(self, screen, text, font, color, outline_color, pos):
        """Render text with an outline effect."""
        x, y = pos
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]  # Offsets for the outline
        for ox, oy in offsets:
            outline_surface = font.render(text, True, outline_color)
            screen.blit(outline_surface, (x + ox, y + oy))
        main_surface = font.render(text, True, color)
        screen.blit(main_surface, (x, y))

    def run(self, screen, clock):
        running = True
        puzzle_solved = False

        while running:
            # Draw the background image
            screen.blit(self.background, (0, 0))

            if not puzzle_solved:
                # Handle key presses to adjust the pressure
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.valve.adjust_pressure(increase=True, amount=self.adjustment_rate)
                elif keys[pygame.K_DOWN]:
                    self.valve.adjust_pressure(increase=False, amount=self.adjustment_rate)

                # Draw the target pressure indicator with outline
                target_text = f"    Target Pressure: {self.valve.target_pressure}"
                self.render_outlined_text(
                    screen, target_text, self.font, (255, 0, 0), (255, 255, 255), (170, 150)
                )

                # Show the current pressure
                current_pressure_text = f"Current Pressure: {int(self.valve.pressure)}"
                current_color = (
                    (0, 255, 0) if self.valve.is_puzzle_solved() else (255, 0, 0)
                )
                current_pressure_render = self.font.render(current_pressure_text, True, current_color)
                screen_center_x = screen.get_width() // 2
                screen_center_y = screen.get_height() // 2
                screen.blit(
                    current_pressure_render,
                    (screen_center_x - current_pressure_render.get_width() // 2, screen_center_y + 100),
                )

                # Check if the puzzle is solved
                if self.valve.is_puzzle_solved():
                    puzzle_solved = True
                    self.solved_time = pygame.time.get_ticks()  # Store the current time

                # Draw the pressure bar container
                pygame.draw.rect(
                    screen, (255, 255, 255), (self.bar_x, self.bar_y, self.bar_width, self.bar_height), 2
                )

                # Draw the pressure bar proportionate to the valve's pressure
                red_bar_width = (self.valve.pressure / 200) * self.bar_width
                pygame.draw.rect(screen, (255, 0, 0), (self.bar_x, self.bar_y, red_bar_width, self.bar_height))

            else:
                # Puzzle solved state
                screen.fill((0, 0, 0))  # Black screen
                solved_text = self.font.render("Pressure corrected!", True, (0, 255, 0))
                screen_center_x = screen.get_width() // 2
                screen_center_y = screen.get_height() // 2
                screen.blit(
                    solved_text,
                    (screen_center_x - solved_text.get_width() // 2, screen_center_y - solved_text.get_height() // 2),
                )

                # Exit the mini-game after 2 seconds
                if pygame.time.get_ticks() - self.solved_time >= 2000:
                    return "solved"

            # Event handling for quitting or exiting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Escape key to quit mini-game
                        running = False

            # Apply brightness and sound settings dynamically
            apply_brightness_and_sound(screen)
            pygame.display.flip()
            clock.tick(60)

        return "quit"












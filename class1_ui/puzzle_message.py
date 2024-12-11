import pygame
from game import *
from config import resolution

def show_balloon(screen,background):

   height = background.get_height()
   speed = 10
   start_y = -100
   end_y = 273

   # Load and scale the balloon image
   balloon_image = pygame.image.load('img/military_drop.png')
   balloon_image = pygame.transform.scale(balloon_image, (300, 300))
   balloon_rect = balloon_image.get_rect(center=(400, start_y))  # Center horizontally
   balloon_moving = True  # Initially moving


   # Draw the balloon
   screen.blit(balloon_image, balloon_rect)
   # Main loop for the balloon dropping
   clock = pygame.time.Clock()
   while balloon_moving:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()

       # Update the balloon's position
       if balloon_rect.y < end_y:
           balloon_rect.y += speed  # Move the balloon down
       else:
           balloon_rect.y = end_y  # Stop at the end position
           balloon_rect.center = (400,437)
           balloon_moving = False  # Stop the loop once it reaches the end

       # Clear the screen
       screen.fill((0, 0, 0))  # Fill with black background
       screen.blit(background,(0,0))

       # Draw the balloon
       screen.blit(balloon_image, balloon_rect)

       # Update the display
       pygame.display.flip()
       clock.tick(30)  # Control the frame rate

       # Update the display
       pygame.display.flip()
       clock.tick(30) # Control the frame rate


def puzzle_message(background,player):
   screen = pygame.display.set_mode(resolution)
   # Call the balloon function to show the balloon dropping
   show_balloon(screen,background)  # Adjust the image path and speed
   user_info(screen,player,False)



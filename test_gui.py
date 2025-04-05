#!/usr/bin/env python3
import pygame

pygame.init()

screen = pygame.display.set_mode((1300, 1300))
pygame.display.set_caption("Inspect Football Image")

# Load your image
football_img = pygame.image.load("assets/football.png").convert_alpha()
football_rect = football_img.get_rect()

#football_img = pygame.transform.scale(football_img, (70, 70))


print(football_img)
print(football_img.get_size())
print(football_rect)

# Find the actual bounds of the non-transparent pixels
width, height = football_img.get_size()
min_x, max_x, min_y, max_y = width, 0, height, 0

for x in range(width):
    for y in range(height):
        color = football_img.get_at((x, y))
        if color[3] > 0:  # If pixel is not fully transparent
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

# Draw the actual content bounds in a different color
pygame.draw.rect(screen, (0, 255, 255), (min_x, min_y, max_x - min_x, max_y - min_y), 2)

# Print the padding amounts
print(f"Left padding: {min_x}px")
print(f"Right padding: {width - max_x}px")
print(f"Top padding: {min_y}px")
print(f"Bottom padding: {height - max_y}px")

running = True
while running:
    screen.fill((30, 30, 30))

    # Draw image at (100, 100)
    screen.blit(football_img, (0, 0))

    # Draw bounding box
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, football_rect.width, football_rect.height), 2)

    # Draw centerline
    pygame.draw.line(screen, (0, 255, 0), (football_rect.width/2, 0), (football_rect.width/2, football_rect.height), 1)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
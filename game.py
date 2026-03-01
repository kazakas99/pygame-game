import pygame

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pygame.display.set_caption('Game')
running = True

font = pygame.font.Font('font/Pixeltype.ttf', 50)
text = font.render('My Game', False, 'Black')

background = pygame.image.load('background/background.jpg').convert()
background = pygame.transform.scale(background, screen.get_size())

player = pygame.image.load('characters/character.png').convert_alpha()
player = pygame.transform.scale(player, (int(player.get_width() * 0.25), int(player.get_height() * 0.25)))
player_rect = player.get_rect(topleft = (0, 203))

snail = pygame.image.load('characters/snail.png').convert_alpha()
snail = pygame.transform.scale(snail, (int(snail.get_width() * 0.45), int(snail.get_height() * 0.45)))
snail_rect = snail.get_rect(topright = (800, 210))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)

    # RENDER YOUR GAME HERE
    screen.blit(background, (0, 0))
    
    screen.blit(text, (300, 50))

    screen.blit(player, player_rect)

    snail_rect.x -= 4
    if snail_rect.right >= 0:
        snail_rect.left = 800
    screen.blit(snail, (snail_rect))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
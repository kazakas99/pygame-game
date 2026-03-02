import pygame

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
pygame.display.set_caption('Game')
running = True
game_active = True
start_time = 0
final_score = 0

font = pygame.font.Font('font/Pixeltype.ttf', 50)
text = font.render('GAME OVER', False, 'Black')
text_rect = text.get_rect(center=(400, 200))

background = pygame.image.load('background/background.jpg').convert()
background = pygame.transform.scale(background, screen.get_size())

player = pygame.image.load('characters/character.png').convert_alpha()
player = pygame.transform.scale(
    player, (int(player.get_width() * 0.25), int(player.get_height() * 0.25)))
player_rect = player.get_rect(topleft=(0, 203))
player_mask = pygame.mask.from_surface(player)

snail = pygame.image.load('characters/snail.png').convert_alpha()
snail = pygame.transform.scale(
    snail, (int(snail.get_width() * 0.45), int(snail.get_height() * 0.45)))
snail_rect = snail.get_rect(topright=(800, 210))
snail_mask = pygame.mask.from_surface(snail)
snail_speed = 4
player_gravity = -20

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 328:
                player_gravity = -20

    screen.blit(background, (0, 0))

    if game_active:
        screen.blit(player, player_rect)
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 328:
            player_rect.bottom = 328

        snail_rect.x -= snail_speed
        if snail_rect.right <= 0:
            snail_rect.left = 800
            snail_speed += 1
            if snail_speed >= 12:
                snail_speed = 12

        screen.blit(snail, snail_rect)

        offset = (snail_rect.x - player_rect.x, snail_rect.y - player_rect.y)
        if player_mask.overlap(snail_mask, offset):
            final_score = (pygame.time.get_ticks() - start_time) // 1000
            game_active = False

        display_score()
    else:
        screen.blit(text, text_rect)
        score_text = font.render(f'Your score is: {final_score}', False, 'Black')
        score_text_rect = score_text.get_rect(center=(400, 250))
        screen.blit(score_text, score_text_rect)
        

    pygame.display.update()
    clock.tick(60)

pygame.quit()

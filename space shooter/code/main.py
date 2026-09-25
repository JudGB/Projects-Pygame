import pygame 
import random 
from os.path import join

# Inicializa o pygame
pygame.init()

win_width = 1080
win_height = 720
display = pygame.display.set_mode([win_width, win_height])
pygame.display.set_caption("Space Shooter")

# Configuração de caminhos usando o join (Boa prática para todas as imagens)
path_images = join('Projects-Pygame', 'space shooter', 'images')

# Ícone da Janela
icon_surf = pygame.image.load(join(path_images, 'meteor.png')).convert_alpha()
pygame.display.set_icon(icon_surf)

# Clock / FPS
clock = pygame.time.Clock()

# Superfícies e Posições (Usando convert/convert_alpha para melhor performance)
player_surf = pygame.image.load(join(path_images, 'player.png')).convert_alpha()
# Alterado para get_rect padrão para funcionar perfeitamente com move_ip
player_rect = player_surf.get_frect(center = (win_width / 2, win_height / 2))
player_direct = pygame.math.Vector2()
player_spd = 300

star_surf = pygame.image.load(join(path_images, 'star.png')).convert_alpha()
star_pos = [(random.randint(0, win_width), random.randint(0, win_height)) for _ in range(20)]

meteor_surf = pygame.image.load(join(path_images, 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_rect(center = (win_width / 2, win_height / 2))

laser_surf = pygame.image.load(join(path_images, 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_rect(bottomleft = (20, 710))


running = True
while running:
    dt = clock.tick() / 1000
    
    # Loop de Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    player_direct.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    player_direct.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    player_direct = player_direct.normalize() if player_direct else player_direct

    player_rect.center += player_direct * player_spd * dt 

    print((player_direct * player_spd).magnitude())
    
    laser_rect.y -= 0.5
    
    # Desenho na Tela
    display.fill("gray25")

    # Desenha as estrelas
    for pos in star_pos:
        display.blit(star_surf, pos)

    # Desenha os elementos do jogo
    display.blit(player_surf, player_rect)
    display.blit(meteor_surf, meteor_rect)
    display.blit(laser_surf, laser_rect)
    
    pygame.display.flip()

pygame.quit()

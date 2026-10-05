import pygame 
import random 
from os.path import join

# Inicializa o pygame
pygame.init()

# Configuração de caminhos usando o join (Boa prática para todas as imagens)
path_images = join('Projects-Pygame', 'space shooter', 'images')

#display tela
win_width = 1080
win_height = 720
display = pygame.display.set_mode([win_width, win_height])
pygame.display.set_caption("Space Shooter")
# Ícone da Janela
icon_surf = pygame.image.load(join(path_images, 'meteor.png')).convert_alpha()
pygame.display.set_icon(icon_surf)

# Clock / FPS
clock = pygame.time.Clock()

#classe do laser
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(join(path_images, 'laser.png')).convert_alpha()
        self.rect = pygame.FRect(pos.x, pos.y, 10, 40)  # Define o tamanho do laser
        self.speed = 600

    def update(self, dt):
        self.rect.y -= 1 * self.speed * dt
        if self.rect.bottom < 0:
            self.kill()  # Remove o laser quando sair da tela

#classe do meteoro
class Meteor(pygame.sprite.Sprite):
    def __init__(self, win_width):
        super().__init__()
        self.image = pygame.image.load(join(path_images, 'meteor.png')).convert_alpha()
        x_posicion = random.randint(20, win_width - 85)
        self.rect = pygame.FRect(x_posicion, -100, 100, 85)  # Define o tamanho do meteor
        self.speed = 400

    def update(self, dt):
        self.rect.y += 0.5 *self.speed * dt
        if self.rect.top > win_width:
            self.kill()  # Remove o meteor quando sair da tela

#classe do coletável
class Collectible(pygame.sprite.Sprite):
    def __init__(self, win_width, win_height):
        super().__init__()

        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

        pygame.draw.circle(
            self.image,
            (255, 245, 180),
            (10, 10),
            8
        )

        x_posicion = random.randint(20, win_width - 20)
        y_posicion = random.randint(20, win_height - 20)

        self.rect = self.image.get_frect(
            center=(x_posicion, y_posicion)
        )

    def update(self, dt):
        pass

#font do texto
fonte = pygame.font.Font(None, 40)

# Superfícies e Posições (Usando convert/convert_alpha para melhor performance)
player_surf = pygame.image.load(join(path_images, 'player.png')).convert_alpha()
# Alterado para get_rect padrão para funcionar perfeitamente com move_ip
player_rect = player_surf.get_frect(center = (win_width / 2, win_height / 2))
player_direct = pygame.math.Vector2()
player_spd = 300

star_surf = pygame.image.load(join(path_images, 'star.png')).convert_alpha()
star_pos = [(random.randint(0, win_width), random.randint(0, win_height)) for _ in range(20)]

running = True
cheating_ = False #liga as colisões para teste

grupo_lasers = pygame.sprite.Group()
grupo_pedras = pygame.sprite.Group()
chance_spawn_pedra = 0.004
grupo_colleta = pygame.sprite.Group()
pontos = 0
for _ in range(10):
    novo_coletavel = Collectible(win_width, win_height)
    grupo_colleta.add(novo_coletavel)

tempo_respawn_laser = 0

while running:
    dt = clock.tick() / 1000
    tempo_atual = pygame.time.get_ticks()
    
    # Loop de Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if tempo_atual - tempo_respawn_laser > 1000:
                    # Exemplo de posição simulada do player
                    pos_player = pygame.math.Vector2(
                        player_rect.centerx - 20,
                        player_rect.top - 40
                    )
                    # Cria o objeto e adiciona direto no grupo
                    novo_laser = Laser(pos_player)
                    grupo_lasers.add(novo_laser)
                    tempo_respawn_laser = tempo_atual
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                cheating_ = not cheating_


    keys = pygame.key.get_pressed()

    player_direct.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
    player_direct.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

    #NORMALIZA o aumento que a na tangente
    #pq quando vai para os lados é 300, mas e quando é na diagonal?
    #nessa hora usamos isso para "normalizar" a diferença que há
    player_direct = player_direct.normalize() if player_direct else player_direct

    #Movimenta o player
    player_rect.center += player_direct * player_spd * dt 

    player_rect.clamp_ip(display.get_rect())

    # Desenho na Tela
    display.fill("gray25")

    # Desenha as estrelas
    for pos in star_pos:
        display.blit(star_surf, pos)

    # Desenha os elementos do jogo
    display.blit(player_surf, player_rect)

    # Texto da pontuação
    texto = fonte.render(f"Pontos: {pontos}", True, "white")
    display.blit(texto, (20, 20))

    # Criando pedras de tempos em tempos (exemplo simples)
    if random.random() < chance_spawn_pedra: 
        nova_pedra = Meteor(win_width)
        grupo_pedras.add(nova_pedra)

    # --- O PODER DOS GRUPOS COMEÇA AQUI ---

    # 1. Atualiza a física de TODOS os objetos de uma vez só passando o 'dt'
    grupo_lasers.update(dt)
    grupo_pedras.update(dt)

    # 2. RESOLVE TODAS AS COLISÕES EM UMA LINHA SEM BUGAR!
    # True (1º): Deleta o laser que colidiu
    # True (2º): Deleta a pedra que colidiu
    pygame.sprite.groupcollide(grupo_lasers, grupo_pedras, True, True) 

    # 3. Desenha tudo na tela (O Pygame renderiza de forma otimizada internamente)
    grupo_lasers.draw(display)
    grupo_pedras.draw(display)
    grupo_colleta.draw(display)

    if cheating_:
        for laser in grupo_lasers:
            pygame.draw.rect(display, "red", laser.rect, 2)

        for pedra in grupo_pedras:
            pygame.draw.rect(display, "green", pedra.rect, 2)


    #colisão com o ponto e o player
    for coletavel in grupo_colleta:
        if player_rect.colliderect(coletavel.rect):
            coletavel.kill()
            pontos += 1


    def resetar_coletaveis():
        grupo_colleta.empty()

        for _ in range(10):
            novo_coletavel = Collectible(win_width, win_height)
            grupo_colleta.add(novo_coletavel)

    def resetar_pedras():
        grupo_pedras.empty()

        if random.random() < chance_spawn_pedra: 
            nova_pedra = Meteor(win_width)
            grupo_pedras.add(nova_pedra)
        

    # colisão com o meteor e o player
    for meteor in grupo_pedras:

        if player_rect.colliderect(meteor.rect) or pontos >= 10:

            # reseta a posição do player
            player_rect.center = (win_width / 2, win_height / 2)
            resetar_coletaveis()
            resetar_pedras()
            pontos = 0

            
                
    print(f"Pontos: {pontos}")

    pygame.display.flip()

clock.tick(60)
pygame.quit()

import pygame
import random

pygame.init()

sonido_fondo = pygame.mixer.Sound("music.mp3")

# Dimensiones de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Cargamos las imagenes de los objetos
player_ship = pygame.image.load('player_ship.png')
makeup = pygame.image.load('makeup.png')
enemy = pygame.image.load('cactus.png')
life_image = pygame.image.load('heart.png')  # Asegúrate de que esta imagen esté en el mismo directorio que tu script

player_position = []
enemies = []
life = 0
points = 0
makeups = []
is_game_over = False
is_play = False
paused = False

ENEMIES_DOWN = 0.4
ENEMIES_UP = 1.2

MAKEUPS_DOWN = 0.3
MAKEUPS_UP = 0.8

max_points = 0


def generate_enemies(number):
    global enemies, width, enemy
    number_enemies = int(number)
    for i in range(2 * number_enemies):
        enemies_position = [random.randrange(width), - enemy.get_height()]
        enemies_speed = random.uniform(ENEMIES_DOWN, ENEMIES_UP)
        enemies.append((enemies_position, enemies_speed))


def generate_makeup(number):
    global makeups, width, makeup
    number_makeups = int(number)
    for i in range(5 * number_makeups):
        makeups_position = [random.randrange(width), -makeup.get_height()]
        makeups_speed = random.uniform(MAKEUPS_DOWN, MAKEUPS_UP)
        makeups.append((makeups_position, makeups_speed))


def show_start_screen():
    start_font = pygame.font.Font(None, 36)
    start_text = start_font.render('Presiona la tecla ESPACIO para comenzar', True, (255, 255, 255))  # Blanco
    controls_font = pygame.font.Font(None, 24)
    controls_text = controls_font.render('Controls:', True, (255, 255, 255))  # Blanco
    left_text = controls_font.render('Flecha izquierda <- Mueve a la izquierda', True, (255, 255, 255))  # Blanco
    right_text = controls_font.render('Flecha derecha -> Mueve a la derecha', True, (255, 255, 255))  # Blanco
    pause_text = controls_font.render('P - Pausar el juego', True, (255, 255, 255))  # Blanco
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Si la barra espaciadora se presiona
                return  # Salir del bucle y comenzar el juego
        # Limpiar la pantalla y dibujar el mensaje
        screen.fill((0, 0, 0))
        screen.blit(start_text, (
            (width - start_text.get_width()) // 2, (height - start_text.get_height()) // 2))  # Centrar el texto
        screen.blit(controls_text, (
            (width - controls_text.get_width()) // 2,
            (height - controls_text.get_height()) // 2 + 50))  # Centrar el texto de los controles
        screen.blit(left_text, (
            (width - left_text.get_width()) // 2,
            (height - left_text.get_height()) // 2 + 80))  # Centrar el texto de mover a la izquierda
        screen.blit(right_text, (
            (width - right_text.get_width()) // 2,
            (height - right_text.get_height()) // 2 + 110))  # Centrar el texto de mover a la derecha
        screen.blit(pause_text, (
            (width - pause_text.get_width()) // 2, (height - pause_text.get_height()) // 2 + 140))
        pygame.display.flip()


def draw_score(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render('Puntuación: ' + str(score), True, (255, 255, 255))  # Blanco
    screen.blit(text, (10, 10))  # Posición de la puntuación en la pantalla


def draw_lifes(screen, avaliableLifes):
    for i in range(avaliableLifes):
        screen.blit(life_image, (10 + i * life_image.get_width(), 40))  # Asegúrate de que las vidas no se solapen


def reset_game():
    # Reestablece todas las variables y el estado del juego a su estado inicial
    sonido_fondo.play()

    global player_position, enemies, life, points, makeups, is_game_over

    is_game_over = False

    player_position = [width / 2, height - player_ship.get_height()]

    # Crear una lista de objetos
    makeups = []
    for i in range(20):
        makeups_position = [random.randrange(width), -makeup.get_height()]
        makeups_speed = random.uniform(MAKEUPS_DOWN, MAKEUPS_UP)
        makeups.append((makeups_position, makeups_speed))

    enemies = []
    for i in range(8):
        enemies_position = [random.randrange(width), - enemy.get_height()]
        enemies_speed = random.uniform(ENEMIES_DOWN, ENEMIES_UP)
        enemies.append((enemies_position, enemies_speed))
    life = 3
    points = 0


show_start_screen()
reset_game()
count = 0
while True:
    count += 1
    for event in pygame.event.get():
        if is_game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                reset_game()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if is_game_over:
                if event.key == pygame.K_r:
                    sonido_fondo.stop()
                    reset_game()
            else:
                if event.key == pygame.K_p:  # Si se presiona la tecla "P"
                    paused = not paused  # Cambiar el estado de pausa
                    if not paused:
                        sonido_fondo.play()

    if not paused:
        if life != 0:
            print(count)
            if count % 1500 == 0:
                generate_enemies(count / 1500)
                generate_makeup(count / 1500)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:  # Si la tecla izquierda está pulsada
                player_position[0] -= 0.75  # Mueve la nave a la izquierda
            if keys[pygame.K_RIGHT]:  # Si la tecla derecha está pulsada
                player_position[0] += 0.75  # Mueve la nave a la derecha

            # Asegúrate de que la nave no se salga de la pantalla
            if player_position[0] < 0:
                player_position[0] = 0
            if player_position[0] > width - player_ship.get_width():
                player_position[0] = width - player_ship.get_width()

            # Mover enemigos
            for enemiesbad in enemies:
                enemiesbad[0][1] += enemiesbad[1]

            for makeup_prize in makeups:
                makeup_prize[0][1] += makeup_prize[
                    1]  # Incrementa la posición y (hacia abajo) del enemigo según su velocidad

            # Detectar colisiones entre la nave del jugador y los enemigos
            for makeup_prize in makeups:
                # Comprueba si la nave del jugador y el enemigo se solapan
                if (player_position[0] < makeup_prize[0][0] + makeup.get_width()
                        and player_position[0] + player_ship.get_width() > makeup_prize[0][0]
                        and player_position[1] < makeup_prize[0][1] + makeup.get_height()
                        and player_position[1] + player_ship.get_height() > makeup_prize[0][1]):
                    # Si hay una colisión, elimina el enemigo
                    makeups.remove(makeup_prize)
                    points += 50
                    print(points)
                    break

            for enemiesbad in enemies:
                # Comprueba si la nave del jugador y el enemigo se solapan
                if (player_position[0] < enemiesbad[0][0] + enemy.get_width()
                        and player_position[0] + player_ship.get_width() > enemiesbad[0][0]
                        and player_position[1] < enemiesbad[0][1] + enemy.get_height()
                        and player_position[1] + player_ship.get_height() > enemiesbad[0][1]):
                    # Si hay una colisión, elimina el enemigo
                    enemies.remove(enemiesbad)
                    life = life - 1
                    break

            for makeup_prize in makeups:
                screen.blit(makeup, makeup_prize[0])

            for enemiesbad in enemies:
                screen.blit(enemy, enemiesbad[0])
            # Dibuja la nave en su nueva posición
            screen.blit(player_ship, player_position)

        else:
            is_game_over = True

            if points > max_points:
                max_points = points

            # Si se debe mostrar la ventana emergente, solo dibuja la ventana emergente
            popup = pygame.Surface((width / 2, height / 2))
            popup.fill((155, 58, 58))  # llenar con rojo

            font = pygame.font.Font(None, 36)
            text = font.render('Game Over :(', True, (255, 255, 255))  # Blanco sobre rojo

            # Calcula la posición del texto para centrarlo en la ventana emergente
            text_pos = ((width / 2 - text.get_width()) / 2, (height / 2 - text.get_height()) / 2)
            popup.blit(text, text_pos)
            screen.blit(popup, (width / 4, height / 4))
            sonido_fondo.stop()

            restart_font = pygame.font.Font(None, 24)
            restart_text = restart_font.render('Presiona R para reiniciar!', True, (255, 255, 255))  # Blanco

            # Calcular la posición del texto para que esté debajo de la ventana emergente
            restart_text_pos = (
                (width - restart_text.get_width()) / 2, (height / 2 - text.get_height()) / 2 + popup.get_height() + 20)
            screen.blit(restart_text, restart_text_pos)

            points_font = pygame.font.Font(None, 18)
            points_text = points_font.render('Mejor puntaje: ' + str(max_points), True, (255, 255, 255))  # Blanco

            points_text_pos = (
                (width - points_text.get_width()) / 2, restart_text_pos[1] + restart_text.get_height() + 10)

            screen.blit(points_text, points_text_pos)

        draw_score(screen, points)
        draw_lifes(screen, life)
        pygame.display.flip()
        screen.fill((0, 0, 0))  # Limpiar la pantalla para el próximo frame
    else:

        pause_font = pygame.font.Font(None, 36)
        pause_text = pause_font.render('Pausa', True, (255, 255, 255))  # Blanco
        screen.blit(pause_text, (
            (width - pause_text.get_width()) // 2, (height - pause_text.get_height()) // 2))  # Centrar el texto
        sonido_fondo.stop()
        pygame.display.flip()

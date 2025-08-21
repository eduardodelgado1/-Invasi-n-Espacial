import pygame
import random
import math
from pygame import mixer

pygame.init()

# Definir tamaño de la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título e icono + imagen de fondo

pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo.jpg")

# agregar música fondo

mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.1)
mixer.music.play(-1)

#---------------------------------------------------------------
# agregar al jugador

jugador_img= pygame.image.load("cohete (1).png")

# varaibles del jugador para desplazarse

jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0

#-----------------------------------------------------------
# agregar al enemigo

enemigo_img = []


# varaibles del jugador para desplazarse
# se podria hacer con clase también

enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 6

for enem in range(cantidad_enemigos):
    enemigo_img.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.4)
    enemigo_y_cambio.append(50)

#------------------------------------------------------------

# agregar a la bala

bala_img= pygame.image.load("bala.png")

# varaibles de la bala para desplazarse

bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# ---------------------------------------------------------
# Puntaje

puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf",32)
texto_x = 10
texto_y = 10

# funcion mstrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje {puntaje}", True, (255,255,255))
    pantalla.blit(texto,(x,y))

#------------------------------------------------------------
# texto final

fuente_final = pygame.font.Font("freesansbold.ttf",40)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))


#------------------------------------------------------------

# funcion de jugador
def jugador(x,y):
    pantalla.blit(jugador_img,(x,y))

#------------------------------------------------------------

# funcion de enemigo
def enemigo(x,y,e):
    pantalla.blit(enemigo_img[e],(x,y))

#-----------------------------------------------------------
# función disparar bala

def disparar_bala(x, y):
    global bala_visible
    bala_visible =True
    pantalla.blit(bala_img, (x + 16,y +10))

#-----------------------------------------------------------
# función establecer la colición nave vs bala

def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1,2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False

#--------------------------------------------------------------
# Para mantener la pantalla activa
se_ejecuta = True
while se_ejecuta:


    pantalla.blit(fondo, (0,0))
    
    # Iterar los eventos del juego
    for evento in pygame.event.get():
        # Evento para cerrar el juego
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento si alguien presiona una tecla 
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.7
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.7
            if evento.key == pygame.K_SPACE:

                sonido_bala=mixer.Sound("disparo.mp3")
                sonido_bala.set_volume(0.1)  # 30% del volumen original
                sonido_bala.play()
                
                if not bala_visible:  # Solo dispara si no hay bala activa
                    bala_x = jugador_x
                    bala_y = jugador_y
                    bala_visible = True

        

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0


    #------------------------------------------------------------------------------
    # Modificar ubicación del jugador
    jugador_x += jugador_x_cambio

    # mantener siempre a jugador dentro y solo llega hasta los vordes

    if jugador_x <= 0:
        jugador_x =0
    if jugador_x >= 736:
        jugador_x =736
    #--------------------------------------------------------------------------

     # Modificar cantidad y ubicación del enemigo
    for enem in range(cantidad_enemigos):

        # Terminar juego cuando enemigo llega abajo
        if enemigo_y[enem] > 500:
            for n in range(cantidad_enemigos):
                enemigo_y[n] = 1000
            texto_final()
            break

        enemigo_x[enem] += enemigo_x_cambio[enem]

        if enemigo_x[enem] <= 0:
            enemigo_x_cambio[enem] = 0.7
            enemigo_y[enem] += enemigo_y_cambio[enem]
        elif enemigo_x[enem] >= 736:
            enemigo_x_cambio[enem] = -0.7
            enemigo_y[enem] += enemigo_y_cambio[enem]

        # Verificar colisión
        if hay_colision(enemigo_x[enem], enemigo_y[enem], bala_x, bala_y):
            sonido_colición = mixer.Sound("Golpe.mp3")
            sonido_colición.play()
            bala_y = jugador_y
            bala_visible = False
            puntaje += 100
            
            enemigo_x[enem] = random.randint(0, 736)
            enemigo_y[enem] = random.randint(50, 200)

        enemigo(enemigo_x[enem], enemigo_y[enem], enem)

    #-------------------------------------------------------------------
    # Movimiento de la bala

     # la bala desaparece al tocar techo
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

     # la bala se dispara de la punta de la nave
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio
        if bala_y <= -64:
            bala_visible = False

   

    #--------------------------------------------------------------------
    jugador(jugador_x, jugador_y)
    
    mostrar_puntaje(texto_x,texto_y)

    # Actualizar
    pygame.display.update()



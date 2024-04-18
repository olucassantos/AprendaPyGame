import pygame
#iniciar o pygame (motor)
pygame.init()
# configuraçao da tela
tamanho = (300,600)
# cria a tela e define o tamanho
tela = pygame.display.set_mode(tamanho)
# define o titulo da tela
pygame.display.set_caption("Pinga")
#criar um relogio para controlar o FPS
relogio = pygame.time.Clock()
#criar um circulo para mostrar na tela
cor = (100,0,0)
posicao = [150,300]
raio = 50
direcao = pygame.Vector2(1, 1)

while True:
    # pega os eventos que estao acontecendo
    for evento in pygame.event.get():
        print(evento)

        # se o evento for de fechar atela
        if evento.type == pygame.QUIT:
            pygame.quit() #fecha o pygame
            exit() #fecha o programa

    #pinta a tela de branco
    tela.fill((255,255,255))
    #cria um circulo para mostrar na tela
    circulo = pygame.draw.circle(tela, cor, posicao, raio)

    # movimenta o circulo para baixo
    posicao[1] += 5 * direcao.y
    # movimenta o circulo para a direita
    posicao[0] += 5 * direcao.x

    # Faz a bola inverter a direção quando chegar na borda
    if posicao[0] + raio >= tamanho[0] or posicao[0] - raio <= 0:
        direcao.x *= -1
    
    if posicao[1] + raio >= tamanho[1] or posicao[1] - raio <= 0:
        direcao.y *= -1

    #atualiza a tela para exibir o que foi desenhado
    pygame.display.update()

    #controla o FPS
    relogio.tick(45)
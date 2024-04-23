import pygame
import random

def geraNovaMusica():
    velocidade = random.randint(1, 5)
    
    if velocidade == 1: duracao = random.randint(50, 70)
    elif velocidade == 2: duracao = random.randint(50, 80)
    elif velocidade == 3: duracao = random.randint(50, 90)
    elif velocidade == 4: duracao = random.randint(50, 100)
    elif velocidade == 5: duracao = random.randint(50, 110)

    listaPassos = []

    for i in range(duracao):
        passo = random.choice(["esquerda", "direita", "cima", "baixo"])
        listaPassos.append(passo)

    return {
        "velocidade": velocidade,
        "duracao": duracao,
        "passos": listaPassos
    }

def criaElementosMusica():
    fonteMusica = pygame.font.SysFont("Arial", 25)
    passos = musica["passos"]
    elementos = []

    for i in range(len(passos)):

        if passos[i] == "esquerda":
            cor = (255, 0, 0)
            seta = fonteMusica.render("←", True, cor)
        elif passos[i] == "direita":
            cor = (0, 255, 0)
            seta = fonteMusica.render("→", True, cor)
        elif passos[i] == "cima":
            cor = (0, 0, 255)
            seta = fonteMusica.render("↑", True, cor)
        elif passos[i] == "baixo":
            cor = (255, 255, 0)
            seta = fonteMusica.render("↓", True, cor)

        elemento = pygame.draw.circle(tela, cor, (150 + ((i + 1) * 80), 40), 30, 4)

        seta_rect = seta.get_rect(center=(elemento.centerx, elemento.centery))
        tela.blit(seta, seta_rect)

        elementos.append({
            "elemento": elemento,
            "seta": seta,
            "cor": cor,
            "seta_rect": seta_rect
        })
    
    return elementos

def movimentaPassos(elementos, musica):
    for elemento in elementos:
        elemento["elemento"].x -= musica['velocidade']
        elemento["seta_rect"].x -= musica['velocidade']

        if elemento["elemento"].x < 0:
            del elemento

    desenhaElementos(elementos)

def desenhaElementos(elementos):
    for elemento in elementos:
        tela.blit(elemento["seta"], elemento["seta_rect"])

pygame.init()
# configuraçao da tela
tamanho = (300,600)
# cria a tela e define o tamanho
tela = pygame.display.set_mode(tamanho)
# define o titulo da tela
pygame.display.set_caption("Crazy Dance")
#criar um relogio para controlar o FPS
relogio = pygame.time.Clock()
#criar um circulo para mostrar na tela

fonteMenu = pygame.font.SysFont(None, 25)
fonteMusica = pygame.font.SysFont(None, 25)

# Variavel para controlar se o jogo começou
jogoComecou = False
musica = None
elementosMusica = []

while True:
    # pega os eventos que estao acontecendo
    for evento in pygame.event.get():
        print(evento)

        # se o evento for de fechar atela
        if evento.type == pygame.QUIT:
            pygame.quit() #fecha o pygame
            exit() #fecha o programa

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not jogoComecou:
                jogoComecou = True
                musica = geraNovaMusica()
                elementosMusica = criaElementosMusica()

    #pinta a tela de branco
    tela.fill((255,255,255))

    if not jogoComecou:
        # desenha o menu
        textoMenu = fonteMenu.render("Pressione espaço para começar...", True, (0, 0, 0))
        tela.blit(textoMenu, (10, 300))

    if jogoComecou:
        # Desenha um circulo para ser o alvo dos passos de dança
        alvo = pygame.draw.circle(tela, (0, 0, 0), (150, 40), 30, 4)

        # Inicia o movimento dos passos
        movimentaPassos(elementosMusica, musica)

    #atualiza a tela para exibir o que foi desenhado
    pygame.display.update()

    #controla o FPS
    relogio.tick(60)
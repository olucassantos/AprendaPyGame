import pygame # Importa a biblioteca Pygame
import random # Importa a biblioteca random (para gerar números aleatórios)

# Cria uma nova bola
def novaBola():
    # Cria um dicionário com as informações da bola
    cores = {
        1: (255, 0, 0),
        2: (0, 255, 0),
        3: (0, 0, 255),
        4: (255, 255, 0),
        5: (255, 0, 255),
        6: (0, 255, 255),
        7: (255, 165, 0),
        8: (0, 0, 0),
        9: (128, 128, 128),
        10: (128, 0, 0),
    }

    velocidade = random.randint(1, 10) # Velocidade aleatória
    cor = cores[velocidade] # Cor de acordo com a velocidade
    tamanho = random.randint(20, 50) # Tamanho aleatório
    vidas = random.randint(1, 10) # Vidas aleatórias

    # Retorna o dicionário com as informações da bola para ser adicionado na lista
    return {
        "posicao": [random.randint(200, 600), random.randint(200, 400)],
        "velocidade": velocidade,
        "cor": cor,
        "tamanho": tamanho,
        "vidas": vidas,
        "direcao": pygame.Vector2(1, 1)
    }

def verificaCliqueBolinhas(posicao, listaBolas):
    global pontuacao # Variável global para alterar a pontuação

    for bola in listaBolas: # Vai verificar bolinha por bolinha
        # Desenha um retangulo temporário para verificar se o click foi dentro da bola
        retanguloTemporario = pygame.draw.circle(
            tela, 
            bola["cor"], 
            bola["posicao"],
            bola["tamanho"]
        )

        # Verifica se o click foi dentro do retangulo
        recebeuClick = retanguloTemporario.collidepoint(posicao)

        # Apaga o retangulo temporário
        del retanguloTemporario

        if recebeuClick: # Se recebeu o click
            bola["vidas"] -= 1

        if bola["vidas"] <= 0: # Se as vidas acabaram
            pontuacao += 1 # Aumenta a pontuação
            listaBolas.remove(bola) # Remove a bola da lista

# Inicializa o Pygame
pygame.init()
# Configurações da tela
tamanho = (800, 600)
# Cria a tela e define o tamanho
tela = pygame.display.set_mode(tamanho)
# Define o título da tela
pygame.display.set_caption("Pinga")

# Criar um relogio para controlar os FPS
relogio = pygame.time.Clock()

# Parametros do circulo
cor = (255, 0, 0)
posicao = [150, 60]
raio = 50
cor_tela = (255, 255, 255)

# Lista de bolas que vão ser desenhadas e movimentadas
listaBolas = []

# Evento para o tempo
novaBolaEvent = pygame.USEREVENT + 1

pontuacao = 0

# Cria uma fonte
fonte = pygame.font.Font(None, 300)
fonteBolinha = pygame.font.Font(None, 15)
fonteGameOver = pygame.font.Font(None, 180)

jogoAcabou = False

# Cria o evento a cada 2 segundos
pygame.time.set_timer(novaBolaEvent, 5000)

# LOOP PRINCIPAL
while True:
    # Pega os eventos que estão acontecendo
    for evento in pygame.event.get():
        if evento.type == novaBolaEvent:
            # Adiciona uma nova bola na lista de bolas
            listaBolas.append(novaBola())

        # Se o evento for de fechar a tela
        if evento.type == pygame.QUIT:
            pygame.quit() # Fecha o Pygame
            exit() # Fecha o programa

        # Verifica se aconteceu o click do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: # Botão esquerdo do mouse
                # Verificar se o click foi dentro de algum circulo
                # Passa a posição do click para a função verificaCliqueBolinha
                verificaCliqueBolinhas(evento.pos, listaBolas)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jogoAcabou = False
                listaBolas = []
                listaBolas.append(novaBola())
                pontuacao = 0

    #########################################

    # Pinta a tela
    tela.fill(cor_tela)

    # Verifica se o jogo acabou
    if len(listaBolas) >= 6: # Se tiver 6 bolas na tela
        jogoAcabou = True
        # Desenha a mensagem de game over
        texto = fonteGameOver.render("Você Perdeu", True, (255, 0, 0))
        texto_rect = texto.get_rect(center=(400, 200))
        tela.blit(texto, texto_rect)

        texto = fonte.render(f"{pontuacao}", True, (0, 0, 0)) # Cria o texto
        texto_rect = texto.get_rect(center=(400, 390)) # Cria um retangulo para o texto
        tela.blit(texto, texto_rect) # Desenha o texto na tela

        texto = fonteBolinha.render("Aperte espaço para recomeçar...", True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(400, 550))
        tela.blit(texto, texto_rect)

    if not jogoAcabou:

        # Desenha a pontuação na tela
        texto = fonte.render(f"{pontuacao}", True, (0, 0, 0)) # Cria o texto
        texto_rect = texto.get_rect(center=(400, 300)) # Cria um retangulo para o texto
        tela.blit(texto, texto_rect) # Desenha o texto na tela

        # Processa a lista de bolas, desenhando e movendo
        for bola in listaBolas:
            # Desenhar a bola na tela
            circulo = pygame.draw.circle(
                tela, 
                bola["cor"], 
                bola["posicao"],
                bola["tamanho"]
            )

            textoBolinha = fonteBolinha.render(f"{bola['vidas']}", True, (0, 0, 0))
            textoBolinhaRect = textoBolinha.get_rect(center=bola["posicao"])
            tela.blit(textoBolinha, textoBolinhaRect)

            # Movimenta a bola com a velocidade e direção
            bola["posicao"][0] += bola["velocidade"] * bola["direcao"].x
            bola["posicao"][1] += bola["velocidade"] * bola["direcao"].y

            # Verifica se a bola bateu no eixo X
            if bola["posicao"][0] >= tamanho[0] - bola["tamanho"]:
                # Reposiciona a bola para não sair da tela
                bola["posicao"][0] = tamanho[0] - bola["tamanho"]
                bola["direcao"].x = -1 # Inverte a direção da bola
            elif bola["posicao"][0] <= bola["tamanho"]:
                # Reposiciona a bola para não sair da tela
                bola["posicao"][0] = bola["tamanho"]
                bola["direcao"].x = 1 # Inverte a direção da bola

            # Verifica se a bola bateu no eixo Y
            if bola["posicao"][1] >= tamanho[1] - bola["tamanho"]:
                # Reposiciona a bola para não sair da tela
                bola["posicao"][1] = tamanho[1] - bola["tamanho"]
                bola["direcao"].y = -1 # Inverte a direção da bola
            elif bola["posicao"][1] <= bola["tamanho"]:
                # Reposiciona a bola para não sair da tela
                bola["posicao"][1] = bola["tamanho"]
                bola["direcao"].y = 1 # Inverte a direção da bola

    #########################################
    # Atualiza a tela para exibir o que foi desenhado
    pygame.display.update()

    # Controla a quantidade de FPS
    relogio.tick(60)
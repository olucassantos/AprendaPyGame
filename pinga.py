import pygame # Importa a biblioteca Pygame
import random # Importa a biblioteca random (para gerar números aleatórios)
import os # Importa a biblioteca os (para acessar arquivos do sistema)

# Cria uma nova bola
def novaBola():
    # Cria um dicionário com as informações da bola
    velocidade = random.randint(1, 10) # Velocidade aleatória
    tipo = random.choice(['morcego', 'olho', 'fantasma']) # Tipo aleatório
    tamanho = random.randint(20, 50) # Tamanho aleatório
    vidas = random.randint(1, 10) # Vidas aleatórias

    # Retorna o dicionário com as informações da bola para ser adicionado na lista
    return {
        "posicao": [random.randint(200, 600), random.randint(200, 400)],
        "velocidade": velocidade,
        "tipo": tipo,
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
tamanho = (960, 540)
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

# Importar as imagens para o jogo
listaPlanoFundos = []
for index in range(1, 7):
    imagem = pygame.image.load(f"assets/planofundo/arvore/{index}.png")
    imagem = pygame.transform.scale(imagem, tamanho).convert_alpha()
    listaPlanoFundos.append(imagem)

listaImagensFantasma = []
listaImagensMorcego = []
listaImagensOlho = []
listaImagensFogo = []


itens = {
    'fantasma': 'ghost',
    'olho': 'fly-eye',
    'fogo': 'fireball',
    'morcego': 'bat'
}

for item in itens:
    # Conta os arquivos da pasta
    quantidade = len(os.listdir(f"assets/{item}"))

    for index in range(1, quantidade + 1):
        imagem = pygame.image.load(f"assets/{item}/{itens[item]}{index}.png")
        imagem = pygame.transform.scale(imagem, (60, 60)).convert_alpha()
        if item == 'fantasma': listaImagensFantasma.append(imagem)
        elif item == 'olho': listaImagensOlho.append(imagem)
        elif item == 'fogo': listaImagensFogo.append(imagem)
        elif item == 'morcego': listaImagensMorcego.append(imagem)

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

    # Desenha o plano de fundo
    for i in range(len(listaPlanoFundos)):
        tela.blit(listaPlanoFundos[i], (0,0))

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
                (255, 255, 255),
                bola["posicao"],
                bola["tamanho"]
            )

            # Decide quais imagens serão usadas para desenhar a bola
            listaImagens = []
            if bola["tipo"] == 'fantasma': listaImagens = listaImagensFantasma
            elif bola["tipo"] == 'olho': listaImagens = listaImagensOlho
            elif bola["tipo"] == 'fogo': listaImagens = listaImagensFogo
            elif bola["tipo"] == 'morcego': listaImagens = listaImagensMorcego

            # Desenha a imagem da bola
            # Divide o tempo por 100 e pega a parte inteira para saber qual imagem desenhar
            tempoJogo = pygame.time.get_ticks() // 100 
            # Calcula o frame da animação com base na quantidade de imagens da lista e o tempo do jogo
            quantidadeImagens = len(listaImagens)
            # Define o frame da animação
            frame = tempoJogo % quantidadeImagens
            # Pega a imagem da lista de imagens
            imagem = listaImagens[frame]
            
            # Desenha a imagem na tela
            tela.blit(imagem, (bola["posicao"][0] - 30, bola["posicao"][1] - 30))

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
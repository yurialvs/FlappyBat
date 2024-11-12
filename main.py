import pygame
import random
import os

# Inicializa o Pygame
pygame.init()

# Definir constantes
LARGURA_TELA = 400
ALTURA_TELA = 600
FPS = 60
GRAVIDADE = 0.5
VELOCIDADE_PAINEL = 2
LIMITE_LINHA = LARGURA_TELA - 50
ESPACO_MIN_OBSTACULO = 100  # Espaço mínimo entre os obstáculos
ESPACO_MAX_OBSTACULO = 200  # Espaço máximo entre os obstáculos

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Carregar imagens
bat_img = pygame.image.load("imagens/bat.png")
obstaculo_img = pygame.image.load("imagens/obstaculo.png")
premio_img = pygame.image.load("imagens/premio.png")
paisagem_img = pygame.image.load("imagens/paisagem.png")

# Criar janela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Flappy Bat")

# Função para desenhar a bat (morceguinho)
def desenha_bat(bat):
    tela.blit(bat_img, (bat.x, bat.y))

# Função para desenhar o obstáculo
def desenha_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        tela.blit(obstaculo_img, (obstaculo.x, obstaculo.y))

# Função para desenhar prêmios
def desenha_premios(premios):
    for premio in premios:
        tela.blit(premio_img, (premio.x, premio.y))

# Função para desenhar a paisagem
def desenha_paisagem(paisagem_x1, paisagem_x2):
    tela.blit(paisagem_img, (paisagem_x1, 0))  # Primeira parte da paisagem
    tela.blit(paisagem_img, (paisagem_x2, 0))  # Segunda parte da paisagem

# Função de checar colisão
def checar_colisao(bat, obstaculos, premios):
    # Checar colisão com obstáculos
    for obstaculo in obstaculos:
        if bat.colliderect(obstaculo):
            return True
    
    # Checar colisão com o teto (topo da tela)
    if bat.top <= 0:
        return True

    # Checar colisão com o chão (parte inferior da tela)
    if bat.bottom >= ALTURA_TELA:
        return True

    # Checar colisão com prêmios
    for premio in premios:
        if bat.colliderect(premio):
            premios.remove(premio)
            return "premio"

    return False

# Função para salvar o recorde
def salvar_recorde(pontuacao, nome):
    try:
        if os.path.exists("records.txt"):
            with open("records.txt", "r") as f:
                conteudo = f.read().strip()
                if conteudo:
                    # Garantir que o formato seja correto (pontuacao:nome)
                    partes = conteudo.split(":")
                    if len(partes) == 2:
                        recorde = int(partes[0])
                        recorde_nome = partes[1]
                    else:
                        # Caso o formato não seja válido, usaremos valores padrão
                        recorde = 0
                        recorde_nome = ""
                else:
                    recorde = 0
                    recorde_nome = ""
        else:
            recorde = 0
            recorde_nome = ""
    except FileNotFoundError:
        # Caso o arquivo não exista, cria-se um novo com valores padrão
        recorde = 0
        recorde_nome = ""

    # Se a pontuação do jogador for maior que o recorde, atualiza o recorde
    if pontuacao > recorde:
        with open("records.txt", "w") as f:
            f.write(f"{pontuacao}:{nome}")  # Salva a pontuação e o nome
        return pontuacao, nome  # Retorna a nova pontuação e nome
    return recorde, recorde_nome  # Retorna o recorde atual e o nome associado

# Função para desenhar a tela inicial
def tela_inicial():
    fonte = pygame.font.Font(None, 48)
    titulo_texto = fonte.render("Flappy Bat", True, BRANCO)
    instrucoes_texto = pygame.font.Font(None, 24).render("Pressione a barra de espaço para iniciar", True, BRANCO)
    
    # Exibe o título e as instruções
    tela.fill(PRETO)
    tela.blit(titulo_texto, (LARGURA_TELA // 2 - titulo_texto.get_width() // 2, ALTURA_TELA // 3))
    tela.blit(instrucoes_texto, (LARGURA_TELA // 2 - instrucoes_texto.get_width() // 2, ALTURA_TELA // 2))
    pygame.display.flip()

# Função para a tela de Game Over
def tela_game_over(pontuacao, recorde, nome):
    fonte = pygame.font.Font(None, 36)
    game_over_texto = fonte.render(f"Game Over! Pontuação: {pontuacao}", True, BRANCO)
    recorde_texto = fonte.render(f"Recorde: {recorde} - {nome}", True, BRANCO)
    novo_jogo_texto = pygame.font.Font(None, 24).render("Pressione 'R' para novo jogo ou 'ESC' para sair", True, BRANCO)

    # Exibe a tela de Game Over
    tela.fill(PRETO)
    tela.blit(game_over_texto, (LARGURA_TELA // 2 - game_over_texto.get_width() // 2, ALTURA_TELA // 3))
    tela.blit(recorde_texto, (LARGURA_TELA // 2 - recorde_texto.get_width() // 2, ALTURA_TELA // 2))
    tela.blit(novo_jogo_texto, (LARGURA_TELA // 2 - novo_jogo_texto.get_width() // 2, ALTURA_TELA // 1.5))
    pygame.display.flip()

# Função para a tela de digitação do nome
def tela_nome_jogador():
    nome = ""
    fonte = pygame.font.Font(None, 36)
    while True:
        tela.fill(PRETO)
        nome_texto = fonte.render(f"Digite seu nome: {nome}", True, BRANCO)
        tela.blit(nome_texto, (LARGURA_TELA // 2 - nome_texto.get_width() // 2, ALTURA_TELA // 2))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome:  # Pressionar Enter para continuar
                    return nome
                elif evento.key == pygame.K_BACKSPACE:  # Backspace para apagar
                    nome = nome[:-1]
                elif evento.key <= 127:  # Verifica se a tecla pressionada é um caractere
                    nome += evento.unicode

# Função principal do jogo
def jogo():
    # Inicializar o relógio e o score
    clock = pygame.time.Clock()
    
    # Perguntar o nome do jogador antes de iniciar
    nome = tela_nome_jogador()
    if nome is None:
        return  # Se o nome for None, o jogador fechou a janela

    bat = pygame.Rect(50, ALTURA_TELA // 2, 47, 30)  # Posição inicial da bat
    obstaculos = []
    premios = []
    paisagem_x1 = 0  # Primeira parte da paisagem
    paisagem_x2 = LARGURA_TELA  # Segunda parte da paisagem
    velocidade_bat_y = 0
    pontuacao = 0
    recorde, recorde_nome = salvar_recorde(pontuacao, nome)
    
    # Variáveis para controle do aparecimento dos obstáculos
    tempo_ultimo_obstaculo = 0
    tempo_ultimo_premio = 0
    intervalo_obstaculo = random.randint(ESPACO_MIN_OBSTACULO, ESPACO_MAX_OBSTACULO)
    intervalo_premio = random.randint(100, 200)  # Menor intervalo para mais prêmios
    
    # Tela de Início
    tela_inicial()
    esperando_inicio = True
    while esperando_inicio:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    esperando_inicio = False
                    break

    # Loop principal do jogo
    rodando = True
    while rodando:
        clock.tick(FPS)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocidade_bat_y = -10  # Empurrar a bat para cima

        # Movimentação da bat
        velocidade_bat_y += GRAVIDADE
        bat.y += velocidade_bat_y
        if bat.y > ALTURA_TELA - 30:
            bat.y = ALTURA_TELA - 30  # Bat não cai para fora da tela
        if bat.y < 0:
            bat.y = 0  # Limita a bat no topo da tela

        # Movimentação da paisagem
        paisagem_x1 -= VELOCIDADE_PAINEL
        paisagem_x2 -= VELOCIDADE_PAINEL
        if paisagem_x1 <= -LARGURA_TELA:
            paisagem_x1 = LARGURA_TELA
        if paisagem_x2 <= -LARGURA_TELA:
            paisagem_x2 = LARGURA_TELA

        # Geração de obstáculos e prêmios
        tempo_ultimo_obstaculo += 1
        if tempo_ultimo_obstaculo >= intervalo_obstaculo:
            altura_obstaculo = random.randint(100, 400)
            obstaculos.append(pygame.Rect(LARGURA_TELA, altura_obstaculo, 47, 40))
            tempo_ultimo_obstaculo = 0
            intervalo_obstaculo = random.randint(ESPACO_MIN_OBSTACULO, ESPACO_MAX_OBSTACULO)

        tempo_ultimo_premio += 1
        if tempo_ultimo_premio >= intervalo_premio:
            altura_premio = random.randint(100, 400)
            premios.append(pygame.Rect(LARGURA_TELA, altura_premio, 47, 40))
            tempo_ultimo_premio = 0
            intervalo_premio = random.randint(100, 200)

        # Movimentação dos obstáculos e prêmios
        for obstaculo in obstaculos:
            obstaculo.x -= VELOCIDADE_PAINEL
        for premio in premios:
            premio.x -= VELOCIDADE_PAINEL

        # Remover obstáculos e prêmios fora da tela
        obstaculos = [o for o in obstaculos if o.x > -50]
        premios = [p for p in premios if p.x > -50]

        # Checar colisões
        colisao = checar_colisao(bat, obstaculos, premios)
        if colisao == "premio":
            pontuacao += 1
        if colisao == True:
            recorde, recorde_nome = salvar_recorde(pontuacao, nome)
            tela_game_over(pontuacao, recorde, recorde_nome)
            esperando_novo_jogo = True
            while esperando_novo_jogo:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_r:
                            jogo()  # Reinicia o jogo
                        if evento.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return

        # Atualizar a tela
        tela.fill(PRETO)
        desenha_paisagem(paisagem_x1, paisagem_x2)
        desenha_bat(bat)
        desenha_obstaculos(obstaculos)
        desenha_premios(premios)

        # Desenhar pontuação
        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(f"Pontos: {pontuacao} | Recorde: {recorde}", True, BRANCO)
        tela.blit(texto, (10, 10))

        # Atualizar display
        pygame.display.flip()

    pygame.quit()

# Rodar o jogo
if __name__ == "__main__":
    jogo()
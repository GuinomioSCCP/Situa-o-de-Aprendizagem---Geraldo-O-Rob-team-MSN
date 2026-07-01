import pygame
from pygame.locals import *
from sys import exit
import random

pygame.init()

frames = pygame.time.Clock()

fonte = pygame.font.SysFont("gabriola", 50, True, False)
fonte2 = pygame.font.SysFont("gabriola", 20, True, False)
fonte_esc = pygame.font.SysFont("gabriola", 25, True, False)
fonte_gameover = pygame.font.SysFont("gabriola", 80, True, False)
fonte_win = pygame.font.SysFont("gabriola", 80, True, False)

tamanho_geraldo = 100

component = 0

vidas = 3

largura = 500
altura = 600

x = 0
y = 100

Verde_claro = (0, 255, 0)
Verde_escuro = (0, 64, 0)

bugs = []
componentes = []

mensagem_borda = False
tempo_mensagem = 0
    
pygame.display.set_caption("Geraldo o Robô")

tela = pygame.display.set_mode((largura, altura))

def gerar_posicao():
    x = random.randint(0, 4)*100
    y = random.randint(1, 5)*100
    return x, y

def gerar_componentes():
    global componentes
    for i in range(3):
        x, y = gerar_posicao()
        if len(componentes) > 0:
            for componente in componentes:
                while componente['x'] == x and componente['y'] == y or componente['x'] == 0 and componente['y'] == 100 or componente['x'] == 100 and componente['y'] == 100 or componente['x'] == 0 and componente['y'] == 200 or componente['x'] == 400 and componente['y'] == 500:
                    x, y = gerar_posicao()

        rect = pygame.draw.rect(tela, (255, 255, 255), (x, y, 100, 100))
        componentes.append({
            'x': x,
            'y': y,
            'coletado': False,
            'rect': rect
        })

def gerar_bugs():
    global bugs
    global componentes

    for i in range(3):
        x, y = gerar_posicao()
        if len(bugs) > 0:
            for bug in bugs:
                while bug['x'] == x and bug['y'] == y or bug['x'] == 0 and bug['y'] == 100 or bug['x'] == 100 and bug['y'] == 100 or bug['x'] == 0 and bug['y'] == 200 or bug['x'] == 400 and bug['y'] == 500:
                    x, y = gerar_posicao()

        if len(componentes) > 0:        
            for componente in componentes:
                while componente['x'] == x and componente['y'] == y:
                    x, y = gerar_posicao()

        rect = pygame.draw.rect(tela, (255, 255, 255), (x, y, 100, 100))
        bugs.append({
            'x': x,
            'y': y,
            'coletado': False,
            'rect': rect
        })

gerar_componentes()
gerar_bugs()

while True:
    frames.tick(60)
    tela.fill((0,0,0))

    texto_formatado_esc = fonte_esc.render("Clique ESC Para Sair!", True, (255, 255, 255))

    texto_formatado_cmpnt_ins = fonte2.render("Componentes Insuficientes!", True, (255, 255, 255))

    texto_formatado_win = fonte_win.render("Você Ganhou!", True, (255, 255, 255))

    texto_formatado_gameover = fonte_gameover.render("Game Over!", True, (255, 255, 255))

    texto_formatado_colisao_parede = fonte2.render("Você Bateu na Parede!", True, (255, 255, 255))

    texto_formatado_pontuacao = fonte.render(f"Pts: {component}", True, (255, 255, 255))

    texto_formatado_vida = fonte.render(f"Vidas: {vidas}", True, (255, 255, 255))
    
    for linha in range(5):
        for coluna in range(5):
            if (linha+coluna) % 2 == 0:
                 cor = Verde_claro
            else:
                cor = Verde_escuro
            pygame.draw.rect(tela, cor, (coluna * 100, 100 + (linha * 100), 100, 100))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                if x >= 100:
                    x -= 100 
                else:
                    mensagem_borda = True
                    tempo_mensagem = pygame.time.get_ticks()

            if event.key == K_d or event.key == K_RIGHT:
                if x < 400:
                    x += 100
                else:
                    mensagem_borda = True
                    tempo_mensagem = pygame.time.get_ticks()

            if event.key == K_w or event.key == K_UP:
                if y >= 200:
                    y -= 100
                else:
                    mensagem_borda = True
                    tempo_mensagem = pygame.time.get_ticks()

            if event.key == K_s or event.key == K_DOWN:
                if y < 500:
                    y += 100
                else:
                    mensagem_borda = True
                    tempo_mensagem = pygame.time.get_ticks()
            
    Servidor_principal = pygame.draw.rect(tela, (255, 0, 0), (400, 500, 100, 100))
    Cyber_geraldo = pygame.draw.rect(tela, (0, 0, 255), (x, y, tamanho_geraldo, tamanho_geraldo))

    if mensagem_borda and pygame.time.get_ticks() - tempo_mensagem < 2000:
        tela.blit(texto_formatado_colisao_parede, (180, 80))
        mensagem_borda = True
    else:
        mensagem_borda = False
    
    for bug in bugs:
        if Cyber_geraldo.colliderect(bug['rect']):
            vidas = vidas - 1
            bug['rect'].x = 0
            bug['rect'].y = 0
   
    for componente in componentes:
        if Cyber_geraldo.colliderect(componente['rect']):
            component += 1
            componente['rect'].x = 0
            componente['rect'].y = 0

    tela.blit(texto_formatado_vida, (0, 0))
    tela.blit(texto_formatado_pontuacao, (375, 0))

    if vidas == 0:
        tela.fill((0, 0, 0))
        tela.blit(texto_formatado_gameover, (60, 200))
        tela.blit(texto_formatado_esc, (60, 280))
        tamanho_geraldo = 0
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            else:
                pass

    if Cyber_geraldo.colliderect(Servidor_principal) and component == 3:
        tela.fill((0, 0, 0))
        tela.blit(texto_formatado_win, (30, 200))
        tela.blit(texto_formatado_esc, (30, 280))
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            else:
                pass

    if Cyber_geraldo.colliderect(Servidor_principal) and component != 3:
        tela.blit(texto_formatado_cmpnt_ins, (155, 60))

    pygame.display.update()
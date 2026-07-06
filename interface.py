import pygame
import sys
import os

# Garantir que a pasta do projeto esteja no sys.path para importar o pacote 'logica'
PROJETO_ROOT = os.path.dirname(__file__)
if PROJETO_ROOT not in sys.path:
    sys.path.append(PROJETO_ROOT)

# Importando todas as lógicas
from logica.busca_bfs import ReguaPuzzleBFS
from logica.busca_dls import ReguaPuzzleDLS
from logica.busca_ordenada import ReguaPuzzleBuscaOrdenada
from logica.busca_backtracking import ReguaPuzzleBacktracking
from logica.busca_a import ReguaPuzzleBuscaAEstrela

# ==========================================
# 1. INTERFACE VISUAL COM PYGAME
# ==========================================
def iniciar_interface():
    # Inicializa o Pygame
    pygame.init()
    
    # Configurações da Tela
    LARGURA, ALTURA = 900, 500
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Resolução - Régua Puzzle")

    # Cores
    COR_FUNDO = (240, 248, 255)
    COR_A = (65, 105, 225)
    COR_B = (220, 20, 60)
    COR_VAZIO = (200, 200, 200)
    COR_TEXTO = (255, 255, 255)
    COR_BOTAO = (100, 149, 237)
    COR_BOTAO_HOVER = (65, 105, 225)

    FONTE_BLOCO = pygame.font.Font(None, 80)
    FONTE_MENU = pygame.font.Font(None, 40)
    FONTE_TITULO = pygame.font.Font(None, 60)
    FONTE_PEQUENA = pygame.font.Font(None, 30)

    # ---------------------------------------------------
    # TELA 1: MENU DE SELEÇÃO
    # ---------------------------------------------------
    def menu_selecao():
        largura_botao, altura_botao = 400, 50
        centro_x = LARGURA // 2 - largura_botao // 2
        
        botoes = [
            {"texto": "Busca em Largura (BFS)", "id": "BFS", "rect": pygame.Rect(centro_x, 100, largura_botao, altura_botao)},
            {"texto": "Profundidade Limitada (DLS)", "id": "DLS", "rect": pygame.Rect(centro_x, 170, largura_botao, altura_botao)},
            {"texto": "Busca Ordenada", "id": "ORD", "rect": pygame.Rect(centro_x, 240, largura_botao, altura_botao)},
            {"texto": "Busca Backtracking", "id": "BCK", "rect": pygame.Rect(centro_x, 310, largura_botao, altura_botao)},
            {"texto": "Busca A* (A Estrela)", "id": "AST", "rect": pygame.Rect(centro_x, 380, largura_botao, altura_botao)}
        ]

        rodando_menu = True
        escolha = None

        while rodando_menu:
            TELA.fill(COR_FUNDO)
            
            titulo = FONTE_TITULO.render("Escolha o Algoritmo de Busca", True, (50, 50, 50))
            TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mouse_click = True

            for botao in botoes:
                cor_atual = COR_BOTAO
                
                if botao["rect"].collidepoint(mouse_pos):
                    cor_atual = COR_BOTAO_HOVER
                    if mouse_click:
                        escolha = botao["id"]
                        rodando_menu = False

                pygame.draw.rect(TELA, cor_atual, botao["rect"], border_radius=10)
                
                texto_surface = FONTE_MENU.render(botao["texto"], True, COR_TEXTO)
                rect_texto = texto_surface.get_rect(center=botao["rect"].center)
                TELA.blit(texto_surface, rect_texto)

            pygame.display.flip()
            
        return escolha

    # ---------------------------------------------------
    # TELA 2: ANIMAÇÃO DA RESOLUÇÃO
    # ---------------------------------------------------
    def desenhar_estado(estado, passo_atual, total_passos, nome_algoritmo, rect_voltar, cor_voltar):
        TELA.fill(COR_FUNDO)
        
        tamanho_bloco = 100
        espaco = 20
        margem_x = (LARGURA - (len(estado) * tamanho_bloco + (len(estado) - 1) * espaco)) // 2
        margem_y = (ALTURA - tamanho_bloco) // 2

        for i, char in enumerate(estado):
            x = margem_x + i * (tamanho_bloco + espaco)
            y = margem_y
            
            if char == 'A': cor = COR_A
            elif char == 'B': cor = COR_B
            else: cor = COR_VAZIO

            pygame.draw.rect(TELA, cor, (x, y, tamanho_bloco, tamanho_bloco), border_radius=15)
            
            if char != '_':
                texto = FONTE_BLOCO.render(char, True, COR_TEXTO)
                rect_texto = texto.get_rect(center=(x + tamanho_bloco // 2, y + tamanho_bloco // 2))
                TELA.blit(texto, rect_texto)

        # Textos informativos no canto superior esquerdo
        fonte_info = pygame.font.Font(None, 36)
        texto_passo = fonte_info.render(f"Passo: {passo_atual} / {total_passos}", True, (50, 50, 50))
        texto_alg = fonte_info.render(f"Algoritmo: {nome_algoritmo}", True, (50, 50, 50))
        
        TELA.blit(texto_passo, (20, 20))
        TELA.blit(texto_alg, (20, 50))

        # Desenhar Botão de Voltar no canto superior direito
        pygame.draw.rect(TELA, cor_voltar, rect_voltar, border_radius=8)
        texto_voltar = FONTE_PEQUENA.render("Voltar ao Menu", True, COR_TEXTO)
        rect_texto_voltar = texto_voltar.get_rect(center=rect_voltar.center)
        TELA.blit(texto_voltar, rect_texto_voltar)
                
        pygame.display.flip()

    # --- FLUXO PRINCIPAL (LOOP MESTRE) ---
    # Este loop garante que ao sair da animação, o menu volte a aparecer
    while True:
        
        algoritmo_escolhido = menu_selecao()
        estado_inicial = ['B', 'A', '_', 'A', 'B']
        
        print(f"Calculando a solução usando {algoritmo_escolhido}...")
        
        if algoritmo_escolhido == "BFS":
            puzzle = ReguaPuzzleBFS(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido == "DLS":
            puzzle = ReguaPuzzleDLS(estado_inicial)
            resultado = puzzle.buscar(limite_profundidade=15)
        elif algoritmo_escolhido == "ORD":
            puzzle = ReguaPuzzleBuscaOrdenada(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido == "BCK":
            puzzle = ReguaPuzzleBacktracking(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido == "AST":
            puzzle = ReguaPuzzleBuscaAEstrela(estado_inicial)
            resultado = puzzle.buscar()

        caminho_solucao = resultado.get("caminho")

        if not caminho_solucao:
            print("Nenhuma solução encontrada com esse algoritmo ou limite!")
            continue # Em vez de fechar, volta pro menu

        passo_atual = 0
        rodando_animacao = True
        relogio = pygame.time.Clock()
        
        ultimo_tempo = pygame.time.get_ticks()
        intervalo_animacao = 1000 

        # Definição do botão voltar
        largura_voltar, altura_voltar = 160, 40
        rect_voltar = pygame.Rect(LARGURA - largura_voltar - 20, 20, largura_voltar, altura_voltar)

        while rodando_animacao:
            cor_voltar = COR_BOTAO
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mouse_click = True

            # Checa clique no botão voltar
            if rect_voltar.collidepoint(mouse_pos):
                cor_voltar = COR_BOTAO_HOVER
                if mouse_click:
                    rodando_animacao = False # Quebra este loop e volta pro While True (Menu)

            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - ultimo_tempo > intervalo_animacao:
                if passo_atual < len(caminho_solucao) - 1:
                    passo_atual += 1
                ultimo_tempo = tempo_atual

            desenhar_estado(caminho_solucao[passo_atual], passo_atual, len(caminho_solucao) - 1, algoritmo_escolhido, rect_voltar, cor_voltar)
            
            relogio.tick(60)

if __name__ == "__main__":
    iniciar_interface()
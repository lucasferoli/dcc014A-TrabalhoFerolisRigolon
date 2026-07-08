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
from logica.busca_gulosa import ReguaPuzzleBuscaGulosa
from logica.busca_ida import ReguaPuzzleBuscaIDAEstrela

# ==========================================
# FUNÇÃO GERADORA DE ESTADOS INICIAIS
# ==========================================
def gerar_estado_inicial(N):
    """
    Gera um tabuleiro embaralhado baseado no tamanho N.
    Ex: N=1 -> ['A', '_', 'B']
    Ex: N=2 -> ['B', 'A', '_', 'A', 'B']
    """
    estado = []
    # Metade esquerda
    for i in range(N):
        estado.append('A' if (N - i) % 2 != 0 else 'B')
    # Centro
    estado.append('_')
    # Metade direita
    for i in range(N):
        estado.append('B' if (N - i) % 2 != 0 else 'A')
    return estado

# ==========================================
# 1. INTERFACE VISUAL COM PYGAME
# ==========================================
def iniciar_interface():
    pygame.init()
    
    # Configurações da Tela (Aumentada para caber o seletor e botões)
    LARGURA, ALTURA = 1000, 700
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
        
        # Variáveis do Seletor
        N_atual = 2
        btn_menos = pygame.Rect(LARGURA // 2 - 120, 100, 50, 40)
        btn_mais = pygame.Rect(LARGURA // 2 + 70, 100, 50, 40)
        
        # Botões de algoritmos (deslocados mais para baixo)
        botoes = [
            {"texto": "Busca em Largura (BFS)", "id": "BFS", "rect": pygame.Rect(centro_x, 260, largura_botao, altura_botao)},
            {"texto": "Profundidade Limitada (DLS)", "id": "DLS", "rect": pygame.Rect(centro_x, 320, largura_botao, altura_botao)},
            {"texto": "Busca Ordenada", "id": "ORD", "rect": pygame.Rect(centro_x, 380, largura_botao, altura_botao)},
            {"texto": "Busca Backtracking", "id": "BCK", "rect": pygame.Rect(centro_x, 440, largura_botao, altura_botao)},
            {"texto": "Busca A* (A Estrela)", "id": "AST", "rect": pygame.Rect(centro_x, 500, largura_botao, altura_botao)},
            {"texto": "Busca Gulosa", "id": "GUL", "rect": pygame.Rect(centro_x, 560, largura_botao, altura_botao)},
            {"texto": "Busca IDA* (IDA Estrela)", "id": "IDA", "rect": pygame.Rect(centro_x, 620, largura_botao, altura_botao)}
        ]

        rodando_menu = True
        escolha_algoritmo = None

        while rodando_menu:
            TELA.fill(COR_FUNDO)
            
            # Título
            titulo = FONTE_TITULO.render("Régua Puzzle - Configuração", True, (50, 50, 50))
            TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mouse_click = True

            # --- DESENHO DO SELETOR DE N ---
            # Botão Menos
            cor_menos = COR_BOTAO_HOVER if btn_menos.collidepoint(mouse_pos) else COR_BOTAO
            pygame.draw.rect(TELA, cor_menos, btn_menos, border_radius=5)
            texto_menos = FONTE_MENU.render("-", True, COR_TEXTO)
            TELA.blit(texto_menos, texto_menos.get_rect(center=btn_menos.center))
            if btn_menos.collidepoint(mouse_pos) and mouse_click and N_atual > 1:
                N_atual -= 1

            # Texto do N atual
            texto_n = FONTE_MENU.render(f"N = {N_atual}", True, (50, 50, 50))
            TELA.blit(texto_n, texto_n.get_rect(center=(LARGURA // 2, 120)))

            # Botão Mais
            cor_mais = COR_BOTAO_HOVER if btn_mais.collidepoint(mouse_pos) else COR_BOTAO
            pygame.draw.rect(TELA, cor_mais, btn_mais, border_radius=5)
            texto_mais = FONTE_MENU.render("+", True, COR_TEXTO)
            TELA.blit(texto_mais, texto_mais.get_rect(center=btn_mais.center))
            if btn_mais.collidepoint(mouse_pos) and mouse_click and N_atual < 5: 
                # Limitamos N a 5 para evitar travamentos, pois tabuleiros gigantes demoram muito
                N_atual += 1

            # Preview do Array Gerado
            estado_preview = gerar_estado_inicial(N_atual)
            texto_preview = FONTE_PEQUENA.render(f"Estado Inicial: {' '.join(estado_preview)}", True, (100, 100, 100))
            TELA.blit(texto_preview, texto_preview.get_rect(center=(LARGURA // 2, 180)))
            pygame.draw.line(TELA, (200, 200, 200), (LARGURA//2 - 300, 220), (LARGURA//2 + 300, 220), 2)

            # --- DESENHO DOS BOTÕES DE ALGORITMO ---
            for botao in botoes:
                cor_atual = COR_BOTAO
                
                if botao["rect"].collidepoint(mouse_pos):
                    cor_atual = COR_BOTAO_HOVER
                    if mouse_click:
                        escolha_algoritmo = botao["id"]
                        rodando_menu = False

                pygame.draw.rect(TELA, cor_atual, botao["rect"], border_radius=10)
                
                texto_surface = FONTE_MENU.render(botao["texto"], True, COR_TEXTO)
                rect_texto = texto_surface.get_rect(center=botao["rect"].center)
                TELA.blit(texto_surface, rect_texto)

            pygame.display.flip()
            
        return escolha_algoritmo, gerar_estado_inicial(N_atual)

    # ---------------------------------------------------
    # TELA 2: ANIMAÇÃO DA RESOLUÇÃO
    # ---------------------------------------------------
    def desenhar_estado(estado, passo_atual, total_passos, nome_algoritmo, rect_voltar, cor_voltar):
        TELA.fill(COR_FUNDO)
        
        # Ajusta o tamanho do bloco se o N for muito grande para caber na tela
        max_blocos = len(estado)
        tamanho_bloco = min(100, (LARGURA - 100) // max_blocos - 10)
        espaco = 10
        margem_x = (LARGURA - (max_blocos * tamanho_bloco + (max_blocos - 1) * espaco)) // 2
        margem_y = (ALTURA - tamanho_bloco) // 2

        # Reduz a fonte do bloco se ele ficar pequeno
        fonte_dinamica = pygame.font.Font(None, int(tamanho_bloco * 0.8))

        for i, char in enumerate(estado):
            x = margem_x + i * (tamanho_bloco + espaco)
            y = margem_y
            
            if char == 'A': cor = COR_A
            elif char == 'B': cor = COR_B
            else: cor = COR_VAZIO

            pygame.draw.rect(TELA, cor, (x, y, tamanho_bloco, tamanho_bloco), border_radius=15)
            
            if char != '_':
                texto = fonte_dinamica.render(char, True, COR_TEXTO)
                rect_texto = texto.get_rect(center=(x + tamanho_bloco // 2, y + tamanho_bloco // 2))
                TELA.blit(texto, rect_texto)

        # Textos informativos
        fonte_info = pygame.font.Font(None, 36)
        texto_passo = fonte_info.render(f"Passo: {passo_atual} / {total_passos}", True, (50, 50, 50))
        texto_alg = fonte_info.render(f"Algoritmo: {nome_algoritmo}", True, (50, 50, 50))
        
        TELA.blit(texto_passo, (20, 20))
        TELA.blit(texto_alg, (20, 50))

        # Desenhar Botão de Voltar
        pygame.draw.rect(TELA, cor_voltar, rect_voltar, border_radius=8)
        texto_voltar = FONTE_PEQUENA.render("Voltar ao Menu", True, COR_TEXTO)
        rect_texto_voltar = texto_voltar.get_rect(center=rect_voltar.center)
        TELA.blit(texto_voltar, rect_texto_voltar)
                
        pygame.display.flip()

    def imprimir_estatisticas(algoritmo, estado_inicial, resultado):
        caminho = resultado.get("caminho")

        print("\n==================================================")
        print(f"        RESULTADO DA BUSCA ({algoritmo})")
        print("==================================================")
        print(f"Estado inicial: {' '.join(estado_inicial)}")

        if caminho:
            print("\nCaminho encontrado:")
            for i, estado in enumerate(caminho):
                print(f"  Passo {i}: {' '.join(estado)}")

            print("\nMetricas da solucao:")
            print(f"Profundidade da solucao : {resultado.get('profundidade')}")
            print(f"Custo total da solucao  : {resultado.get('custo')}")
        else:
            print("\nNenhuma solucao encontrada.")

        print("\nMetricas da execucao:")
        print(f"Nos visitados              : {resultado.get('nos_visitados')}")
        print(f"Nos expandidos             : {resultado.get('nos_expandidos')}")
        print(f"Fator de ramificacao medio : {resultado.get('fator_ramificacao_medio', 0):.2f}")
        print(f"Tempo de execucao          : {resultado.get('tempo_execucao', 0):.6f} segundos")
        print("==================================================\n")

    # --- FLUXO PRINCIPAL (LOOP MESTRE) ---
    while True:
        # Agora o menu retorna DUAS coisas: o algoritmo e o estado configurado
        algoritmo_escolhido, estado_inicial = menu_selecao()
        
        print(f"Calculando solução para {estado_inicial} usando {algoritmo_escolhido}...")
        
        resultado = {} 
        
        if algoritmo_escolhido == "BFS":
            puzzle = ReguaPuzzleBFS(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido == "DLS":
            puzzle = ReguaPuzzleDLS(estado_inicial)
            # DLS pode precisar de um limite muito maior se o N for grande
            limite_dinamico = len(estado_inicial) * 4 
            resultado = puzzle.buscar(limite_profundidade=limite_dinamico)
        elif algoritmo_escolhido == "ORD":
            puzzle = ReguaPuzzleBuscaOrdenada(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido == "BCK":
            puzzle = ReguaPuzzleBacktracking(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido == "AST":
            puzzle = ReguaPuzzleBuscaAEstrela(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido in ["GULOSA", "GUL"]: 
            puzzle = ReguaPuzzleBuscaGulosa(estado_inicial)
            resultado = puzzle.buscar()
        elif algoritmo_escolhido == "IDA":
            puzzle = ReguaPuzzleBuscaIDAEstrela(estado_inicial)
            resultado = puzzle.buscar()

        imprimir_estatisticas(algoritmo_escolhido, estado_inicial, resultado)

        caminho_solucao = resultado.get("caminho") 

        if not caminho_solucao:
            print("Nenhuma solução encontrada! Tente um algoritmo diferente ou aumente os limites.")
            continue 

        passo_atual = 0
        rodando_animacao = True
        relogio = pygame.time.Clock()
        ultimo_tempo = pygame.time.get_ticks()
        
        # Aumentamos a velocidade da animação para N maiores
        intervalo_animacao = max(200, 1000 - (len(estado_inicial) * 100)) 

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

            if rect_voltar.collidepoint(mouse_pos):
                cor_voltar = COR_BOTAO_HOVER
                if mouse_click:
                    rodando_animacao = False 

            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - ultimo_tempo > intervalo_animacao:
                if passo_atual < len(caminho_solucao) - 1:
                    passo_atual += 1
                ultimo_tempo = tempo_atual

            desenhar_estado(caminho_solucao[passo_atual], passo_atual, len(caminho_solucao) - 1, algoritmo_escolhido, rect_voltar, cor_voltar)
            
            relogio.tick(60)

if __name__ == "__main__":
    iniciar_interface()

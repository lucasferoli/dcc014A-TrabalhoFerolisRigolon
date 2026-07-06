import pygame
import sys
from collections import deque

# ==========================================
# 1. LÓGICA DE INTELIGÊNCIA ARTIFICIAL
# ==========================================
class ReguaPuzzleBFS:
    def __init__(self, estado_inicial):
        self.estado_inicial = tuple(estado_inicial)
        self.N = (len(estado_inicial) - 1) // 2

    def eh_meta(self, estado):
        encontrou_A = False
        for char in estado:
            if char == 'A':
                encontrou_A = True
            elif char == 'B' and encontrou_A:
                return False
        return True

    def obter_sucessores(self, estado):
        sucessores = []
        idx_vazio = estado.index('_')
        tamanho = len(estado)

        for idx_bloco in range(tamanho):
            if idx_bloco == idx_vazio: continue
            distancia = abs(idx_vazio - idx_bloco)
            if distancia <= self.N:
                novo_estado = list(estado)
                novo_estado[idx_vazio], novo_estado[idx_bloco] = novo_estado[idx_bloco], novo_estado[idx_vazio]
                sucessores.append((tuple(novo_estado), distancia))
        return sucessores

    def buscar(self):
        visitados = set()
        fila = deque([(self.estado_inicial, [self.estado_inicial])])
        visitados.add(self.estado_inicial)

        while fila:
            estado_atual, caminho_atual = fila.popleft()

            if self.eh_meta(estado_atual):
                return caminho_atual

            for proximo_estado, _ in self.obter_sucessores(estado_atual):
                if proximo_estado not in visitados:
                    visitados.add(proximo_estado)
                    fila.append((proximo_estado, caminho_atual + [proximo_estado]))
        return None

# ==========================================
# 2. INTERFACE VISUAL COM PYGAME
# ==========================================
def iniciar_interface():
    # Inicializa o Pygame
    pygame.init()
    
    # Configurações da Tela
    LARGURA, ALTURA = 800, 300
    TELA = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Resolução - Régua Puzzle")

    # Cores
    COR_FUNDO = (240, 248, 255) # Azul bem claro (AliceBlue)
    COR_A = (65, 105, 225)      # Royal Blue
    COR_B = (220, 20, 60)       # Crimson Red
    COR_VAZIO = (200, 200, 200) # Cinza
    COR_TEXTO = (255, 255, 255) # Branco

    # Fonte para as letras
    FONTE = pygame.font.Font(None, 80)

    # Função para desenhar os blocos na tela
    def desenhar_estado(estado, passo_atual, total_passos):
        TELA.fill(COR_FUNDO)
        
        tamanho_bloco = 100
        espaco = 20
        # Centralizar na tela matematicamente
        margem_x = (LARGURA - (len(estado) * tamanho_bloco + (len(estado) - 1) * espaco)) // 2
        margem_y = (ALTURA - tamanho_bloco) // 2

        # Desenhar cada bloco do estado atual
        for i, char in enumerate(estado):
            x = margem_x + i * (tamanho_bloco + espaco)
            y = margem_y
            
            # Escolhe a cor baseada na letra
            if char == 'A':
                cor = COR_A
            elif char == 'B':
                cor = COR_B
            else:
                cor = COR_VAZIO

            # Desenha o quadrado (com bordas arredondadas)
            pygame.draw.rect(TELA, cor, (x, y, tamanho_bloco, tamanho_bloco), border_radius=15)
            
            # Desenha a letra se não for vazio
            if char != '_':
                texto = FONTE.render(char, True, COR_TEXTO)
                # Centraliza a letra no bloco
                rect_texto = texto.get_rect(center=(x + tamanho_bloco // 2, y + tamanho_bloco // 2))
                TELA.blit(texto, rect_texto)

        # Desenhar indicador de passos
        fonte_pequena = pygame.font.Font(None, 36)
        texto_passo = fonte_pequena.render(f"Passo: {passo_atual} / {total_passos}", True, (50, 50, 50))
        TELA.blit(texto_passo, (20, 20))
                
        pygame.display.flip()

    # --- Lógica de Execução ---
    estado_inicial = ['B', 'A', '_', 'A', 'B']
    print("Calculando a solução...")
    
    puzzle = ReguaPuzzleBFS(estado_inicial)
    caminho_solucao = puzzle.buscar()

    if not caminho_solucao:
        print("Nenhuma solução encontrada!")
        pygame.quit()
        return

    # Controle de Animação
    passo_atual = 0
    rodando = True
    relogio = pygame.time.Clock()
    
    # Temporizador (1000 milissegundos = 1 segundo de intervalo entre os frames)
    ultimo_tempo = pygame.time.get_ticks()
    intervalo_animacao = 1000 

    # Loop Principal do Jogo
    while rodando:
        # 1. Checa eventos (como clicar no X para fechar a janela)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # 2. Atualiza a lógica de tempo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultimo_tempo > intervalo_animacao:
            # Avança para o próximo passo, se não tiver chegado no final
            if passo_atual < len(caminho_solucao) - 1:
                passo_atual += 1
            ultimo_tempo = tempo_atual

        # 3. Desenha na tela
        estado_para_desenhar = caminho_solucao[passo_atual]
        desenhar_estado(estado_para_desenhar, passo_atual, len(caminho_solucao) - 1)
        
        # Limita a 60 FPS
        relogio.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    iniciar_interface()
import time
import heapq

class ReguaPuzzleBuscaAEstrela:
    def __init__(self, estado_inicial):
        self.estado_inicial = tuple(estado_inicial)
        self.N = (len(estado_inicial) - 1) // 2

        # Estatísticas globais
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0

    def eh_meta(self, estado):
        """
        Verifica se o estado é uma meta: nenhum 'B' pode estar à direita de qualquer 'A'.
        """
        encontrou_A = False
        for char in estado:
            if char == 'A':
                encontrou_A = True
            elif char == 'B' and encontrou_A:
                return False
        return True

    def heuristica(self, estado):
        """
        Heurística h(n): Conta quantos blocos 'B' estão à direita de um bloco 'A'.
        Como cada um desses blocos precisa se mover no mínimo 1 casa para resolver o problema,
        o custo total real sempre será maior ou igual a essa contagem.
        Portanto, a heurística é admissível.
        """
        custo_h = 0
        encontrou_A = False
        for char in estado:
            if char == 'A':
                encontrou_A = True
            elif char == 'B' and encontrou_A:
                custo_h += 1
        return custo_h

    def obter_sucessores(self, estado):
        """
        Gera os estados sucessores válidos e os custos dos movimentos.
        Regra: distância máxima de N posições até o espaço vazio '_'[cite: 12].
        O custo de um pulo é igual à distância percorrida.
        """
        sucessores = []
        idx_vazio = estado.index('_')
        tamanho = len(estado)

        for idx_bloco in range(tamanho):
            if idx_bloco == idx_vazio:
                continue

            distancia = abs(idx_vazio - idx_bloco)
            if distancia <= self.N: # [cite: 12]
                novo_estado = list(estado)
                novo_estado[idx_vazio], novo_estado[idx_bloco] = novo_estado[idx_bloco], novo_estado[idx_vazio]
                sucessores.append((tuple(novo_estado), distancia)) # 

        return sucessores

    def buscar(self):
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0

        tempo_inicio = time.time()

        # Dicionário de fechados: armazena o menor custo g(n) conhecido para chegar a cada estado
        custos_otimos = {}

        # Fila de prioridades (Heap). A chave primária é f(n) = g(n) + h(n).
        # Formato: (custo_f, id_unico, custo_g, estado_atual, caminho)
        fila_prioridade = []
        id_contador = 0

        custo_g_inicial = 0
        custo_f_inicial = custo_g_inicial + self.heuristica(self.estado_inicial)

        heapq.heappush(fila_prioridade, (custo_f_inicial, id_contador, custo_g_inicial, self.estado_inicial, [self.estado_inicial]))
        custos_otimos[self.estado_inicial] = custo_g_inicial
        self.nos_visitados += 1

        solucao = None

        while fila_prioridade:
            custo_f_atual, _, custo_g_atual, estado_atual, caminho_atual = heapq.heappop(fila_prioridade)

            # Se achamos um caminho mais caro do que um já registrado anteriormente, ignoramos
            if custo_g_atual > custos_otimos.get(estado_atual, float('inf')):
                continue

            # Validação de meta
            if self.eh_meta(estado_atual):
                solucao = {
                    "caminho": caminho_atual,
                    "profundidade": len(caminho_atual) - 1,
                    "custo": custo_g_atual
                }
                break

            # Expansão do nó
            self.nos_expandidos += 1
            sucessores = self.obter_sucessores(estado_atual)
            self.total_filhos_gerados += len(sucessores)

            for proximo_estado, custo_movimento in sucessores:
                novo_custo_g = custo_g_atual + custo_movimento
                
                # Regra de atualização: se o estado é inédito ou achamos um trajeto mais barato (g menor)
                if proximo_estado not in custos_otimos or novo_custo_g < custos_otimos[proximo_estado]:
                    custos_otimos[proximo_estado] = novo_custo_g
                    self.nos_visitados += 1
                    id_contador += 1
                    
                    novo_custo_f = novo_custo_g + self.heuristica(proximo_estado)

                    heapq.heappush(fila_prioridade, (
                        novo_custo_f,
                        id_contador,
                        novo_custo_g,
                        proximo_estado,
                        caminho_atual + [proximo_estado]
                    ))

        tempo_fim = time.time()
        tempo_execucao = tempo_fim - tempo_inicio

        fator_ramificacao_medio = (self.total_filhos_gerados / self.nos_expandidos) if self.nos_expandidos > 0 else 0

        if solucao:
            solucao.update({
                "nos_expandidos": self.nos_expandidos,
                "nos_visitados": self.nos_visitados,
                "fator_ramificacao_medio": fator_ramificacao_medio,
                "tempo_execucao": tempo_execucao
            })
            return solucao
        else:
            return {
                "caminho": None,
                "profundidade": 0,
                "custo": None,
                "nos_expandidos": self.nos_expandidos,
                "nos_visitados": self.nos_visitados,
                "fator_ramificacao_medio": fator_ramificacao_medio,
                "tempo_execucao": tempo_execucao
            }

# --- Bloco de teste direto (Opcional) ---
if __name__ == "__main__":
    estado_inicial_teste = ['B', 'A', '_', 'A', 'B']
    puzzle = ReguaPuzzleBuscaAEstrela(estado_inicial_teste)
    resultado = puzzle.buscar()
    
    print("==================================================")
    print("         PROPRIEDADES DA SOLUÇÃO (A*)             ")
    print("==================================================")
    if resultado["caminho"]:
        for i, est in enumerate(resultado["caminho"]):
            print(f"  Passo {i}: {' '.join(est)}")
        print(f"\nProfundidade : {resultado['profundidade']}")
        print(f"Custo total  : {resultado['custo']}")
    else:
        print("Nenhuma solução encontrada.")
    print("--------------------------------------------------")
    print(f"Tempo de execução : {resultado['tempo_execucao']:.6f} s")
    print("==================================================")
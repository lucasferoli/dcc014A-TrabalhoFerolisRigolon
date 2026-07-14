import time
import sys
from collections import deque

class ReguaPuzzleBFS:
    def __init__(self, estado_inicial):
        self.estado_inicial = tuple(estado_inicial)
        self.N = (len(estado_inicial) - 1) // 2

        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0

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
            if idx_bloco == idx_vazio:
                continue

            distancia = abs(idx_vazio - idx_bloco)
            if distancia <= self.N:
                novo_estado = list(estado)
                novo_estado[idx_vazio], novo_estado[idx_bloco] = novo_estado[idx_bloco], novo_estado[idx_vazio]
                sucessores.append((tuple(novo_estado), distancia))

        return sucessores

    def buscar(self):
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0

        tempo_inicio = time.time()

        # Conjunto global de visitados para evitar loops de repetição de estados
        visitados = set()

        fila = deque([(self.estado_inicial, [self.estado_inicial], 0)])
        visitados.add(self.estado_inicial)
        self.nos_visitados += 1

        solucao = None

        while fila:
            estado_atual, caminho_atual, custo_atual = fila.popleft()

            if self.eh_meta(estado_atual):
                solucao = {
                    "caminho": caminho_atual,
                    "profundidade": len(caminho_atual) - 1,
                    "custo": custo_atual
                }
                break

            # Expansão do nó
            self.nos_expandidos += 1
            sucessores = self.obter_sucessores(estado_atual)
            self.total_filhos_gerados += len(sucessores)

            for proximo_estado, custo_movimento in sucessores:
                if proximo_estado not in visitados:
                    visitados.add(proximo_estado)
                    self.nos_visitados += 1

                    fila.append((
                        proximo_estado,
                        caminho_atual + [proximo_estado],
                        custo_atual + custo_movimento
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

if __name__ == "__main__":
    estado_inicial_teste = ['B', 'A', '_', 'A', 'B']

    print(f"Iniciando Busca em Largura (BFS) para o Estado Inicial: {estado_inicial_teste}\n")

    puzzle = ReguaPuzzleBFS(estado_inicial_teste)
    resultado = puzzle.buscar()

    print("==================================================")
    print("            PROPRIEDADES DA SOLUÇÃO (BFS)         ")
    print("==================================================")
    if resultado["caminho"]:
        print("Caminho encontrado:")
        for i, est in enumerate(resultado["caminho"]):
            print(f"  Passo {i}: {' '.join(est)}")
        print(f"\nProfundidade da Solução : {resultado['profundidade']}")
        print(f"Custo total da Solução  : {resultado['custo']}")
    else:
        print("Nenhuma solução encontrada.")

    print("--------------------------------------------------")
    print(f"Total de nós visitados        : {resultado['nos_visitados']}")
    print(f"Total de nós expandidos       : {resultado['nos_expandidos']}")
    print(f"Fator de ramificação médio     : {resultado['fator_ramificacao_medio']:.2f}")
    print(f"Tempo de execução             : {resultado['tempo_execucao']:.6f} segundos")
    print("==================================================")
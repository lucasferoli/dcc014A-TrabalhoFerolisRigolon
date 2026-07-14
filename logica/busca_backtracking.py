import time
import sys


# Aumenta o limite de recursão em tabuleiros grandes
sys.setrecursionlimit(10000)

class ReguaPuzzleBacktracking:
    def __init__(self, estado_inicial):
        self.estado_inicial = tuple(estado_inicial)
        self.N = (len(estado_inicial) - 1) // 2

        # Estatísticas globais
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0

        self.visitados_caminho_atual = set()

        # Melhor solução encontrada (caminho, custo)
        self.melhor_caminho = None
        self.melhor_custo = float('inf')

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

        # Verifica todas as posições possíveis na régua
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
        self.melhor_caminho = None
        self.melhor_custo = float('inf')
        self.visitados_caminho_atual = set()

        tempo_inicio = time.time()

        self._backtracking_recursivo(self.estado_inicial, [self.estado_inicial], 0)

        tempo_fim = time.time()
        tempo_execucao = tempo_fim - tempo_inicio

        # Cálculo do fator de ramificação médio
        fator_ramificacao_medio = (self.total_filhos_gerados / self.nos_expandidos) if self.nos_expandidos > 0 else 0

        return {
            "caminho": self.melhor_caminho,
            "profundidade": len(self.melhor_caminho) - 1 if self.melhor_caminho else 0,
            "custo": self.melhor_custo if self.melhor_caminho else None,
            "nos_expandidos": self.nos_expandidos,
            "nos_visitados": self.nos_visitados,
            "fator_ramificacao_medio": fator_ramificacao_medio,
            "tempo_execucao": tempo_execucao
        }

    def _backtracking_recursivo(self, estado_atual, caminho_atual, custo_atual):
        self.nos_visitados += 1

        if custo_atual >= self.melhor_custo:
            return

        if self.eh_meta(estado_atual):
            self.melhor_custo = custo_atual
            self.melhor_caminho = list(caminho_atual)
            return

        # Expansão do nó
        self.nos_expandidos += 1
        sucessores = self.obter_sucessores(estado_atual)
        self.total_filhos_gerados += len(sucessores)

        self.visitados_caminho_atual.add(estado_atual)

        sucessores.sort(key=lambda x: x[1])

        for proximo_estado, custo_movimento in sucessores:
            if proximo_estado not in self.visitados_caminho_atual:
                self._backtracking_recursivo(
                    proximo_estado,
                    caminho_atual + [proximo_estado],
                    custo_atual + custo_movimento
                )

        self.visitados_caminho_atual.remove(estado_atual)

if __name__ == "__main__":
    estado_inicial_teste = ['B', 'A', '_', 'A', 'B']

    print(f"Iniciando Busca Backtracking para o Estado Inicial: {estado_inicial_teste}\n")

    puzzle = ReguaPuzzleBacktracking(estado_inicial_teste)
    resultado = puzzle.buscar()

    print("==================================================")
    print("            PROPRIEDADES DA SOLUÇÃO               ")
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

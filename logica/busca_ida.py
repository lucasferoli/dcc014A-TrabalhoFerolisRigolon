import time
import sys

sys.setrecursionlimit(10000)

class ReguaPuzzleBuscaIDAEstrela:
    def __init__(self, estado_inicial):
        self.estado_inicial = tuple(estado_inicial)
        self.N = (len(estado_inicial) - 1) // 2

        # Estatísticas globais
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0
        self.custo_final = 0

    def eh_meta(self, estado):

        encontrou_A = False
        for char in estado:
            if char == 'A':
                encontrou_A = True
            elif char == 'B' and encontrou_A:
                return False
        return True

    def heuristica(self, estado):

        custo_h = 0
        encontrou_A = False
        for char in estado:
            if char == 'A':
                encontrou_A = True
            elif char == 'B' and encontrou_A:
                custo_h += 1
        return custo_h

    def obter_sucessores(self, estado):

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
                sucessores.append((tuple(novo_estado), distancia))

        return sucessores

    def buscar(self):
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0
        self.custo_final = 0

        tempo_inicio = time.time()

        limite_f = self.heuristica(self.estado_inicial)
        
        caminho_atual = [self.estado_inicial]
        visitados_ramo = {self.estado_inicial}
        self.nos_visitados += 1

        solucao = None

        while True:
            resultado, novo_limite = self._ida_recursivo(
                estado=self.estado_inicial, 
                custo_g=0, 
                limite_f=limite_f, 
                caminho=caminho_atual, 
                visitados_ramo=visitados_ramo
            )

            if resultado == "ENCONTRADO":
                solucao = {
                    "caminho": list(caminho_atual),
                    "profundidade": len(caminho_atual) - 1,
                    "custo": self.custo_final
                }
                break
            
            if resultado == "NAO_ENCONTRADO":
 
                break

            limite_f = novo_limite

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

    def _ida_recursivo(self, estado, custo_g, limite_f, caminho, visitados_ramo):
        f_atual = custo_g + self.heuristica(estado)

        if f_atual > limite_f:
            return "CORTE", f_atual

        if self.eh_meta(estado):
            self.custo_final = custo_g 
            return "ENCONTRADO", f_atual

        min_f_excedente = float('inf')
        self.nos_expandidos += 1
        sucessores = self.obter_sucessores(estado)
        self.total_filhos_gerados += len(sucessores)

        sucessores.sort(key=lambda x: self.heuristica(x[0]) + custo_g + x[1])

        for proximo_estado, custo_movimento in sucessores:
            if proximo_estado not in visitados_ramo:
                visitados_ramo.add(proximo_estado)
                caminho.append(proximo_estado)
                self.nos_visitados += 1

                resultado, limite_filho = self._ida_recursivo(
                    proximo_estado,
                    custo_g + custo_movimento,
                    limite_f,
                    caminho,
                    visitados_ramo
                )

                if resultado == "ENCONTRADO":
                    return "ENCONTRADO", limite_filho

                if limite_filho < min_f_excedente:
                    min_f_excedente = limite_filho

                
                caminho.pop()
                visitados_ramo.remove(proximo_estado)

        if min_f_excedente == float('inf'):
            return "NAO_ENCONTRADO", float('inf')

        return "CORTE", min_f_excedente

if __name__ == "__main__":
    estado_inicial_teste = ['B', 'A', '_', 'A', 'B'] 
    puzzle = ReguaPuzzleBuscaIDAEstrela(estado_inicial_teste)
    resultado = puzzle.buscar()
    
    print("==================================================")
    print("         PROPRIEDADES DA SOLUÇÃO (IDA*)           ")
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
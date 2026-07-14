import time

class ReguaPuzzleDLS:
    def __init__(self, estado_inicial):
        self.estado_inicial = tuple(estado_inicial)
        self.N = (len(estado_inicial) - 1) // 2

        # Estatísticas globais
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

    def buscar(self, limite_profundidade):
        self.nos_expandidos = 0
        self.nos_visitados = 0
        self.total_filhos_gerados = 0

        tempo_inicio = time.time()

        # Para evitar ciclos dentro do mesmo ramo ativo do caminho
        caminho_atual = [self.estado_inicial]
        visitados_ramo = {self.estado_inicial}

        solucao = self._dls_recursivo(
            self.estado_inicial,
            limite_profundidade,
            caminho_atual,
            visitados_ramo,
            custo_atual=0
        )

        tempo_fim = time.time()
        tempo_execucao = tempo_fim - tempo_inicio

        fator_ramificacao_medio = (self.total_filhos_gerados / self.nos_expandidos) if self.nos_expandidos > 0 else 0

        resultado = {
            "nos_expandidos": self.nos_expandidos,
            "nos_visitados": self.nos_visitados,
            "fator_ramificacao_medio": fator_ramificacao_medio,
            "tempo_execucao": tempo_execucao
        }

        if solucao:
            resultado.update(solucao)
        else:
            resultado.update({"caminho": None, "profundidade": 0, "custo": None})

        return resultado

    def _dls_recursivo(self, estado_atual, limite, caminho, visitados_ramo, custo_atual):
        self.nos_visitados += 1

        if self.eh_meta(estado_atual):
            return {
                "caminho": list(caminho),
                "profundidade": len(caminho) - 1,
                "custo": custo_atual
            }

        # Se o limite chegou a 0 e não é meta, corta a busca
        if limite <= 0:
            return None

        # Expansão do nó
        self.nos_expandidos += 1
        sucessores = self.obter_sucessores(estado_atual)
        self.total_filhos_gerados += len(sucessores)

        for proximo_estado, custo_movimento in sucessores:
            if proximo_estado not in visitados_ramo:
                visitados_ramo.add(proximo_estado)
                caminho.append(proximo_estado)

                resultado_filho = self._dls_recursivo(
                    proximo_estado,
                    limite - 1,
                    caminho,
                    visitados_ramo,
                    custo_atual + custo_movimento
                )

                if resultado_filho:
                    return resultado_filho

                caminho.pop()
                visitados_ramo.remove(proximo_estado)

        return None

if __name__ == "__main__":
    estado_inicial_teste = ['B', 'A', '_', 'A', 'B']

    limite = 10

    print(f"Iniciando Busca em Profundidade Limitada (DLS) com Limite = {limite}")
    print(f"Estado Inicial: {estado_inicial_teste}\n")

    puzzle = ReguaPuzzleDLS(estado_inicial_teste)
    resultado = puzzle.buscar(limite_profundidade=limite)

    print("==================================================")
    print("            PROPRIEDADES DA SOLUÇÃO (DLS)         ")
    print("==================================================")
    if resultado["caminho"]:
        print("Caminho encontrado:")
        for i, est in enumerate(resultado["caminho"]):
            print(f"  Passo {i}: {' '.join(est)}")
        print(f"\nProfundidade da Solução : {resultado['profundidade']}")
        print(f"Custo total da Solução  : {resultado['custo']}")
    else:
        print(f"Nenhuma solução encontrada dentro do limite {limite}.")

    print("--------------------------------------------------")
    print(f"Total de nós visitados        : {resultado['nos_visitados']}")
    print(f"Total de nós expandidos       : {resultado['nos_expandidos']}")
    print(f"Fator de ramificação médio     : {resultado['fator_ramificacao_medio']:.2f}")
    print(f"Tempo de execução             : {resultado['tempo_execucao']:.6f} segundos")
    print("==================================================")
# ==================== Importação de Bibliotecas ====================
from random import *

# ========== Debug ==========
debug_pop_ini = False
debug_ordenando_pop = False
debug_selecionar_pais = False
debug_roleta = False
debug_crossover = False
debug_mutacao_1 = False
debug_mutacao_2 = False
debug_sobrescrever_populacao = False
debug_por_geracao = False

# ==================== Classes e Métodos ====================
class Individuo():
    def __init__(self, tamanhoCromossomo, valorMaxCromossomo, geracao = 0):
        self.geracao = geracao
        self.notaAvaliacao = 0      # Valores de 0 a 100%
        self.tamanhoCromossomo = tamanhoCromossomo
        self.valorMaxCromossomo = valorMaxCromossomo
        self.cromossomos = []

        for i in range(tamanhoCromossomo):
            self.cromossomos.append(randrange(0,256,1))      # Gera genoma aleatório com valor entre 0 e 255

class Populacao():
    def __init__(self):
        self.populacao = []
        self.geracao = 0
        self.melhorGeral = Individuo(3, 255)        # Inicializa um indivíduo qualquer
        self.listaMelhoresDaGeracao = []

    def inicializarPopulacao(self, tamanhoCromossomo, valorMaxCromossomo, tamanhoPopulacao):
        self.tamanhoPopulacao = tamanhoPopulacao

        for i in range(tamanhoPopulacao):
            self.populacao.append(Individuo(tamanhoCromossomo, valorMaxCromossomo))

    def avaliarPopulacaoMaisEscura(self):
        notaMax = self.populacao[0].valorMaxCromossomo * self.populacao[0].tamanhoCromossomo        # Calculo da nota máxima possível

        for ind in range(self.tamanhoPopulacao):
            soma = 0
            
            for crom in range(self.populacao[0].tamanhoCromossomo):
                soma += self.populacao[ind].cromossomos[crom]
            if debug_pop_ini: print("Soma RGB Individuo %i: %i" % (ind, soma))

            somaEmPercentualDaNotaMax = (100 * soma) / notaMax

            self.populacao[ind].notaAvaliacao = 100 - (somaEmPercentualDaNotaMax)       # Tornando Inversamente Proporcional
            
            if debug_pop_ini: print("Nota do Individuo %i: %s" % (ind, str(self.populacao[ind].notaAvaliacao)))

    # def avaliarPopulacaoComModelo(self, modelo):
    #     self.modelo = modelo
    #             ...

    def ordenarPopulacaoPorNota(self):
        self.populacao = sorted(
            self.populacao,
            key = lambda populacao: populacao.notaAvaliacao,
            reverse = True
        )

    def melhorIndividuoGeral(self, melhorAtual):
        if melhorAtual.notaAvaliacao > self.melhorGeral.notaAvaliacao:
            self.melhorGeral = melhorAtual

        return self.melhorGeral

    def roletaViciada(self, pesos):
        somaPesos = 0
        posicaoEscolhida = -1

        for i in range(len(pesos)):
            somaPesos += self.populacao[i].notaAvaliacao
        
        valorSorteado = randrange(0, round(somaPesos)+1)

        if debug_roleta:
            print("Pesos: %s" % str(pesos))
            print("Len Pesos: %s" % str(len(pesos)))
            print("Soma dos Pesos Depois: %f" % somaPesos)
            print("Valor Sorteado: %s" % str(valorSorteado))

        while valorSorteado > 0:
            posicaoEscolhida += 1
            valorSorteado -= pesos[posicaoEscolhida]

        return posicaoEscolhida

    def selecionarPais(self, modo):
        if modo == "propFitness":
            if debug_selecionar_pais: print("[DEBUG] Modo de Seleção proporcional à Avaliação")

            pesos = []
            for i in range(len(self.populacao)):
                pesos.append(self.populacao[i].notaAvaliacao)
            posicaoEscolhida = self.roletaViciada(pesos)

            pai = self.populacao[posicaoEscolhida]

            return pai

        elif modo == "propRanking":
            if debug_selecionar_pais: print("[DEBUG] Modo de Seleção proporcional ao Ranking")

        else:
            if debug_selecionar_pais: print("[DEBUG] ERRO - Insira um modo de seleção válido!")
    
    def realizarCrossover(self, modo, pai1, pai2):
        filhos = []
        qtdPosicoesCorte = self.populacao[0].tamanhoCromossomo - 1

        if debug_crossover: print("Genoma Pai 1: %s" % pai1.cromossomos)
        if debug_crossover: print("Genoma Pai 2: %s" % pai2.cromossomos)

        if modo == "umPontoCorte":
            if debug_crossover: print("[DEBUG] Modo Ponto de Cruzamento Único escolhido")

            posicaoCorte = randrange(1,qtdPosicoesCorte+1,1)
            
            if debug_crossover: print("[DEBUG] Ponto de Corte: %s" % posicaoCorte)

            cromossomoFilho1 = pai1.cromossomos[0:posicaoCorte] + pai2.cromossomos[posicaoCorte::]       # Cromossomo do Filho 1
            cromossomoFilho2 = pai1.cromossomos[posicaoCorte::] + pai2.cromossomos[0:posicaoCorte]      # Cromossomo do Filho 2

            filhos = [
                Individuo(self.populacao[0].tamanhoCromossomo, self.populacao[0].valorMaxCromossomo, pai1.geracao + 1),
                Individuo(self.populacao[0].tamanhoCromossomo, self.populacao[0].valorMaxCromossomo, pai1.geracao + 1)
            ]
  
            filhos[0].cromossomos = cromossomoFilho1 
            filhos[1].cromossomos = cromossomoFilho2

        elif modo == "doisPontosCorte":
            if debug_crossover: print("[DEBUG] Modo Dois Pontos de Cruzamento escolhido")

        elif modo == "cruzamentoUniforme":
            if debug_crossover: print("[DEBUG] Modo de Cruzamento Uniforme escolhido")

        else:
            if debug_crossover: print("[DEBUG] ERRO - Insira um modo de crossover válido!")

        return filhos

    def realizarMutacao(self, filho, taxaPercMutacao):
        if debug_mutacao_1: print("[DEBUG Mutação] Antes da Mutação: %s" % filho.cromossomos)
        
        for crom in range(self.populacao[0].tamanhoCromossomo):
            sorteio = randrange(0,101,1)
            if debug_mutacao_2: print("Filho: %s \t\t| Sorteio: %s" % (str(filho.cromossomos), sorteio))
            
            if sorteio < taxaPercMutacao:      # Determina se haverá mutação ou não
                if debug_mutacao_2: print("[DEBUG Mutação] Houve Mutação!")
                filho.cromossomos[crom] = randrange(0, 256, 1)      # Gera alelo aleatório para o genoma do filho mudar

        if debug_mutacao_1: print("[DEBUG Mutação] Depois da Mutação: %s" % filho.cromossomos)
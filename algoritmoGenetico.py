# ==================== Importação de Bibliotecas ====================
from random import *
import matplotlib.pyplot as plt
import os

# ========== Limpa o terminal para uma melhor visualização ====================
os.system('cls' if os.name == 'nt' else 'clear')

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

        for i in range(self.tamanhoCromossomo):
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
            
            for crom in range(tamanhoCromossomo):
                soma += self.populacao[ind].cromossomos[crom]
            if debug_pop_ini: print("Soma RGB Individuo %i: %i" % (ind, soma))

            somaEmPercentualDaNotaMax = (100 * soma) / notaMax

            self.populacao[ind].notaAvaliacao = 100 - (somaEmPercentualDaNotaMax)       # Tornando Inversamente Proporcional
            
            if debug_pop_ini: print("Nota do Individuo %i: %s" % (ind, str(self.populacao[ind].notaAvaliacao)))

    # def avaliarPopulacaoComModelo(self, modelo):
    #     self.modelo = modelo

    #     for ind in range(self.tamanhoPopulacao):
    #         for crom in range(tamanhoCromossomo):
    #             cmsIndividuo = self.populacao[ind].cromossomos[crom]

    #             self.modelo[crom]
                
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
            for i in range(tamanhoPopulacao):
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
        qtdPosicoesCorte = tamanhoCromossomo - 1

        if debug_crossover: print("Genoma Pai 1: %s" % pai1.cromossomos)
        if debug_crossover: print("Genoma Pai 2: %s" % pai2.cromossomos)

        if modo == "umPontoCorte":
            if debug_crossover: print("[DEBUG] Modo Ponto de Cruzamento Único escolhido")

            posicaoCorte = randrange(1,qtdPosicoesCorte+1,1)
            
            if debug_crossover: print("[DEBUG] Ponto de Corte: %s" % posicaoCorte)

            cromossomoFilho1 = pai1.cromossomos[0:posicaoCorte] + pai2.cromossomos[posicaoCorte::]       # Cromossomo do Filho 1
            cromossomoFilho2 = pai1.cromossomos[posicaoCorte::] + pai2.cromossomos[0:posicaoCorte]      # Cromossomo do Filho 2

            filhos = [
                Individuo(tamanhoCromossomo, valorMaxCromossomo, pai1.geracao + 1),
                Individuo(tamanhoCromossomo, valorMaxCromossomo, pai1.geracao + 1)
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
        
        for crom in range(tamanhoCromossomo):
            sorteio = randrange(0,101,1)
            if debug_mutacao_2: print("Filho: %s \t\t| Sorteio: %s" % (str(filho.cromossomos), sorteio))
            
            if sorteio < taxaPercMutacao:      # Determina se haverá mutação ou não
                if debug_mutacao_2: print("[DEBUG Mutação] Houve Mutação!")
                filho.cromossomos[crom] = randrange(0, 256, 1)      # Gera alelo aleatório para o genoma do filho mudar

        if debug_mutacao_1: print("[DEBUG Mutação] Depois da Mutação: %s" % filho.cromossomos)


# ==================== Principal ====================

# De início não usaremos modelo, então a busca será pelo valor RGB mais escuro possível
# meuModelo = [255, 0, 50]        # Valor RGB do meu modelo
# tamanhoCromossomo = len(meuModelo)

tamanhoCromossomo = 3
valorMaxCromossomo = 255

tamanhoPopulacao = 20
taxaPercMutacao = 1      # 0 a 100%
numeroGeracoes = 100
modoSelecaoPais = "propFitness"     # Modos Possíveis: 'propFitness' ou 'propRanking'
modoCrossover = "umPontoCorte"      # Modos Possíveis: 'umPontoCorte' ou 'doisPontosCorte' ou 'cruzamentoUniforme'

besouros = Populacao()

# ---------- POPULACAO INICIAL ----------
besouros.inicializarPopulacao(tamanhoCromossomo, valorMaxCromossomo, tamanhoPopulacao)     # Criar População Inicial

if debug_pop_ini:
    # ---------- Visualizar Cromossomos da População Inicial ----------
    for individuo in range(len(besouros.populacao)):
        print("[DEBUG Pop.Ini.] Genoma do Indivíduo %i: %s" % (individuo, str(besouros.populacao[individuo].cromossomos)))

# besouros.avaliarPopulacaoComModelo(meuModelo)        # Avaliar População Inicial com base no modelo
besouros.avaliarPopulacaoMaisEscura()        # Avaliar População Inicial

if debug_ordenando_pop:
    print("---------- Populacao antes de Ordenar ----------")
    for indice in range(tamanhoPopulacao):
        print("> Indivíduo %i \t| Nota %s" % (indice, besouros.populacao[indice].notaAvaliacao))

besouros.ordenarPopulacaoPorNota()     # Ordenar População Inicial

if debug_ordenando_pop:
    print("\n---------- Populacao depois de Ordenar ----------")
    for indice in range(tamanhoPopulacao):
        print("> Indivíduo %i \t| Nota %s" % (indice, besouros.populacao[indice].notaAvaliacao))

melhorBesouro = besouros.melhorIndividuoGeral(besouros.populacao[0])      # Melhor Individuo

besouros.listaMelhoresDaGeracao.append(besouros.populacao[0])

print("---------- MELHOR BESOURO DA GERAÇÃO INICIAL ----------")
print("     > Genoma: %s" % str(besouros.populacao[0].cromossomos))
print("     > Nota: %s" % str(besouros.populacao[0].notaAvaliacao))
print("     > Geração: %s\n" % str(besouros.populacao[0].geracao))


# ---------- NOVAS GERACOES ----------
for ger in range(numeroGeracoes):
    pais = []
    filhos = []
    novaPopulacao = []

    pais.append(besouros.selecionarPais(modoSelecaoPais))            # Selecionar Pais (Roleta Viciada)
    pais.append(besouros.selecionarPais(modoSelecaoPais))            # Selecionar Pais (Roleta Viciada)

    # print("Geração dos Pais: %s" % pais[0].geracao)
    # print("Genoma do Pai 1: %s" % pais[0].cromossomos)
    # print("Genoma do Pai 2: %s" % pais[1].cromossomos)

    for novosIndividuos in range(round(tamanhoPopulacao/2)):
        filhos = besouros.realizarCrossover(modoCrossover, pais[0], pais[1])       # Realizar Crossover

        # print("Geração dos Filhos: %s" % filhos[0].geracao)
        # print("Genoma do Filho 1: %s" % filhos[0].cromossomos)
        # print("Genoma do Filho 2: %s\n" % filhos[1].filcromossomos)

        besouros.realizarMutacao(filhos[0], taxaPercMutacao)           # Realizar Mutação
        besouros.realizarMutacao(filhos[1], taxaPercMutacao)           # Realizar Mutação
        
        novaPopulacao.append(filhos[0])
        novaPopulacao.append(filhos[1])
    
    if debug_sobrescrever_populacao: print("Tamanho da Nova População: %s" % len(novaPopulacao))

    if debug_sobrescrever_populacao:
        print("População Inicial")
        for i in range(tamanhoPopulacao):
            print(besouros.populacao[i].cromossomos)
    
    besouros.populacao = list(novaPopulacao)        # Sobrescrever População

    if debug_sobrescrever_populacao:
        print("Nova População")
        for i in range(tamanhoPopulacao):
            print(besouros.populacao[i].cromossomos)

    besouros.avaliarPopulacaoMaisEscura()        # Avaliar Nova População

    besouros.ordenarPopulacaoPorNota()     # Ordenar Nova População

    melhorBesouro = besouros.melhorIndividuoGeral(besouros.populacao[0])      # Melhor Individuo
    
    besouros.listaMelhoresDaGeracao.append(besouros.populacao[0])
    
    if debug_por_geracao:
        print("---------- GERAÇÃO %i ----------" % ger)
        print("> Melhor Indivíduo da Geração: ")
        print("     > Genoma: %s" % str(besouros.populacao[0].cromossomos))
        print("     > Nota: %s" % str(besouros.populacao[0].notaAvaliacao))
        print("     > Geração: %s" % str(besouros.populacao[0].geracao))
        print("> Melhor Indivíduo Geral: ")
        print("     > Genoma: %s" % str(melhorBesouro.cromossomos))
        print("     > Nota: %s" % str(melhorBesouro.notaAvaliacao))
        print("     > Geração: %s\n" % str(melhorBesouro.geracao))


# ---------- RESULTADO ----------
print("---------- MELHOR BESOURO GERAL ----------")
print("     > Genoma: %s" % str(melhorBesouro.cromossomos))
print("     > Nota: %s" % str(melhorBesouro.notaAvaliacao))
print("     > Geração: %s\n" % str(melhorBesouro.geracao))

# ---------- Lista dos Melhores por Geração ----------
notasMelhores = []

for ger in range(numeroGeracoes):
    notasMelhores.append(besouros.listaMelhoresDaGeracao[ger].notaAvaliacao)
    # print("Geração: %s \t\t| Nota: %s" % (ger, besouros.listaMelhoresDaGeracao[ger].notaAvaliacao))

# ---------- Impressao do gráfico dos melhores de cada geração ----------
plt.plot(notasMelhores)
plt.title("Melhores de cada geração")
plt.xlabel("Geração")
plt.ylabel("Nota de Avaliação (%)")
plt.gcf().canvas.set_window_title("Algoritmo Genético - Besouros Escuros")

plt.show()
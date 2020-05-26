# ==================== Importação de Bibliotecas ====================
from algoritmoGenetico import *
import matplotlib.pyplot as plt

import os

# ========== Limpa o terminal para uma melhor visualização ====================
os.system('cls' if os.name == 'nt' else 'clear')

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


# ==================== RESULTADO ====================
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
"""
	Compilador miniC

Tipo de Compilador:
	Top-Down Descendente Recursivo Preditivo
"""

'''
	Proximos passos:
		1. Analise Estatica
			1. Declaracao de variaveis
				# realizar a leitura do codigo fonte e verificar a declaracao de variaveis
				#	Se encontrar uma declaracao
				#		adicionar a variavel na tabela de simbolos (tabSimb)
				#	Se encontrar um uso de variavel
				#		verificar a declaracao da variavel na tabela de simbolos (tabSimb)
				#	Dica: Usar o lexema do Lexico
		2. Geracao de codigo intermediario
			1. Geracao de comandos
			2. Interpretacao de comandos

		3. Maquina Virtual
'''
import Lexico
import Sintatico
import VirtualMachine
import argparse
import sys

class Main:
	"""docstring for main"""

	file = sys.argv[1]
	sin = Sintatico.Sintatico(file)
	codigo = sin.parse()
	
	# vt = VirtualMachine.VirtualMachine(codigo)
	# print('codigo')
	# print(codigo)
	# vt.transforma(codigo)
	# vt.executaQuadruplas()


	# file = sys.argv[1]
	# arquivo = open(file, 'r')
	# lexico = Lexico.Arquivo(arquivo.read())
	# token = Lexico.Token()
	# tk = 0
	# while(tk != 36):
	# #for x in range(1,30):
	# 	tk = lexico.getToken()
	# 	print('Token: ',token.msg[tk])
	# 	#print('\n\n')


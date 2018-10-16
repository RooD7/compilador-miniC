"""
	Compilador miniC

Tipo de Compilador:
	Top-Down Descendente Recursivo Preditivo
"""
import Lexico
import Sintatico
import argparse
import sys

class Main:
	"""docstring for main"""

	file = sys.argv[1]
	sin = Sintatico.Sintatico(file)
	sin.parse()
	
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


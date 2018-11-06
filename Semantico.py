'''
	Analisador Semantico
'''

'''
 for id temp2:
 	if id in tabSimb:
 		"erro"
 	else:
 		tabSimb[id] = (tosp1, integer(0))
'''

class ErroSemantico(Exception):
	"""docstring for ErroSemantico"""
	def __init__(self, tk):
		self.token = tk

	def __str__(self):
		return "ERRO: Semantico\n"

class TabSimb:
	pass

class Semantico:
	pass

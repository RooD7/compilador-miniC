'''
	Analisador Sintatico
'''
import Lexico

Token = Lexico.Token()
Atual = Lexico.Atual()

class ErroSintatico(Exception):
	"""docstring for ErroSintatico"""
	def __init__(self, tk):
		self.token = tk
		# Atual = Lexico.Atual()

	def __str__(self):
		return "ERRO: era esperado o Token "+str(Token.msg[self.token])+", mas veio o Token "+str(Token.msg[Atual.token])+": linha "+str(Atual.linha)+", coluna: "+str(Atual.coluna)+"\n"

class ErroSemantico(Exception):
	"""docstring for ErroSintatico"""
	def __init__(self, lex):
		self.lexema = lex
		# Atual = Lexico.Atual()

	def __str__(self):
		return "ERRO: a variavel '"+str(self.lexema)+"': linha "+str(Atual.linha)+", coluna: "+str(Atual.coluna)+"\n"


class Sintatico(object):
		
	def __init__(self, file):
		self.arquivo = open(file, 'r')
		self.lexico = Lexico.Arquivo(self.arquivo.read())
		self.tabSimb = {}
		self.temp = 0
		self.label = 0
		

	def parse(self):
		
		try:
			Atual.token = self.lexico.getToken()
			codigo = self.function()
			self.consome(Token.eof)
			print(codigo)
		except ErroSintatico as e:
			print(e)
			raise 
		self.arquivo.close()


	# OK
	def consome(self, tk):
		if(tk == Atual.token):
			print('####1 '+str(Atual.token)+' - '+str(Atual.lexema))
			Atual.token = self.lexico.getToken()
			print('####2 '+str(Atual.token)+' - '+str(Atual.lexema))
		else:
			raise ErroSintatico(tk)

	def geraTemp(self):
		self.temp += 1
		return '_temp'+str(self.temp)

	def geraLabel(self):
		self.label += 1
		return '_temp'+str(self.label)


	'''
		###############################
					Funcao main
		###############################
	'''
	# OK
	def function(self):
		lexema1 = self.type()
		self.consome(Token.ident)
		# if Atual.lexema in self.tabSimb:
		# 	raise ErroSemantico(Atual.lexema)
		self.consome(Token.abrePar)
		[bol1, lista1] = self.argList()
		self.consome(Token.fechaPar)
		[bol2, lista2, result2] = self.bloco()
		if bol1 and not bol2:
			return [lexema1+lista1+lista2,[]]
		elif bol1 and bol2:
			return [lexema1+lista1+lista2, result2]
		elif not bol1 and bol2:
			return [lexema1+lista2, result2]
		elif not bol1 and not bol2:
			return [lexema1, []]

	# OK
	def argList(self):
		if (Atual.token == Token.inte) or (Atual.token == Token.floate):
			lista1 = self.arg()
			[bol2, lista2] = self.restoArgList(lista1)
			if bol2:
				return [True, lista1+lista2]
			else:
				return [True, lista1]
		else:
			return [False, []]

	# OK
	def arg(self):
		lexema = self.type()
		if not Atual.lexema in self.tabSimb:
			raise ErroSemantico(Atual.lexema)
		self.consome(Token.ident)
		codigo = []
		codigo += lexema
		codigo += Atual.lexema
		return codigo

	# OK
	def restoArgList(self,f1):
		if(Atual.token == Token.virg):
			self.consome(Token.virg)
			[bol1, lista1] = self.argList()
			if bol1:
				return [True, lista1]
			else:
				return [True, []]
		else:
			return [False, f1]
		

	# OK ???
	def type(self):
		if(Atual.token == Token.inte):
			self.consome(Token.inte)
		# elif(Atual.token == Token.floate):
		else:
			self.consome(Token.floate)
		return [[],Atual.lexema]


	# OK
	def bloco(self):
		self.consome(Token.abreCha)
		[bol1, lista1, result2] = self.stmtList([])
		self.consome(Token.fechaCha)
		return [bol1, lista1, result2]

	# OK
	def stmtList(self, f1):
		if((Atual.token == Token.note) or (Atual.token == Token.abrePar) or 
			(Atual.token == Token.soma) or (Atual.token == Token.sub) or 
			(Atual.token == Token.ptoVirg) or (Atual.token == Token.ident) or 
			(Atual.token == Token.NUMint) or (Atual.token == Token.NUMfloat) or 
			(Atual.token == Token.breack) or (Atual.token == Token.continuee) or 
			(Atual.token == Token.returne) or (Atual.token == Token.foor) or 
			(Atual.token == Token.ife) or (Atual.token == Token.printe) or 
			(Atual.token == Token.scan) or (Atual.token == Token.whilee) or 
			(Atual.token == Token.abreCha)):
			result1 = self.stmt()
			[bol1, lista1, result2] = self.stmtList(result1)
			return [True, lista1, result2]
		elif((Atual.token == Token.inte) or (Atual.token == Token.floate)):
			print('declaration')
			print(Atual.token)
			[lista1, result1] = self.declaration()
			[bol2, lista2, result2] = self.stmtList(result1)
			return [True, lista1+lista2, result2]
		else:
			return [False, [], f1]

	# OK
	def stmt(self):
		print('--------Atual TOken')
		print(Atual.token)
		if((Atual.token == Token.printe) or (Atual.token == Token.scan)):
			return self.ioStmt()
		elif(Atual.token == Token.foor):
			return self.forStmt()
		elif(Atual.token == Token.whilee):
			return self.whileStmt()
		elif(Atual.token == Token.ife):
			return self.ifStmt()
		elif(Atual.token == Token.abreCha):
			return self.bloco()
		elif(Atual.token == Token.breack):
			self.consome(Token.breack)
			self.consome(Token.ptoVirg)
			codigo = []
			codigo += ['call','break',None,None]
			return [[], codigo]
		elif(Atual.token == Token.continuee):
			self.consome(Token.continuee)
			self.consome(Token.ptoVirg)
			codigo = []
			codigo += ['call','continue',None,None]
			return [[], codigo]
		elif(Atual.token == Token.returne):
			self.consome(Token.returne)
			[bol1, lista1, result1] = self.fator()
			self.consome(Token.ptoVirg)
			return [lista1, result1]
		elif(Atual.token == Token.ptoVirg):
			self.consome(Token.ptoVirg)
		 # elif((Atual.token == Token.note) or ((Atual.token == Token.soma) or 
			# (Atual.token == Token.sub) or ((Atual.token == Token.NUMint) or 
			# (Atual.token == Token.NUMfloat) or (Atual.token == Token.ident) or 
			# (Atual.token == Token.abrePar)))):
		else:
			[lista1, result1] = self.expr()
			self.consome(Token.ptoVirg)
			return [lista1, result1]

	'''
		###############################
			Descricao das intrucoes
		###############################
	'''

	'''
		declaracoes
	'''

	# OK
	def declaration(self):
		[lista1, result1] = self.type()
		[bol1, lista2, result2] = self.identList()
		self.consome(Token.ptoVirg)
		if bol1:
			return [lista1+lista2, result1+result2]
		else:
			return [lista1, result1]

	# OK
	def identList(self):
		self.tabSimb[Atual.lexema] = Atual.token
		self.consome(Token.ident)
		return self.restoIdentList(Atual.lexema)

	# OK
	def restoIdentList(self,f1):
		if(Atual.token == Token.virg):
			self.consome(Token.virg)
			self.tabSimb[Atual.lexema] = Atual.token
			self.consome(Token.ident)
			[bol1, lista1, result1] = self.restoIdentList(f1)
			return [bol1, lista1, f1+result1]
		else:
			return [False, [], f1]

	'''
		Comando FOR
	'''

	# OK
	def forStmt(self):
		self.consome(Token.foor)
		self.consome(Token.abrePar)
		[lista_OpExpr1, result_OpExpr1] = self.optExpr()
		self.consome(Token.ptoVirg)
		[lista_OpExpr2, result_OpExpr2] = self.optExpr()
		self.consome(Token.ptoVirg)
		[lista_OpExpr3, result_OpExpr3] = self.optExpr()
		self.consome(Token.fechaPar)
		lista_stmt = self.stmt()

		inicio1 	= self.geraLabel()
		inicio2 	= self.geraLabel()
		fim 		= self.geraLabel()
		codigo = []
		codigo += result_OpExpr1
		codigo += ['label', inicio1, None, None]
		codigo += ['if', result_OpExpr2, inicio2, fim]
		codigo += ['label', inicio2, None, None]
		codigo += lista_stmt
		codigo += result_OpExpr3
		codigo += ['jump', inicio1, None, None]
		codigo += ['label', fim, None, None]
		return [[],codigo]

	# OK
	def optExpr(self):
		if((Atual.token == Token.note) or (((Atual.token == Token.soma) or (Atual.token == Token.sub)) or 
		((Atual.token == Token.NUMint) or (Atual.token == Token.NUMfloat) or 
		(Atual.token == Token.ident) or (Atual.token == Token.abrePar)))):
			return self.expr()
		else:
			return []

	'''
		Comando de IO
	'''

	# OK
	def ioStmt(self):
		if(Atual.token == Token.scan):
			self.consome(Token.scan)
			self.consome(Token.abrePar)
			if not Atual.lexema in self.tabSimb:
				raise ErroSemantico(Atual.lexema)
			aux = Atual.lexema
			self.consome(Token.ident)

			#self.consome(Token.strg)
			#self.consome(Token.virg)
			#self.consome(Token.ident)
			
			self.consome(Token.fechaPar)
			self.consome(Token.ptoVirg)
			#novoTemp = self.geraTemp()
			codigo = ['call','scan', aux]
			return [[], codigo]
#############################
		# elif(Atual.token == Token.printe):
		else:
			self.consome(Token.printe)
			self.consome(Token.abrePar)
			[lista1, result1] = self.outList()
			codigo = ['call','print',result1]
			self.consome(Token.fechaPar)
			self.consome(Token.ptoVirg)
			return [[], codigo]

	# OK
	def outList(self):
		result1 = self.out()
		[bol2, lista2, result2] = self.restoOutList(result1)

		if not bol2:
			return [[], result1]
		else:
			return [lista2, result1+result2]
			

	# OK
	def out(self):
		if(Atual.token == Token.strg):
			aux = Atual.lexema
			self.consome(Token.strg)
		elif(Atual.token == Token.ident):
			if not Atual.lexema in self.tabSimb:
				raise ErroSemantico(Atual.lexema)
			aux = Atual.lexema
			self.consome(Token.ident)
		elif(Atual.token == Token.NUMint):
			aux = Atual.lexema
			self.consome(Token.NUMint)
		# elif(Atual.token == Token.NUMfloat):
		else:
			aux = Atual.lexema
			self.consome(Token.NUMfloat)
##############################
		cod = []
		cod += aux
		return cod

	# OK
	def restoOutList(self,f1):
		if(Atual.token == Token.virg):
			self.consome(Token.virg)
############################
			result1 = self.out()
			[bol2, lista2, result2] = self.restoOutList(f1)
			return [bol2, lista2, result1+result2]
		else:
			return [False, [], f1]

	''' 
		Comando WHILE
	'''

	# OK
	def whileStmt(self):
		self.consome(Token.whilee)
		self.consome(Token.abrePar)
		# self.expr()
		[lista, result] = self.expr()
		self.consome(Token.fechaPar)
		inicio1 	= self.geraLabel()
		inicio2 	= self.geraLabel()
		fim 		= self.geraLabel()
		# self.stmt()
		listaCom = self.stmt()
		codigo = []
		codigo += ['label', inicio1, None, None]
		codigo += lista
		codigo += ['if', result, inicio2, fim]
		codigo += ['label', inicio2, None, None]
		codigo += listaCom
		codigo += ['jump', inicio1, None, None]
		codigo += ['label', fim, None, None]
		return [[],codigo]


	'''
		Comando IF
	'''

	# OK
	def ifStmt(self):
		self.consome(Token.ife)
		self.consome(Token.abrePar)
		[lista_expr, result_expr] = self.expr()
		self.consome(Token.fechaPar)
		inicio_if 	= self.geraLabel()
		inicio_el 	= self.geraLabel()
		fim_if 		= self.geraLabel()
		lista_stmt = self.stmt()
		lista_else = self.elsePart(lista_stmt)
		codigo = []
		codigo += lista_expr
		codigo += ['if', result_expr, inicio_if, inicio_el]
		codigo += ['label', inicio_if, None, None]
		codigo += lista_stmt
		codigo += ['jump', fim_if, None, None]
		codigo += ['label', inicio_el, None, None]
		codigo += lista_else
		codigo += ['label', fim_if, None, None]
		return [[],codigo]


	# OK
	def elsePart(self, f1):
		if(Atual.token == Token.elsee):
			self.consome(Token.elsee)
			#[bol_stmt, lista_stmt, result_stmt] = self.stmt()
			return self.stmt()
		else:
			return [False, [], f1]

	'''
		###############################
					Expressoes
		###############################
	'''

	# OK
	def expr(self):
		[bol, lista, result]  = self.atrib()
		return [lista, result]

	# OK
	def atrib(self):
		[bol1, lista1, result1] = self.oor()
		[bol2, lista2, result2] = self.restoAtrib(result1)
		#verificar a condicao
		#if bol2:

		if not bol2:
			# return [bol1, lista1, result1]
			return [bol1, lista1, result1]
		# tem atribuicao
		elif not bol1:
			quad = ['=', result1, result2, None]
			# return [False, lista2+quad, result1] # nao left value
			return [False, lista2+quad, result1] # nao left value
		else:
			raise ErroSemantico(Atual.lexema)
			# ERRO


	# OK
	def restoAtrib(self, f1):
		#if((oor) and (Atual.token == Token.atrib)):
		if(Atual.token == Token.atrib):
			self.consome(Token.atrib)
			[bol1, lista1, f2] = self.atrib()
			novoTemp = self.geraTemp()
			quad = ['=', novoTemp, f1, f2]
###################
			return [bol1, lista1+quad, f2]
		else:
			return [True, [], f1]

	# OK
	def oor(self):
		[bol1, lista1, result1] = self.ande()
		[bol2, lista2, result2] = self.restoOr(result1)
		if (bol1 and bol2):
			return [True, lista1, result1]
		else:
			return [False, lista1+lista2, result2]

	# OK
	def restoOr(self, f1):
		if(Atual.token == Token.oor):
			self.consome(Token.oor)
			[bol1, lista1, f2] = self.ande()
			novoTemp = self.geraTemp()
			quad = ['||', novoTemp, f1, f2]
			[bol2, lista2, result] = self.restoOr(f1)
			if bol2:
				return [False, lista1, f2]
			else:
				return [False, lista1+quad+lista2, result]
		else:
			return [True, [], f1]

	# OK
	def ande(self):
		[bol1, lista1, result1] = self.note()
		[bol2, lista2, result2] = self.restoAnd(result1)
		if (bol1 and bol2):
			return [True, lista1, result1]
		else:
			return [False, lista1+lista2, result2]

	# OK
	def restoAnd(self, f1):
		if(Atual.token == Token.ande):
			self.consome(Token.ande)
			[bol1, lista1, f2] = self.note()
			novoTemp = self.geraTemp()
			quad = ['&&', novoTemp, f1, f2]
			[bol2, lista2, result] = self.restoAnd(f1)
			if bol2:
				return [False, lista1, f2]
			else:
				return [False, lista1+quad+lista2, result]
		else:
			return [True, [], f1]

	# OK
	def note(self):
		if(Atual.token == Token.note):
			self.consome(Token.note)
			[bol, lista, result] = self.note()
			novoTemp = self.geraTemp()
			quad = ['!', novoTemp,result, None]
			# Minha versao
			#return [True, lista+quad, novoTemp]
			# Versao Lucas
			return [False, lista+quad, novoTemp]
		else:
			return self.rel()

	# OK
	def rel(self):
		[bol1, lista1, result1] = self.add()
		[bol2, lista2, result2] = self.restoRel(result1)
		if (bol1 and bol2):
			return [True, lista1, result1]
		else:
			return [False, lista1+lista2, result2]

	# OK
	def restoRel(self, f1):
		if(Atual.token == Token.igual):
			self.consome(Token.igual)
			[bol1, lista1, f2] = self.add()
			novoTemp = self.geraTemp()
			quad = ['==', novoTemp, f1, f2]
		elif(Atual.token == Token.difer):
			self.consome(Token.difer)
			[bol1, lista1, f2] = self.add()
			novoTemp = self.geraTemp()
			quad = ['!=', novoTemp, f1, f2]
		elif(Atual.token == Token.menIgual):
			self.consome(Token.menIgual)
			[bol1, lista1, f2] = self.add()
			novoTemp = self.geraTemp()
			quad = ['<=', novoTemp, f1, f2]
		elif(Atual.token == Token.maiIgual):
			self.consome(Token.maiIgual)
			[bol1, lista1, f2] = self.add()
			novoTemp = self.geraTemp()
			quad = ['>=', novoTemp, f1, f2]
		elif(Atual.token == Token.menor):
			self.consome(Token.menor)
			[bol1, lista1, f2] = self.add()
			novoTemp = self.geraTemp()
			quad = ['<', novoTemp, f1, f2]
		elif(Atual.token == Token.maior):
			self.consome(Token.maior)
			[bol1, lista1, f2] = self.add()
			novoTemp = self.geraTemp()
			quad = ['>', novoTemp, f1, f2]
		else:
			return [True, [], f1]
#####################################
		return [False, lista1+quad, f2]

	# OK OK
	def add(self):
		[bol1, lista1, result1] = self.mult()
		[bol2, lista2, result2] = self.restoAdd(result1)
		if (bol1 and bol2):
			return [True, lista1, result1]
		else:
			return [False, lista1+lista2, result2]

	# OK OK
	def restoAdd(self, f1):
		if(Atual.token == Token.soma):
			self.consome(Token.soma)
			[bol1, lista2, f2] = self.mult()
			novoTemp = self.geraTemp()
			quad = ['+', novoTemp, f1, f2]
			[bol2, lista3, result] = self.restoAdd(novoTemp)
		elif(Atual.token == Token.sub):
			self.consome(Token.sub)
			[bol1, lista2, f2] = self.mult()
			novoTemp = self.geraTemp()
			quad = ['-', novoTemp, f1, f2]
			[bol2, lista3, result] = self.restoAdd(novoTemp)
		# Vazio
		else:
			return [True, [], f1]
		return [False, lista2+quad+lista3, result]


	# OK OK
	def mult(self):
		[bol1, lista1, result1] = self.uno()
		[bol2, lista2, result2] = self.restoMult(result1)
		if (bol1 and bol2):
			return [True, lista1, result1]
		else:
			return [False, lista1+lista2, result2]

	# # OK OK
	def restoMult(self, f1):
		if(Atual.token == Token.mult):
			self.consome(Token.mult)
			[bol1, lista2, f2] = self.uno()
			novoTemp = self.geraTemp()
			quad = ['*', novoTemp, f1, f2]
			[bol2, lista3, result] = self.restoMult(novoTemp)
		elif(Atual.token == Token.div):
			self.consome(Token.div)
			[bol1, lista2, f2] = self.uno()
			novoTemp = self.geraTemp()
			quad = ['/', novoTemp, f1, f2]
			[bol2, lista3, result] = self.restoMult(novoTemp)
		elif(Atual.token == Token.mod):
			self.consome(Token.mod)
			[bol1, lista2, f2] = self.uno()
			novoTemp = self.geraTemp()
			quad = ['%', novoTemp, f1, f2]
			[bol2, lista3, result] = self.restoMult(novoTemp)
		# Vazio
		else:
			return [True, [], f1]
		return [False, lista2+quad+lista3, result]


	# OK OK
	def uno(self):
		if(Atual.token == Token.soma):
			self.consome(Token.soma)
			[bol, lista, result] = self.uno()
			novoTemp = self.geraTemp()
			'''
				# geraTemp eh um gerador de variaveis temporarias, 
				# que nao possa ser declarada pelo usuario, sugestao (_temp1, _temp2,...)
				# sao variaveis que nao sao aceitas pela gramatica.
			'''
			quad = ['+', novoTemp,'0',result]
			return [False, lista+quad, novoTemp]

		elif(Atual.token == Token.sub):
			self.consome(Token.sub)
			[bol, lista, result] = self.uno()
			novoTemp = self.geraTemp()
			quad = ['-', novoTemp,'0',result]
			return [False, lista+quad, novoTemp]
		else:
			return self.fator()

	# OK OK
	def fator(self):
		if (Atual.token == Token.ident):
			if not Atual.lexema in self.tabSimb:
				raise ErroSemantico(Atual.lexema)
			aux = Atual.lexema
			self.consome(Token.ident)
			#novoTemp = self.geraTemp()
			#quad = ['+', novoTemp, 0, Atual.lexico.lexema]
			#return [True, quad, Atual.lexico.lexema]
			return [True, [], aux]
		elif(Atual.token == Token.abrePar):
			self.consome(Token.abrePar)
			aux = self.atrib()
			self.consome(Token.fechaPar)
			return aux
		elif (Atual.token == Token.NUMint):
			aux = Atual.lexema
			self.consome(Token.NUMint)
			#novoTemp = self.geraTemp()
			#quad = ['+', novoTemp, 0, Atual.lexico.lexema]
			#return [True, quad, Atual.lexico.lexema]
			return [False, [], aux]
		else:
			aux = Atual.lexema
			self.consome(Token.NUMfloat)
			#novoTemp = self.geraTemp()
			#quad = ['+', novoTemp, 0, Atual.lexico.lexema]
			#return [True, quad, Atual.lexico.lexema]
			return [False, [], aux]
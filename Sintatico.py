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
		return "ERRO: a variavel '"+str(self.lexema)+"' nao foi declarada: linha "+str(Atual.linha)+", coluna: "+str(Atual.coluna)+"\n"

class Sintatico(object):
		
	def __init__(self, file):
		self.arquivo = open(file, 'r')
		self.lexico = Lexico.Arquivo(self.arquivo.read())
		self.tabSimb = {}
		

	def parse(self):
		
		try:
			Atual.token = self.lexico.getToken()
			self.function()
			self.consome(Token.eof)
		except ErroSintatico as e:
			print(e)
			raise 
		self.arquivo.close()


	# OK
	def consome(self, tk):
		if(tk == Atual.token):
			Atual.token = self.lexico.getToken()
		else:
			raise ErroSintatico(tk)


	'''
		###############################
					Funcao main
		###############################
	'''
	# OK
	def function(self):
		self.type()
		self.consome(Token.ident)
		# if not Atual.lexema in self.tabSimb:
		# 	raise ErroSemantico(Atual.lexema)
		self.consome(Token.abrePar)
		self.argList()
		self.consome(Token.fechaPar)
		self.bloco()

	# OK
	def argList(self):
		if (Atual.token == Token.inte) or (Atual.token == Token.floate):
			self.arg()
			self.restoArgList()
		else:
			pass

	# OK
	def arg(self):
		self.type()
		if not Atual.lexema in self.tabSimb:
			raise ErroSemantico(Atual.lexema)
		self.consome(Token.ident)

	# OK
	def restoArgList(self):
		if(Atual.token == Token.virg):
			self.consome(Token.virg)
			self.argList()
		else:
			pass
		

	# OK ???
	def type(self):
		if(Atual.token == Token.inte):
			self.consome(Token.inte)
		# elif(Atual.token == Token.floate):
		else:
			self.consome(Token.floate)


	# OK
	def bloco(self):
		self.consome(Token.abreCha)
		self.stmtList()
		self.consome(Token.fechaCha)

	# OK
	def stmtList(self):
		if((Atual.token == Token.note) or (Atual.token == Token.abrePar) or 
			(Atual.token == Token.soma) or (Atual.token == Token.sub) or 
			(Atual.token == Token.ptoVirg) or (Atual.token == Token.ident) or 
			(Atual.token == Token.NUMint) or (Atual.token == Token.NUMfloat) or 
			(Atual.token == Token.breack) or (Atual.token == Token.continuee) or 
			(Atual.token == Token.returne) or (Atual.token == Token.inte) or 
			(Atual.token == Token.floate) or (Atual.token == Token.foor) or 
			(Atual.token == Token.ife) or (Atual.token == Token.printe) or 
			(Atual.token == Token.scan) or (Atual.token == Token.whilee) or 
			(Atual.token == Token.abreCha)):
			self.stmt()
			self.stmtList()
		else:
			pass

	# OK
	def stmt(self):
		if((Atual.token == Token.printe) or (Atual.token == Token.scan)):
			self.ioStmt()
		elif(Atual.token == Token.foor):
			self.forStmt()
		elif(Atual.token == Token.whilee):
			self.whileStmt()
		elif(Atual.token == Token.ife):
			self.ifStmt()
		elif(Atual.token == Token.abreCha):
			self.bloco()
		elif(Atual.token == Token.breack):
			self.consome(Token.breack)
			self.consome(Token.ptoVirg)
		elif(Atual.token == Token.continuee):
			self.consome(Token.continuee)
			self.consome(Token.ptoVirg)
		elif(Atual.token == Token.returne):
			self.consome(Token.returne)
			self.fator()
			self.consome(Token.ptoVirg)
		elif((Atual.token == Token.inte) or (Atual.token == Token.floate)):
			self.declaration()
		elif(Atual.token == Token.ptoVirg):
			self.consome(Token.ptoVirg)
		 # elif((Atual.token == Token.note) or ((Atual.token == Token.soma) or 
			# (Atual.token == Token.sub) or ((Atual.token == Token.NUMint) or 
			# (Atual.token == Token.NUMfloat) or (Atual.token == Token.ident) or 
			# (Atual.token == Token.abrePar)))):
		else:
			self.expr()
			self.consome(Token.ptoVirg)	

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
		self.type()
		self.identList()
		self.consome(Token.ptoVirg)

	# OK
	def identList(self):
		self.tabSimb[Atual.lexema] = Atual.token
		self.consome(Token.ident)
		self.restoIdentList()

	# OK
	def restoIdentList(self):
		if(Atual.token == Token.virg):
			self.consome(Token.virg)
			self.tabSimb[Atual.lexema] = Atual.token
			self.consome(Token.ident)
			self.restoIdentList()
		else:
			pass

	'''
		Comando FOR
	'''

	# OK
	def forStmt(self):
		self.consome(Token.foor)
		self.consome(Token.abrePar)
		self.optExpr()
		self.consome(Token.ptoVirg)
		self.optExpr()
		self.consome(Token.ptoVirg)
		self.optExpr()
		self.consome(Token.fechaPar)
		self.stmt()

	# OK
	def optExpr(self):
		if((Atual.token == Token.note) or (((Atual.token == Token.soma) or (Atual.token == Token.sub)) or 
		((Atual.token == Token.NUMint) or (Atual.token == Token.NUMfloat) or 
		(Atual.token == Token.ident) or (Atual.token == Token.abrePar)))):
			self.expr()
		else:
			pass

	'''
		Comando de IO
	'''

	# OK
	def ioStmt(self):
		if(Atual.token == Token.scan):
			self.consome(Token.scan)
			self.consome(Token.abrePar)
			self.consome(Token.strg)
			self.consome(Token.virg)
			if not Atual.lexema in self.tabSimb:
				raise ErroSemantico(Atual.lexema)
			self.consome(Token.ident)
			self.consome(Token.fechaPar)
			self.consome(Token.ptoVirg)
		# elif(Atual.token == Token.printe):
		else:
			self.consome(Token.printe)
			self.consome(Token.abrePar)
			self.outList()
			self.consome(Token.fechaPar)
			self.consome(Token.ptoVirg)

	# OK
	def outList(self):
		self.out()
		self.restoOutList()

	# OK
	def out(self):
		if(Atual.token == Token.strg):
			self.consome(Token.strg)
		elif(Atual.token == Token.ident):
			if not Atual.lexema in self.tabSimb:
				raise ErroSemantico(Atual.lexema)
			self.consome(Token.ident)
		elif(Atual.token == Token.NUMint):
			self.consome(Token.NUMint)
		# elif(Atual.token == Token.NUMfloat):
		else:
			self.consome(Token.NUMfloat)

	# OK
	def restoOutList(self):
		if(Atual.token == Token.virg):
			self.consome(Token.virg)
			self.out()
			self.restoOutList()
		else: 
			pass

	''' 
		Comando WHILE
	'''

	# OK
	def whileStmt(self):
		self.consome(Token.whilee)
		self.consome(Token.abrePar)
		self.expr()
		(lista, result) = self.expr()
		self.consome(Token.fechaPar)
		inicio 	= self.geraLabel()
		fim 	= self.geraLabel()
		self.stmt()
		listaCom = self.stmt(inicio, fim)
		codigo = []
		codigo += ('label', inicio, None, None)
		codigo += lista
		codigo += ('if', result, None, fim)
		codigo += listaCom
		codigo += ('jump', inicio, None, None)
		codigo += ('label', fim, None, None)
		return codigo


	'''
		Comando IF
	'''

	# OK
	def ifStmt(self):
		self.consome(Token.ife)
		self.consome(Token.abrePar)
		self.expr()
		self.consome(Token.fechaPar)
		self.stmt()
		self.elsePart()


	# OK
	def elsePart(self):
		if(Atual.token == Token.elsee):
			self.consome(Token.elsee)
			self.stmt()
		else:
			pass

	'''
		###############################
					Expressoes
		###############################
	'''

	# OK
	def expr(self):
		self.atrib()

	# OK
	def atrib(self):
		#r1 = self.oor()
		[boo1, lista1, result1] = self.oor()
		self.restoAtrib(r1)
		[boo2, lista2, result2] = self.restoAtrib()
		if not boo2:
			return [boo1, lista1, result1]
		# tem atribuicao
		elif boo1:
			opera = ['=', result1, result2, None]
			lista3 = lista2 + opera
			return [False, lista3, result1] # nao left value
		else:
			pass
			# ERRO


	# OK
	def restoAtrib(self, oor):
		if((oor) and (Atual.token == Token.atrib)):
			self.consome(Token.atrib)
			self.atrib()
		else:
			pass

	# OK
	def oor(self):
		r1 = self.ande()
		r2 = self.restoOr()
		if (r1 and r2):
			return True
		else:
			return False

	# OK
	def restoOr(self):
		if(Atual.token == Token.oor):
			self.consome(Token.oor)
			self.ande()
			self.restoOr()
		else:
			return True
		return False

	# OK
	def ande(self):
		r1 = self.note()
		r2 = self.restoAnd()
		if (r1 and r2):
			return True
		else:
			return False

	# OK
	def restoAnd(self):
		if(Atual.token == Token.ande):
			self.consome(Token.ande)
			self.note()
			self.restoAnd()
		else:
			return True
		return False

	# OK
	def note(self):
		if(Atual.token == Token.note):
			self.consome(Token.note)
			self.note()
		else:
			return self.rel()

	# OK
	def rel(self):
		[bol1, lista1, result1] = self.add()
		[bol2, lista2, result2] = self.restoRel()
		if (bol1 and bol2):
			return [True, lista1+lista2, result2]
		else:
			return [False, lista1+lista2, result2]

	# OK
	def restoRel(self):
		if(Atual.token == Token.igual):
			self.consome(Token.igual)
			[bol1, lista1, result1] = self.add()
			quad = ['==', f2, f1, f2]
		elif(Atual.token == Token.difer):
			self.consome(Token.difer)
			self.add()
		elif(Atual.token == Token.menIgual):
			self.consome(Token.menIgual)
			self.add()
		elif(Atual.token == Token.maiIgual):
			self.consome(Token.maiIgual)
			self.add()
		elif(Atual.token == Token.menor):
			self.consome(Token.menor)
			self.add()
		elif(Atual.token == Token.maior):
			self.consome(Token.maior)
			[bol1, lista1, result1] = self.add()
		else:
			return [True, [], f1]
		return False

	# OK OK
	def add(self):
		[bol1, lista1, result1] = self.mult()
		[bol2, lista2, result2] = self.restoAdd(result1)
		if (bol1 and bol2):
			return [True, lista1+lista2, result2]
		else:
			return [False, lista1+lista2, result2]

	# OK OK
	def restoAdd(self):
		if(Atual.token == Token.soma):
			self.consome(Token.soma)
			[lista2, f2] = self.mult()
			quad = ['+', f2, f1, f2]
			[lista3, result] = self.restoAdd(f2)
		elif(Atual.token == Token.sub):
			self.consome(Token.sub)
			[lista2, f2] = self.mult()
			quad = ['-', f2, f1, f2]
			[lista3, result] = self.restoAdd(f2)
		# Vazio
		else:
			return [True, [], f1]
		return [False, lista2+quad+lista3, result]


	# OK OK
	def mult(self):
		[bol1, lista1, result1] = self.uno()
		[bol2, lista2, result2] = self.restoMult(result1)
		if (bol1 and bol2):
			return [True, lista1+lista2, result2]
		else:
			return [False, lista1+lista2, result2]

	# # OK OK
	def restoMult(self, f1):
		if(Atual.token == Token.mult):
			self.consome(Token.mult)
			[lista2, f2] = self.uno()
			quad = ['*', f2, f1, f2]
			[lista3, result] = self.restoMult(f2)
		elif(Atual.token == Token.div):
			self.consome(Token.div)
			[lista2, f2] = self.uno()
			quad = ['/', f2, f1, f2]
			[lista3, result] = self.restoMult(f2)
		elif(Atual.token == Token.mod):
			self.consome(Token.mod)
			[lista2, f2] = self.uno()
			quad = ['%', f2, f1, f2]
			[lista3, result] = self.restoMult(f2)
		# Vazio
		else:
			return [True, [], f1]
		return [False, lista2+quad+lista3, result]


	# OK
	def uno(self):
		if(Atual.token == Token.soma):
			self.consome(Token.soma)
			self.uno()
		elif(Atual.token == Token.sub):
			self.consome(Token.sub)
			self.uno()

			[left, lista, res] = self.uno()
			novoTemp = self.geraTemp()
			'''
				# geraTemp eh um gerador de variaveis temporarias, 
				# que nao possa ser declarada pelo usuario, sugestao (_temp1, _temp2,...)
				# sao variaveis que nao sao aceitas pela gramatica.
			'''
			quad = ['-', novoTemp,'0',res]
			novaLista = lista + quad
			return [False, novaLista, novoTemp]
		else:
			return self.fator()
		return False

	# OK
	def fator(self):
		if (Atual.token == Token.ident):
			if not Atual.lexema in self.tabSimb:
				raise ErroSemantico(Atual.lexema)
			self.consome(Token.ident)
			return [True, [], Atual.lexico.lexema]
		elif(Atual.token == Token.abrePar):
			self.consome(Token.abrePar)
			aux = [False, lista, res] = self.atrib()
			self.consome(Token.fechaPar)
			return aux
		elif (Atual.token == Token.NUMint):
			self.consome(Token.NUMint)
			return [False, [], Atual.lexico.lexema]
		else:
			self.consome(Token.NUMfloat)
			return [False, [], Atual.lexico.lexema]
		return False
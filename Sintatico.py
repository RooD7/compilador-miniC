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

class Sintatico(object):
		
	def __init__(self, file):
		arquivo = open(file, 'r')
		self.lexico = Lexico.Arquivo(arquivo.read())
		

	def parse(self):
		
		try:
			Atual.token = self.lexico.getToken()
			self.function()
			consome(Token.eof)
		except ErroSintatico as e:
			print(e)
			raise 
		arquivo.close()


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
		elif(Atual.token == Token.floate):
			self.consome(Token.floate)

	# OK
	def bloco(self):
		self.consome(Token.abreCha)
		self.stmtList()
		self.consome(Token.fechaCha)

	# OK
	def stmtList(self):
		if((Atual.token == Token.note) or 
		(Atual.token == Token.abrePar) or
		(Atual.token == Token.soma) or
		(Atual.token == Token.sub) or
		(Atual.token == Token.ptoVirg) or
		(Atual.token == Token.ident) or
		(Atual.token == Token.NUMint) or
		(Atual.token == Token.NUMfloat) or
		(Atual.token == Token.breack) or
		(Atual.token == Token.continuee) or
		(Atual.token == Token.inte) or
		(Atual.token == Token.floate) or
		(Atual.token == Token.foor) or
		(Atual.token == Token.ife) or
		(Atual.token == Token.printe) or
		(Atual.token == Token.scan) or
		(Atual.token == Token.whilee) or
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
			consome(Token.breack)
		elif(Atual.token == Token.continuee):
			consome(Token.continuee)
		elif((Atual.token == Token.inte) or (Atual.token == Token.floate)):
			self.declaration()
		elif(Atual.token == Token.ptoVirg):
			consome(Token.ptoVirg)
		elif((Atual.token == Token.note) or ((Atual.token == Token.soma) or (Atual.token == Token.sub) or 
			((Atual.token == Token.NUMint) or (Atual.token == Token.NUMfloat) or 
				(Atual.token == Token.ident) or (Atual.token == Token.abrePar) ) )):
			self.expr()
			consome(Token.ptoVirg)	

	'''
		###############################
			Descricao das intrucoes
		###############################
	'''

	'''
		declaraçoes
	'''

	# OK
	def declaration(self):
		self.type()
		self.identList()
		self.consome(Token.ptoVirg)

	# OK
	def identList(self):
		self.consome(Token.ident)
		self.restoIdentList()

	# OK
	def restoIdentList(self):
		if(Atual.token == Token.virg):
			self.consome(Token.virg)
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
		if((Atual.token == Token.note) or ((Atual.token == Token.soma) or (Atual.token == Token.sub) or 
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
			self.consome(Token.ident)
			self.consome(Token.fechaPar)
			self.consome(Token.ptoVirg)
		elif(Atual.token == Token.printe):
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
			self.consome(Token.ident)
		elif(Atual.token == Token.NUMint):
			self.consome(Token.NUMint)
		elif(Atual.token == Token.NUMfloat):
			self.consome(Token.NUMfloat)
		# else:
		# 	raise Exception('ERRO! ARG <out> | '+str(Atual.token))

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
		self.consome(Token.fechaPar)
		self.stmt()

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
		self.oor()
		self.restoAtrib()

	# OK
	def restoAtrib(self):
		if(Atual.token == Token.igual):
			self.consome(Token.igual)
			self.atrib()
		else:
			pass

	# OK
	def oor(self):
		self.ande()
		self.restoOr()

	# OK
	def restoOr(self):
		if(Atual.token == Token.oor):
			self.consome(Token.oor)
			self.ande()
			self.restoOr()
		else:
			pass

	# OK
	def ande(self):
		self.note()
		self.restoAnd()

	# OK
	def restoAnd(self):
		if(Atual.token == Token.ande):
			self.consome(Token.ande)
			self.note()
			self.restoAnd()
		else:
			pass

	# OK
	def note(self):
		if(Atual.token == Token.note):
			self.consome(Token.note)
			self.note()
		else:
			self.rel()

	# OK
	def rel(self):
		self.add()
		self.restoRel()

	# OK
	def restoRel(self):
		if(Atual.token == Token.igual):
			self.consome(Token.igual)
			self.add()
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
			self.add()
		else:
			pass

	# OK
	def add(self):
		self.mult()
		self.restoAdd()

	# OK
	def restoAdd(self):
		if(Atual.token == Token.soma):
			self.consome(Token.soma)
			self.mult()
			self.restoAdd()
		elif(Atual.token == Token.sub):
			self.consome(Token.sub)
			self.mult()
			self.restoAdd()
		else:
			pass

	# OK
	def mult(self):
		self.uno()
		self.restoMult()

	#
	'''
		Traducao usando sintese (pai 'sintetiza' atributos dos filhos)
	'''
	# OK
	def restoMult(self):
		if(Atual.token == Token.mult):
			self.consome(Token.mult)
			self.uno()
			self.restoMult()
		elif(Atual.token == Token.div):
			self.consome(Token.div)
			self.uno()
			self.restoMult()
		elif(Atual.token == Token.mod):
			self.consome(Token.mod)
			self.uno()
			self.restoMult()
		else:
			pass

	# OK
	def uno(self):
		if(Atual.token == Token.soma):
			self.consome(Token.soma)
			self.uno()
		elif(Atual.token == Token.sub):
			self.consome(Token.sub)
			self.uno()
		else:
			self.fator()

	# OK
	def fator(self):
		if (Atual.token == Token.ident):
			self.consome(Token.ident)
		elif(Atual.token == Token.abrePar):
			self.consome(Token.abrePar)
			self.atrib()
			self.consome(Token.fechaPar)
		elif (Atual.token == Token.NUMint):
			self.consome(Token.NUMint)
		elif (Atual.token == Token.NUMfloat):
			self.consome(Token.NUMfloat)
		# else:
		# 	raise Exception('ERRO! ARG <fator> | '+str(Atual.token))

	'''
	def entra():
		consome(Token.input)
		consome(Token.abrePar)
		if (Atual.token == Token.strg):
			print(Token.lexema)
		consome(Token.strg)
		consome(Token.virg)
		if(Atual.token == Token.ident):
			res = input()
			tabSimb[Atual.lexema] = float(res)
			consome(Token.ident)
			consome(Token.fechaPar)
			consome(Token.ptoVirg)
	'''
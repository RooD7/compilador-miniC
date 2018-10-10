def parse(self):
	apenArquivo()
	getToken()
	self.soma()
	consome(tkEOF)
	fechaAqrquivo()


#
def consome(self):
	if(Token == Atual.token):
		getToken()
	else:
		print("ERRO: era esperado o Token "+msg(Token+", mas veio o Token "+msg(Atual.token)+": linha "+Atual.linha+", coluna: "Atual.coluna+"\n"))

#
def atrib(self):
	pass

'''
	###############################
				Funcao main
	###############################
'''

'''
	###############################
		Descricao das intrucoes
	###############################
'''

'''
	declaracoes
'''

'''
	Comando FOR
'''

'''
	Comando de IO
'''

''' 
	Comando WHILE
'''

def whileStmt(self):
	consome(Token.whilee)
	consome(Token.abrePar)
	self.expr()
	consome(Token.fechaPar)
	self.stmt()

'''
	Comando IF
'''
# OK
def ifStmt(self):
	if(Atual.token == Token.ife):
		consome(Token.ife)
		consome(Token.abrePar)
		self.expr()
		consome(Token.fechaPar)
		self.stmt()
		self.elsePart()


# OK
def elsePart(self):
	if(Atual.token == Token.elsee):
		consome(Token.elsee)
		self.stmt()

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
		consome(Token.igual)
		self.atrib()

# OK
def oor(self):
	self.ande()
	self.restoOr()

# OK
def restoOr(self):
	if(Atual.token == Token.oor):
		consome(Token.oor)
		self.ande()
		self.restoOr()

# OK
def ande(self):
	self.note()
	self.restoAnd()

# OK
def restoAnd(self):
	if(Atual.token == Token.ande):
		consome(Token.ande)
		self.note()
		self.restoAnd()

# OK
def note(self):
	if(Atual.token == Token.note):
		consome(Token.note)
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
		consome(Token.igual)
		self.add()
	elif(Atual.token == Token.difer):
		consome(Token.difer)
		self.add()
	elif(Atual.token == Token.menIgual):
		consome(Token.menIgual)
		self.add()
elif(Atual.token == Token.maiIgual):
		consome(Token.maiIgual)
		self.add()
	elif(Atual.token == Token.menor):
		consome(Token.menor)
		self.add()
elif(Atual.token == Token.maior):
		consome(Token.maior)
		self.add()

# OK ??
def add(self):
	res1 = self.mult()
	res2 = self.restoAdd()
	res = res1 + res2
	return res

# OK
def restoAdd(self):
	if(Atual.token == Token.soma):
		consome(Token.soma)
		r1 = self.mult()
		r2 = self.restoAdd()
		res = r1 + r2
		return res
	elif(Atual.token == Token.sub):
		consome(Token.sub)
		r1 = self.mult()
		r2 = self.restoAdd()
		res = r1 - r2
		return res	

# OK ???
def mult(self):
	r1 = uno()
	r2 = restoMult()
	res = r1 * r2
	return res

#
'''
	Traducao usando sintese (pai 'sintetiza' atributos dos filhos)
'''

# OK
def restoMult(self):
	if(Atual.token == Token.mult):
		consome(Token.mult)
		uno()
		r1 = mult()
		r2 = restoMult()
		res = r1 * r2
		return res
	elif(Atual.token == Token.div):
		consome(Token.div)
		r1 = uno()
		r2 = restoMult()
		res = r1 / r2
		return res
	elif(Atual.token == Token.mod):
		consome(Token.mod)
		r1 = uno()
		r2 = restoMult()
		res = r1 % r2
		return res

'''
	Traducao usando heranca (filho 'herda' atributo do pai)
# OK ''
 def restoMult(r1):
 	if(Atual.token == Token.mult):
 		consome(Token.mult)
 		r2 = uno()
 		res = r1 * r2
 		r3 = restoMult(res)
 		return r3
'''

# OK
def uno(self):
	if(Atual.token == Token.soma):
		consome(Token.soma)
		uno()
	elif(Atual.token == Token.sub):
		consome(Token.sub)
		uno()
	else:
		fator()

# OK
def fator(self):
	if (Atual.token == Token.ident):
		if (Atual.lexema in tabSimb):
			res = tabSimb[Atual.lexema]
		else:
			raise Exception("variavel nao declarada")
		consome(Token.ident)
	elif(Atual.token == Token.abrePar):
		consome(Token.abrePar)
		res = self.atrib()
		consome(Token.fechaPar)
	elif (Atual.token == Token.NUMint):
		res = int(Atual.lexema)
		consome(Token.NUMint)
	elif (Atual.token == Token.NUMfloat):
		res = float(Atual.lexema)
		consome(Token.NUMfloat)
	return res

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
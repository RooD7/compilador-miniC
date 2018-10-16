class Token:
	erro		=  0 ## erro
	abrePar 	=  1 ## abre parenteses
	fechaPar 	=  2 ## fecha parenteses
	abreCha 	=  3 ## abre chaves
	fechaCha 	=  4 ## fecha chaves
	ident		=  5 ## identificador (variavel)
	inte		=  6 ## int
	floate		=  7 ## float
	breack		=  8 ## break
	continuee	=  9 ## continue
	ptoVirg		= 10 ## ponto e virgula
	virg		= 11 ## virgula
	foor		= 12 ## for
	scan		= 13 ## scan
	printe		= 14 ## print
	strg		= 15 ## str
	NUMint		= 16 ## numero inteiro
	NUMfloat	= 17 ## numero float
	whilee		= 18 ## while
	ife			= 19 ## if
	elsee		= 20 ## else
	igual		= 21 ## igual
	difer		= 22 ## diferente
	atrib		= 23 ## atributo
	menIgual	= 24 ## menor igual
	maiIgual	= 25 ## maior igual
	menor		= 26 ## menor
	maior		= 27 ## maior
	oor 		= 28 ## or
	ande		= 29 ## and
	note		= 30 ## not
	soma		= 31 ## soma
	sub			= 32 ## subtracao
	mult		= 33 ## multiplicacao
	div			= 34 ## divisao
	mod			= 35 ## mod
	eof			= 36 ## eof
	returne		= 37 ## return
	

	msg = ('erro','(',')','{','}','IDENT','int','float','break','continue',';',',','for','scan','print','STR','NUMint','NUMfloat','while','if','else','==','!=','=','<=','>=','<','>','||','&&','!','+','-','*','/','%','EOF')

class Atual:
	linha	= 1
	coluna	= 0
	token	= 0
	lexema	= ''

class Arquivo:
	nome	= None
	arq		= None
	linha	= None
	cursor	= None

	def __init__(self, arq):
		self.arq = arq

	def getToken(self):
		estado = 1
		prev = ''
		while(True):
			#print('Linha atual: ',Atual.linha)
			### eof
			if self.arq is '':
				Atual.token = Token.eof
				return Token.eof
			else:
				car = self.arq[0]
				self.arq = self.arq[1:]
				
			Atual.lexema += car
			Atual.coluna += 1

			#print('LINHA = ',Atual.linha)
			#print('CAR = ',car)
			#print('COLUNA = ',Atual.coluna)
			#print('LEXEMA = ',Atual.lexema)
			#print('TOKEN = ',Atual.token)

			if(estado == 1):
				if(car == '\n'):
					Atual.linha += 1
					Atual.coluna = 0
				if(car in (' ','\t')):
					continue
				#break
				elif(car.lower() == 'b'):
					prev = 'b'
					estado = 26
				#continue
				elif(car.lower() == 'c'):
					prev = 'c'
					estado = 27
				#int, if
				elif(car.lower() == 'i'):
					prev = 'i'
					estado = 12
				#else
				elif(car.lower() == 'e'):
					prev = 'e'
					estado = 21
				#float, for
				elif(car.lower() == 'f'):
					prev = 'f'
					estado = 13
				#print
				elif(car.lower() == 'p'):
					prev = 'p'
					estado = 15
				#scan
				elif(car.lower() == 's'):
					prev = 's'
					estado = 16
				#while
				elif(car.lower() == 'w'):
					prev = 'w'
					estado = 17
				#return
				elif(car.lower() == 'r'):
					prev = 'r'
					estado = 28
				#strg
				elif(car.lower() == '"'):
					prev = '"'
					estado = 18
				# div, /*, //
				elif(car == '/'):
					prev = '/'
					estado = 10
				# !, !=
				elif(car == '!'):
					prev = '!'
					estado = 20
				# >, >=
				elif(car == '>'):
					prev = '>'
					estado = 22
				# <, <=
				elif(car == '<'):
					prev = '<'
					estado = 23
				# ||
				elif(car == '|'):
					prev = '|'
					estado = 24
				# &&
				elif(car == '&'):
					prev = '&'
					estado = 25
				elif(car == ','):
					return Token.virg
				elif(car == ';'):
					return Token.ptoVirg
				elif(car == '('):
					return Token.abrePar
				elif(car == ')'):
					return Token.fechaPar
				elif(car == '{'):
					return Token.abreCha
				elif(car == '}'):
					return Token.fechaCha
				elif(car == '+'):
					return Token.soma
				elif(car == '-'):
					return Token.sub
				elif(car == '*'):
					return Token.mult
				elif(car == '%'):
					return Token.mod
				elif(car == '='):
					prev = '='
					estado = 14
				elif('a' <= car.lower() <= 'z'):
					estado = 2
				elif('0' <= car <= '9'):
					estado = 4
			elif (estado == 2):
				# letra ou digito
				if(('a' <= car.lower() <= 'z') or ('0' <= car <= '9')):
					continue
				else:
					self.returCar(car)
					estado = 3
			### ident
			elif (estado == 3):
				Atual.token = Token.ident
				self.returCar(car)
				return Token.ident
			elif (estado == 4):
				if ('0' <= car <= '9'):
					continue
				if (car == '.'):
					estado = 6
				else:
					self.returCar(car)
					estado = 5
			###	NUMint
			elif (estado == 5):
				Atual.token = Token.NUMint
				self.returCar(car)
				return Token.NUMint
			elif (estado == 6):
				if ('0' <= car <= '9'):
					estado = 7
				else:
					estado = 8
			elif (estado == 7):
				if('0' <= car <= '9'):
					continue
				else:
					estado = 9
			### erro
			elif (estado == 8):
				# atualiza o atual
				Atual.token = Token.erro
				self.returCar(car)
				# return erro
				return Token.erro
			### NUMfloat
			elif (estado == 9):
				# atualiza o atual
				Atual.token = Token.NUMfloat
				self.returCar(car)
				# return NUMfloat
				return Token.NUMfloat
			### comentario
			elif (estado == 10):
				if((car == '*') and (prev == '/')):
					estado = 11
				elif((car == '/') and (prev == '/')):
					estado = 19
				else:
					self.returCar(car)
					return Token.div
			elif(estado == 11):
				if(car == '*'):
					prev = '*'
				elif((car == '/') and (prev == '*')):
					estado = 1
				elif(car == '\n'):
					Atual.linha += 1
					Atual.coluna = 0
				else:
					prev = ''
			## int
			elif (estado == 12):
				if((car == 'n') and (prev == 'i')):
					prev += 'n'
				elif((car == 't') and (prev == 'in')):
					prev += 't'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'int')):
					self.returCar(car)
					return Token.inte
				elif((car == 'f') and (prev == 'i')):
					prev += 'f'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'if')):
					self.returCar(car)
					return Token.ife
				else:
					estado = 2
			## float
			elif (estado == 13):
				#print('PREV = '+prev)
				if((car == 'l') and (prev == 'f')):
					prev += 'l'
				elif((car == 'o') and (prev == 'fl')):
					prev += 'o'
				elif((car == 'a') and (prev == 'flo')):
					prev += 'a'
				elif((car == 't') and (prev == 'floa')):
					prev += 't'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'float')):
					self.returCar(car)
					return Token.floate
				elif((car == 'o') and (prev == 'f')):
					prev += 'o'
				elif((car == 'r') and (prev == 'fo')):
					prev += 'r'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'for')):
					self.returCar(car)
					return Token.foor
				else:
					estado = 2
			elif (estado == 14):
				if((car == '=') and (prev == '=')):
					#self.returCar(car)
					return Token.igual
				else:
					self.returCar(car)
					return Token.atrib
			## print
			elif (estado == 15):
				#print('PREV = '+prev)
				if((car == 'r') and (prev == 'p')):
					prev += 'r'
				elif((car == 'i') and (prev == 'pr')):
					prev += 'i'
				elif((car == 'n') and (prev == 'pri')):
					prev += 'n'
				elif((car == 't') and (prev == 'prin')):
					prev += 't'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'print')):
					self.returCar(car)
					return Token.printe
				else:
					estado = 2
			## scan
			elif (estado == 16):
				#print('PREV = '+prev)
				if((car == 'c') and (prev == 's')):
					prev += 'c'
				elif((car == 'a') and (prev == 'sc')):
					prev += 'a'
				elif((car == 'n') and (prev == 'sca')):
					prev += 'n'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'scan')):
					self.returCar(car)
					return Token.scan
				else:
					estado = 2
			## while
			elif (estado == 17):
				#print('PREV = '+prev)
				if((car == 'h') and (prev == 'w')):
					prev += 'h'
				elif((car == 'i') and (prev == 'wh')):
					prev += 'i'
				elif((car == 'l') and (prev == 'whi')):
					prev += 'l'
				elif((car == 'e') and (prev == 'whil')):
					prev += 'e'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'while')):
					self.returCar(car)
					return Token.whilee
				else:
					estado = 2
			## strg
			elif (estado == 18):
				if(car != '"'):
					continue
				else:
					# self.returCar(car)
					return Token.strg
			## comentario //
			elif (estado == 19):
				if(car != '\n'):
					continue
				else:
					Atual.linha += 1
					Atual.coluna = 0
					estado = 1
			## !, !=
			elif(estado == 20):
				if((car == '=') and (prev == '!')):
					return Token.difer
				else:
					return Token.note
			## else
			elif (estado == 21):
				#print('PREV = '+prev)
				if((car == 'l') and (prev == 'e')):
					prev += 'l'
				elif((car == 's') and (prev == 'el')):
					prev += 's'
				elif((car == 'e') and (prev == 'els')):
					prev += 'e'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'else')):
					self.returCar(car)
					return Token.elsee
				else:
					estado = 2
			## >, >=
			elif(estado == 22):
				if((car == '=') and (prev == '>')):
					return Token.maiIgual
				else:
					return Token.maior
			## <, <=
			elif(estado == 23):
				if((car == '=') and (prev == '<')):
					return Token.menIgual
				else:
					return Token.menor
			## ||
			elif(estado == 24):
				if((car == '|') and (prev == '|')):
					return Token.oor
				else:
					return Token.erro
			## &&
			elif(estado == 25):
				if((car == '&') and (prev == '&')):
					return Token.ande
				else:
					return Token.erro
			## break
			elif (estado == 26):
				#print('PREV = '+prev)
				if((car == 'r') and (prev == 'b')):
					prev += 'r'
				elif((car == 'e') and (prev == 'br')):
					prev += 'e'
				elif((car == 'a') and (prev == 'bre')):
					prev += 'a'
				elif((car == 'k') and (prev == 'brea')):
					prev += 'k'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'break')):
					self.returCar(car)
					return Token.breack
				else:
					estado = 2
			## continue
			elif (estado == 27):
				#print('PREV = '+prev)
				if((car == 'o') and (prev == 'c')):
					prev += 'o'
				elif((car == 'n') and (prev == 'co')):
					prev += 'n'
				elif((car == 't') and (prev == 'con')):
					prev += 't'
				elif((car == 'i') and (prev == 'cont')):
					prev += 'i'
				elif((car == 'n') and (prev == 'conti')):
					prev += 'n'
				elif((car == 'u') and (prev == 'contin')):
					prev += 'u'
				elif((car == 'e') and (prev == 'continu')):
					prev += 'e'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'continue')):
					self.returCar(car)
					return Token.continuee
				else:
					estado = 2
			## return
			elif (estado == 28):
				if((car == 'e') and (prev == 'r')):
					prev += 'e'
				elif((car == 't') and (prev == 're')):
					prev += 't'
				elif((car == 'u') and (prev == 'ret')):
					prev += 'u'
				elif((car == 'r') and (prev == 'retu')):
					prev += 'r'
				elif((car == 'n') and (prev == 'retur')):
					prev += 'n'
				elif(not('a' <= car.lower() <= 'z') and (prev == 'return')):
					self.returCar(car)
					return Token.returne
				else:
					estado = 2




	def returCar(self,car):
		self.arq = car + self.arq
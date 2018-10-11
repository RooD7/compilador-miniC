class Token:
	erro		= 0 ## erro
	abrePar 	= 1 # abre parenteses
	fechaPar 	= 2 # fecha parenteses
	abreCha 	= 3 # abre chaves
	fechaCha 	= 4 # fecha chaves
	ident		= 5	## identificador (variavel)
	inte		= 6 # int
	floate		= 7 # float
	breack		= 8 # break
	continuee	= 9 # continue
	ptoVirg		= 10 ## ponto e virgula
	virg		= 11 # virgula
	foor		= 12 # for
	scan		= 13 # scan
	printe		= 14 # print
	strg		= 15 # str
	NUMint		= 16 ## numero inteiro
	NUMfloat	= 17 ## numero float
	whilee		= 18 # while
	ife			= 19 # if
	elsee		= 20 # else
	igual		= 21 # igual
	difer		= 22 # diferente
	atrib		= 23 # atributo
	menIgual	= 24 # menor igual
	maiIgual	= 25 # maior igual
	menor		= 26 # menor
	maior		= 27 # maior
	oor 		= 28 # or
	ande		= 29 # and
	note		= 30 # not
	soma		= 31 # soma
	sub			= 32 # subtracao
	mult		= 33 # multiplicacao
	div			= 34 # divisao
	mod			= 35 # mod
	eof			= 36 ## eof
	

	msg = ('erro','(',')','{','}','IDENT','int','float','break','continue',';','for','scan','print','STR','NUMint','NUMfloat','while','if','else','==','!=','=','<=','>=','<','>','||','&&','!','+','-','*','/','%','EOF')

class Atual:
	linha	= 1
	coluna	= 1
	token	= ''
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
				
			#print('LINHA = ',Atual.linha)
			print('CAR = ',car)
			#print('COLUNA = ',Atual.coluna)
			#print('LEXEMA = ',Atual.lexema)
			#print('TOKEN = ',Atual.token)
			Atual.lexema += car
			Atual.coluna += 1


			if(estado == 1):
				if(car == '\n'):
					Atual.linha += 1
					Atual.coluna = 1
				if(car in (' ','\t')):
					continue
				elif(car.lower() == 'i'):
					estado = 12
				elif('a' <= car.lower() <= 'z'):
					estado = 2
				elif('0' <= car <= '9'):
					estado = 4
				elif(car == '/'):
					estado = 10
				elif(car == ';'):
					return Token.ptoVirg
			elif (estado == 2):
				# letra ou digito
				if(('a' <= car.lower() <= 'z') or ('0' <= car <= '9')):
					continue
				else:
					estado = 3
			### ident
			elif (estado == 3):
				# atualiza o atual
				Atual.linha += 1
				Atual.token = Token.ident
				# return identificador
				return Token.ident
			elif (estado == 4):
				if ('0' <= car <= '9'):
					continue
				if (car == '.'):
					estado = 6
				else:
					estado = 5
			###	NUMint
			elif (estado == 5):
				# atualiza o atual
				Atual.linha += 1
				Atual.token = Token.NUMint
				# return NUMint
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
				Atual.linha += 1
				Atual.token = Token.erro
				# return erro
				return Token.erro
			### NUMfloat
			elif (estado == 9):
				# atualiza o atual
				Atual.linha += 1
				Atual.token = Token.NUMfloat
				# return NUMfloat
				return Token.NUMfloat
			### comentario
			elif (estado == 10):
				if(car == '*'):
					estado = 11
				else:
					return Token.div
			elif(estado == 11):
				if(car == '*'):
					continue
				elif(car == '\n'):
					Atual.linha += 1
					Atual.coluna = 1
				elif(car == '/'):
					estado = 1
			## int
			elif (estado == 12):
				if(car == 'i'):
					prev = 'i'
					continue
				elif((car == 'n') and (prev == 'i')):
					prev += 'n'
					continue
				elif((car == 't') and (prev == 'in')):
					prev += 't'
					continue
				elif(('a' <= car.lower() <= 'z') and (prev == 'int')):
					estado = 2
					continue
				else:
					return Token.inte


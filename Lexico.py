class Token:
	erro		= 0 # erro
	abrePar 	= 1 # abre parenteses
	fechaPar 	= 2 # fecha parenteses
	abreCha 	= 3 # abre chaves
	fechaCha 	= 4 # fecha chaves
	ident		= 5	# Variavel
	Inte		= 6 # int
	Floate		= 7 # float
	breack		= 8 # break
	continuee	= 9 # continue
	ptoVirg		= 10 # ponto e virgula
	virg		= 11 # virgula
	foor		= 12 # for
	scan		= 13 # scan
	printe		= 14 # print
	strg		= 15 # str
	NUMint		= 16 # numero inteiro
	NUMfloat	= 17 # numero float
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
	

	msg = ('erro','(',')','{','}','IDENT','int','float','break','continue',';','for','scan','print','STR','NUMint','NUMfloat','while','if','else','==','!=','=','<=','>=','<','>','||','&&','!','+','-','*','/','%')

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
		while(True):
			#print('Linha atual: ',Atual.linha)
			if self.arq is '':
				break
			else:
				car = self.arq[0]
				self.arq = self.arq[1:]
				
			print('CAR = ',car)
			Atual.lexema += car
			Atual.coluna += 1
			if(estado == 1):
				if(car == '\n'):
					Atual.linha += 1
				if(car in (' ','\n','\t')):
					continue
				elif('a' <= car.lower() <= 'z'):
					estado = 2
				elif('0' <= car <= '9'):
					estado = 4
			elif (estado == 2):
				# letra ou digito
				if(('a' <= car.lower() <= 'z') or ('0' <= car <= '9')):
					continue
				else:
					estado = 3
			elif (estado == 3):
				# atualiza o atual
				Atual.linha += 1
				# return identificador
				return Token.ident
			elif (estado == 4):
				if ('0' <= car <= '9'):
					continue
				if (car == '.'):
					estado = 6
				else:
					estado = 5
			elif (estado == 5):
				# atualiza o atual
				Atual.linha += 1
				# return num
				return Token.num
			elif (estado == 6):
				if ('0' <= car <= '9'):
					estado = 7
				else:
					estado = 8
			elif (estado == 7):
				if('0' <= car <= '9'):
					continue
				else:
					estado = 5
			elif (estado == 8):
				# atualiza o atual
				Atual.linha += 1
				# return erro
				return Token.erro
			elif (car == eof):
				return Token.eof


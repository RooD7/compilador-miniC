class VirtualMachine(object):

	def __init__(self, lista):
		self.operadores  = ['+', '-', '*', '/', '%', '>', '<', '==', '>=', '<=', '!=']
		self.lista = lista
	'''
		% modulo
		// divisão de inteiro
	'''

	def transforma(self, lista):
		novaLista = []
		i = 0
		while(i < len(lista)):
			if not(type(lista[i]) is list):
				novaLista.append([lista[i], lista[i+1], lista[i+2], lista[i+3]])
				# print(novaLista)
				i+=4
				# if(i >= len(lista)):
				# 	print('entrou')
				# 	return novaLista
				#return novaLista
			else:
				#print(lista[i])
				novaLista += self.transforma(lista[i])
				#print(novaLista)
				#break
				i+=1
			if(i == len(lista)):
				return novaLista
			#print()

		return novaLista

	def procuraLista(self, lista):
		i = 0
		while(i < len(self.lista)):
			if(self.lista[i] == lista):
				return (i+1)
			i+=1

	def subtituiValor(self, atual, valor):
		i = 0
		while(i < len(self.lista)):
			if(atual in self.lista[i]):
				if((self.lista[i])[0] == atual):
					(self.lista[i])[0] = valor
				if((self.lista[i])[1] == atual):
					(self.lista[i])[1] = valor
				if((self.lista[i])[2] == atual):
					(self.lista[i])[2] = valor
				if((self.lista[i])[3] == atual):
					(self.lista[i])[3] = valor
			i+=1


	def executaQuadruplas(self):
		listaRespostas = []
		i = 0
		while(i < len(self.lista)):
			# CALL
			if((self.lista[i])[0] == 'call'):
				# PRINT
				if((self.lista[i])[1] == 'print'):
					if(((self.lista[i])[2] != None) and ((self.lista[i])[3] != None)):
						listaRespostas.append(str((self.lista[i])[2])+str((self.lista[i])[3]))
						print(str((self.lista[i])[2])+str((self.lista[i])[3]))
					elif((self.lista[i])[2] != None):
						listaRespostas.append(str((self.lista[i])[2]))
						print(str((self.lista[i])[2]))
					elif((self.lista[i])[3] != None):
						listaRespostas.append(str((self.lista[i])[3]))
						(str((self.lista[i])[3]))
						print(str((self.lista[i])[3]))
					else:
						print()
				# SCAN
				elif((self.lista[i])[1] == 'scan'):
					if((self.lista[i])[2] != None):
						aux = input()
						self.subtituiValor((self.lista[i])[2], aux)
						listaRespostas.append(aux)
				# BREAK
				elif((self.lista[i])[1] == 'break'):
					listaRespostas.append('break')
					break
				# CONTINUE
				elif((self.lista[i])[1] == 'continue'):
					listaRespostas.append('continue')
					continue

			# OPERADORES
			elif(((self.lista[i])[0] in self.operadores) or ((self.lista[i])[0] == '=')):
				# print(self.lista[i])
				if((self.lista[i])[0] == '+'):
					aux = (float((self.lista[i])[2]) + float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '-'):
					aux = (float((self.lista[i])[2]) - float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '*'):
					aux = (float((self.lista[i])[2]) * float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '/'):
					aux = (float((self.lista[i])[2]) / float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '%'):
					aux = (float((self.lista[i])[2]) % float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '>'):
					# print('comparação')
					aux = (float((self.lista[i])[2]) > float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '<'):
					aux = (float((self.lista[i])[2]) < float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '<='):
					aux = (float((self.lista[i])[2]) <= float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '>='):
					aux = (float((self.lista[i])[2]) >= float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '=='):
					aux = (float((self.lista[i])[2]) == float((self.lista[i])[3]))
					self.subtituiValor((self.lista[i])[1], aux)
					listaRespostas.append(aux)
				
				elif((self.lista[i])[0] == '='):
					subtituiValor(((self.lista[i])[1]), ((self.lista[i])[2]))
					listaRespostas.append(float((self.lista[i])[2]))

			# IF
			elif((self.lista[i])[0] == 'if'):
				# print(self.lista[i])
				if((self.lista[i])[1] == True):
					# print('verdadeiro')
					i = self.procuraLista(['label', (self.lista[i])[2], None, None])
					i-=1
				else:
					# print('false')
					i = self.procuraLista(['label', (self.lista[i])[3], None, None])
					i-=1

			# JUMP
			elif((self.lista[i])[0] == 'jump'):
				# print(self.lista[i])
				i = self.procuraLista(['label', (self.lista[i])[1], None, None])
				i-=1
			i+=1
		return listaRespostas



if __name__ == '__main__':
	
	lista1 = [['call','scan', 'a', None, 
				'call', 'scan','b', None, 
				'+', 'c', 'a', 'b'], 
				'>', 'temp', 'a', 'b', 
				'if','temp','maior','menor', 
				'label','maior', None, None, 
				'call','print','"a maior"', None,
				'jump', 'fim', None, None, 
				'label', 'menor', None, None, 
				'call', 'print', 'b maior', None, 
				'label', 'fim', None, None, 
				'call', 'break', None, None]
	m = VirtualMachine(lista1)
	# print('lista1')
	# print(lista1)
	m.lista = m.transforma(lista1)
	#print('lista2')
	#print(m.lista)
	# print()
	resp = m.executaQuadruplas()
	# print()
	# print(resp)
	# print()
	# print('de novo')
	# print(m.lista)
	# print(m.transforma(['call','scan','"entre a: "','a']))
	# print(m.transforma(['call','print','"a maior"', None]))
	# print(m.transforma(['+','c','a','b']))
	# print(m.transforma(['call','print','"media = "','c']))
	# print(m.transforma(['>','temp','a','b']))
	# print(m.transforma(['if','temp','maior','menor']))
	# print(m.transforma(['if','temp','maior', None]))
	# print(m.transforma(['label','maior', None, None]))
	# print(m.transforma(['jump', 'fim', None, None]))
	# print(m.transforma(['call', 'stop', None, None]))

	# inst = ('call','scan','a',None)
	# r = transforma(inst)




		
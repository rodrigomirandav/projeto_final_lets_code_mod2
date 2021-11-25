import random
import csv
import time
from IPython.display import clear_output

class Morador:
  def __init__(self, nome= None, apartamento= None):
    '''
    Representa um morador do prédio

    Parâmetros
    ----------
    nome : str (opcional)
        Nome do morador
    apartamento : Apartamento (opcional)
        Objeto da classe Apartamento
    '''
    self.nome = nome
    self.apartamento = apartamento

    if self.nome == None:
      self.nome = input("Qual o nome do morador? ")

    if self.apartamento == None:
      numero_apartamento = input("Qual o número do apartamento? ")
      while not numero_apartamento.isnumeric():
        numero_apartamento = input("Qual o número do apartamento? ")
      self.apartamento = Apartamento.criar_apartamento_morador(int(numero_apartamento), self)
  
  def __repr__(self):
    return f"Morador: {self.nome}"

  def votar(self, urna, numero_candidato= 0):
    '''
    Acrescenta um voto na urna caso o apartamento não tenha votado ainda

    Parâmetros
    ----------
    urna : Urna
        Urna em que o voto será realizado
    numero_candidato : int (opcional)
        Número do candidato em que se deseja votar

    Retorno
    -------
    out : bool
      Retorna se o voto foi computado com sucesso.
        True -> voto computado
        False -> Voto já estava registrado 
    '''
    while str(numero_candidato) not in urna.retorna_numeros_candidatos():
      numero_candidato = input("Qual o número do candidato em quem deseja votar? ")
    return urna.votar(self.apartamento, int(numero_candidato))

class Candidato(Morador):

  def __init__(self, nome= None, apartamento= None):
    '''
    Representa um candidato como sendo um morador que poderá ser votado na eleição
        
    Parâmetros
    ----------
    nome : str (opcional)
      Nome do candidato
    apartamento : Apartamento (opcional)
       Objeto da classe apartamento onde o candidato mora
    '''
    super().__init__(nome, apartamento)
    self._numero_candidato = 0
    self.__votos = 0
  
  def __repr__(self):
    return f"Candidato {self.numero_candidato}: {self.nome}"

  @property
  def numero_candidato(self):
    return self._numero_candidato

  @numero_candidato.setter
  def atualizar_numero(self, numero_candidato):    
    self._numero_candidato = numero_candidato  

  @property
  def votos(self):
    return self.__votos

  @votos.setter
  def contabiliza_votos(self):
    self.__votos += 1 
  
class Apartamento:
  lista_de_apartamentos = []
  
  def __init__(self, numero_apartamento):
    '''
    Representa um apartamento do prédio

    Parâmetros
    ----------
    numero_apartamento : int (obrigatório)
        Número do apartamento
    '''
    if(not isinstance(numero_apartamento, int)):
      raise ValueError('O número do apartamento precisar ser int.')
    if Apartamento.buscar_apartamento(numero_apartamento) != None:
      raise ValueError("O apartamento já existe!")

    self.lista_de_moradores = []
    self.__voto = False
    self.numero_apartamento = numero_apartamento
    Apartamento.lista_de_apartamentos.append(self)
  
  def __repr__(self):
    return f"Apartamento {self.numero_apartamento}: {self.lista_de_moradores}"
  
  def adicionar_morador(self, morador):
    self.lista_de_moradores.append(morador)
  
  def imprimir_moradores(self):
    '''
    Imprime moradores que moram no apartamento
    '''
    print("Lista de Moradores:")
    for morador in self.lista_de_moradores:
        print(morador.nome)

  @property
  def voto(self):
    return self.__voto
  
  @voto.setter
  def atualiza_voto(self, valor):
    self.__voto = valor

  @staticmethod
  def criar_apartamento_morador(numero_apartamento, morador):
    '''
    Cadastra um novo apartamento

    Parâmetros
    ----------
    numero_apartamento : int (obrigatório)
      Número do apartamento a ser cadastrado
    morador : Morador (obrigatório)
      Objeto da classe Morador que habita o apartamento

    Retorno
    -------
    apartamento : Apartamento
      Objeto criado na classe Apartamento
    '''
    apartamento = Apartamento.buscar_apartamento(numero_apartamento)
    if apartamento == None:
      apartamento = Apartamento(numero_apartamento)
    apartamento.adicionar_morador(morador)
    return apartamento
    
  @staticmethod
  def buscar_apartamento(numero_apartamento):
    '''
    Verifica se o numero do apartamento já está na lista de apartamentos

    Parâmetros
    ----------
    numero_apartamento : int (obrigatório)
        Número do apartamento que deseja buscar

    Retorno:
    out : Apartamento
        Retorna o apartamento encontrado na lista ou vazio caso não esteja na lista
    '''
    apart = [apart for apart in Apartamento.lista_de_apartamentos if apart.numero_apartamento == numero_apartamento]
    if apart:
      return apart[0]
    else:
      return None

class Urna:
  def __init__(self):
    '''
    Representa uma urna para votação
    '''
    self.lista_de_apartamentos = []
    self.lista_de_candidatos = []
  
  def adiciona_apartamentos(self, apartamentos):
    '''
    Adiciona uma lista de apartamentos participantes na urna

    Parâmetros 
    ----------
    apartamentos : list
        Adiciona os apartamentos fornecidos em uma lista de apartamentos relacionados àquela urna
    '''
    self.lista_de_apartamentos = apartamentos
  
  def adicionar_candidato(self, candidato):
    numeros = self.retornar_numero_candidatos()
    novo_numero = random.randint(1,100)
    while novo_numero in numeros:
      novo_numero = random.randint(1,100)
    candidato.atualizar_numero = novo_numero
    self.lista_de_candidatos.append(candidato)

  def votar(self, apartamento, numero_candidato):
    if apartamento.retorna_voto() == False:
      candidatos = [candidato for candidato in self.lista_de_candidatos if candidato.numero_candidato == numero_candidato]
      
      if not candidatos:
        return False

      apartamento.atualiza_voto(True)  
      candidatos[0].contabiliza_votos()
      return True
    else:
      print("Seu apartamento já votou")
      return False
  
  def votacao_andamento(self):
    return any([True for apart in self.lista_de_apartamentos if apart.voto == False])

  def retornar_numero_candidatos(self):
    return [candidato.numero_candidato for candidato in self.lista_de_candidatos]

class Sistema:
  def __init__(self):
    self.urna = Urna()
    self.opcao = None

  def run(self):
      while self.opcao != "h":
        clear_output(wait=True)
        print('''Selecione uma opção:
        a) Cadastrar morador
        b) Cadastrar candidato
        c) Listar apartamentos
        d) Listar moradores
        e) Importar dados moradores e candidatos
        f) Realizar votação
        g) Realizar votação em lote
        h) Sair\n''')
        self.opcao = input('Opção: ').lower()
    
        if self.opcao == 'a':
          morador = Morador()
          print("Morador criado com sucesso")
          time.sleep(2)
        elif self.opcao == 'b':
          candidato = Candidato()
          self.urna.adicionar_candidato(candidato)
          print("Candidato criado com sucesso")
          time.sleep(2)
        elif self.opcao == 'c':
          print(Apartamento.lista_de_apartamentos)
          time.sleep(5)
        elif self.opcao == 'd':
          for apartamento in Apartamento.lista_de_apartamentos:
            print(apartamento.lista_de_moradores)
          time.sleep(5)
        elif self.opcao == 'e':
          print('Trabalhando nisso!')
        elif self.opcao == 'h':
          print('Sistema finalizado com sucesso')
        else:
          print("Opção inválida! Tente Novamente:")

if __name__ == "__main__":
  sistema = Sistema()
  sistema.run()
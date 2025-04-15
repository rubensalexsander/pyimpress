"""COMO UTILIZAR:
### Ver impressoras disponíveis:
>>> python pyimpress printers

Será apresentada uma lista das impressoras disponíveis no momento. (Ex.: "0-Canon G3160")
Utilize o número a frente da impressora para imprimir um arquivo no próximo passo.

### Imprimir arquivo:
>>> python pyimpress 0 ~/Desktop/arq1.pdf 1-4 fv

0: Número da impressora conforme visto a cima;
~/Desktop/arq1.pdf: Caminho para o arquivo
1-4: Intervalo das páginas
fv: Pode ser "normal" (impressão em apenas um lado do papel) ou "fv" (impressão em ambos os lados do papel)
"""

import sys
import cups

class PyImpress:
    def __init__(self):
        # Conecta ao servidor CUPS
        self.conn = cups.Connection()
        
    def get_printers(self):
        # Lista de impressoras disponíveis
        self.printers = self.conn.getPrinters()
        return self.printers

    def print(self, printer, arq, range):
        # Define intervalo de páginas
        opcoes = {
            'page-ranges': range
        }

        # Envia trabalho de impressão
        job_id = self.conn.printFile(printer, arq, "Meu Documento", opcoes)

        print(f"Trabalho enviado! ID: {job_id}")

    def get_intervalos_frente_verso(self, intervalo_paginas:str):
        paginas_odd, paginas_even = '', ''

        # Faz split na string de intervalo
        intervalo = intervalo_paginas.split(sep='-')

        # Define número mínimo e máximo:
        intervalo_min = int(intervalo[0])
        intervalo_max = int(intervalo[1])

        # Define valores odd
        for i in range(intervalo_min, intervalo_max+1):
            if (i % 2): paginas_odd += str(i) + ', '

        # Retira vírgula da última página ímpar
        paginas_odd = paginas_odd[0:-2]

        # Define valores even
        for i in range(intervalo_min, intervalo_max+1):
            if not (i % 2): paginas_even += str(i) + ', '

        # Retira vírgula da última página par
        paginas_even = paginas_even[0:-2]
        
        return paginas_odd, paginas_even

def main():
    # Define instância de PyImpress
    pyimpress = PyImpress()
    
    # Printa impressoras disponíveis
    if len(sys.argv) == 2:
      if sys.argv[1] == 'printers':
        printers = pyimpress.get_printers()
        
        print(f"\nImpressoras disponíveis: ({len(printers)})")
        
        for i in range(len(printers)):
            print(str(i) + '-' + list(printers.keys())[i])
        
        print('')
    
    # Faz impressão fv(frente e verso) e normal 
    elif len(sys.argv) == 5:
        #['./pyimpress.py', 'impress', '0', './arq1', '1-4', 'fv']
        printer = list(pyimpress.get_printers().keys())[int(sys.argv[1])]
        arq = sys.argv[2]
        range_arq = sys.argv[3]
        type = sys.argv[4]
        
        print('\nArquivo: ' + arq)
        
        # Faz impressão normal
        if type == 'normal':
            # Faz a impressão
            print(f'Imprimindo: {range_arq}\n')
            pyimpress.print(printer=printer, arq=arq, range=range_arq)
        
        # Faz impressão frente e verso
        elif type == 'fv':
            range_odd, range_even = pyimpress.get_intervalos_frente_verso(range_arq)
            
            if int(range_arq[0]) % 2 == 0:
                # Faz a impressão das páginas pares
                print(f'Imprimindo páginas pares: {range_even}\n')
                pyimpress.print(printer=printer, arq=arq, range=range_even)
                
                input('Pressione "Enter" para imprimir as páginas ímpares!\n')
                
                # Faz a impressão das páginas ímpares
                print(f'Imprimindo páginas impares: {range_odd}\n')
                pyimpress.print(printer=printer, arq=arq, range=range_odd)
            else:
                # Faz a impressão das páginas ímpares
                print(f'Imprimindo páginas impares: {range_odd}\n')
                pyimpress.print(printer=printer, arq=arq, range=range_odd)
                
                input('Pressione "Enter" para imprimir as páginas pares!\n')
                
                # Faz a impressão das páginas pares
                print(f'Imprimindo páginas pares: {range_even}\n')
                pyimpress.print(printer=printer, arq=arq, range=range_even)

if __name__ == "__main__":
    main()

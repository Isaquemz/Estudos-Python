def calculator(value_1,value_2,operator):
    '''Função responsavel por realizar a operação se estiver dentro das possiveis e retornar o valor.'''

    operator = operator.lower().strip(" ")

    if operator in ('soma','sum','som'):

        result = value_1 + value_2
        status = True

    elif operator in ('subtração','subtracao','subtracão','subtraçao','sub','subtrai','subtraia','subtrair'):

        result = value_1 - value_2
        status = True

    elif operator in ('multiplicação','multiplicacao','multiplicacão','multiplicaçao','multiplica','multiplicar','multiplique'):

        result = value_1 * value_2
        status = True

    elif operator in ('divisão','divisao','divide','dividir'):

        result = value_1 / value_2
        status = True

    else:

        print('Operação invalida, tente novamente!')
        result = 0
        status = False
    
    return result,status

def verifica_numero(value):
    '''Função que verifica se é um numero e retorna em formato int. '''

    try:

        valor = int(value)
        status = True

    except:
        valor = 0
        status = False
    
    return valor,status

# ------------------ executando o programa ----------------- #

tentativa = 0
status_valor_1,status_valor_2,status_operacao = False,False,False

while status_operacao == False:

    operator_in = input('Digite a operação que deseja realizar: \n')

    while status_valor_1 == False or status_valor_2 == False:
        if tentativa > 0:
            print('Valores invalidos, tente novamente!')

        valor_1_in,status_valor_1 = verifica_numero(input('Digite o primeiro valor inteiro: \n'))
        valor_2_in,status_valor_2 = verifica_numero(input('Digite o segundo valor inteiro: \n'))
        
        tentativa +=1

    result,status_operacao = calculator(valor_1_in, valor_2_in, operator_in)

if status_operacao:
    print(f'O resultado da operação é {result}.')
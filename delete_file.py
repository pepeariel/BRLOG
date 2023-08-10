import os

# Delete files from a specific path
try:
    for arquivo in os.listdir(os.getcwd()):
    	
        if 'relatorio' in arquivo:
            print(arquivo)
            os.remove(arquivo)
            print(f'{arquivo} removido com sucesso!')
    
except Exception as e:
    print('Erro devido a:', e)

try:
    os.remove(r'/home/ec2-user/Relatório de entregas.xlsx')
    print('Arquivo excel removido com sucesso!')
except Exception as e:
    print('Erro devido a:', e)

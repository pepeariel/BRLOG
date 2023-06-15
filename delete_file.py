import os

# Delete files from a specific path
try:
    os.remove(r'/home/ec2-user/Documents/BRLOG/Relatório de entregas.xlsx')
    print('Arquivo removido com sucesso!')
except Exception as e:
    print('Erro devido a:', e)
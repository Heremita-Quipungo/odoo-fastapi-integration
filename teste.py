# importamos o tempo
import pyttsx3
import time

engine = pyttsx3.init()

# Boa Vida
print('bem-vindo a calculadora')
engine.say('bem-vindo a calculadora')
engine.runAndWait()
time.sleep(2)

print('escolha que operação desejas:')
a = True
while a==True:
    c = str(input(' insere a operação; + - '))
    if c == '+' or c == '-':
        a = False
    else:
        print('opção i-''nvalida')

while True:
    try:
        d = float(input('Insere um numero a: '))
        break
    except:
        print('erro')


while True:
    try:
        b = float(input('Insere un numero b: '))
        break
    except:
        print('erro ')


b = float(b)
d = float(d)

if c == '+' :
    print(d + b)
elif c == '-':
    print(d - b)


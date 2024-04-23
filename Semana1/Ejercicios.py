

def first_act():
    '''Ejercicio 1
    escibir programa que lea numero impar del teclado. Si no es impar debe repetirse el programa'''
    while True:
        try:
            n = int(input("Introduce un numero impar: "))
        except Exception:
            print("Ingresa un valor correcto")
            continue
        if(n%2 != 0):
            break

def second_act():
    '''Ejercicio 2
    Escribe un programa que pida al usuario cuantos numeros quiere introducir. 
    Luego que lea todos los numeros y realice una media aritmetica'''

    media = 0
    while True:
        try:
            n = int(input("Cantidad de numeros a leer: "))
            if n == 0:
                print("Introduce un valor correcto")
                continue
            break
        except:
            print("Introduce un valor correcto")
            continue
    for i in range(n):
        while True:
            try:
                media += int(input("Valor: "))
                break
            except:
                print("Introduce un valor correcto")
                continue
    media = media/n
    print("La media es: ", media)


def third_act():
    '''Ejercicio 3
    Generar las siguientes listas'''
    # Todos los numeros del 0 al 10
    for i in range(0,11):
        print(i, end=" ")
    print("")
    # Todos los numeros del -10 al 0
    for i in range(-10,1):
        print(i, end=" ")
    print("")
    # Todos los numeros pares del 0 al 20
    l = [i for i in range(0,21) if i%2 == 0]
    for i in l:
        print(i, end= " ")
    print("")
    # Todos los numeros impares entre -20 y 0
    l = [i for i in range(-20,1) if i%2 != 0]
    for i in l:
        print(i, end=" ")
    print("")
    # Todos los numeros multiples de 5 del 0 al 50
    l =[i for i in range(0,51) if i%5==0]
    for i in l:
        print(i, end=" ")


def fourth_act(lis1,lis2):
    '''Ejercicio 4
    Dadas 2 listas creadas genera una tercera lista con los elementos que esten presentes en ambas. 
    Retornar esta nueva lista sin elementos duplicados'''
    dir = {}
    lis1 = lis1+lis2

    for i in lis1:
        if i not in dir.keys():
            dir[i] = 1
        else:
            dir[i] += 1

    lis = [i for i in dir.keys() if dir[i]>1]
    print(lis)


def fifth_act():
    '''Ejercicio 5
    Programa que sume todos los numeros pares enteros del 0 al 100'''

    suma = sum(list([i for i in range(0,101) if i%2 == 0]))
    print(suma)


def sixth_act(elem, lista):
    '''Ejercicio 6
    Programa que cuente cuantas veces aparece un elemento en una lista'''

    cont = len([i for i in lista if i==elem])
    print(cont)



if __name__ == "__main__":
    lis = [1,2,3,3,4,5,2,4,3,3,7]
    n = int(input("Elemento a buscar "))
    sixth_act(n, lis)
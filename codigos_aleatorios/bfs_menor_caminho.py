import random

DX = [ -1, 1, 0, 0 ]
DY = [ 0, 0, -1, 1]

def anotar_matriz(matriz: list[list[int]], tamanho: int, entrada: tuple, saida: tuple) -> None:

    X_ENTRADA, Y_ENTRADA = entrada[0], entrada[1]
    X_SAIDA, Y_SAIDA = saida[0], saida[1]

    fila = []

    if matriz[X_ENTRADA][Y_ENTRADA] != 0:
        return
    
    matriz[X_ENTRADA][Y_ENTRADA] = 1

    fila.append((X_ENTRADA, Y_ENTRADA))
    
    while fila:   
        atual = fila.pop(0)
        i, j = atual[0], atual[1]

        for d in range(4):
            x = i + DX[d]
            y = j + DY[d]

            if x >= 0 and x < tamanho and y >= 0 and y < tamanho and matriz[x][y] != -1:
                if matriz[x][y] == 0 or matriz[x][y] > matriz[i][j] + 1:
                    matriz[x][y] = matriz[i][j] + 1

                    if x != X_SAIDA or y != Y_SAIDA:
                        fila.append((x, y))

def extrair_caminho(matriz: list[list[int]], tamanho: int, entrada: tuple, saida: tuple, caminho: list) -> bool:

    X_ENTRADA, Y_ENTRADA = entrada[0], entrada[1]
    X_SAIDA, Y_SAIDA = saida[0], saida[1]

    if matriz[X_SAIDA][Y_SAIDA] == -1 or matriz[X_SAIDA][Y_SAIDA] == 0 or matriz[X_ENTRADA][Y_ENTRADA] == -1:
        return False
    
    caminho.append((X_SAIDA, Y_SAIDA))
    i, j = X_SAIDA, Y_SAIDA

    while (i, j) != (X_ENTRADA, Y_ENTRADA):
        passo_atual = matriz[i][j]
        achou = False

        for d in range(4):
            x, y = i + DX[d], j + DY[d]

            if 0 <= x < tamanho and 0 <= y < tamanho and matriz[x][y] == passo_atual - 1:
                caminho.append((x, y))
                i, j = x, y
                achou = True
                break

        if not achou:
            return False
        
    return True

def criar_ambiente(tamanho: int, densidade: int):

    matriz = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

    for i in range(tamanho):
        for j in range(tamanho):

            if i == 0 or i == tamanho - 1 or j == 0 or j == tamanho - 1:
                matriz[i][j] = -1
            else:
                rho = random.randint(1, 100)

                if rho <= densidade:
                    matriz[i][j] = -1
                else:
                    matriz[i][j] = 0
    
    return matriz
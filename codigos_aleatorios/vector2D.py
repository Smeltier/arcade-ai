import math

class Vector2D:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.norma: float = Vector2D._calcularnorma(x, y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __add__(self, vetor_secundario):
        x_secundario: float = vetor_secundario.getX()
        y_secundario: float = vetor_secundario.getY()
        return Vector2D(self.x + x_secundario, self.y + y_secundario)

    def inverter_vetor(self):
        return Vector2D(-self.x, -self.y)

    def _calcularnorma(x: float, y: float) -> float:
        norma: float = math.sqrt(x ** 2 + y ** 2)

        return norma

    def zerar(self):
        self.norma = 0
        self.x = 0
        self.y = 0

    def calcular_distancia(self, vetor: object) -> float:
        novox = abs(self.x - vetor.x)
        novoy = abs(self.y - vetor.y)

        vetor_diferenca = Vector2D(novox, novoy)

        return vetor_diferenca.norma

    def normalizar(self) -> None:
        norma: float = self.norma

        if norma == 0:
            raise ValueError("Não é possível normalizar um vetor nulo.")

        self.x /= norma
        self.y /= norma
        self.setNorma = 1

    def normalizar_ip(self) -> object:
        norma: float = self.norma

        if norma == 0:
            raise ValueError("Não é possível normalizar um vetor nulo.")
        
        novox = self.x / norma
        novoy = self.y / norma

        return Vector2D(novox, novoy)

    def produto_escalar(self, vetor: object) -> float:
        resultado_produto_escalar: float = self.x * vetor.x + self.y * vetor.y

        return resultado_produto_escalar

    def angulo_entreVetores(self, vetor: object) -> float:
        produto_escalar: float = Vector2D.produto_escalar(self, vetor)
        angulo: float = math.acos(produto_escalar / (self.norma * vetor.norma))

        return angulo
    
    def area_entreVetores(self, vetor: object) -> float:
        x1, y1 = self.x, self.y
        x2, y2 = vetor.x, vetor.y

        return  abs(x1 * y2 - x2 * y1)
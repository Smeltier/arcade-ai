from codigos_aleatorios.objects.agente import Agent

def circulo_retangulo(cir: Agent, ret: Agent):
    """
    Calcula se houve colisão entre um Agente circular e um Agente retangular.
    
    Args:
        cir  (Agente): Representação de um círculo.
        ret (Agente): Representação de um retângulo.
    
    Returns:
        tuple: (colidiu: bool, lateral: bool)
            - colidiu: True se houve colisão
            - lateral: True se colisão foi nas laterais (E/D), False se foi em cima/baixo
    """

    cx, cy, r = cir.position.x, cir.position.y, cir.raio
    rx, ry, rw, rh = ret.position.x, ret.position.y, ret.largura, ret.altura

    closest_x = max(rx, min(cx, rx + rw))
    closest_y = max(ry, min(cy, ry + rh))

    distance_x = cx - closest_x
    distance_y = cy - closest_y
    distance_sq = distance_x ** 2 + distance_y ** 2

    colidiu = False
    lateral = False

    if distance_sq < r ** 2:
        colidiu = True
        lateral = abs(distance_x) > abs(distance_y)
    
    return colidiu, lateral, distance_x, distance_y

def retangulo_retangulo(ret1: Agent, ret2: Agent):
    """
    Verifica colisão entre dois retângulos e qual lado ocorreu a colisão.
    
    Args:
        ret1 (Agente): Primeiro retângulo.
        ret2 (Agente): Segundo retângulo.
    
    Returns:
        tuple: (colidiu: bool, lateral: bool)
            - colidiu: True se houve colisão
            - lateral: True se colisão foi nas laterais (E/D), False se foi em cima/baixo
    """

    left1, right1 = ret1.position.x, ret1.position.x + ret1.largura
    top1, bottom1 = ret1.position.y, ret1.position.y + ret1.altura

    left2, right2 = ret2.position.x, ret2.position.x + ret2.largura
    top2, bottom2 = ret2.position.y, ret2.position.y + ret2.altura

    if right1 < left2 or left1 > right2 or bottom1 < top2 or top1 > bottom2:
        return False, None

    # sobreposição horizontal.
    dx = min(right1, right2) - max(left1, left2) 

    # sobreposição vertical.
    dy = min(bottom1, bottom2) - max(top1, top2)

    lateral = dx < dy

    return True, lateral
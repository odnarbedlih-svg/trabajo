def queensAttack(n, k, r_q, c_q, obstacles):
    # Distancias máximas iniciales a los bordes en las 8 direcciones
    d = {
        'U': n - r_q,                   # Arriba (Up)
        'D': r_q - 1,                   # Abajo (Down)
        'R': n - c_q,                   # Derecha (Right)
        'L': c_q - 1,                   # Izquierda (Left)
        'UR': min(n - r_q, n - c_q),    # Arriba-Derecha
        'UL': min(n - r_q, c_q - 1),    # Arriba-Izquierda
        'DR': min(r_q - 1, n - c_q),    # Abajo-Derecha
        'DL': min(r_q - 1, c_q - 1)     # Abajo-Izquierda
    }
    
    # Recorremos cada obstáculo para reducir las distancias si interfieren
    for r, c in obstacles:
        if c == c_q: # Misma columna (Arriba o Abajo)
            if r > r_q: d['U'] = min(d['U'], r - r_q - 1)
            else:       d['D'] = min(d['D'], r_q - r - 1)
            
        elif r == r_q: # Misma fila (Derecha o Izquierda)
            if c > c_q: d['R'] = min(d['R'], c - c_q - 1)
            else:       d['L'] = min(d['L'], c_q - c - 1)
            
        elif r - r_q == c - c_q: # Diagonal principal (UR o DL)
            if r > r_q: d['UR'] = min(d['UR'], r - r_q - 1)
            else:       d['DL'] = min(d['DL'], r_q - r - 1)
            
        elif r - r_q == c_q - c: # Diagonal secundaria (UL o DR)
            if r > r_q: d['UL'] = min(d['UL'], r - r_q - 1)
            else:       d['DR'] = min(d['DR'], r_q - r - 1)
            
    # Retornamos la suma total de casillas atacables en todas las direcciones
    return sum(d.values())


# Ejemplo de uso
if __name__ == '__main__':
    n, k = 5, 3
    r_q, c_q = 4, 3
    obstacles = [[5,5], [4,2], [2,3]]

    print("Total de ataques posibles:", queensAttack(n, k, r_q, c_q, obstacles))

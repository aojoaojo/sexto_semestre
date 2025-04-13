def matrix2bytes(matrix):
    """Converte uma matriz 4x4 de bytes de volta para uma string."""
    text = ''
    for row in matrix:
        for byte in row:
            text += chr(byte)
    return text

matriz = [
    [116, 111, 32, 115],
    [101, 109, 32, 99],
    [97, 102, 101, 32],
    [104, 111, 106, 101]
]

texto_original = matrix2bytes(matriz)
print("Resposta:", texto_original)
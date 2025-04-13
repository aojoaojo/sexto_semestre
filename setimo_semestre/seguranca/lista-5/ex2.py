def add_round_key(state, key):
    result = []
    for i in range(4):
        row = []
        for j in range(4):
            row.append(state[i][j] ^ key[i][j])
        result.append(row)
    return result

def matrix2bytes(matrix):
    text = ''
    for row in matrix:
        for byte in row:
            text += chr(byte)
    return text

S = [
    [202, 248, 93, 204],
    [72, 28, 184, 101],
    [209, 75, 62, 217],
    [122, 202, 220, 131]
]

K = [
    [175, 139, 46, 173],
    [104, 122, 205, 11],
    [178, 34, 81, 183],
    [21, 191, 253, 162]
]

original_state = add_round_key(S, K)
texto_original = matrix2bytes(original_state)

print("Resposta:", texto_original)
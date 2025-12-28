



def codage(binary):
    return [bit for b in binary for bit in ([0, 1] if b == 1 else [1, 0])]


def Decodage(binary):
    return [1 if binary[i]<binary[i + 1] else 0 for i in range(0, len(binary)-1,2)]





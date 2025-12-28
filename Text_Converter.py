


def text_to_binary(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def binary_to_text(binary_list):
    binary_str = ''.join(map(str, binary_list))
    return ''.join(chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8))
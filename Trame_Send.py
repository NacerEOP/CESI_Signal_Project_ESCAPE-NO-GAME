def calculate_crc(message_bits):
    """
    Simple XOR-based CRC calculation for binary data.
    """
    crc = 0
    for bit in message_bits:
        crc ^= bit  # XOR operation
    return crc

def add_trame_to_message(message_bits):
    """
    Adds trame to the binary message:
    [Prefix][ID][Message][Suffix][CRC]
    """
    prefix = [0, 1]           # 2-bit start flag
    message_id = [1, 0, 0, 1] # Example 4-bit message ID
    suffix = [1, 0]           # 2-bit end flag

    # Combine the message parts
    message_with_trame = prefix + message_id + message_bits + suffix

    # Calculate CRC
    crc = calculate_crc(message_with_trame)
    crc_bits = [int(x) for x in format(crc, '08b')]  # Convert CRC to 8 bits (1 byte)

    # Final trame with CRC
    full_trame = message_with_trame + crc_bits
    return full_trame


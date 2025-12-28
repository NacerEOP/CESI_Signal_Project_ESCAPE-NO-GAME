def calculate_crc(message_bits):
    """
    Simple XOR-based CRC calculation for binary data.
    """
    crc = 0
    for bit in message_bits:
        crc ^= bit  # XOR operation
    return crc



def retrieve_message_from_trame(trame):
    """
    Extracts the original message from the received trame and validates CRC.
    """
    # Extract CRC (last 8 bits)
    received_crc_bits = trame[-8:]
    message_with_crc = trame[:-8]

    # Calculate CRC for the received message
    calculated_crc = calculate_crc(message_with_crc)
    received_crc_value = int(''.join(map(str, received_crc_bits)), 2)

    print(f"Received CRC: {received_crc_value} | Calculated CRC: {calculated_crc}")

    if received_crc_value == calculated_crc:
        print("✅ CRC validé avec succès.")
        
        # Extract the message parts
        prefix = message_with_crc[:2]         # 2-bit prefix
        message_id = message_with_crc[2:6]    # 4-bit message ID
        message_bits = message_with_crc[6:-2] # Actual message
        suffix = message_with_crc[-2:]        # 2-bit suffix

        return message_bits
    else:
        print("❌ Erreur de CRC, message corrompu.")
        return None


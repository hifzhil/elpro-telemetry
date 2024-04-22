def hex_to_decimal(hex_str):
    return int(hex_str, 16)

def decrypt_data(string):
    fragments = [string[i:i+4] for i in range(0, len(string), 4)] 
    dec_array = [hex_to_decimal(fragment) for fragment in fragments]
    return dec_array
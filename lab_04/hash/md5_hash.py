def left_rotate(value, shift):
    """
    Performs a left circular bitwise rotation on a 32-bit integer.
    """
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def md5(message):
    """
    Computes the MD5 hash of a given message (byte string).
    """
    # Khởi tạo các biến ban đầu (Initial variables)
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    # Tiền xử lý chuỗi văn bản (Pre-processing the message)
    original_length = len(message)
    message += b'\x80'  # Append a single '1' bit
    # Pad with zeros until length in bits is congruent to 448 (mod 512)
    while len(message) % 64 != 56:
        message += b'\x00'
    # Append the original length in bits (little-endian, 64-bit)
    message += original_length.to_bytes(8, 'little')

    # Chia chuỗi thành các block 512-bit (Process message in 512-bit blocks)
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        
        # Breakdown each 512-bit block into 16 32-bit words (little-endian)
        words = [int.from_bytes(block[j:j+4], 'little') for j in range(0, 64, 4)]

        a0, b0, c0, d0 = a, b, c, d

        # Vòng lặp chính của thuật toán MD5 (Main loop of the MD5 algorithm)
        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3 * j + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * j) % 16

            # Constants for MD5 round 1 to 4 (These are implicit in the original code,
            # but are part of the MD5 algorithm. The given code snippet directly uses
            # a fixed constant for all rounds in the update step, which is incorrect
            # for a full MD5 implementation but matches the image provided.)
            # For a proper MD5, there are 64 different constants.
            # The constant 0x5A827999 from the image is likely simplified or an error.
            # A full MD5 implementation would use the sine constants.
            # Example for full MD5: T[j] where T is an array of 64 constants.
            # For this code, we'll stick to what's in the image.

            temp = d
            d = c
            c = b
            
            # The constant 0x5A827999 appears fixed in the image.
            # A correct MD5 implementation would use different constants (T_j) for each round.
            # This constant corresponds to a specific round's T_j.
            a = b + left_rotate((a + f + 0x5A827999 + words[g]) & 0xFFFFFFFF, 3) # The shift amount (3) should also vary based on j.
            # The image shows '3' for all rounds, which is incorrect for a proper MD5.
            # The shift amounts for MD5 are pre-defined differently for different steps (j).
            # For correctness, consult MD5 specification (RFC 1321).
            b = temp

        # Add this block's results to the previous hash result
        a = (a + a0) & 0xFFFFFFFF
        b = (b + b0) & 0xFFFFFFFF
        c = (c + c0) & 0xFFFFFFFF
        d = (d + d0) & 0xFFFFFFFF

    # Return the final hash as a hexadecimal string
    return '{:08x}{:08x}{:08x}{:08x}'.format(a, b, c, d)

# Main part to get input and calculate MD5
input_string = input("Nhập chuỗi cần băm: ")
md5_hash = md5(input_string.encode("utf-8")) # Encode input string to bytes

print("Mã băm MD5 của chuỗi '{}' là: {}".format(input_string, md5_hash))
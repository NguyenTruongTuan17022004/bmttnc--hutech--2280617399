import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""

    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))

            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]

    message = ""
    for i in range(0, len(binary_message), 8):
        char_code = int(binary_message[i:i+8], 2)
        char = chr(char_code)
        # Assuming the '1111111111111110' marker from the encoding
        # corresponds to a specific character or sequence.
        # In the encoding, '1111111111111110' is 16 bits.
        # If the intention was to decode the 16-bit marker as two characters,
        # you'd need to adjust the decoding logic.
        # For simplicity, if the original intention was to use a null character
        # (ASCII 0) as a termination, that would be '00000000'.
        # Let's assume the termination marker implies a specific byte
        # that results in a null character or similar for simplicity,
        # or that the '1111111111111110' is decoded as the last two bytes.
        # The prompt image says "Kết thúc thông điệp khi gặp dấu '\0'",
        # so let's use that as the termination.
        if char == '\0':  # Kết thúc thông điệp khi gặp dấu '\0'
            break
        message += char

    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()
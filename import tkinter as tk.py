import tkinter as tk
from tkinter import messagebox

# Vigenere Cipher Standard (26 huruf alfabet)
def vigenere_cipher_standard(text, key, mode):
    alphabet_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet_lower = 'abcdefghijklmnopqrstuvwxyz'
    result = ''
    key = key.upper()  # Key diubah ke uppercase untuk keseragaman shift
    key_len = len(key)
    
    j = 0  # Indeks untuk key
    for i, char in enumerate(text):
        if char.isupper():  # Jika huruf besar
            shift = alphabet_upper.index(key[j % key_len])  # Shift berdasarkan huruf di key
            idx = alphabet_upper.index(char)  # Dapatkan indeks huruf di alfabet besar
            if mode == 'encrypt':
                new_idx = (idx + shift) % 26  # Enkripsi
            else:  # decrypt
                new_idx = (idx - shift) % 26  # Dekripsi
            result += alphabet_upper[new_idx]  # Tambahkan hasil ke teks output
            j += 1  # Hanya maju ke huruf key berikutnya jika char adalah huruf
        elif char.islower():  # Jika huruf kecil
            shift = alphabet_upper.index(key[j % key_len])  # Shift tetap berdasarkan key yang uppercase
            idx = alphabet_lower.index(char)  # Dapatkan indeks huruf di alfabet kecil
            if mode == 'encrypt':
                new_idx = (idx + shift) % 26  # Enkripsi
            else:  # decrypt
                new_idx = (idx - shift) % 26  # Dekripsi
            result += alphabet_lower[new_idx]  # Tambahkan hasil ke teks output
            j += 1  # Maju ke huruf key berikutnya
        else:
            result += char  # Jika bukan huruf, tetap tambahkan ke hasil tanpa modifikasi
    
    return result

# Vigenere Cipher Extended (256 karakter ASCII)
def vigenere_cipher_extended(text, key, mode):
    result = ''
    key_len = len(key)
    for i, char in enumerate(text):
        shift = ord(key[i % key_len])  # Ambil nilai ASCII dari karakter kunci
        char_code = ord(char)  # Ambil nilai ASCII dari karakter teks
        if mode == 'encrypt':
            new_code = (char_code + shift) % 256  # Operasi modulo 256
        else:  # decrypt
            new_code = (char_code - shift) % 256  # Operasi modulo 256
        result += chr(new_code)  # Ubah kembali nilai ASCII ke karakter
    return result

# Playfair Cipher (26 huruf alfabet)
def playfair_cipher(text, key, mode):
    def create_matrix(key):
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        key = ''.join(sorted(set(key.upper()), key=lambda x: key.index(x)))
        matrix = [char for char in key if char in alphabet]
        for char in alphabet:
            if char not in matrix:
                matrix.append(char)
        return [matrix[i:i+5] for i in range(0, 25, 5)]

    def find_position(char, matrix):
        for row_idx, row in enumerate(matrix):
            if char in row:
                return row_idx, row.index(char)

    def process_pair(a, b, matrix, mode):
        ra, ca = find_position(a, matrix)
        rb, cb = find_position(b, matrix)
        if ra == rb:
            if mode == 'encrypt':
                return matrix[ra][(ca+1)%5] + matrix[rb][(cb+1)%5]
            else:
                return matrix[ra][(ca-1)%5] + matrix[rb][(cb-1)%5]
        elif ca == cb:
            if mode == 'encrypt':
                return matrix[(ra+1)%5][ca] + matrix[(rb+1)%5][cb]
            else:
                return matrix[(ra-1)%5][ca] + matrix[(rb-1)%5][cb]
        else:
            return matrix[ra][cb] + matrix[rb][ca]

    matrix = create_matrix(key)
    text = text.replace('J', 'I').upper().replace(' ', '')
    if len(text) % 2 != 0:
        text += 'X'

    result = ''
    for i in range(0, len(text), 2):
        result += process_pair(text[i], text[i+1], matrix, mode)

    return result

# One-Time Pad (26 huruf alfabet)
def one_time_pad(text, key, mode):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = ''
    key = key.upper()
    key_len = len(key)
    
    if len(key) < len(text):  # Kunci harus sama panjang atau lebih panjang dari teks
        messagebox.showerror("Error", "Key must be at least as long as the text")
        return ""

    for i, char in enumerate(text):
        if char.isalpha():
            shift = alphabet.index(key[i])  # Ambil indeks dari karakter kunci
            idx = alphabet.index(char.upper())
            if mode == 'encrypt':
                new_idx = (idx + shift) % 26
            else:  # decrypt
                new_idx = (idx - shift) % 26
            result += alphabet[new_idx] if char.isupper() else alphabet[new_idx].lower()
        else:
            result += char  # Biarkan karakter non-alfabet tidak berubah
    return result

# Enigma Cipher (3-rotor)
def enigma_cipher(text, key, mode):
    # Rotor configurations (using simple alphabets for simulation)
    rotor_1 = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'  # Example rotor wiring
    rotor_2 = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
    rotor_3 = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
    reflector = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'  # Simple reflector wiring

    # Alphabet used
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Set initial rotor positions (based on key)
    rotor_1_position = alphabet.index(key[0].upper())
    rotor_2_position = alphabet.index(key[1].upper())
    rotor_3_position = alphabet.index(key[2].upper())

    result = ''

    def rotate_rotor(rotor):
        return rotor[1:] + rotor[0]

    for char in text.upper():
        if char not in alphabet:
            result += char  # Ignore non-alphabet characters
            continue
        
        # Rotate rotors
        rotor_1 = rotate_rotor(rotor_1)
        rotor_1_position = (rotor_1_position + 1) % 26

        if rotor_1_position == 0:  # Rotor 1 full rotation, rotate rotor 2
            rotor_2 = rotate_rotor(rotor_2)
            rotor_2_position = (rotor_2_position + 1) % 26
            
            if rotor_2_position == 0:  # Rotor 2 full rotation, rotate rotor 3
                rotor_3 = rotate_rotor(rotor_3)
                rotor_3_position = (rotor_3_position + 1) % 26

        # Pass through the rotors (forward)
        idx = alphabet.index(char)
        idx = alphabet.index(rotor_1[idx])
        idx = alphabet.index(rotor_2[idx])
        idx = alphabet.index(rotor_3[idx])

        # Pass through reflector
        idx = alphabet.index(reflector[idx])

        # Pass back through the rotors (reverse)
        idx = rotor_3.index(alphabet[idx])
        idx = rotor_2.index(alphabet[idx])
        idx = rotor_1.index(alphabet[idx])

        # Get final letter
        result += alphabet[idx]

    return result

# GUI
def process_cipher():
    text = input_text.get("1.0", "end-1c")
    key = key_entry.get()
    cipher_type = cipher_var.get()
    mode = mode_var.get()
    
    if cipher_type == "Vigenere Standard":
        result = vigenere_cipher_standard(text, key, mode)
    elif cipher_type == "Vigenere Extended":
        result = vigenere_cipher_extended(text, key, mode)
    elif cipher_type == "Playfair":
        result = playfair_cipher(text, key, mode)
    elif cipher_type == "One-Time Pad":
        result = one_time_pad(text, key, mode)
    elif cipher_type == "Enigma":
        result = enigma_cipher(text, key, mode)
    else:
        messagebox.showerror("Error", "Unsupported cipher type")
        return
    
    output_text.delete("1.0", "end")
    output_text.insert("1.0", result)

# Main window
root = tk.Tk()
root.title("Cipher GUI")

# Input text
tk.Label(root, text="Input Text:").pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack()

# Key entry (3 letters for Enigma Cipher)
tk.Label(root, text="Key:").pack()
key_entry = tk.Entry(root)
key_entry.pack()

# Cipher type
cipher_var = tk.StringVar(value="Vigenere Standard")
tk.Label(root, text="Cipher Type:").pack()
cipher_options = ["Vigenere Standard", "Vigenere Extended", "Playfair", "One-Time Pad", "Enigma"]
cipher_menu = tk.OptionMenu(root, cipher_var, *cipher_options)
cipher_menu.pack()

# Mode (Encrypt/Decrypt)
mode_var = tk.StringVar(value="encrypt")
tk.Label(root, text="Mode:").pack()
mode_menu = tk.OptionMenu(root, mode_var, "encrypt", "decrypt")
mode_menu.pack()

# Output text
tk.Label(root, text="Output Text:").pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack()

# Process button
process_button = tk.Button(root, text="Process", command=process_cipher)
process_button.pack()

root.mainloop()
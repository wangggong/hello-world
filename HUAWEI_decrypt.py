import sys

def decrypt(encrypted_letter):
    if 'A' <= encrypted_letter <= 'Z':
        return chr(ord(encrypted_letter.lower()) + 1) if encrypted_letter != 'Z' else 'a'
    if 'a' <= encrypted_letter <= 'z':
        decrypt_lower = {'abc': '2', 'def': '3', 'ghi': '4', 'jkl': '5', 'mno': '6', 'pqrs': '7', 'tuv': '8' ,'wxyz': '9'}
        return decrypt_lower[filter(lambda x: encrypted_letter in x, decrypt_lower)[0]]
    return encrypted_letter



encrypted_lines = sys.stdin.readlines()
for encrypted_line in encrypted_lines:
    print ''.join([decrypt(letter) for letter in encrypted_line.strip()])

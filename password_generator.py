import random
import string

def generate_password(length=12, use_uppercase=True, use_digits=True, use_special=True):
    # Define the character pools
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase if use_uppercase else ""
    digits = string.digits if use_digits else ""
    special_characters = string.punctuation if use_special else ""
    
    # Combine all the chosen pools
    all_characters = lowercase_letters + uppercase_letters + digits + special_characters
    
    if not all_characters:
        raise ValueError("At least one character type must be selected")
    
    # Ensure the password has at least one of each required type
    password = []
    if use_uppercase:
        password.append(random.choice(uppercase_letters))
    if use_digits:
        password.append(random.choice(digits))
    if use_special:
        password.append(random.choice(special_characters))
        
    # Fill the rest of the password length with random choices
    remaining_length = length - len(password)
    password += random.choices(all_characters, k=remaining_length)
    
    # Shuffle to avoid predicatable patterns
    random.shuffle(password)
    
    # Convert the list to a string
    return ''.join(password)

# Example usage
length = int(input("Enter the password length: "))
use_uppercase = input("Include uppercase letters? (yes/no): ").strip().lower() == "yes"
use_digits = input("Include digits? (yes/no): ").strip().lower() == "yes"
use_special = input("Include special characters? (yes/no): ").strip().lower() == "yes"

password = generate_password(length, use_uppercase, use_digits, use_special)
print(f"Generated Password: {password}")
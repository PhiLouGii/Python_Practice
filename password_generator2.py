import random
import string
import tkinter as tk
from tkinter import messagebox

# Function to generate a password
def generate_password():
    try:
        length = int(length_entry.get())
        use_uppercase = uppercase_var.get()
        use_digits = digits_var.get()
        use_special = special_var.get()
        
        #Define character pools
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase if use_uppercase else ""
        digits = string.digits if use_digits else ""
        special_characters = string.punctuation if use_special else ""
        
        all_characters = lowercase_letters + uppercase_letters + digits + special_characters
        
        if not all_characters:
            raise ValueError("At least one character type must be selected.")
        
        # Ensure password includes at least one character of each selected type
        password = []
        if use_uppercase:
            password.append(random.choice(uppercase_letters))
        if use_digits:
            password.append(random.choice(digits))
        if use_special:
            password.append(random.choice(special_characters))
            
        # Fill the remaining length with random characters
        remaining_length = length -len(password)
        password += random.choices(all_characters, k=remaining_length)
        random.shuffle(password)
        
        # Display the password
        password_entry.delete(0, tk.END)
        password_entry.insert(0, ''.join(password))
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        
# Create the main application window
app = tk.Tk()
app.title("Password Generator")
app.geometry("400x300")
app.resizable(False, False)

# Title label
title_label = tk.Label(app, text="Password Generator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Password length input
length_frame = tk.Frame(app)
length_frame.pack(pady=5)
length_label = tk.Label(length_frame, text="Password Length:")
length_label.pack(side=tk.LEFT, padx=5)
length_entry = tk.Entry(length_frame, width=5)
length_entry.pack(side=tk.LEFT)

# Options for character inclusion
options_frame = tk.Frame(app)
options_frame.pack(pady=5)

uppercase_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

uppercase_check = tk.Checkbutton(options_frame, text="Include Uppercase", variable=uppercase_var)
uppercase_check.pack(anchor=tk.W)
digits_check = tk.Checkbutton(options_frame, text="Include Digits", variable=digits_var)        
digits_check.pack(anchor=tk.W)
special_check = tk.Checkbutton(options_frame, text="Include Special Characters", variable=special_var)
special_check.pack(anchor=tk.W)

# Generate password button
generate_button = tk.Button(app, text="Generate Password", command=generate_password, bg="blue", fg="white")
generate_button.pack(pady=10)

# Display the generated password
password_entry = tk.Entry(app, font=("Arial", 14), justify="center", width=30)
password_entry.pack(pady=10)

# Run the application
app.mainloop()
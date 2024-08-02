from gtts import gTTS
from playsound import playsound
import tkinter as tk
import time
import os
from tkinter import ttk

# Function to convert text to speech
def Text_to_speech():
    Message = entry_field.get()
    language = language_combobox.get()  # Get the selected language
    
    if not Message:
        print("No text provided.")
        return
    
    # Map language names to language codes
    language_code_map = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Chinese': 'zh',
        # Add more languages here
    }
    
    lang_code = language_code_map.get(language, 'en')  # Default to English if not found
    speech = gTTS(text=Message, lang=lang_code)
    file_path = 'GetProjects.mp3'
    speech.save(file_path)
    playsound(file_path)
    time.sleep(3)
    os.remove(file_path)

# Create the Tkinter window
root = tk.Tk()
root.title("Text to Speech with Language Selection")

# Entry field for text input
entry_field = tk.Entry(root, width=50)
entry_field.pack(pady=10)

# Dropdown for language selection
language_label = tk.Label(root, text="Select Language:")
language_label.pack(pady=5)

language_combobox = ttk.Combobox(root, values=[
    'English', 'Spanish', 'French', 'German', 'Chinese'
])
language_combobox.set('English')  # Set default selection
language_combobox.pack(pady=5)

# Button to trigger text-to-speech
speak_button = tk.Button(root, text="Speak", command=Text_to_speech)
speak_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

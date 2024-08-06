from speechTranslator import speechTranslator
import tkinter as tk
from tkinter import ttk
import threading

def speech_input(st, from_lang, to_lang, original_text_box, translated_text_box, stop_event):
    def run():
        recognized_text = st.speechToText(stop_event)
        if recognized_text:
            translated_text = st.textToText(recognized_text, from_lang, to_lang)
            original_text_box.delete(1.0, tk.END)
            original_text_box.insert(tk.END, recognized_text)
            translated_text_box.delete(1.0, tk.END)
            translated_text_box.insert(tk.END, translated_text)

    if not stop_event.is_set():
        stop_event.clear()
        threading.Thread(target=run).start()
    else:
        stop_event.set()

def text_input(st, from_lang, to_lang, original_text_box, translated_text_box):
    recognized_text = original_text_box.get(1.0, tk.END).strip()
    if recognized_text:
        translated_text = st.textToText(recognized_text, from_lang, to_lang)
        translated_text_box.delete(1.0, tk.END)
        translated_text_box.insert(tk.END, translated_text)
        
def swap_sides(from_lang_var, to_lang_var, original_text_box, translated_text_box, root):
    from_lang, to_lang = to_lang_var.get(), from_lang_var.get()
    from_lang_var.set(from_lang), to_lang_var.set(to_lang)
    from_text, to_text = original_text_box.get(1.0, tk.END).strip(), translated_text_box.get(1.0, tk.END).strip()
    original_text_box.delete(1.0, tk.END), original_text_box.insert(tk.END, to_text)
    translated_text_box.delete(1.0, tk.END), translated_text_box.insert(tk.END, from_text)
    root.update_idletasks()
    

def main():
    st = speechTranslator()
     # Available languages
    languages = st.getAllLanguages()

    root = tk.Tk()
    root.title("Speech Translator")

    from_lang_var = tk.StringVar(root)
    to_lang_var = tk.StringVar(root)

    from_lang_var.set('english')  # default value
    to_lang_var.set('spanish')    # default value

    from_lang_menu = ttk.Combobox(root, textvariable=from_lang_var, values=list(languages.keys()))
    to_lang_menu = ttk.Combobox(root, textvariable=to_lang_var, values=list(languages.keys()))

    from_lang_label = tk.Label(root, text="From Language")
    to_lang_label = tk.Label(root, text="To Language")
    
    original_text_label = tk.Label(root, text="Original Text")
    original_text_box = tk.Text(root, height=5, width=50)

    translated_text_label = tk.Label(root, text="Translated Text")
    translated_text_box = tk.Text(root, height=5, width=50)
    
    swap_button = tk.Button(root, text="Swap\n<-\n->", command=lambda: swap_sides(from_lang_var, to_lang_var, original_text_box, translated_text_box, root))
    
    play_audio_button = tk.Button(root, text="Play Audio", command=lambda: st.textToSpeech(translated_text_box.get(1.0, tk.END).strip(), languages[to_lang_var.get()]))
    
    inputButtonFrame = tk.Frame(root)

    stop_event = threading.Event()
    record_button = tk.Button(inputButtonFrame, text="Hold to Speak", command=lambda: speech_input(st, languages[from_lang_var.get()], languages[to_lang_var.get()], original_text_box, translated_text_box, stop_event))   
    translate_button = tk.Button(inputButtonFrame, text="Translate Text", command=lambda: text_input(st, languages[from_lang_var.get()], languages[to_lang_var.get()], original_text_box, translated_text_box))
    record_button.grid(row=0, column=0)
    translate_button.grid(row=0, column=1, padx=10)



    from_lang_label.grid(row=0, column=0)
    from_lang_menu.grid(row=1, column=0)
    to_lang_label.grid(row=0, column=2)
    to_lang_menu.grid(row=1, column=2)
    original_text_label.grid(row=2, column=0)
    swap_button.grid(row=3, column=1)
    original_text_box.grid(row=3, column=0, padx=20)
    translated_text_label.grid(row=2, column=2)
    translated_text_box.grid(row=3, column=2, padx=20)
    inputButtonFrame.grid(row=4, column=0, pady=10)
    play_audio_button.grid(row=4, column=2, pady=10)
    


    root.mainloop()

if __name__ == "__main__":
    main()

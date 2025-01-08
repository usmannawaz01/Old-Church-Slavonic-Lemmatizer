import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from collections import defaultdict


def create_ocs_lemma_dict_with_counts(file_path):
    ocs_lemma_dict = defaultdict(list)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                word, lemma = line.strip().split(',')
                ocs_lemma_dict[word.strip()].append(lemma.strip())
    return ocs_lemma_dict


def lemmatize_with_ocs_dict_and_counts(text, ocs_lemma_dict):
    lemmatized_words = []
    word_lemma_pairs = []
    words = text.split()
    for word in words:
        lemmas = ocs_lemma_dict.get(word)
        if lemmas:
            lemma_counter = defaultdict(int)
            for lemma in lemmas:
                lemma_counter[lemma] += 1
            most_common_lemma = max(lemma_counter, key=lemma_counter.get)
            lemmatized_words.append(most_common_lemma)
            word_lemma_pairs.append((word, most_common_lemma))
        else:
            lemmatized_words.append(word)
            word_lemma_pairs.append((word, word))
    return ' '.join(lemmatized_words), word_lemma_pairs


def show_word_lemma_table(word_lemma_pairs):
    table_window = tk.Toplevel()
    table_window.title("Word-Lemma Table")


    frame = tk.Frame(table_window)
    frame.pack(fill=tk.BOTH, expand=True)


    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    table_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=table_frame, anchor="nw")


    tk.Label(table_frame, text="Word", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(table_frame, text="Lemma", font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=5)


    for i, (word, lemma) in enumerate(word_lemma_pairs):
        tk.Label(table_frame, text=word, font=("Arial", 10)).grid(row=i+1, column=0, padx=10, pady=5)
        tk.Label(table_frame, text=lemma, font=("Arial", 10)).grid(row=i+1, column=1, padx=10, pady=5)

    table_window.mainloop()


def show_datasets(file_paths):
    dataset_window = tk.Toplevel()
    dataset_window.title("View Datasets")

    tk.Label(dataset_window, text="Select a dataset file to view its content:", font=("Arial", 12)).pack(pady=5)

    file_frame = tk.Frame(dataset_window)
    file_frame.pack(fill=tk.BOTH, expand=True)

    file_listbox = tk.Listbox(file_frame, font=("Arial", 12), height=10)
    file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

    scrollbar = tk.Scrollbar(file_frame, orient=tk.VERTICAL, command=file_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    file_listbox.configure(yscrollcommand=scrollbar.set)

    for file_path in file_paths:
        file_listbox.insert(tk.END, file_path)

    content_box = scrolledtext.ScrolledText(dataset_window, wrap=tk.WORD, font=("Arial", 12), height=15, width=80)
    content_box.pack(padx=10, pady=5)

    def display_file_content(event):
        selection = file_listbox.curselection()
        if selection:
            selected_file = file_paths[selection[0]]
            with open(selected_file, 'r', encoding='utf-8') as file:
                content = file.read()
            content_box.delete("1.0", tk.END)
            content_box.insert(tk.END, content)

    file_listbox.bind("<<ListboxSelect>>", display_file_content)


def create_gui(ocs_lemma_dict):
    current_word_lemma_pairs = []

    def lemmatize_text():
        input_text = input_text_box.get("1.0", tk.END).strip()
        if not input_text:
            messagebox.showwarning("Input Error", "Please paste some text to lemmatize.")
            return
        lemmatized_text, word_lemma_pairs = lemmatize_with_ocs_dict_and_counts(input_text, ocs_lemma_dict)
        output_text_box.delete("1.0", tk.END)
        output_text_box.insert(tk.END, lemmatized_text)

        show_table_button.config(state=tk.NORMAL)
        nonlocal current_word_lemma_pairs
        current_word_lemma_pairs = word_lemma_pairs

    def show_table():
        show_word_lemma_table(current_word_lemma_pairs)

    def view_datasets():
        dataset_files = [
            "fold1words.txt", "fold2words.txt",
            "fold3words.txt", "fold4words.txt",
            "fold5words.txt"
        ]
        show_datasets(dataset_files)

    root = tk.Tk()
    root.title("Old Church Slavonic Lemmatizer")

    tk.Label(root, text="Paste Old Church Slavonic Text Below:", font=("Arial", 12)).pack(pady=5)
    input_text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, font=("Arial", 12))
    input_text_box.pack(padx=10, pady=5)

    lemmatize_button = tk.Button(root, text="Lemmatize Text", font=("Arial", 12), command=lemmatize_text)
    lemmatize_button.pack(pady=5)

    tk.Label(root, text="Lemmatized Text Output Below:", font=("Arial", 12)).pack(pady=5)
    output_text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, font=("Arial", 12))
    output_text_box.pack(padx=10, pady=5)

    show_table_button = tk.Button(root, text="Show Word-Lemma Table", font=("Arial", 12), state=tk.DISABLED, command=show_table)
    show_table_button.pack(pady=5)

    dataset_button = tk.Button(root, text="View Datasets", font=("Arial", 12), command=view_datasets)
    dataset_button.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":

    lemma_dict_file = "dic_f2_train.txt"

    try:
        ocs_lemma_dict = create_ocs_lemma_dict_with_counts(lemma_dict_file)
        create_gui(ocs_lemma_dict)
    except FileNotFoundError:
        messagebox.showerror("File Error", f"Lemma dictionary file not found at path: {lemma_dict_file}")

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from newspaper import Article  
from PyPDF2 import PdfReader  

# Load the model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Function to summarize text
def summarize_text(article, max_length=130, min_length=30, num_beams=4):
    inputs = tokenizer(article, max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=num_beams,
        early_stopping=True,
    )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Function to extract text from URLs
def extract_text_from_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        raise ValueError(f"Error extracting text from URL: {e}")

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

# GUI application
class SummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarizer")
        self.root.geometry("800x600")
        
        # Input Frame
        self.input_frame = tk.LabelFrame(root, text="Input Article", padx=10, pady=10, font=("Arial", 12, "bold"))
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.url_entry = tk.Entry(self.input_frame, width=50, font=("Arial", 12), fg="gray")
        self.url_entry.insert(0, "Enter URL here...")  # Placeholder for URL input
        self.url_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.url_button = tk.Button(self.input_frame, text="Fetch from URL", command=self.fetch_url, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.url_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.pdf_button = tk.Button(self.input_frame, text="Load PDF", command=self.load_pdf, bg="#008CBA", fg="white", font=("Arial", 12))
        self.pdf_button.grid(row=0, column=2, padx=5, pady=5, columnspan=2)
        
        self.text_input = scrolledtext.ScrolledText(self.input_frame, height=10, wrap="word", font=("Courier", 12), bg="lightyellow")
        self.text_input.grid(row=1, column=0,columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Summarize Button (moved above the Summary section)
        self.summarize_button = tk.Button(root, text="Summarize", command=self.summarize_input, bg="#008CBA", fg="white", font=("Arial", 14, "bold"))
        self.summarize_button.grid(row=1, column=0, padx=10, pady=10)

        # Output Frame (Summary section)
        self.output_frame = tk.LabelFrame(root, text="Summary", padx=10, pady=10, font=("Arial", 12, "bold"))
        self.output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        
        self.summary_output = scrolledtext.ScrolledText(self.output_frame, height=10, wrap="word", font=("Courier", 12), bg="lightgray")
        self.summary_output.pack(fill="both", expand="yes", padx=5, pady=5)



        # Configure grid weights for resizing
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def fetch_url(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL.")
            return
        try:
            article_text = extract_text_from_url(url)
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, article_text)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        try:
            article_text = extract_text_from_pdf(file_path)
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, article_text)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def summarize_input(self):
        article_text = self.text_input.get(1.0, tk.END).strip()
        if not article_text:
            messagebox.showerror("Error", "Please provide text to summarize.")
            return
        try:
            summary = summarize_text(article_text)
            self.summary_output.delete(1.0, tk.END)
            self.summary_output.insert(tk.END, summary)
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = SummarizerApp(root)
    root.mainloop()

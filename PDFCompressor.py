import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
from PIL import Image, ImageTk
import os
import subprocess

class PDFToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToyotechICT Solutions")
        self.root.geometry("600x500")
        self.root.config(bg="#E0F7FA")
        
        # Add PNG icon (Linux or macOS only)
        try:
            icon_image = Image.open("icon.png")
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            self.root.iconphoto(True, self.icon_photo)
        except Exception as e:
            print(f"Error loading PNG icon: {e}")

        self.file_paths = []

        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="PDF Merger and Compressor", font=("Helvetica", 18, "bold"), bg="#E0F7FA")
        title_label.pack(pady=10)

        # Merge PDF Section
        merge_frame = tk.Frame(self.root, bg="#E0F7FA", bd=2, relief=tk.SOLID)
        merge_frame.pack(pady=10, padx=10, fill=tk.X)

        merge_label = tk.Label(merge_frame, text="Merge PDFs", font=("Helvetica", 14, "bold"), bg="#80DEEA")
        merge_label.pack(pady=5, fill=tk.X)

        select_merge_button = tk.Button(merge_frame, text="Select PDF Files", command=self.select_merge_files, bg="#4FC3F7", fg="white")
        select_merge_button.pack(pady=5)

        self.merge_files_frame = tk.Frame(merge_frame, bg="#E0F7FA")
        self.merge_files_frame.pack(pady=5, padx=10, fill=tk.X)

        self.merge_button = tk.Button(merge_frame, text="Merge PDFs", command=self.merge_files, state=tk.DISABLED, bg="#0288D1", fg="white")
        self.merge_button.pack(pady=5)

        # Compress PDF Section
        compress_frame = tk.Frame(self.root, bg="#E0F7FA", bd=2, relief=tk.SOLID)
        compress_frame.pack(pady=10, padx=10, fill=tk.X)

        compress_label = tk.Label(compress_frame, text="Compress PDF", font=("Helvetica", 14, "bold"), bg="#80DEEA")
        compress_label.pack(pady=5, fill=tk.X)

        select_compress_button = tk.Button(compress_frame, text="Select a PDF File", command=self.select_compress_file, bg="#4FC3F7", fg="white")
        select_compress_button.pack(pady=5)

        self.compress_files_frame = tk.Frame(compress_frame, bg="#E0F7FA")
        self.compress_files_frame.pack(pady=5, padx=10, fill=tk.X)

        self.compress_button = tk.Button(compress_frame, text="Compress PDF", command=self.compress_file, state=tk.DISABLED, bg="#0288D1", fg="white")
        self.compress_button.pack(pady=5)

    def select_merge_files(self):
        self.file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if self.file_paths:
            for widget in self.merge_files_frame.winfo_children():
                widget.destroy()

            for file_path in self.file_paths:
                file_label = tk.Label(self.merge_files_frame, text=os.path.basename(file_path), bg="#E0F7FA")
                file_label.pack(anchor="w")

            messagebox.showinfo("Selected Files", f"Selected {len(self.file_paths)} files.")
            self.merge_button.config(state=tk.NORMAL)

    def select_compress_file(self):
        self.file_paths = [filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])]
        if self.file_paths[0]:
            for widget in self.compress_files_frame.winfo_children():
                widget.destroy()

            file_label = tk.Label(self.compress_files_frame, text=os.path.basename(self.file_paths[0]), bg="#E0F7FA")
            file_label.pack(anchor="w")

            messagebox.showinfo("Selected File", f"Selected file: {os.path.basename(self.file_paths[0])}")
            self.compress_button.config(state=tk.NORMAL)

    def merge_files(self):
        merger = PdfMerger()
        for file_path in self.file_paths:
            merger.append(file_path)

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_path:
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Merge Complete", f"PDF files merged successfully and saved to {output_path}.")

    def compress_file(self):
        compressed_output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not compressed_output_path:
            return

        command = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={compressed_output_path}",
            self.file_paths[0]
        ]

        subprocess.run(command, check=True)
        messagebox.showinfo("Compression Complete", f"PDF file compressed successfully and saved to {compressed_output_path}.")

def main():
    root = tk.Tk()
    app = PDFToolApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

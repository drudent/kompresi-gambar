import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, master):
        self.root = master
        self.input_files = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.status = tk.StringVar(value="")
        self.compression_percentage = tk.IntVar(value=50)  # Default: 50 singular values
        self.preview_windows = []
        self.icon = tk.PhotoImage(file='logo.png')
        self.root.iconphoto(True, self.icon)

        self.root.title("Kompresi Gambar | Aljabar Kel. 6 BA")
        self.root.configure(bg="#eeeeee")
        self.root.geometry("800x426")
        self.root.maxsize(800, 426)
        self.root.minsize(800, 426)

        # Menu Bar
        menu_bar = tk.Menu(self.root, bg="#eeeeee", relief="flat")
        menu_bar.add_command(label="Bantuan", command=self.show_bantuan)
        menu_bar.add_command(label="Tentang", command=self.show_tentang)
        self.root.configure(menu=menu_bar)

        # Button frame for input
        input_frame = tk.Frame(self.root, bg="#eeeeee")
        input_frame.pack(fill="x", padx=15, pady=8)

        # Input file
        tk.Label(input_frame, text="Pilih Gambar:", bg="#eeeeee", anchor="w").pack(
            fill="x"
        )

        tk.Button(
            input_frame,
            text="Pilih Gambar",
            command=self.select_input_files,
            bg="#3498db",
            fg="#ffffff",
            activebackground="#1d577e",
            activeforeground="#ffffff",
            relief="flat",
        ).pack(pady=8, ipadx=24, ipady=6, side="left")

        tk.Entry(
            input_frame, 
            textvariable=self.input_files, 
            bg="#fff", 
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground="#999999",
            highlightcolor="#999999"
        ).pack(
            fill="x", padx=(20, 0), pady=8, ipadx=24, ipady=9
        )

        # Button frame for Output
        output_frame = tk.Frame(self.root, bg="#eeeeee")
        output_frame.pack(fill="x", padx=15, pady=8)

        # Output folder
        tk.Label(output_frame, text="Pilih Output Folder:", bg="#eeeeee", anchor="w").pack(
            fill="x", pady=(8, 0)
        )
        
        tk.Button(
            output_frame,
            text="Pilih Output Folder:",
            command=self.select_output_folder,
            bg="#3498db",
            fg="#ffffff",
            activebackground="#22638f",
            activeforeground="#ffffff",
            relief="flat",
        ).pack(pady=8, ipadx=24, ipady=6, side="left")

        tk.Entry(
            output_frame, 
            textvariable=self.output_folder, 
            bg="#fff", 
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground="#999999",
            highlightcolor="#999999"
        ).pack(
            padx=(20, 0), pady=8, ipadx=24, ipady=9, fill="x"
        )

        # Persentase kompresi
        tk.Label(self.root, text="Jumlah Singular Values (1-100):", bg="#eeeeee", anchor="w").pack(
            fill="x", padx=12, pady=(16, 0)
        )
        tk.Scale(
            self.root,
            from_=1,
            to=100,
            orient="horizontal",
            variable=self.compression_percentage,
            bg="#eeeeee",
        ).pack(fill="x", padx=15, pady=(2, 8))

        # Status
        tk.Label(
            self.root, textvariable=self.status, bg="#eeeeee", anchor="w", wraplength=320, font=("", 11)
        ).pack(padx=12, pady=(0, 8), anchor="center")

        # Button frame for Preview and Compress
        button_frame = tk.Frame(self.root, bg="#eeeeee")
        button_frame.pack(fill="x", padx=15, pady=8)

        # Clear status button
        tk.Button(
            button_frame,
            text="Bersihkan",
            command=self.reset_status,
            bg="#717d7e",
            fg="#ffffff",
            activebackground="#4e5455",
            activeforeground="#ffffff",
            relief="flat",
        ).pack(side="left", padx=(0, 10), ipady=6, ipadx=32)

        # Preview button
        tk.Button(
            button_frame,
            text="Preview",
            command=self.preview_compression,
            bg="#e67e22",
            fg="#ffffff",
            activebackground="#9b5518",
            activeforeground="#ffffff",
            relief="flat",
        ).pack(side="left", padx=(10, 10), ipady=6, ipadx=32)

        # Compress button
        tk.Button(
            button_frame,
            text="Kompres",
            command=self.compress_images,
            bg="#27ae60",
            fg="#ffffff",
            activebackground="#156135",
            activeforeground="#ffffff",
            relief="flat",
        ).pack(side="left", padx=(10, 10), ipady=6, ipadx=32)

        # Button frame for Clear and Exit
        bottom_frame = tk.Frame(self.root, bg="#eeeeee")
        bottom_frame.pack(fill="x", padx=15, pady=(4, 12))

        # Exit button
        tk.Button(
            bottom_frame,
            text="Keluar",
            command=self.exit_application,
            bg="#c0392b",
            fg="#ffffff",
            activebackground="#7a251b",
            activeforeground="#ffffff",
            relief="flat",
        ).pack(side="right", padx=(4, 0), ipady=6, ipadx=32)

    def preview_compression(self):
        input_files = self.input_files.get().split("; ")
        
        if not input_files or input_files[0] == "":
            self.status.set("Error: File tidak valid!")
            return
        for filepath in input_files:
            if os.path.isfile(filepath):
                try:
                    # Create preview window
                    preview_window = tk.Toplevel(self.root)
                    preview_window.title("Preview Kompresi")
                    preview_window.geometry("800x400")
                    self.preview_windows.append(preview_window)

                    # Original image
                    original_frame = tk.Frame(preview_window)
                    original_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)
                    tk.Label(original_frame, text="Gambar Asli").pack()

                    # Compressed image
                    compressed_frame = tk.Frame(preview_window)
                    compressed_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
                    tk.Label(compressed_frame, text="Preview Hasil Kompresi").pack()

                    # Load and display original image
                    original_img = Image.open(filepath)
                    # Resize for display
                    original_img.thumbnail((350, 350))
                    original_photo = ImageTk.PhotoImage(original_img)
                    original_label = tk.Label(original_frame, image=original_photo)
                    original_label.image = original_photo
                    original_label.pack()

                    # Create preview of compressed image
                    k = self.compression_percentage.get()
                    compressed_img = compress_image_with_color(filepath, k)
                    
                    # Resize for display
                    compressed_img.thumbnail((350, 350))
                    compressed_photo = ImageTk.PhotoImage(compressed_img)
                    compressed_label = tk.Label(compressed_frame, image=compressed_photo)
                    compressed_label.image = compressed_photo
                    compressed_label.pack()

                except Exception as e:
                    self.status.set(f"Error dalam preview: {e}")
                    continue

    def select_input_files(self):
        files = filedialog.askopenfilenames(
            title="Pilih Gambar Input",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")],
        )
        if files:
            self.input_files.set("; ".join(files))

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)

    def compress_images(self):
        input_files = self.input_files.get().split("; ")
        output_path = self.output_folder.get()

        if not input_files or input_files[0] == "":
            self.status.set("Error: File tidak valid!")
            return
        if not os.path.isdir(output_path):
            self.status.set("Error: Folder output tidak valid!")
            return

        self.status.set("Memproses gambar menggunakan SVD...")

        for filepath in input_files:
            if os.path.isfile(filepath):
                filename = os.path.basename(filepath)
                destination_file = os.path.join(output_path, filename)

                try:
                    # Kompresi menggunakan SVD dengan warna
                    k = self.compression_percentage.get()
                    compressed_img = compress_image_with_color(filepath, k)
                    compressed_img.save(destination_file)

                except Exception as e:
                    self.status.set(f"Error memproses {filename}: {e}")
                    continue

        self.status.set("Kompres sukses!")

    def reset_status(self):
        self.input_files.set("")
        self.output_folder.set("")
        self.status.set("")

    def exit_application(self):
        # Close all preview windows
        for window in self.preview_windows:
            window.destroy()
        self.root.quit()

    def show_bantuan(self):
        messagebox.showinfo(
            "Bantuan",
            """1. Pilih gambar yang ingin dikompresi.
2. Pilih folder output untuk menyimpan hasil gambar.
3. Atur jumlah singular values (1-100) untuk mengontrol kualitas hasil.
4. Tekan "Preview" untuk melihat hasil sebelum menyimpan.
5. Tekan "Kompres" untuk memulai proses.
"""
        )

    def show_tentang(self):
        messagebox.showinfo(
            "Tentang",
            """Image Compression Aljaber V,1.0.0
Aplikasi ini digunakan untuk mengompresi gambar dengan format JPG, JPEG, PNG, MPEG, dan HEIC.
"""
        )

def compress_color_channel(channel_matrix, k):
    """
    Kompres satu channel warna menggunakan SVD.
    """
    U, S, Vt = np.linalg.svd(channel_matrix, full_matrices=False)
    # Rekonstruksi matriks menggunakan k singular values
    S_k = np.diag(S[:k])
    U_k = U[:, :k]
    Vt_k = Vt[:k, :]
    compressed_channel = np.dot(U_k, np.dot(S_k, Vt_k))
    return np.clip(compressed_channel, 0, 255).astype(np.uint8)

def compress_image_with_color(input_file, k):
    """
    Kompres gambar berwarna menggunakan SVD untuk setiap channel warna.
    Args:
        input_file (str): Path file gambar input.
        k (int): Jumlah singular values yang dipertahankan.
    Returns:
        PIL.Image: Gambar yang telah dikompresi
    """
    # Baca gambar berwarna
    img = Image.open(input_file)
    
    # Konversi ke RGB jika dalam mode lain (misal RGBA)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Pisahkan ke array numpy
    img_array = np.array(img)
    
    # Proses setiap channel warna
    compressed_channels = []
    for channel in range(3):  # RGB memiliki 3 channel
        channel_matrix = img_array[:, :, channel]
        compressed_channel = compress_color_channel(channel_matrix, k)
        compressed_channels.append(compressed_channel)
    
    # Gabungkan kembali channel-channel yang telah dikompresi
    compressed_array = np.stack(compressed_channels, axis=2)
    
    # Konversi kembali ke gambar PIL
    return Image.fromarray(compressed_array)

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    app = MainWindow(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
import io

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")

        self.label = tk.Label(root, text="Enter comma-separated values:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=5)

        self.generate_button = tk.Button(root, text="Generate QR Codes", command=self.generate_qr_codes)
        self.generate_button.pack(pady=20)

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

    def generate_qr_codes(self):
        values = self.entry.get().split(',')
        if not values or values == ['']:
            messagebox.showerror("Error", "Please enter some values.")
            return

        self.canvas.delete("all")
        
        for index, value in enumerate(values):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(value.strip())
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((100, 100), Image.LANCZOS)

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            img = Image.open(io.BytesIO(img_byte_arr))

            img = ImageTk.PhotoImage(img)

            x_position = (index % 4) * 110 + 10
            y_position = (index // 4) * 110 + 10
            self.canvas.create_image(x_position, y_position, anchor='nw', image=img)
            self.canvas.image = img

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()


import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import os

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

        self.save_button = tk.Button(root, text="Save QR Codes", command=self.save_qr_codes)
        self.save_button.pack(pady=5)

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.qr_images = []

    def generate_qr_codes(self):
        values = self.entry.get().split(',')
        if not values or values == ['']:
            messagebox.showerror("Error", "Please enter some values.")
            return

        self.canvas.delete("all")
        self.qr_images.clear()
        
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

            img_byte_arr = ImageTk.PhotoImage(img)._PhotoImage__photo.write("img{}.png".format(index), format='png')

            photo_img = ImageTk.PhotoImage(img)
            self.qr_images.append(photo_img)

            x_position = (index % 4) * 110 + 10
            y_position = (index // 4) * 110 + 10
            self.canvas.create_image(x_position, y_position, anchor='nw', image=photo_img)

    def save_qr_codes(self):
        if not self.qr_images:
            messagebox.showerror("Error", "No QR codes generated.")
            return

        directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Directory to Save QR Codes")
        if directory:
            for index, qr_image in enumerate(self.qr_images):
                qr_image.write(os.path.join(directory, f"qr_code_{index}.png"), format="png")

            messagebox.showinfo("Success", "QR codes saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()


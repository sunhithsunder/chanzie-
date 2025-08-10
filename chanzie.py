import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
import random
import sys

# App state
app_running = True

# Main window setup
root = tk.Tk()
root.title("chanzie!!")
root.state('zoomed')  # Fullscreen with window controls
root.configure(bg="#ffe6f0")

# Fonts
custom_font = ("Segoe Print", 13)
header_font = ("Segoe Print", 20, "bold")
title_font = ("Segoe Print", 36, "bold")

# Handle close


def on_close():
    global app_running
    app_running = False
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
root.bind("<Escape>", lambda e: on_close())

# Background canvas with hearts
canvas = tk.Canvas(root, bg="#ffe6f0", highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

# Place hearts
for _ in range(70):
    x = random.randint(0, root.winfo_screenwidth())
    y = random.randint(50, root.winfo_screenheight())
    heart = random.choice(["💖", "💕", "💓", "💞", "💘"])
    canvas.create_text(x, y, text=heart, font=(
        "Segoe UI Emoji", random.randint(12, 20)))

# Title banner
title_banner = tk.Label(root, text="chanzie!!",
                        bg="#ffe6f0", font=title_font, fg="#ff3399")
title_banner.place(relx=0.5, y=10, anchor="n")

# Clock
clock_label = tk.Label(root, text="", bg="#ffe6f0", font=("Segoe Print", 12))
clock_label.place(x=10, y=10)


def update_clock():
    now = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=now)
    if app_running:
        root.after(1000, update_clock)


# Content Frame
frame = tk.Frame(root, bg="#ffe6f0")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Entry
title_label = tk.Label(frame, text="Title:", bg="#ffe6f0", font=header_font)
title_label.grid(row=0, column=0, sticky="w")
title_entry = tk.Entry(frame, font=custom_font, width=40)
title_entry.grid(row=0, column=1, pady=10)

# Body Text
body_text = tk.Text(frame, font=custom_font, wrap="none",  # disable word wrap for horizontal scroll
                    height=20, width=60, bg="#fff0f5")
body_text.grid(row=1, column=0, columnspan=2, pady=10)

# Vertical Scrollbar
scrollbar_y = tk.Scrollbar(frame, command=body_text.yview)
scrollbar_y.grid(row=1, column=2, sticky="ns")
body_text.config(yscrollcommand=scrollbar_y.set)

# Horizontal Scrollbar
scrollbar_x = tk.Scrollbar(frame, orient="horizontal", command=body_text.xview)
scrollbar_x.grid(row=2, column=0, columnspan=2, sticky="ew")
body_text.config(xscrollcommand=scrollbar_x.set)

# Save button


def save_file():
    title = title_entry.get().strip()
    body = body_text.get("1.0", tk.END).strip()
    if not body:
        messagebox.showerror("nooo babygirl!!!",
                             "write something before you save silly!!")
        return
    if not title:
        title = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = filedialog.asksaveasfilename(
        defaultextension=".chanzie",
        filetypes=[("Chanzie Files", "*.chanzie")],
        initialfile=title
    )
    if filename:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write(
                f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(body)


save_button = tk.Button(root, text="💾 Save", font=(
    "Segoe Print", 10), bg="#ff99cc", command=save_file)
save_button.place(relx=0.97, rely=0.01, anchor="ne")

# Load button


def load_file(filename=None):
    if not filename:
        filename = filedialog.askopenfilename(defaultextension=".chanzie", filetypes=[
                                              ("Chanzie Files", "*.chanzie")])
    if filename and os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                title_entry.delete(0, tk.END)
                title_entry.insert(0, lines[0].replace("Title: ", "").strip())
                body_text.delete("1.0", tk.END)
                body_text.insert(tk.END, "".join(lines[3:]))


load_button = tk.Button(root, text="📂 Load", font=(
    "Segoe Print", 10), bg="#ff99cc", command=load_file)
load_button.place(relx=0.87, rely=0.01, anchor="ne")

# If a file is passed via command-line (e.g., double-click)
if len(sys.argv) > 1:
    passed_file = sys.argv[1]
    if os.path.isfile(passed_file) and passed_file.lower().endswith(".chanzie"):
        load_file(passed_file)

# Start everything
update_clock()
root.mainloop()

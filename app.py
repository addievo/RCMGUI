import tkinter as tk
from ctypes import windll
from PIL import Image, ImageTk


def get_key_status():
    hllDll = windll.LoadLibrary("User32.dll")
    VK_CAPITAL, VK_SCROLL = 0x14, 0x91
    return (hllDll.GetKeyState(VK_CAPITAL) & 1) == 1, (hllDll.GetKeyState(VK_SCROLL) & 1) == 1


def update_status():
    caps_lock, num_lock = get_key_status()
    highest_recoil = caps_lock and num_lock

    # Updating the "Lowest Recoil" indicator
    update_indicator(caps_lock_indicator, caps_lock and not highest_recoil)

    # Updating the "Medium Recoil" indicator
    update_indicator(num_lock_indicator, num_lock and not highest_recoil)

    # Updating the "Highest Recoil" indicator
    update_indicator(scroll_lock_indicator, highest_recoil)

    root.after(1000, update_status)

def update_indicator(indicator, status):
    color = "#00FF00" if status else "#FF0000"
    indicator.config(bg=color)

def close_app():
    root.destroy()

root = tk.Tk()
root.overrideredirect(True)  # Turn off the default title bar
root.geometry('200x200+200+200')  # New geometry for the window
root.title("RCM")
root.resizable(False, False)

# Gradient background
gradient = Image.new("RGB", (200, 200), color=0)
for y in range(200):
    r = int(101 * (1 - y / 199) + 234 * (y / 199))
    g = int(78 * (1 - y / 199) + 170 * (y / 199))
    b = int(163 * (1 - y / 199) + 200 * (y / 199))
    for x in range(200):
        gradient.putpixel((x, y), (r, g, b))

gradient_image = ImageTk.PhotoImage(gradient)
background_label = tk.Label(root, image=gradient_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Draggable area setup
def start_move(event):
    root.x = event.x
    root.y = event.y

def on_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")



movable_area = tk.Label(root, bg='#654ea3')  # Set the background color to match your design
movable_area.place(x=0, y=0, width=200, height=20)  # Adjust the height as needed

movable_area.bind("<ButtonPress-1>", start_move)
movable_area.bind("<B1-Motion>", on_move)


# Create a minimalist close button
close_button = tk.Label(root, text="x", font=("Arial", 12, "bold"), fg='black', bg='#654ea3')  # Match the gradient start color
close_button.place(x=195, y=1, width=5, height=5)  # Adjust width and height as needed

close_button.bind("<Button-1>", lambda e: close_app())

# Status indicators
caps_lock_indicator = tk.Canvas(root, width=20, height=20, bg='red', highlightthickness=0)
caps_lock_indicator.place(x=155, y=60)

num_lock_indicator = tk.Canvas(root, width=20, height=20, bg='red', highlightthickness=0)
num_lock_indicator.place(x=155, y=110)

scroll_lock_indicator = tk.Canvas(root, width=20, height=20, bg='red', highlightthickness=0)
scroll_lock_indicator.place(x=155, y=160)

# Text labels
font_settings = ("Arial", 12)
tk.Label(root, text="Lowest Recoil:", font=font_settings, bg='white').place(x=25, y=57)
tk.Label(root, text="Medium Recoil:", font=font_settings, bg='white').place(x=25, y=107)
tk.Label(root, text="Highest Recoil:", font=font_settings, bg='white').place(x=25, y=157)

update_status()

root.mainloop()

import tkinter as tk

def start_download():
    url = url_entry.get()
    print("Downloading:", url)


window = tk.Tk()
window.title("Mini Download Manager")
window.geometry("500x250")


label = tk.Label(window, text="Download URL:")
label.pack(pady=10)


url_entry = tk.Entry(window, width=60)
url_entry.pack()


download_button = tk.Button(
    window,
    text="Start Download",
    command=start_download
)
download_button.pack(pady=20)


window.mainloop()
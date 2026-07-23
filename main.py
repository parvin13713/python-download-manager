import tkinter as tk
from tkinter import ttk
from downloader import download_file


def update_progress(value):
    progress_bar["value"] = value
    window.update_idletasks()


def start_download():
    url = url_entry.get()

    try:
        status_label.config(text="Downloading...")
        
        filename = download_file(url, update_progress)

        status_label.config(
            text=f"Downloaded: {filename}"
        )

    except Exception as e:
        status_label.config(
            text="Download failed ❌"
        )
        print(e)


window = tk.Tk()
window.title("Mini Download Manager")
window.geometry("500x300")


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


progress_bar = ttk.Progressbar(
    window,
    length=400
)
progress_bar.pack(pady=10)


status_label = tk.Label(window, text="")
status_label.pack()


window.mainloop()
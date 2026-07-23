from downloader import download_file
import tkinter as tk

def start_download():
    url = url_entry.get()

    filename = download_file(url)

    status_label.config(
        text=f"Downloaded: {filename}"
    )


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

status_label = tk.Label(window, text="")
status_label.pack()
window.mainloop()
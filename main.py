import threading
import tkinter as tk
from tkinter import ttk, filedialog
from downloader import download_file


def update_progress(percent, downloaded, total_size, speed):

    def update():

        progress_bar["value"] = percent

        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)
        speed_mb = speed / (1024 * 1024)

        info_label.config(
            text=f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB\n"
                 f"Speed: {speed_mb:.2f} MB/s"
        )

    window.after(0, update)



def download_thread(url):

    try:
        save_path = filedialog.asksaveasfilename(
            title="Save File",
            initialfile=url.split("/")[-1]
        )

        if not save_path:
            status_label.config(text="Download cancelled")
            download_button.config(state="normal")
            return


        download_file(
            url,
            save_path,
            update_progress
        )


        status_label.config(
            text="Download completed ✅"
        )

        download_button.config(
            state="normal"
        )


    except Exception as e:

        status_label.config(
            text="Download failed ❌"
        )

        print(type(e))
        print(e)

        download_button.config(
            state="normal"
        )



def start_download():

    url = url_entry.get()

    download_button.config(
        state="disabled"
    )

    status_label.config(
        text="Downloading..."
    )


    thread = threading.Thread(
        target=download_thread,
        args=(url,)
    )

    thread.start()



window = tk.Tk()

window.title("Mini Download Manager")
window.geometry("500x300")



label = tk.Label(
    window,
    text="Download URL:"
)

label.pack(pady=10)



url_entry = tk.Entry(
    window,
    width=60
)

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



info_label = tk.Label(
    window,
    text="Downloaded: 0 MB / 0 MB\nSpeed: 0 MB/s"
)

info_label.pack(pady=5)



status_label = tk.Label(
    window,
    text=""
)

status_label.pack()



window.mainloop()
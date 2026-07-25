import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog

from downloader import download_file


progress_queue = queue.Queue()


def update_gui():

    try:

        while True:

            (
                percent,
                downloaded,
                total_size,
                speed,
                eta
            ) = progress_queue.get_nowait()

            progress_bar["value"] = percent

            downloaded_mb = downloaded / (1024 * 1024)

            total_mb = total_size / (1024 * 1024) if total_size else 0

            speed_mb = speed / (1024 * 1024)

            if eta > 0:

                minutes = int(eta // 60)

                seconds = int(eta % 60)

                eta_text = f"{minutes:02d}:{seconds:02d}"

            else:

                eta_text = "--:--"

            info_label.config(

                text=(
                    f"Downloaded : {downloaded_mb:.2f} MB / {total_mb:.2f} MB\n"
                    f"Speed      : {speed_mb:.2f} MB/s\n"
                    f"Remaining  : {eta_text}"
                )

            )

    except queue.Empty:

        pass

    window.after(100, update_gui)


def progress_callback(
    percent,
    downloaded,
    total_size,
    speed,
    eta
):

    progress_queue.put(

        (
            percent,
            downloaded,
            total_size,
            speed,
            eta
        )

    )


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

            progress_callback

        )

        status_label.config(

            text="Download completed ✅"

        )

    except Exception as e:

        status_label.config(

            text=f"Error: {e}"

        )

    download_button.config(

        state="normal"

    )


def start_download():

    url = url_entry.get().strip()

    if not url:

        status_label.config(

            text="Please enter a URL"

        )

        return

    progress_bar["value"] = 0

    info_label.config(

        text="Downloaded : 0 MB / 0 MB\n"
             "Speed      : 0 MB/s\n"
             "Remaining  : --:--"
    )

    status_label.config(

        text="Downloading..."

    )

    download_button.config(

        state="disabled"

    )

    threading.Thread(

        target=download_thread,

        args=(url,),

        daemon=True

    ).start()


window = tk.Tk()

window.title("Mini Download Manager")

window.geometry("520x320")

window.resizable(False, False)


tk.Label(

    window,

    text="Download URL:"

).pack(

    pady=(15, 5)

)


url_entry = tk.Entry(

    window,

    width=70

)

url_entry.pack()


download_button = tk.Button(

    window,

    text="Start Download",

    command=start_download

)

download_button.pack(

    pady=15

)


progress_bar = ttk.Progressbar(

    window,

    orient="horizontal",

    mode="determinate",

    length=450,

    maximum=100

)

progress_bar.pack()


info_label = tk.Label(

    window,

    text=(
        "Downloaded : 0 MB / 0 MB\n"
        "Speed      : 0 MB/s\n"
        "Remaining  : --:--"
    ),

    justify="left",

    font=("Consolas", 10)

)

info_label.pack(

    pady=10

)


status_label = tk.Label(

    window,

    text=""

)

status_label.pack()


update_gui()

window.mainloop()
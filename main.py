import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog

from downloader import download_file


progress_queue = queue.Queue()

cancel_event = threading.Event()


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

            total_mb = total_size / (1024 * 1024)

            speed_mb = speed / (1024 * 1024)


            if eta > 0:

                minutes = int(eta // 60)

                seconds = int(eta % 60)

                eta_text = f"{minutes:02d}:{seconds:02d}"

            else:

                eta_text = "--:--"


            info_label.config(

                text=(
                    f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB\n"
                    f"Speed: {speed_mb:.2f} MB/s\n"
                    f"Remaining: {eta_text}"
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

            download_button.config(
                state="normal"
            )

            return


        cancel_event.clear()


        result = download_file(

            url,

            save_path,

            progress_callback,

            cancel_event

        )


        if result == "cancelled":

            status_label.config(
                text="Download cancelled ⛔"
            )

        else:

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


    cancel_button.config(

        state="disabled"

    )



def start_download():

    url = url_entry.get().strip()


    if not url:

        status_label.config(

            text="Enter URL"

        )

        return


    cancel_event.clear()


    download_button.config(

        state="disabled"

    )


    cancel_button.config(

        state="normal"

    )


    status_label.config(

        text="Downloading..."

    )


    threading.Thread(

        target=download_thread,

        args=(url,),

        daemon=True

    ).start()



def cancel_download():

    cancel_event.set()

    status_label.config(

        text="Cancelling..."

    )



window = tk.Tk()

window.title("Mini Download Manager")

window.geometry("520x360")

window.resizable(False, False)



tk.Label(

    window,

    text="Download URL:"

).pack(pady=10)



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

download_button.pack(pady=10)



cancel_button = tk.Button(

    window,

    text="Cancel Download",

    command=cancel_download,

    state="disabled"

)

cancel_button.pack()



progress_bar = ttk.Progressbar(

    window,

    length=450,

    maximum=100,

    mode="determinate"

)

progress_bar.pack(pady=15)



info_label = tk.Label(

    window,

    text=(
        "Downloaded: 0 MB / 0 MB\n"
        "Speed: 0 MB/s\n"
        "Remaining: --:--"
    ),

    font=("Consolas", 10)

)

info_label.pack()



status_label = tk.Label(

    window,

    text=""

)

status_label.pack(pady=10)



update_gui()


window.mainloop()
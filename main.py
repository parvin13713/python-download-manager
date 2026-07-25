import threading
import queue
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import json
import os

from downloader import download_file


progress_queue = queue.Queue()

cancel_event = threading.Event()
pause_event = threading.Event()

history_file = "downloads.json"



def load_history():

    if os.path.exists(history_file):

        with open(
            history_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    return []



def save_history(data):

    with open(
        history_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )



def add_history(url, path, status):

    history = load_history()

    history.append(
        {
            "url": url,
            "file": path,
            "status": status,
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    )

    save_history(history)



def show_history():

    history_window = tk.Toplevel(window)

    history_window.title(
        "Download History"
    )

    history_window.geometry(
        "600x300"
    )


    text = tk.Text(
        history_window,
        width=70,
        height=15
    )

    text.pack(
        padx=10,
        pady=10
    )


    history = load_history()


    if not history:

        text.insert(
            tk.END,
            "No downloads yet."
        )

    else:

        for item in history:

            text.insert(
                tk.END,
                f"File: {item['file']}\n"
                f"Status: {item['status']}\n"
                f"Date: {item['date']}\n"
                f"{'-'*40}\n"
            )



def update_gui():

    try:

        while True:

            data = progress_queue.get_nowait()

            (
                percent,
                downloaded,
                total_size,
                speed,
                eta

            ) = data


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

                text=
                f"Downloaded: {downloaded_mb:.2f} MB / {total_mb:.2f} MB\n"
                f"Speed: {speed_mb:.2f} MB/s\n"
                f"Remaining: {eta_text}"

            )


    except queue.Empty:

        pass


    window.after(
        100,
        update_gui
    )



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

        pause_event.clear()



        result = download_file(

            url,

            save_path,

            progress_callback,

            cancel_event,

            pause_event

        )



        if result == "cancelled":

            status_label.config(
                text="Download cancelled ⛔"
            )

            add_history(
                url,
                save_path,
                "Cancelled"
            )


        else:

            status_label.config(
                text="Download completed ✅"
            )

            add_history(
                url,
                save_path,
                "Completed"
            )



    except Exception as e:

        status_label.config(
            text=f"Error: {e}"
        )

        print(e)



    download_button.config(
        state="normal"
    )



def start_download():

    url = url_entry.get().strip()


    if not url:

        return



    download_button.config(
        state="disabled"
    )


    pause_button.config(
        state="normal"
    )


    cancel_button.config(
        state="normal"
    )


    resume_button.config(
        state="disabled"
    )


    status_label.config(
        text="Downloading..."
    )



    threading.Thread(

        target=download_thread,

        args=(url,),

        daemon=True

    ).start()



def pause_download():

    pause_event.set()


    pause_button.config(
        state="disabled"
    )


    resume_button.config(
        state="normal"
    )


    status_label.config(
        text="Paused ⏸️"
    )



def resume_download():

    pause_event.clear()


    pause_button.config(
        state="normal"
    )


    resume_button.config(
        state="disabled"
    )


    status_label.config(
        text="Downloading..."
    )



def cancel_download():

    cancel_event.set()


    pause_event.clear()


    status_label.config(
        text="Cancelling..."
    )



window = tk.Tk()

window.title(
    "Mini Download Manager"
)

window.geometry(
    "520x480"
)



tk.Label(
    window,
    text="Download URL:"
).pack(
    pady=10
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
    pady=10
)



pause_button = tk.Button(
    window,
    text="Pause ⏸️",
    command=pause_download,
    state="disabled"
)

pause_button.pack()



resume_button = tk.Button(
    window,
    text="Resume ▶️",
    command=resume_download,
    state="disabled"
)

resume_button.pack()



cancel_button = tk.Button(
    window,
    text="Cancel ⛔",
    command=cancel_download,
    state="disabled"
)

cancel_button.pack(
    pady=5
)



history_button = tk.Button(
    window,
    text="Download History",
    command=show_history
)

history_button.pack()



progress_bar = ttk.Progressbar(
    window,
    length=450,
    maximum=100
)

progress_bar.pack(
    pady=15
)



info_label = tk.Label(
    window,
    text=
    "Downloaded: 0 MB / 0 MB\n"
    "Speed: 0 MB/s\n"
    "Remaining: --:--"
)

info_label.pack()



status_label = tk.Label(
    window,
    text=""
)

status_label.pack(
    pady=10
)



update_gui()


window.mainloop()
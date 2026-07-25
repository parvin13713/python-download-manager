import requests
import time
import os


def download_file(
        url,
        save_path,
        progress_callback,
        cancel_event,
        pause_event
):

    downloaded = 0

    downloaded = 0


    headers = {}





    response = requests.get(
        url,
        headers=headers,
        stream=True,
        timeout=30
    )


    # اگر Resume پشتیبانی نشد، از اول شروع کن
    if downloaded > 0 and response.status_code == 200:

        downloaded = 0

        response.close()

        response = requests.get(
            url,
            stream=True,
            timeout=30
        )


    response.raise_for_status()


    total_size = int(
        response.headers.get(
            "content-length",
            0
        )
    )


    if downloaded > 0:
        total_size += downloaded


    start_time = time.time()


    mode = "ab" if downloaded > 0 else "wb"


    with open(save_path, mode) as file:

        for chunk in response.iter_content(
            chunk_size=64 * 1024
        ):

            # Pause
            while pause_event.is_set():

                if cancel_event.is_set():
                    return "cancelled"

                time.sleep(0.5)


            # Cancel
            if cancel_event.is_set():
                return "cancelled"


            if not chunk:
                continue


            file.write(chunk)

            downloaded += len(chunk)


            elapsed = time.time() - start_time


            speed = (
                downloaded / elapsed
                if elapsed > 0
                else 0
            )


            if total_size > 0:

                percent = (
                    downloaded /
                    total_size *
                    100
                )

                remaining = total_size - downloaded

                eta = (
                    remaining / speed
                    if speed > 0
                    else 0
                )

            else:

                percent = 0
                eta = 0



            progress_callback(
                percent,
                downloaded,
                total_size,
                speed,
                eta
            )


    return "completed"
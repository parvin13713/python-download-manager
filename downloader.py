import requests
import time


def download_file(url, save_path, progress_callback):

    response = requests.get(
        url,
        stream=True
    )

    total_size = int(
        response.headers.get("content-length", 0)
    )

    downloaded = 0
    start_time = time.time()

    with open(save_path, "wb") as file:

        for chunk in response.iter_content(chunk_size=1024 * 64):

            if chunk:

                file.write(chunk)

                downloaded += len(chunk)

                elapsed = time.time() - start_time

                speed = downloaded / elapsed if elapsed > 0 else 0

                if total_size:
                    percent = downloaded * 100 / total_size
                else:
                    percent = 0

                print(
                    "PROGRESS:",
                    downloaded,
                    "bytes",
                    "speed:",
                    speed
                )

                progress_callback(
                    percent,
                    downloaded,
                    total_size,
                    speed
                )

    return save_path
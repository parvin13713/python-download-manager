import requests
import time


def download_file(url, save_path, progress_callback):

    response = requests.get(
        url,
        stream=True,
        timeout=30
    )

    response.raise_for_status()

    total_size = int(
        response.headers.get("content-length", 0)
    )

    downloaded = 0
    start_time = time.time()

    with open(save_path, "wb") as file:

        for chunk in response.iter_content(chunk_size=64 * 1024):

            if not chunk:
                continue

            file.write(chunk)

            downloaded += len(chunk)

            elapsed = time.time() - start_time

            speed = downloaded / elapsed if elapsed > 0 else 0

            if total_size > 0:
                percent = downloaded / total_size * 100

                remaining = total_size - downloaded

                eta = remaining / speed if speed > 0 else 0

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

    return save_path
import requests


def download_file(url, save_path, progress_callback):

    response = requests.get(
        url,
        stream=True
    )

    total_size = int(
        response.headers.get("content-length", 0)
    )

    downloaded = 0

    with open(save_path, "wb") as file:

        for chunk in response.iter_content(chunk_size=1024 * 64):

            if chunk:

                file.write(chunk)

                downloaded += len(chunk)

                if total_size:
                    percent = downloaded * 100 / total_size
                    progress_callback(percent)

    return save_path
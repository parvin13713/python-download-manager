import requests
from urllib.parse import urlparse


def download_file(url, progress_callback):
    parsed_url = urlparse(url)

    filename = parsed_url.path.split("/")[-1]

    if not filename:
        filename = "downloaded_file"

    response = requests.get(url, stream=True)

    total_size = int(response.headers.get("content-length", 0))

    downloaded = 0

    with open(filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

                downloaded += len(chunk)

                if total_size:
                    percent = downloaded * 100 / total_size
                    progress_callback(percent)

    return filename
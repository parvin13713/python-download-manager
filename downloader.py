import requests


def download_file(url):
    filename = url.split("/")[-1]

    response = requests.get(url, stream=True)

    with open(filename, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

    return filename
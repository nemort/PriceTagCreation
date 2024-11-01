import requests


def download_file(file_link):
    # Отправляем запрос на скачивание файла
    response = requests.get(file_link)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Получаем имя файла из заголовков
        content_disposition = response.headers.get('Content-Disposition')

        if content_disposition:
            filename = content_disposition.split('filename=')[-1].strip('"')
        else:
            filename = 'downloaded_file.pdf'

        # Сохраняем файл
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return None


def upload_file_to_file_io(file_path):
    upload_url = 'https://file.io'

    with open(file_path, 'rb') as f:
        # Отправляем POST-запрос с файлом
        response = requests.post(upload_url, files={'file': f})

    if response.status_code == 200:
        data = response.json()
        # Проверяем, есть ли ссылка
        if 'link' in data:
            return data['link']
        else:
            return None
    else:
        return None

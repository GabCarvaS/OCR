#!/usr/bin/env python3
from flask import Flask, request, jsonify
import re
import requests
import shutil
import os

'''
Exemplos

link q recebe = 'https://drive.google.com/file/d/ID_DO_ARQUIVO/view'
link q monta = 'https://drive.google.com/u/0/uc?id=ID_DO_ARQUIVO&export=download'
'''

app = Flask(__name__)

def download_pdf_file(url: str, filename: str) -> str:
    """Download PDF from given URL to local directory.

    :param url: The URL of the PDF file to be downloaded
    :return: The name of the downloaded PDF file if successful, otherwise an empty string.
    """
    # Request URL and get response object
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        # Save in the current working directory
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, 'wb') as pdf_object:
            pdf_object.write(response.content)
            print(f'{filename} foi salvo!')
            return filename
    else:
        print(f'Não foi possível realizar o download do pdf: {url}')
        print(f'HTTP response status code: {response.status_code}')
        return ""

@app.route('/download-pdf', methods=['GET'])
def handle_download_pdf():
    url = request.args.get('url')

    if url:
        match = re.search(r"/d/([^/]+)/", url)
        if match:
            id = match.group(1)
            urlDownload = f'https://drive.google.com/u/0/uc?id={id}&export=download'
            file_path = f'{id}.pdf'
            filename = download_pdf_file(urlDownload, file_path)

            if filename:
                return jsonify({'link': urlDownload, 'msg' :f'PDF file "{filename}" was successfully downloaded and saved.'})
            else:
                return f'Não foi possível realizar o download do pdf: {urlDownload}'
    else:
        return 'Não foi possível processar.'

if __name__ == '__main__':
    app.run()
import requests

def download_excel_from_drive(file_id, destination):
    session = requests.Session()
    url = "https://drive.google.com/uc?export=download"
    response = session.get(url, params={'id': file_id}, stream=True)

    confirm_token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            confirm_token = value
            break

    if confirm_token:
        response = session.get(url, params={'id': file_id, 'confirm': confirm_token}, stream=True)

    response.raise_for_status()  # Raise an error for bad responses

    with open(destination, 'wb') as file:
        # Download the file in chunks to avoid using too much memory
        # chunk_size is in measured in bytes
        for chunk in response.iter_content(chunk_size=32 * 1024):
            if chunk :
                file.write(chunk)
    print(f"Downloaded Excel file to {destination}")

if __name__ == "__main__":
    # url = https://docs.google.com/spreadsheets/d/1gDmIuytuJN20gT75umywfNQ6TzjapWkK/edit?usp=sharing&ouid=118211237999630088242&rtpof=true&sd=true
    file_id = "1gDmIuytuJN20gT75umywfNQ6TzjapWkK"
    destination = "config_file.xlsx"

    download_excel_from_drive(file_id, destination)
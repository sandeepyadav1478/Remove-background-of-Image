# Requires "requests" to be installed (see python-requests.org)
import requests

api_key = "ZtKMPLtVtWx4K7VKvAkpokpnkjbi"
img_loc = "D:\py\Image Alteration\IMG_4384.JPG"
save_loc = "D:\py\Image Alteration\IMG_4384bg.PNG"

print("Sending request for server, please keep patience, it will take some time.")

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(img_loc, 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': api_key},
)
if response.status_code == requests.codes.ok:
    with open(save_loc, 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)
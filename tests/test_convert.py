import requests

# get the file from the get_url
get_url = "https://github.com/ProteoWizard/pwiz/raw/master/example_data/small.RAW"
# download the file to /app/small.RAW
response = requests.get(get_url)
with open("small.RAW", "wb") as file:
    file.write(response.content)
# if this doesn't work error the test


# URL of the FastAPI server
url = "http://127.0.0.1:8000/convert"

# File to be uploaded
files = {"files": open("small.RAW", "rb")}

# Send a POST request to the convert endpoint
response = requests.post(url, files=files)

# Print the response
print(response.json())

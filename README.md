# msconvert_api
A simple API (fastAPI) for running msconvert. 

The api uploads a file and then downloads the converted file in mzML format.

NB: Import note this is not a good method for large files. The file is uploaded to the server and then downloaded
and this process can be taxing and slow for both the server and your computer. 
This is mainly used for smaller files and in a local environment, where /data is mounted to the server

## Installation

The script can be run via a docker or directly via python.
For docker installation, see below.
```bash
docker build -t msconvert_api .
docker run -p 8000:8000 msconvert_api
```
For python installation, see below.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Usage
The script runs via the fastAPI framework and is very simple to use. Currently there are not any flag 
associated with the script. 
Future work will include the ability to specify centroiding, the output format and other options.

Via a curl command, the script can be run as follows:
```bash
curl -X POST -F "files=@file1.raw"  http://localhost:8000/convert
```

You can also see the swagger documentation at http://localhost:8000/docs

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

## License
MIT License

## Acknowledgements
The script here is just a wrapper for the already amazing proteowizard/msconvert tool. 
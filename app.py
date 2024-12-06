import os
import shutil
import subprocess
import zipfile
import urllib.parse
from typing import List

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def find_suffix_filenames(path_to_dir, suffix=".mzML", include_path=True):
    """
    :description: This function will find all the csv files in a directory
    :param path_to_dir: the path to the directory to search
    :param suffix: the file extension to search for
    :param include_path: whether to include the path in the filename
    :example: filenames = find_csv_filenames("my/directory")
            for name in filenames:
                print name
    :return: a list of all the csv files in the directory
    :source: https://stackoverflow.com/questions/9234560/find-all-csv-files-in-a-directory-using-python
    """
    filenames = os.listdir(path_to_dir)
    if include_path:
        res = [
            os.path.join(path_to_dir, filename)
            for filename in filenames
            if filename.endswith(suffix)
        ]
    else:
        res = [filename for filename in filenames if filename.endswith(suffix)]
    return res


@app.post("/convert")
async def convert_files(
    files: List[UploadFile] = File(...), centroid: bool = True, download: bool = True
):
    wine_path = shutil.which("wine")
    if not wine_path:
        return {"error": "Wine is not installed or not found in PATH"}

    msconvert_command = [wine_path, "msconvert"]
    if centroid:
        msconvert_command.extend(["--zlib", "--filter", "peakPicking true 1-"])

    for file in files:
        # Save the uploaded file to disk
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())

        # Check if the uploaded file is a zip file
        if zipfile.is_zipfile(file.filename):
            # Extract the contents of the zip file to a temporary directory
            with zipfile.ZipFile(file.filename, "r") as zip_ref:
                tmp_dir = "tmp"
                zip_ref.extractall(tmp_dir)

                file_list = find_suffix_filenames(
                    tmp_dir, suffix=".d", include_path=True
                )
                file_list.extend(
                    find_suffix_filenames(tmp_dir, suffix=".raw", include_path=True)
                )
                print(f"This is the file list {file_list}")

            # Run the msconvert command
            for file_ele in file_list:
                if file_ele.endswith(".d") or file_ele.endswith(".raw"):
                    process = subprocess.run(
                        msconvert_command + [file_ele], capture_output=True
                    )
                    print(f"Running -- {msconvert_command} + {[file_ele]}")

                    print(f"RETCODE: {process.returncode}")
                    print(f"STDOUT: {process.stdout.decode()}")
                    print(f"STDERR: {process.stderr.decode()}")

            # Remove the temporary directory even if its not empty
            shutil.rmtree(tmp_dir)
        else:
            print("No zip file detected.")
            # Run the msconvert command on the uploaded file
            process = subprocess.run(
                msconvert_command + [file.filename], capture_output=True
            )
            print(f"RETCODE: {process.returncode}")
            print(f"STDOUT: {process.stdout.decode()}")
            print(f"STDERR: {process.stderr.decode()}")

    mzml_files = find_suffix_filenames(".", suffix=".mzML", include_path=True)
    print(f"mzml files = {mzml_files}")

    if not mzml_files:
        return {"error": "No mzML files were generated"}

    if download:
        filename = urllib.parse.quote_from_bytes(mzml_files[0].encode("utf-8"))
        return FileResponse(
            path=mzml_files[0], filename=filename, media_type="application/xml"
        )
    else:
        return {"message": f"Files converted successfully {mzml_files}"}


# example to run
# curl -X POST -F "files=@file1.raw"  http://localhost:8000/convert

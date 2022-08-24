import os
import shutil
from threading import Timer
import uuid
import zipfile

from flask import Flask, render_template, redirect, request, send_file, url_for
from werkzeug.utils import secure_filename


def file_is_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() == "PDF"


app = Flask(__name__)
app.config.from_object("config")


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "pdfsingle" not in request.files and "pdfmult" not in request.files:
            return redirect(request.url)

        # We now ensured either pdfsingle or pdfmult is in request.files

        # Creating containing folders
        try: os.mkdir("sensitive-pdfs/")
        except: ...
        try: os.mkdir("anonymized-pdfs/")
        except: ...

        # Prioritizing the single file upload over the folder
        if request.files.getlist("pdfsingle")[0].filename:
            file = request.files["pdfsingle"]

            # Input error
            if file.filename is None:
                return redirect(request.url)

            if file_is_pdf(file.filename):
                original_filename = secure_filename(file.filename)

                filename = str(uuid.uuid4()) + ".pdf"
                file.save(os.path.join("sensitive-pdfs", filename))

                out = os.system(f"python script.py single sensitive-pdfs/{filename}")

                # Planning the file deletion in 5 min (= 300 s)
                Timer(300, os.remove, ("anonymized-pdfs/" + filename,)).start()

                # Deleting original
                os.remove("sensitive-pdfs/" + filename)

                if out != 0:
                    return redirect("error")                                                                   # Failure
                else:
                    return send_file("../anonymized-pdfs/" + filename, attachment_filename=original_filename)  # Success

            else:
                return redirect("error.html")  # Not a PDF

        # The user sent a folder of files
        else:
            filelist = request.files.getlist("pdfmult")

            # Naming folder
            folder = str(uuid.uuid4()) + '/'                                 # Out

            # Creating folders
            try: os.mkdir("sensitive-pdfs/" + folder)
            except Exception as e: print(e)
            try: os.mkdir("anonymized-pdfs/" + folder)
            except Exception as e: print(e)

            for file in filelist:
                breakpoint()
                # Input error
                if file.filename is None:
                    return redirect(request.url)

                if file_is_pdf(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join("sensitive-pdfs/" + folder, filename))

                    out = os.system(f"python script.py multiple sensitive-pdfs/{folder}")

                    if out != 0:
                        return redirect(url_for("error"))  # Failure case

            # Creating ZIP archive
            out_files = os.listdir("anonymized-pdfs/" + folder)
            with zipfile.ZipFile("anonymized-pdfs/" + folder + "out.zip", "w") as zipper:
                for file in out_files:
                    zipper.write("anonymized-pdfs/" + folder + file, compress_type=zipfile.ZIP_DEFLATED)

            # Planning the files deletion in 5 min (= 300 s)
            for dr in ("sensitive-pdfs/", "anonymized-pdfs/"):
                try:
                    Timer(300, shutil.rmtree, (dr + folder,)).start()
                except:
                    print("Error when trying to delete", dr)

            return send_file("../anonymized-pdfs/" + folder + "out.zip")

    return render_template("index.html")


@app.route("/upload/", methods=["GET", "POST"])
def upload():


    # breakpoint()
    return "", 204


@app.route("/error/")
def error():

    return render_template("error.html")

if __name__ == "__main__":
    app.run()

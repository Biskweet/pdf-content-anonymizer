import os
from flask import Flask, render_template, redirect, request

from werkzeug.utils import secure_filename

from .forms import FileForm


def file_is_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "pdf"


app = Flask(__name__)
app.config.from_object("config")


@app.route('/')
def index():
    form = FileForm()
    return render_template("index.html", form=form)


@app.route("/upload/", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if "pdf" not in request.files:
            return redirect(request.url)
        file = request.files["pdf"];
        if file.filename == '':
            print("\n========\n FILE HAS EMPTY FILENAME \n========\n")
            return redirect(request.url)

        if file and file_is_pdf(file.filename):
            print("\n======== FILE IS PDF ========\n")
            filename = secure_filename.filename(file.filename)
            file.save(os.path.join("sensitive-pdfs", filename))

    # breakpoint()
    return "", 204


if __name__ == "__main__":
    app.run()

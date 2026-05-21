from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import secure_filename
from extensions import csrf
import os

from services.disease_service import process_image

disease_bp = Blueprint("disease", __name__)

UPLOAD_FOLDER = "static/uploads"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@csrf.exempt
@disease_bp.route("/disease", methods=["GET", "POST"])
def disease_detection():

    error = None
    output_image = None
    disease_summary = {}

    if request.method == "POST":

        if "file" not in request.files:
            error = "No file uploaded"

        else:
            file = request.files["file"]

            if file.filename == "":
                error = "No selected file"

            elif file and allowed_file(file.filename):

                filename = secure_filename(file.filename)

                filepath = os.path.join(UPLOAD_FOLDER, filename)

                file.save(filepath)

                output_path, processing_error, disease_counts = process_image(filepath)

                if processing_error:
                    error = processing_error

                else:
                    output_image = url_for("static", filename=output_path)
                    disease_summary = disease_counts

    return render_template(
        "disease.html",
        error=error,
        output_image=output_image,
        disease_summary=disease_summary
    )
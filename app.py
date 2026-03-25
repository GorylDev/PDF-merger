from flask import Flask, request, render_template, send_file
import PyPDF2
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
MERGED_PDF = "merged.pdf"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def merge_pdfs(pdf_list, output_filename):
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_filename)
    merger.close()

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        files = request.files.getlist("pdf_files")
        pdf_paths = []
        for file in files:
            if file.filename.endswith(".pdf"):
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                pdf_paths.append(file_path)
        merge_pdfs(pdf_paths, MERGED_PDF)
        return send_file(MERGED_PDF, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf, extract_images_from_pdf, is_image_based_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def detect_certification_platform(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    if text and "coursera" in text.lower():
        return "coursera"
    return "saylor" if is_image_based_pdf(pdf_path) else None

def execute_script(platform, pdf_path):
    try:
        if platform == "coursera":
            import coursera
            return coursera.run_verification(pdf_path)
        elif platform == "saylor":
            import saylor
            return saylor.run_verification(pdf_path)
        else:
            return "❌ Platform not supported."
    except Exception as e:
        return f"❌ Error during verification: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    file = request.files.get('certificate')
    if not file or not file.filename.endswith('.pdf'):
        return "Please upload a valid PDF", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    platform = detect_certification_platform(filepath)
    if not platform:
        return "❌ Only Coursera and Saylor certificates are supported.", 400

    output = execute_script(platform, filepath)
    return render_template("result.html", platform=platform.capitalize(), output=output)

if __name__ == '__main__':
    app.run(debug=True)

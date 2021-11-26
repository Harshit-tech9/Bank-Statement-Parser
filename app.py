import os
from flask import Flask, flash, request, redirect, render_template,jsonify
from werkzeug.utils import secure_filename
import easyocr
import numpy as np
from pdf2image import convert_from_path

app=Flask(__name__, template_folder='templates')

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload1.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
       
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #upload_path = './' # local path
            upload_path = 'https://hdrive.herokuapp.com/drive/gcbucketobjects/1/bankstatement123/' # remote path
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(upload_path,filename))
            flash('File successfully uploaded')
            return redirect('/')
        else:
            flash('Allowed file types is pdf')
            return redirect(request.url)

'''@app.route('/echo', methods=['POST'])
def b_stmnt():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('./',filename))
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        images = convert_from_path(filename, 500, poppler_path = r"C:\Program Files\Poppler\poppler-0.68.0\bin")
        images[0] 

    
        reader = easyocr.Reader(['en']) 

        bounds = reader.readtext(np.array(images[0]), min_size=1, slope_ths=0.2, ycenter_ths=0.7, height_ths=0.8, width_ths=1, decoder='beamsearch', beamWidth=15) 

        text = ''
        for i in range(len(bounds)):
            text = text + bounds[i][1] +'\n'

        Bank_Name = bounds[1][1]

        if Bank_Name == "HDFC BANK":
            Account_No = bounds[31][1]
            Account_Holder = bounds[9][1] + ' ' + bounds[10][1]
            Account_Address = bounds[15][1] + ' ' + bounds[18][1] + ' ' + bounds[21][1] + ' ' + bounds[26][1] + ' ' + bounds[29][1]
            Account_Type = bounds[37][1]
            Ifsc_Code = bounds[38][1][16:]
            Branch_Name = bounds[3][1] 

            return jsonify({
                            "bank_name": Bank_Name , 
                            "account_number": Account_No , 
                            "account_holder": Account_Holder , 
                            "account_address": Account_Address , 
                            "account_type": Account_Type , 
                            "ifsc_code": Ifsc_Code , 
                            "branch_name": Branch_Name 
                            })
        return redirect('/')
'''

if __name__ == "__main__":
    app.run(debug=True)


''''# importing the required libraries
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
   if request.method == 'POST': 
      f = request.files['file'] 
      f.save(secure_filename(f.filename)) 
      return 'file uploaded successfully' 
		
if __name__ == '__main__':
   app.run() '''
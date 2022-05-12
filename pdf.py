from flask import Flask, request, render_template, jsonify
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from tabula import read_pdf
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'XT--00493Y'


class PhotoForm(FlaskForm):
    fileupload = FileField('Select PDF file:* ', validators=[FileRequired()])
    submit = SubmitField('Upload')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PhotoForm()
    if request.method == "POST":
        try:
            f = form.fileupload.data

            df = read_pdf(f, pages='all', output_format='json')
            table = []
            for data in df[0]['data']:
                row = []
                for r in data:
                    row.append(r['text'])
                table.append(row)
            # return jsonify(table)  
            
            return render_template('index.html', form=form, data=table)
        except (IndexError, subprocess.CalledProcessError):
            return render_template('index.html', form=form, error='Content must be tabular sheet')

    else:
        return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=9001)

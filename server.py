import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from src.response import Response

UPLOAD_FOLDER = f'{os.getcwd()}\\files'
"""Temporary file storage directory."""

ALLOWED_EXTENSIONS = {'mp3', 'ogg', 'wav',}
"""File extensions allowed for upload."""

# flask config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

def allowed_file(filename):
    """Checks the file extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def process_audio():
  """Processes audio file and returns a command."""
  # check if the post request has the audio part
  if 'audio' not in request.files:
    response = Response('Missing \'audio\' file key.')
    return response.to_dict(), 400
  
  file = request.files['audio']
  print(file.filename)
  
  if not file or file.filename == '':
    response = Response('No file uploaded.')
    return response.to_dict(), 400

  filename = secure_filename(file.filename)

  if allowed_file(file.filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    response = Response(f'Successfully uploaded {filename}')
    return response.to_dict(), 200
  else:
    response = Response(f'Disallowed file type: {filename}')
    return response.to_dict(), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

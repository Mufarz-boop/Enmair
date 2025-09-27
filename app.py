import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Folder simpan image & video
IMAGE_FOLDER = os.path.join(app.static_folder, "image")
VIDEO_FOLDER = os.path.join(app.static_folder, "video")
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    # ambil semua foto & video
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    videos = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(('.mp4', '.webm', '.avi'))]
    return render_template('gallery.html', images=images, videos=videos, total=len(images))

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('gallery'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('gallery'))

    # cek extension
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext in ['png', 'jpg', 'jpeg', 'gif']:
        save_path = os.path.join(IMAGE_FOLDER, file.filename)
    elif ext in ['mp4', 'webm', 'avi']:
        save_path = os.path.join(VIDEO_FOLDER, file.filename)
    else:
        return "Format file tidak didukung", 400

    file.save(save_path)
    return redirect(url_for('gallery'))

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)
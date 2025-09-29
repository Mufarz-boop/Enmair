import os
from flask import render_template, flash
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey"

# 🔹 Folder untuk simpan image & video
IMAGE_FOLDER = os.path.join(app.static_folder, "image")
VIDEO_FOLDER = os.path.join(app.static_folder, "video")
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

PROFILE_FILENAME = 'profile.jpg'  # nama file profil tetap


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# 🔹 Dummy blog - Penyesuaian Post
posts = [
    {
        "title": "Enmair - Website Dinamis dengan Flask",
        "date": "29 September 2025",
        "preview": "Sebuah proyek website interaktif menggunakan Flask dan Bootstrap.",
        "full": (
            "Enmair adalah proyek website dinamis yang dibangun menggunakan Flask, "
            "mengintegrasikan template rendering, routing, dan framework CSS seperti Bootstrap. "
            "Website ini menampilkan halaman Home, About, dan fitur login sederhana, "
            "serta menggunakan desain modern dengan efek kaca dan animasi halus. "
            "Sangat cocok sebagai referensi belajar full-stack web development."
        ),
        "category": "Full-Stack Web",
        "link": "https://github.com/Mufarz-boop/Enmair.git",
    },
]

# 🔹 Dummy libraries
libraries_data = [
    {
        "title": "Pakai Otakmu",
        "description": "Library untuk membuat antarmuka pengguna interaktif dengan desain minimalis.",
        "type": "image",
        "file": "Erudition 11.jpg",
        "link": "https://www.youtube.com/watch?v=KwI_ePEniGQ"
    },
]

# 🔹 Routes utama
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        file = request.files.get('profile')
        if file and allowed_file(file.filename):
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], PROFILE_FILENAME)
            # Hapus file lama jika ada
            if os.path.exists(save_path):
                os.remove(save_path)
            # Simpan file baru
            file.save(save_path)
            flash("Foto profil berhasil diperbarui!", "success")
            return redirect(url_for('about'))

    # Profile image selalu nama file tetap
    profile_image = PROFILE_FILENAME
    return render_template('about.html', profile_image=profile_image)


# 🔹 Gallery & Upload
@app.route('/gallery')
def gallery():
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    videos = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(('.mp4', '.webm', '.avi'))]
    return render_template('gallery.html', images=images, videos=videos, total=len(images))


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash("Tidak ada file yang dipilih!", "warning")
        return redirect(url_for('gallery'))

    file = request.files['file']
    if file.filename == '':
        flash("Nama file kosong!", "warning")
        return redirect(url_for('gallery'))

    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext in ['png', 'jpg', 'jpeg', 'gif']:
        save_path = os.path.join(IMAGE_FOLDER, file.filename)
    elif ext in ['mp4', 'webm', 'avi']:
        save_path = os.path.join(VIDEO_FOLDER, file.filename)
    else:
        flash("Format file tidak didukung!", "danger")
        return redirect(url_for('gallery'))

    file.save(save_path)
    flash(f"{file.filename} berhasil diupload!", "success")
    return redirect(url_for('gallery'))


@app.route('/blog_story')
@app.route('/blog_story/<category>')
def blog_story(category=None):
    categories = sorted(set(p['category'] for p in posts))

    if category:
        filtered_posts = [p for p in posts if p['category'].lower() == category.lower()]
        if not filtered_posts:
            flash(f"Tidak ada post untuk kategori '{category}'", "info")
            filtered_posts = posts  # fallback menampilkan semua post
        return render_template('blog_story.html', posts=filtered_posts, categories=categories, active_category=category)
    
    return render_template('blog_story.html', posts=posts, categories=categories, active_category=None)


# 🔹 Library page
@app.route('/library')
def library():
    return render_template('library.html', libraries=libraries_data)


if __name__ == '__main__':
    app.run(debug=True)
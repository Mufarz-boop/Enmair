import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# 🔹 Folder untuk simpan image & video
IMAGE_FOLDER = os.path.join(app.static_folder, "image")
VIDEO_FOLDER = os.path.join(app.static_folder, "video")
os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# 🔹 Dummy data blog (gunakan nama file saja, bukan url_for)
posts = [
    {
        "title": "Belajar Flask dari Nol",
        "date": "27 September 2025",
        "preview": "Flask itu microframework Python yang ringan...",
        "full": "Flask adalah framework Python yang memudahkan pembuatan website dinamis. Dengan Flask, kita bisa membuat routing, template, form handling, dan API endpoint dengan mudah. Cocok untuk belajar konsep web development dan prototyping cepat.",
        "category": "Coding",
        "image_file": "Erudition 14.jpg"
    },
    {
        "title": "Tips Styling dengan CSS Modern",
        "date": "20 September 2025",
        "preview": "CSS modern sekarang punya banyak fitur keren...",
        "full": "Dengan CSS modern, kita bisa membuat layout lebih fleksibel menggunakan flexbox, grid, dan custom properties. Animasi dan transisi pun lebih smooth. Hal ini bikin desain lebih rapi, responsif, dan mudah di-maintain.",
        "category": "CSS",
        "image_file": "Erudition 13.jpg"
    },
    {
        "title": "Mengapa GitHub Penting?",
        "date": "15 September 2025",
        "preview": "GitHub bukan cuma tempat taruh kode...",
        "full": "GitHub menyediakan repository online untuk kode, memudahkan kolaborasi tim, version control, dan dokumentasi. Recruiter juga sering mengecek GitHub kandidat untuk melihat kualitas kode dan project yang pernah dibuat.",
        "category": "GitHub",
        "image_file": "Erudition 12.jpg"
    },
    {
        "title": "Perjalanan Saya di Dunia Web",
        "date": "10 September 2025",
        "preview": "Dari Hello World sampai jatuh cinta dengan web dev...",
        "full": "Aku mulai coding karena penasaran, mencoba HTML, CSS, Bootstrap, hingga Flask. Sekarang aku makin percaya diri membuat website sendiri.",
        "category": "Personal",
        "image_file": "Erudition 11.jpg"
    }
]

# 🔹 Routes utama
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# 🔹 Gallery (images & videos)
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

# 🔹 Blog storytelling
@app.route('/blog_story')
def blog_story():
    return render_template('blog_story.html', posts=posts)

@app.route('/blog/category/<category>')
def blog_category(category):
    filtered_posts = [p for p in posts if p['category'].lower() == category.lower()]
    return render_template('blog_story.html', posts=filtered_posts)

# 🔹 Projects page
@app.route('/projects')
def projects():
    return render_template('projects.html')

if __name__ == '__main__':
    app.run(debug=True)
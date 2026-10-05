# Portofolio Pribadi: Ervhino Aryo Seto

| | |
|---|---|
| **Nama** | Ervhino Aryo Seto |
| **NPM** | 2506551125 |
| **Kelas** | PBP F |
| **Deploy (PWS)** | https://ervhino-aryo-myportofolio.pws.cs.ui.ac.id/ |

Project website portofolio pribadi berbasis Django pada mata kuliah Pemrograman Berbasis Platform (CSGE602022), Fasilkom UI, semester Gasal 2026/2027.

---

## Daftar Isi
1. [Fitur](#fitur)
2. [Peran dan Hak Akses](#peran-dan-hak-akses)
3. [Menjalankan Proyek](#menjalankan-proyek)
4. [Progres Mingguan](#progres-mingguan)
5. [Pertanyaan Reflektif](#pertanyaan-reflektif)
6. [AI Disclosure](#ai-disclosure)

---

## Fitur

- **Profil**: foto, NPM, program studi, dan bio. Halaman utama juga menampilkan waktu login terakhir yang dibaca dari cookie `last_login`.
- **Education**: tiga kartu riwayat pendidikan lengkap dengan logo institusi dan ringkasan yang bisa dibuka-tutup. Layout memakai CSS Grid `auto-fit` agar menyesuaikan ukuran layar.
- **Experience**: data disimpan di database (judul, deskripsi, kategori, thumbnail, dan status berlangsung/selesai).
- **Projects**: data disimpan di database (tahun, kategori, teknologi, URL proyek, gambar, dan penanda *featured* yang tampil sebagai badge), diurutkan berdasarkan featured dan tahun.
- **Form dan Data Delivery**: tambah dan ubah data lewat `ModelForm` (satu template untuk dua aksi), hapus dengan konfirmasi, dan penyajian data sebagai JSON (`/api/experiences/`, `/api/projects/`).
- **Autentikasi dan session**: registrasi, login, dan logout memakai sistem bawaan Django. Cookie `last_login` dibuat saat login dan dihapus saat logout.
- **Otorisasi**: empat peran dengan pengecekan di dalam view. Aksi yang tidak diizinkan dibalas HTTP 403.
- **Star**: user yang login bisa memberi atau membatalkan star pada Experience dan Projects (satu star per user lewat relasi `ManyToManyField` ke `User`).
- **Interaktivitas AJAX** (Experience dan Projects): data dimuat lewat `fetch()`, ada state loading/kosong/error dengan tombol "Coba lagi", pencarian dengan debouncing, modal tambah data, notifikasi toast, dan proteksi XSS.
- **Keamanan**: token CSRF di semua POST, `escapeHtml` di setiap nilai yang disisipkan lewat JavaScript, `strip_tags` pada `clean_<field>` di `ModelForm`, dan `SECRET_KEY` dibaca dari environment variable.
- **Pengujian**: unit test untuk halaman, endpoint JSON, hak akses tiap peran, status 201/400/403, perlindungan XSS, dan toggle star.

## Peran dan Hak Akses

| Peran | Lihat | Star | Tambah | Edit | Hapus |
|---|:---:|:---:|:---:|:---:|:---:|
| Pengunjung (belum login) | ✅ | ❌ | ❌ | ❌ | ❌ |
| User terdaftar | ✅ | ✅ | ❌ | ❌ | ❌ |
| Editor (grup `Editor`) | ✅ | ✅ | ❌ | ✅ | ❌ |
| Pemilik / superuser | ✅ | ✅ | ✅ | ✅ | ✅ |

Tombol yang tidak boleh dipakai disembunyikan di template, tetapi pembatasan yang sebenarnya dilakukan di dalam view, sehingga permintaan langsung ke URL tetap ditolak.

## Menjalankan Proyek

```bash
# 1. Clone repositori
git clone https://github.com/ervhinoaryoseto-del/myportofolio.git
cd myportofolio

# 2. Buat dan aktifkan virtual environment
python -m venv env
env\Scripts\activate            # macOS/Linux: source env/bin/activate

# 3. Pasang dependensi
pip install -r requirements.txt

# 4. Siapkan environment variable lalu isi SECRET_KEY
copy .env.example .env          # macOS/Linux: cp .env.example .env

# 5. Terapkan migrasi dan buat akun pemilik (superuser)
python manage.py migrate
python manage.py createsuperuser

# 6. Jalankan server development
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` di browser.

**Menyiapkan peran Editor:** masuk ke `/admin/`, buka *Groups* lalu *Add group*, buat grup bernama persis `Editor` (tanpa permission tambahan karena pengecekan dilakukan di view), kemudian masukkan akun yang dipilih ke grup tersebut lewat menu *Users*.

**Menjalankan test:**

```bash
python manage.py test
```

**Catatan konfigurasi:**
- Secara bawaan proyek memakai SQLite. Jika `PRODUCTION=True`, proyek memakai PostgreSQL dari variabel `DB_*`, dan `SECRET_KEY` wajib diisi.
- Skrip Selenium opsional ada di `scripts/e2e_check.py` (butuh `pip install -r requirements-dev.txt`), dan tidak ikut terbaca saat `manage.py test`.

## Progres Mingguan

| Minggu | Yang dikerjakan |
|---|---|
| **Tutorial 1** | Membuat proyek Django awal dan halaman profil statis dengan HTML5 dan CSS3, lalu deploy ke PWS. |
| **Tugas 1** | Menambah section Education berisi tiga kartu dengan logo institusi dan ringkasan yang bisa dibuka-tutup, memakai CSS Grid dan layout responsif. |
| **Tutorial 2** | Membuat aplikasi `main`, model `Experience` beserta migrasinya, halaman `/` dan `/experience/` yang membaca data dari context dan database, navigasi memakai `{% url %}`, serta unit test. |
| **Tugas 2** | Membuat model `Project` yang lebih kaya (tahun, kategori, teknologi, featured, ordering), halaman `/projects/` dengan badge featured, daftar teknologi, dan tampilan data kosong, serta unit test tambahan. |
| **Tutorial 3** | Membuat kerangka `base.html`, `ProjectForm`, endpoint `/api/projects/`, dan penghapusan proyek lewat modal konfirmasi. |
| **Tugas 3** | Menerapkan CRUD pada Experience dengan satu template untuk tambah dan ubah, endpoint JSON Experience, dan daftar yang diambil dari JSON hasil deserialisasi. |
| **Tutorial 4** | Menambahkan registrasi, login, logout, cookie `last_login`, status login di navbar, pembatasan aksi pada Projects, dan star lewat `starred_by`. |
| **Tugas 4** | Menerapkan otorisasi pada Experience: star, peran Editor lewat Django Group dengan helper `is_editor_user()`, pembatasan di view (HTTP 403), dan tombol aksi yang disesuaikan dengan peran. |
| **Tutorial 5** | Mengubah halaman Projects menjadi AJAX: endpoint JSON dengan info star, pencarian dengan debouncing, modal tambah proyek dengan Fetch API, toast, dan perlindungan XSS. |
| **Tugas 5** | Menerapkan seluruh pola Tutorial 5 pada Experience: halaman hanya kerangka dan data dimuat lewat `fetch()`, JSON dirakit manual dengan info star, state loading/kosong/error, pencarian dengan debounce 300 ms, modal tambah data, view `create_experience_ajax` (201/400/403), toast, `escapeHtml`, dan `strip_tags`. Helper `escapeHtml` dan `getCookie` dipindah ke `static/js/utils.js`, lalu test suite disusun ulang. |

**Perbaikan setelah review (Tugas 5):** format `ended_at` pada form edit diperbaiki agar sesuai dengan `datetime-local`, badge featured dikembalikan pada render AJAX Projects, `SECRET_KEY` dan `DEBUG` dipindah ke environment variable, serta test yang gagal diperbarui.

---

## Pertanyaan Reflektif

### Tugas 1

1. Penggunaan elemen semantik HTML5

Ya, saya memakai elemen semantik seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Bagian Profile dan Education saya buat dengan `<section>`, sedangkan tiap ringkasan pendidikan memakai `<article>`. Elemen semantik membantu mengelompokkan konten berdasarkan fungsinya, membuat struktur HTML lebih terorganisir dan mudah dipahami, serta mengurangi ketergantungan pada `<div>`. Hal ini juga memudahkan saya mengatur CSS karena tiap bagian halaman punya struktur yang jelas.

2. Tantangan membuat halaman responsif

Tantangan utamanya adalah menjaga susunan konten tetap nyaman dibaca dan tidak berdempetan saat layar mengecil. Di desktop saya memakai CSS Grid untuk menempatkan identitas, foto, dan informasi profil, lalu di mobile susunannya saya ubah menjadi satu kolom dengan `@media`. Prioritas informasi saya atur agar nama dan identitas muncul lebih dulu, disusul foto dan informasi tambahan. Pada bagian Education saya memakai `auto-fit` dan `minmax()` supaya jumlah kolom menyesuaikan lebar layar, dan ukuran logo di mobile saya kecilkan agar kartu tetap proporsional.

3. Keterbatasan web statis dan rencana pengembangan

Pada web statis, semua informasi harus ditulis dan diperbarui manual di HTML. Ini merepotkan ketika jumlah data bertambah, misalnya saat ingin menambah pengalaman, proyek, atau pencapaian baru. Untuk iterasi berikutnya saya ingin data portofolio (pendidikan, pengalaman, proyek) dikelola lewat database agar bisa diubah tanpa menyentuh struktur HTML. Saya juga ingin menampilkan daftar proyek secara dinamis per kategori dan menambahkan dark mode agar pengunjung bisa memilih tema yang sesuai preferensinya.

### Tugas 2

1. Alur ketika pengguna membuka halaman portofolio baru, mulai dari permintaan hingga data tampil di browser. Jelaskan peran `urls.py` proyek, `urls.py` aplikasi, view, model, dan template.

Request pertama kali diterima Django dan masuk ke `urls.py` proyek. Dari sana Django mencari pola URL yang cocok dan meneruskannya ke `urls.py` aplikasi `main`. Setelah cocok, request diteruskan ke view yang sesuai (konsep MVT). Di dalam view, data diambil dari model, misalnya `Project.objects.all()`, lalu dimasukkan ke context dan dikirim ke template. Template memakai Django Template Language untuk melakukan perulangan dan menampilkan nama proyek, deskripsi, tahun, dan teknologi. Hasil HTML-nya dikirim ke browser sehingga pengguna melihat halaman yang berisi data dari database.
*2. Mengapa data bagian portofolio baru sebaiknya disimpan pada model, bukan ditulis langsung di template? Jelaskan dampaknya terhadap pemeliharaan dan pengembangan.

Menyimpan data di model memisahkan data dari tampilan (MVT). Jika data di-hardcode di template, setiap menambah, mengubah, atau menghapus proyek saya harus mengedit HTML, dan ini makin merepotkan ketika datanya banyak. Dengan model, data dikelola lewat database (misalnya lewat `/admin/`) dan template hanya bertugas menampilkannya. Aplikasi jadi lebih mudah dipelihara dan dikembangkan karena perubahan data tidak bergantung pada kode tampilan.

3. Apa perbedaan `makemigrations` dan `migrate`? Berikan contoh perubahan model yang mengharuskan keduanya.

`makemigrations` membuat berkas migrasi berdasarkan perubahan pada model, yaitu catatan perubahan struktur yang akan diterapkan ke database. `migrate` menerapkan migrasi tersebut ke database. Contohnya, jika model `Project` saya tambahi field `project_url`, saya menjalankan `python manage.py makemigrations` untuk mencatat penambahan field itu, lalu `python manage.py migrate` agar perubahannya benar-benar diterapkan ke database.

### Tugas 3

1. ModelForm dan `{% csrf_token %}`

ModelForm terhubung langsung dengan model Django, sehingga saya tidak perlu membuat input dan validasi dari nol. ModelForm juga memastikan data yang dimasukkan sesuai dengan field dan aturan di model. Adapun `{% csrf_token %}` melindungi form dari serangan Cross-Site Request Forgery: token memastikan request POST benar-benar berasal dari form di aplikasi kita, bukan dari request berbahaya yang dibuat pihak lain.

2. JSON dibanding XML

JSON lebih sederhana, ringkas, dan mudah dibaca. Strukturnya berupa pasangan key-value dan array yang sesuai dengan struktur data JavaScript, sehingga mudah diproses aplikasi. JSON juga banyak dipakai untuk komunikasi frontend dan backend, terutama pada pengembangan API.

3. Alur view yang mengembalikan JSON dan alasan perlunya serialization

Request masuk ke view, lalu view mengambil data `Project` dari database lewat Django ORM. Hasilnya berupa object atau QuerySet Django yang belum bisa langsung dikirim sebagai JSON. Karena itu dilakukan serialization (misalnya `serializers.serialize("json", projects)`) untuk mengubahnya menjadi format JSON, lalu dikembalikan ke client lewat `HttpResponse` dengan `content_type="application/json"`.

### Tugas 5

1. Jelaskan apa itu *debouncing* dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

Debouncing adalah teknik untuk menunda eksekusi suatu fungsi sampai pengguna berhenti melakukan input selama waktu tertentu. Pada fitur pencarian AJAX, debouncing penting agar request ke server tidak dikirim setiap kali pengguna mengetik satu karakter. Dengan begitu, jumlah request dapat dikurangi sehingga server lebih ringan dan pencarian menjadi lebih efisien.

2. Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?

await digunakan untuk menunggu proses asynchronous dari fetch() selesai sebelum kode berikutnya dijalankan. Dengan await, hasil dari fetch() dapat langsung disimpan dan diproses, misalnya untuk mengambil response JSON dari server. Jika tidak menggunakan await, fetch() akan langsung mengembalikan Promise, sehingga kode berikutnya dapat berjalan sebelum response dari server tersedia dan data belum bisa langsung diproses sebagai hasil request.

3. Jelaskan apa itu serangan XSS (*Cross-Site Scripting*) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui *template* Django!

XSS (Cross-Site Scripting) adalah serangan dengan memasukkan script atau HTML berbahaya ke dalam data yang kemudian ditampilkan pada halaman web. Data yang ditampilkan melalui AJAX/JavaScript lebih rentan jika kita langsung memasukkannya ke HTML, misalnya menggunakan innerHTML, karena browser dapat menganggap isi data sebagai HTML atau script. Karena itu, data yang berasal dari server perlu di-escape terlebih dahulu sebelum dimasukkan ke halaman, sehingga karakter khusus seperti < dan > tidak dianggap sebagai kode HTML yang dapat dijalankan.

---

## AI Disclosure

### Tugas 1
Saya memakai Google Gemini (Gemini Pro 3.1) sebagai alat bantu belajar. Saya menjelaskan ide tugas dan potongan kode yang sedang saya kerjakan agar lebih paham, lalu memakai Gemini Pro untuk mempelajari struktur HTML dan styling CSS. Gemini juga membantu saya memperbaiki bug duplikasi dari pekerjaan di lab, serta mempelajari CSS untuk layout grid dan indikator interaktif.

Kode `index.html` saya kerjakan sendiri. Untuk section Education saya melihat referensi sintaks di w3schools, menentukan konsep dan section yang ingin ditambahkan, memilih dan memasukkan data, menyesuaikan tampilan dengan kebutuhan desain, dan memeriksa hasilnya langsung di browser.

### Tugas 2
Saya memakai Gen-AI Gemini (Gemini Pro 3.1) untuk memahami pembuatan superuser Django beserta langkah-langkahnya di terminal, serta untuk memahami beberapa konsep dan mengecek implementasi saya. Seluruh proses dan kode tetap saya sesuaikan dan kerjakan sendiri berdasarkan kebutuhan tugas.

### Tugas 3
Saya memakai ChatGPT (GPT-5.6 Luna) untuk membantu memahami konsep ModelForm, CSRF token, dan serialization di Django, termasuk contoh implementasi yang relevan dengan tugas. Seluruh kode dan implementasi saya kerjakan sendiri berdasarkan pemahaman dari Tutorial 3.

Saya juga berkonsultasi soal action pada form tambah dan ubah. Awalnya saya membuat dua template berbeda, tetapi setelah berdiskusi saya memutuskan memakai satu template untuk kedua aksi. Keputusan ini membantu saya memahami prinsip DRY (*Don't Repeat Yourself*).

### Tugas 4
Saya memakai Gemini (Gemini Pro 3.1) untuk mengulas materi Tutorial 4, terutama autentikasi, session, dan implementasi cookie. Karena jarak pengerjaan tutorial dan tugas cukup dekat, implementasi konsep dan kode saya kerjakan sendiri. AI juga saya manfaatkan untuk memastikan endpoint JSON dari Tugas 3 tetap berfungsi tanpa membocorkan informasi sensitif.

### Tugas 5
**Tools:** Chatgpt (GPT-5.6 Luna) lewat chatgpt.com 
Log chat (Pengerjaan Tugas 5): https://chatgpt.com/share/6ac3c86e-25d0-83ec-b712-f7773911814b 
Log chat (Improve dari feedback penilaian): https://chatgpt.com/share/6ac3c880-f63c-83ec-be17-936650df9a13

**Strategi prompting:** saya copy paste teks Tutorial 05 beserta memberikan instruksi tugas, lalu meminta langkah prosedeur implementasi yang disesuaikan dengan model dan kode saya (`Experience`, grup `Editor`, `starred_by`). Lalu, saat terjadi error saya mengunggah file proyek agar menyesuaikan memakai nama field yang benar, lalu menulis, menjalankan, dan menguji hasilnya sendiri di browser dengan akun untuk tiap implementasi.

**Bagian yang dibantu AI:**
- Halaman AJAX (state loading/kosong/error, pencarian dengan debounce, modal, toast, dan `escapeHtml`)
- Review keseluruhan proyek, penyusunan ulang test, dan adjustment draf README ini
- Kerangka endpoint JSON manual dengan info star dan view create_experience_ajax
- Prosedeur untuk memperbaiki bug dan penyelesaian feedback dari penilaiaan sebelumnya.

**Keterbatasan AI dan perbaikan manual:**
- AI menghasilkan output code dengan aturan peran yang keliru (Editor boleh menambah data). Namun, saya mengembalikan kejalan yang benar: Editor hanya boleh mengedit, sedangkan menambah dan menghapus khusus superuser(admin).
- AI menyatakan field `starred_by` tidak butuh migrasi, padahal tabel penghubungnya belum ada di database saya sehingga muncul `no such table: main_experience_starred_by`. Saat `migrate`, ternyata ada tabel sisa dari percobaan migrasi sebelumnya yang bentrok dengan migrasi `0004`. Saya memperbaikinya lewat Django shell setelah mem-backup data star terlebih dulu supaya data star tidak hilang.
- Saat saya merapikan template Projects mengikuti saran AI, container `#grid` ikut terhapus sehingga daftar proyek tidak tampil. Saya mengembalikannya.
- Review kode menemukan bahwa test suite banyak yang gagal dan ada bug pada form edit (`ended_at` terkosongkan karena format `datetime-local`), lalu keduanya saya perbaiki dan uji ulang.
- AI sering mengusulkan lebih dari yang diminta sehingga hasilnya perlu saya sorting agar sesuai dengan cakupan tugas.

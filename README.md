Nama : Ervhino Aryo Seto

NPM : 2506551125

Kelas : PBP F

### Tugas 1
1. Iya, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>` dalam merancang struktur tugas website portofolio. Seperti, pada bagian Profile dan Education saya buat menggunakan `<section>`, sedangkan setiap summary pendidikan menggunakan `<article>`. Penggunaan elemen semantik membantu saya mengelompokkan konten berdasarkan fungsi dan membuat struktur HTML lebih terorganisir serta mudah dipahami. Selain itu, penggunaan elemen seperti `<header>` dan `<footer>` membuat struktur halaman menjadi lebih jelas tanpa perlu ketergantungan pada `<div>` untuk seluruh bagian website. Hal ini juga memudahkan saya ketika mengatur CSS karena setiap bagian halaman memiliki struktur yang jelas.

2. Tantangan utama ketika membuat website responsive adalah memastikan susunan konten tetap enak dibaca dan tidak terlalu berdempetan ketika ukuran layar mengecil. Pada tampilan desktop, saya menggunakan CSS Grid untuk menempatkan identitas, foto, dan informasi profil dalam beberapa bagian, sedangkan pada mobile saya mengubah susunannya menjadi satu kolom menggunakan @media. Saya mengatur elemen berdasarkan prioritas informasi dan kebutuhan space. Informasi utama seperti nama dan identitas paling diprioritaskan, kemudian foto dan informasi tambahan ditempatkan setelahnya. Pada bagian Education, saya menggunakan auto-fit dan minmax() agar jumlah kolom dapat menyesuaikan ukuran layar. Saya juga mengubah ukuran logo pendidikan pada mobile agar kartu tetap proporsional dan tidak terlalu memenuhi layar.

3. Karena website yang dibuat masih berupa static web, informasi pada portofolio masih harus ditulis dan diperbarui secara manual di dalam kode HTML. Hal ini menjadi keterbatasan ketika jumlah informasi semakin banyak, misalnya ketika saya ingin menambahkan pengalaman, proyek, atau pencapaian baru karena setiap perubahan harus dilakukan langsung pada source code. Pada iterasi proyek berikutnya, saya ingin menambahkan fungsionalitas dinamis yang memungkinkan data portofolio seperti pendidikan, pengalaman, dan proyek dikelola melalui database sehingga informasi dapat ditambahkan atau diperbarui tanpa harus mengubah struktur HTML secara manual. Saya juga tertarik menambahkan halaman atau fitur yang memungkinkan pengunjung berinteraksi lebih lanjut dengan portofolio, seperti menampilkan daftar proyek secara dinamis berdasarkan kategori. Selain itu saya juga ingin menambahkan fitur dark mode agar pengunjung dapat memilih tema yang sesuai dengan preferensi mereka. Dengan adanya fitur-fitur ini, portofolio saya akan menjadi lebih interaktif dan mudah dikelola.

## AI Disclosure
Dalam pengerjaan Tugas 1 ini, saya menggunakan bantuan dari Google Gemini sebagai alat bantu selama proses pengembangan.
Saya menjelaskan ide saya untuk mengerjakan tugas 1 dan beberapa bagian kode yang sedang saya kerjakan, untuk memahami lebih mendalam. Kemudian menggunakan Gemini Pro untuk membantu saya belajar struktur dalam menyusun HTML dan styling CSS. Pada waktu mengerjakannya saya juga dibantu untuk memperbaiki bug duplikasi dari hasil pengerjaan saya di lab saat masih tersisa waktu karena sudah menyelesaikan Tutorial 01, dan membantu saya belajar menyusun CSS untuk layout grid, serta indikator interaktif.

Saya mengerjakan kode index.html dengan sendiri, dimana pada section education dengan melihat referensi syntax dari w3schools, menentukan konsep dan section yang ingin ditambahkan, memilih serta memasukkan data, menyesuaikan tampilan sesuai kebutuhan desain, dan melakukan pengecekan hasilnya secara langsung di browser.

### Tugas 2
1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.9
= Saat user membuka halaman portofolio baru, request pertama kali diterima oleh Django dan masuk ke urls.py yang ada di project. Dari sana, Django akan mencari URL yang sesuai dan meneruskannya ke urls.py pada aplikasi main. Setelah URL nya cocok, request diteruskan ke view yang sesuai (konsep MVT).

Lalu di dalam view, aplikasi mengambil data yang dibutuhkan dari model, misalnya data project menggunakan Project.objects.all(). Data tersebut kemudian dimasukkan ke context dan dikirim ke template. Selanjutnya, dari template  yang akan menggunakan Django Template Language untuk melakukan loop terhadap data tersebut dan show informasi kaya nama project, deskripsi, tahun, dan tech stack. Setelah proses selesai, Django mengirimkan hasil HTML ke browser sehingga pengguna dapat melihat halaman portofolio yang sudah berisi data dari database.

2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.
= Menurut saya, menyimpan data pada model lebih baik karena data dan tampilan menjadi terpisah (MVT). Kalau data project ditulis langsung(Hard code) di dalam template, maka akan membuat kita ribet. Karena setiap kali ingin menambah, mengubah, atau menghapus project kita harus mengubah kode HTML-nya juga. Nah, hal ini akan cukup merepotkan kalau jumlah data semakin banyak.

Dengan menggunakan model, data bisa dikelola melalui database dan template hanya bertugas menampilkan data tersebut. Jadi, kalau saya ingin menambahkan project baru, saya cukup menambahkan datanya pake /admin tanpa perlu mengubah struktur halaman. Cara ini juga membuat aplikasi lebih mudah dipelihara dan dikembangkan karena perubahan pada data tidak terlalu bergantung pada kode tampilan.

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.
= makemigrations digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model. Jadi, Django akan mencatat perubahan struktur model yang nantinya perlu diterapkan ke database. Sedangkan migrate digunakan untuk menerapkan migration tersebut ke database.

Contohnya, jika saya memiliki model Project lalu ingin menambahkan field baru seperti project_url, saya perlu menjalankan python manage.py makemigrations untuk membuat migration yang mencatat penambahan field tersebut. Setelah itu, saya menjalankan python manage.py migrate agar perubahan tersebut benar-benar diterapkan pada database. Jadi intinya, makemigrations membuat catatan perubahannya, sedangkan migrate menerapkan perubahan tersebut ke database.

## AI Disclosure
Saat pengerjaan tugas 2 ini,saya menggunakan bantuan Gen-AI untuk membantu saya memahami proses pembuatan superuser pada Django dan langkah-langkah yang perlu dilakukan melalui terminal. Selain itu, saya juga menggunakan Gen-AI untuk membantu memahami beberapa konsep dan mengecek implementasi yang saya kerjakan. Seluruh proses dan kode tetap saya sesuaikan dan kerjakan sendiri berdasarkan kebutuhan tugas.
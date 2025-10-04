from flask import Flask, render_template, request, redirect, url_for, session
from logic import db_manager
import datetime

db = db_manager("odevler.db")

app = Flask(__name__)
app.secret_key = "gizli-anahtar"

DOGRU_AD = "admin"
DOGRU_SIFRE = "1234"

# --- Veritabanından ödev çekme fonksiyonu ---

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ad = request.form.get("ad")
        sifre = request.form.get("sifre")

        if ad == DOGRU_AD and sifre == DOGRU_SIFRE:
            session["kullanici"] = ad
            return redirect(url_for("admin"))
        else:
            return render_template("index.html", hata="Hatalı kullanıcı adı veya şifre!")

    return render_template("index.html")

@app.route("/sinif1")
def sinif1():
    odevler = db.get_homeworks("8A")
    return render_template("sinif1.html", odevler=odevler)

@app.route("/sinif2")
def sinif2():
    odevler = db.get_homeworks("8B")
    return render_template("sinif2.html", odevler=odevler)

@app.route("/admin")
def admin():
    if "kullanici" in session:
        return render_template("admin.html")
    else:
        return redirect(url_for("index"))

@app.route("/cikis")
def cikis():
    session.pop("kullanici", None)
    return redirect(url_for("index"))

@app.route('/ogrenci', methods=['POST'])
def ogrenci():
    ogrenci_id = request.form.get('ogrenci_id')
    ogrenci_ad = request.form.get('ogrenci_ad')
    print(f'{ogrenci_ad}, {ogrenci_id}')
    # Öğrenci sayfasına yönlendir
    db.ogrenci_ekle(ogrenci_id, ogrenci_ad)

    return render_template("ogrenci.html", ogrenciler=ogrenci)

@app.route("/veri", methods=["POST"])
def veri():
    deger1 = request.form.get("deger1")
    deger2 = request.form.get("deger2")
    deger3 = request.form.get("deger3")
    deger4 = request.form.get("deger4")
    deger5 = request.form.get("deger5")
    deger6 = request.form.get("deger6")

    now = datetime.datetime.now()

    test_id = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.microsecond}'

    db.odev_yukle(test_id, deger1, deger2, deger3, deger4, deger5, deger6)

    return render_template("veri.html", test_id=test_id)

@app.route("/odev/<int:odev_id>")
def odev_sayfasi(odev_id):
    # Test bilgilerini al
    odev = db.get_test_by_id(odev_id)
    if not odev:
        return "Ödev bulunamadı", 404

    # Öğrenci cevaplarını al
    cevaplar = db.get_ogrenci_cevaplari(odev_id)
    
    # Cevapları dict formatına çevir
    ogrenci_cevaplari = []
    for c in cevaplar:
        ogrenci_cevaplari.append({
            'ogrenci_adi': c[2],   # ogrenci_name
            'cevaplar': c[3],      # cevaplar
            'puan': c[4]           # puan
        })
    
    # Sınıf ortalamasını hesapla
    toplam_puan = sum(c['puan'] for c in ogrenci_cevaplari)
    if ogrenci_cevaplari:
        ortalama = toplam_puan / len(ogrenci_cevaplari)
    else:
        ortalama = 0

    # Jinja template'e gönder
    odev_dict = {
        'test_id': odev[1],
        'sinif': odev[2],
        'ders': odev[3],
        'tarih': odev[4],
        'kitap': odev[5],
        'sayfalar': odev[6],
        'cevaplar': odev[7]
    }

    return render_template("odev_sayfasi.html", odev=odev_dict, ogrenci_cevaplari=ogrenci_cevaplari, ortalama=ortalama)


@app.route("/cevap_gonder", methods=["POST"])
def cevap_gonder():
    # Formdan gelen veriler
    test_id = request.form["test_id"]
    cevaplar_ogrenci = request.form["cevaplar"].upper()
    ogrenci_adi = request.form["ogrenci_adi"]

    # Ödev bilgilerini al
    test = db.get_test_by_id(test_id)
    if not test:
        return "Bu ID ile kayıtlı bir ödev bulunamadı."

    # test tuple yapısında, cevaplar 7. index (id:0, test_id:1, sinif:2, ders:3, tarih:4, kitap:5, sayfalar:6, cevaplar:7)
    dogru_cevaplar = test[7].upper() if test[7] else ""

    # Puan hesaplama
    puan = sum(1 for ogr, dogru in zip(cevaplar_ogrenci, dogru_cevaplar) if ogr == dogru)

    # Öğrenci cevabını kaydet
    db.ogrenci_cevabi_ekle(test_id, ogrenci_adi, cevaplar_ogrenci, puan)

    return f"Cevabınız kaydedildi. Doğru Sayınız: {puan}"



if __name__ == "__main__":
    app.run(debug=True)
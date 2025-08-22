from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Doğru kullanıcı bilgileri (örnek)
DOGRU_AD = "admin"
DOGRU_SIFRE = "1234"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ad = request.form.get("ad")
        sifre = request.form.get("sifre")
        print("Ad:", ad)
        print("Şifre:", sifre)

        if ad == DOGRU_AD and sifre == DOGRU_SIFRE:
            return redirect(url_for("admin"))
        else:
            return render_template("index.html", hata="Hatalı kullanıcı adı veya şifre!")

    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/veri", methods=["GET", "POST"])
def veri():
    deger1 = request.form.get("deger1")
    deger2 = request.form.get("deger2")
    deger3 = request.form.get("deger3")
    deger4 = request.form.get("deger4")
    deger5 = request.form.get("deger5")

    print("Deger1:", deger1)
    print("Deger2:", deger2)
    print("Deger3:", deger3)
    print("Deger4:", deger4)
    print("Deger5:", deger5)

    return render_template("veri.html")
                    

@app.route("/sinif1")
def sinif1():
    return render_template("sinif1.html")

@app.route("/sinif2")
def sinif2():
    return render_template("sinif2.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '3463159q'
app.config['MYSQL_DB'] = 'gsamonin'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    dn = datetime.now().date()
    if request.method == "POST":
        guestsDetails = request.form
        firstname = guestsDetails['firstname']
        secondname = guestsDetails['secondname']
        phone = guestsDetails['phone']
        email = guestsDetails['email']
        bil = guestsDetails['bil']
        amountPer = guestsDetails['amountPer']
        time_nach = guestsDetails['time_nach']
        time_okon = guestsDetails['time_okon']
        hn = datetime.strptime(time_nach, "%H:%M").time()
        hk = datetime.strptime(time_okon, "%H:%M").time()
        if hn > hk:
            return "Даже самые дорогие в мире часы — не стоят одной секунды жизненного времени!"
        date_game = guestsDetails['date_game']
        dg = datetime.strptime(date_game, "%Y-%m-%d").date()
        if dg < dn:
            return "Вы не можете играть в прошлом. " \
                   "Самое страшное — когда прошлым становятся те, кто должен был стать будущим."
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO guests(firstname, secondname, "
                    "phone, email) VALUES(%s, %s, %s, %s)", (firstname, secondname, phone, email))
        mysql.connection.commit()
        cur.execute("SELECT * FROM guests WHERE phone like %s", [phone])
        person = cur.fetchone()
        id = person[0]
        cur.execute("INSERT INTO game(guest_idgame, bil_id, amount, time_nach, time_okon, date_game) "
                    "VALUES(%s, %s, %s, %s, %s, %s)", (id, bil, amountPer, time_nach, time_okon, date_game))
        mysql.connection.commit()
        cur.close()
    return render_template("index.html")


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu where NOT id_menu = 10")
    data = cur.fetchall()
    cur.close
    print(data)
    return render_template("menu.html", menu = data)


@app.route('/price')
def price():
    return render_template("price.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)

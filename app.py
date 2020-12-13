from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if request.form['button'] == 'Sign in':
            return redirect('http://127.0.0.1:5000/signin')

        if request.form['button'] == 'Check Profile':
            pf = request.form
            id = pf['AccountID']
            password = pf['Password']

            return redirect(url_for('profile', id=id, password=password))

        if request.form['button'] == 'Search':
            return redirect('http://127.0.0.1:5000/search')

        if request.form['button'] == 'Recommend Movie':
            return redirect('http://127.0.0.1:5000/recommend')

        if request.form['button'] == 'Bye Bye':
            return redirect('https://www.google.com')

    return render_template('main.html')


@app.route('/profile/<id>/<password>', methods=['GET', 'POST'])
def profile(id, password):
    name = id
    pas = password;

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT * FROM customer WHERE AccountID = %s AND Password = %s", [name, pas])
    if resultVal > 0:
        customerDetails = cur.fetchall()
        return render_template('Profile.html', customerDetails=customerDetails)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        if request.form['button'] == 'Search Held Movie':
            userdetails = request.form

            accountid = userdetails['Current']
            return redirect(url_for('resultchm', val=accountid))

        if request.form['button'] == 'Search Movie Queue':
            userdetails = request.form

            accountid = userdetails['Queue']
            return redirect(url_for('resultsmq', val=accountid))

        if request.form['button'] == 'Search Movie Type':
            userdetails = request.form

            movietype = userdetails['MovieType']
            return redirect(url_for('resultsmt', val=movietype))

        if request.form['button'] == 'Search Keyword':
            userdetails = request.form

            movietype = "%" + userdetails['Keyword'] + "%"
            return redirect(url_for('resultsk', val=movietype))

        if request.form['button'] == 'Search Actor':
            userdetails = request.form

            factor = userdetails['FActor']
            lactor = userdetails['LActor']

            return redirect(url_for('resultsa', val1=factor, val2=lactor))

        if request.form['button'] == 'Go Back':
            return redirect('http://127.0.0.1:5000/main')

    return render_template('search.html')


@app.route('/resultchm/<val>', methods=['GET', 'POST'])
def resultchm(val):
    if request.method == 'POST':
        if request.form['button'] == 'Main Page':
            return redirect('http://127.0.0.1:5000/main')

    accountid = val;

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT DISTINCT b.MovieID, MovieName, Account FROM customer, borrow as b, Movie as m WHERE b.MovieID = m.MovieID AND Account = %s", [accountid])

    if resultVal > 0:
        details = cur.fetchall()
        print(details)
        return render_template('resultchm.html', details=details)


@app.route('/resultsmq/<val>', methods=['GET', 'POST'])
def resultsmq(val):
    if request.method == 'POST':
        if request.form['button'] == 'Main Page':
            return redirect('http://127.0.0.1:5000/main')

    accountid = val;

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT DISTINCT MovieQueue, FirstName, LastName, AccountID FROM customer WHERE MovieQueue >= 1 AND AccountID = %s", [accountid])

    if resultVal > 0:
        details = cur.fetchall()
        return render_template('resultsmq.html', details=details)


@app.route('/resultsmt/<val>', methods=['GET', 'POST'])
def resultsmt(val):
    if request.method == 'POST':
        if request.form['button'] == 'Main Page':
            return redirect('http://127.0.0.1:5000/main')

    movietype = val;

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT MovieID, MovieName, MovieType FROM Movie WHERE MovieType = %s", [movietype])

    if resultVal > 0:
        details = cur.fetchall()
        return render_template('resultsmt.html', details=details)


@app.route('/resultsk/<val>', methods=['GET', 'POST'])
def resultsk(val):
    if request.method == 'POST':
        if request.form['button'] == 'Main Page':
            return redirect('http://127.0.0.1:5000/main')

    keyword = val;

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT MovieID, MovieName FROM movie WHERE MovieName LIKE %s", [keyword])

    if resultVal > 0:
        details = cur.fetchall()
        return render_template('resultsk.html', details=details)


@app.route('/resultsa/<val1>/<val2>', methods=['GET', 'POST'])
def resultsa(val1, val2):
    if request.method == 'POST':
        if request.form['button'] == 'Main Page':
            return redirect('http://127.0.0.1:5000/main')

    firstname = val1;
    lastname = val2;

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT DISTINCT m.MovieID, m.MovieName, a.ActorID, a.FirstName, a.LastName FROM movie AS m, actor AS a WHERE m.ActorID = a.ActorID AND a.FirstName = %s AND a.LastName = %s", [firstname, lastname])

    if resultVal > 0:
        details = cur.fetchall()
        return render_template('resultsa.html', details=details)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        if request.form['button'] == 'Im Feeling Lucky':
            userdetails = request.form

            accountid = userdetails['AccountID']
            return redirect(url_for('resultlucky', val=accountid))

        if request.form['button'] == 'Give Rating':
            userdetails = request.form

            accountid = userdetails['AccountID']
            movieid = userdetails['MovieID']
            rating = userdetails['rating']

            print(rating)

            return redirect(url_for('resultrating', val1=accountid, val2=movieid, val3=rating))

        if request.form['button'] == 'Go Back':
            return redirect('http://127.0.0.1:5000/main')

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT MAX(NumberofCopies), MovieName FROM movie")

    if resultVal > 0:
        details = cur.fetchall()
        return render_template('recommend.html', details=details)


@app.route('/resultlucky/<val>', methods=['GET', 'POST'])
def resultlucky(val):
    if request.method == 'POST':
        if request.form['button'] == 'Main Page':
            return redirect('http://127.0.0.1:5000/main')

    accountid = val;

    cur = mysql.connection.cursor()
    resultVal = cur.execute("SELECT DISTINCT c.FirstName, c.LastName, m.MovieName, m.MovieType FROM customer AS c, borrow AS b, movie AS m WHERE b.MovieID <> m.MovieID AND c.AccountID = b.Account AND b.bMovieType = m.MovieType AND c.AccountID = %s", [accountid])

    if resultVal > 0:
        details = cur.fetchall()
        return render_template('resultlucky.html', details=details)


@app.route('/resultrating/<val1>/<val2>/<val3>', methods=['GET', 'POST'])
def resultrating(val1, val2, val3):
    if request.method == 'POST':
        if request.form['button'] == 'Main Page':
            return redirect('http://127.0.0.1:5000/main')

    accountid = val1;
    movieid = val2;
    rating = val3;

    cur = mysql.connection.cursor()
    cur.execute("UPDATE borrow SET Rating = %s WHERE Account = %s AND MovieID = %s", [rating, accountid, movieid])
    mysql.connection.commit()

    resultVal = cur.execute("SELECT * FROM borrow WHERE Account = %s", [accountid])

    if resultVal > 0:
        details = cur.fetchall()
        return render_template('resultrating.html', details=details)


@app.route('/signin', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        if request.form['button'] == 'Submit':
            userdetails = request.form

            firstname = userdetails['FirstName']
            lastname = userdetails['LastName']
            accountid = userdetails['AccountID']
            password = userdetails['Password']
            streetaddress = userdetails['StreetAddress']
            city_province = userdetails['City_Province']
            zipcode = userdetails['ZipCode']
            country = userdetails['Country']
            email = userdetails['Email']
            phonenumber = userdetails['PhoneNumber']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO customer(FirstName, LastName, AccountID, Password, StreetAddress, City_Province, ZipCode, Country, Email, PhoneNumber) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (firstname, lastname, accountid, password, streetaddress, city_province, zipcode, country, email, phonenumber))
            mysql.connection.commit()
            cur.close()
            return redirect('http://127.0.0.1:5000/main')

        elif request.form['button'] == 'Cancel':
            return redirect('http://127.0.0.1:5000/main')

    return render_template('signin.html')


@app.route('/add', methods=['GET', 'POST'])
def add():

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)

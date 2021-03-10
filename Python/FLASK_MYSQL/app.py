from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL
import sys

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mydbtest2.cqugl4aipzsd.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = sys.argv[1]
app.config['MYSQL_DB'] = 'MYSQL_DB_TEST'

mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        details = request.form
        content = details['content']
        cur = mysql.connection.cursor()

        command = "INSERT INTO Tasks(content, date_created) VALUES ('%s', NOW())" % content
        print(command)

        try:
            cur.execute(command)
            mysql.connection.commit()
            cur.close()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        cur = mysql.connection.cursor()
        cur.execute("select * from Tasks order by date_created, content")
        myresult = cur.fetchall()
        tasks = []
        for task in myresult:
            tasks.append(task)

        cur.close()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    command = "DELETE FROM Tasks where id=%d" % id
    print(command)
    try:
        cur.execute(command)
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    command = "SELECT * FROM Tasks where id=%d" % id
    print(command)
    cur.execute(command)
    task = cur.fetchone()

    if request.method == 'POST':
        command = "UPDATE Tasks SET content='%s' where id=%d" % (request.form['content'], id)
        print(command)

        try:
            cur.execute(command)
            mysql.connection.commit()
            cur.close()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
 


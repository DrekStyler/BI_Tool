import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g

app = Flask(__name__)
app.config.from_object('_config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in.')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials.'
            return render_template('login.html', error = error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('companies'))
    return render_template('login.html')

@app.route('/companies/')
def companies():
    g.db = connect.db()
    cur = g.db.execute(
        'select name, revenue from companies'
    )
    open_companies = [
        dict(name=row[0], revenue=row[1])
    ]
    g.db.close()
    return render_template(
        'companies',
        form=addCompanyForm(request.form),
        open_companies=open_companies
    )

@app.route('/add/', method=['POST'])
@login_required
def new_company():
    g.db = connect_db()
    name = request.form['name']
    revenue = request.form['revenue']
    if not name or not revenue:
        flash("All fields are required")
        return redirect(url_for('tasks'))
    else:
        g.db.execute('insert into companies (name,revenue) values (?,?)', [
                request.form['name'],
                request.form['revenue']
            ]
        )
        g.db.commit()
        g.db.close()
        flash('New Entry Was Added')
        return redirect(url_for('companies'))

@app.route('/delete/<int:company_id>/')
@login_required
def delete_entry(company_id):
    g.db = connect_db()
    g.db.execute('delete from companies where company_id =' +str(company_id))
    g.db.commit()
    g.db.close()
    flash('Company Deleted')
    return redirect(url_for('companies'))

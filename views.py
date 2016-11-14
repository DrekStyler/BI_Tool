import sqlite3, pygal, json
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from forms import AddCompanyForm

app = Flask(__name__)
app.config.from_object('_config')

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

def __init__(self, name, revenue):
    self.name = name
    self.revenue = revenue

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
    g.db = connect_db()
    cur = g.db.execute(
        'select name,revenue,company_id from companies'
    )

    open_companies = [
        dict(name=row[0], revenue=row[1], company_id=row[2]) for row in cur.fetchall()
    ]
    g.db.close()
    # title = 'Average Revenue'
    # bar_chart = pygal.Bar(width=1200, height=600, explicit_size=True, title=title, disable_xml_declaration=True)
    # html = """
    #         <h3>%s<//h3>
    #           <div>
    #              %s
    #          </div>
    #     </html>
    #     """ % (title, bar_chart.render())
    # return html
    return render_template(
        'companies.html',
        form=AddCompanyForm(request.form),
        open_companies=open_companies
    )

@app.route('/add/', methods=['POST'])
@login_required
def new_company():
    g.db = connect_db()
    name = request.form['name']
    revenue = request.form['revenue']
    if not name or not revenue:
        flash("All fields are required")
        return redirect(url_for('companies'))
        print('nay')
    else:
        g.db.execute('insert into companies(name,revenue) values (?,?)', [
                request.form['name'],
                request.form['revenue']
            ]
        )
        g.db.commit()
        g.db.close()
        flash('New Entry Was Added')
        print('yay')
        return redirect(url_for('companies'))

@app.route('/delete/<int:company_id>/')
@login_required
def delete_entry(company_id):
    g.db = connect_db()
    g.db.execute('delete from companies where company_id='+str(company_id))
    g.db.commit()
    g.db.close()
    flash('Company Deleted')
    return redirect(url_for('companies'))

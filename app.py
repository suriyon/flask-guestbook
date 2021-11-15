
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.secret_key = b'g[[uhcxiN'
db = SQLAlchemy(app)

class Guestbook(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    guest_name = db.Column(db.String(length=50), nullable=False, unique=False)
    text = db.Column(db.String(length=1024), nullable=False)

    def __repr__(self):
        return f'{self.guest_name}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/guestbook')
def guestbook():
    guestbooks = Guestbook.query.all()

    return render_template('guestbook.html', guestbooks=guestbooks)

@app.route('/add_text', methods=['GET', 'POST'])
def add_text():
    if request.method == 'POST':
        guest_name = request.form['guest_name']
        text = request.form['text']

        guestbook = Guestbook(guest_name=guest_name, text=text)

        db.session.add(guestbook)
        db.session.commit()
        flash('Add text successfully!', 'success')

        return redirect(url_for('guestbook'))

    return render_template('add_text.html')

@app.route('/edit_text/<int:id>', methods=['GET', 'POST'])
def edit_text(id):
    # guestbook = Guestbook.query.filter_by(id=id).first()    
    # print(guestbook)

    query = db.session.query(Guestbook).filter(Guestbook.id==id)
    guestbook = query.first()

    if guestbook:
        if request.method == 'POST':
            guestbook.guest_name = request.form['guest_name']
            guestbook.text = request.form['text']

            db.session.commit()
            flash('Update text successfully!', 'success')
            return redirect(url_for('guestbook'))
        else:
            return render_template('edit_text.html', guestbook=guestbook)
    
    # return redirect(url_for('guestbook'))
    

@app.route('/delete_text/<int:id>', methods=['GET', 'POST'])
def delete_text(id):
    Guestbook.query.filter(Guestbook.id==id).delete()
    db.session.commit()
    flash('Delete text successfully!', 'success')
    return redirect(url_for('guestbook'))

if __name__ == '__main__':
    app.run(debug=True)

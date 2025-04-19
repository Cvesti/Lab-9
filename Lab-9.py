from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Для CSRF защиты
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Contact {self.name}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        
        new_contact = Contact(name=name, phone=phone)
        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'При добавлении контакта произошла ошибка'
    
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('index.html', contacts=contacts)

@app.route('/delete/<int:id>')
def delete(id):
    contact_to_delete = Contact.query.get_or_404(id)
    
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'При удалении контакта произошла ошибка'

@app.route('/clear_all', methods=['POST'])
def clear_all():
    try:
        num_rows_deleted = db.session.query(Contact).delete()
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return f'При очистке телефонной книги произошла ошибка: {str(e)}'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
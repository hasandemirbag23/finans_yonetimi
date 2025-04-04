from finance_app import app, db
from datetime import datetime
from finance_app.models.models import User, Income, Expense, Budget
import os

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

def create_tables():
    with app.app_context():
        db.create_all()
        
        # Eğer admin kullanıcısı yoksa oluştur
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('password')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True) 
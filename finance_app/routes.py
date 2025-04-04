from flask import render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from finance_app import app, db
from finance_app.models.models import User, Income, Expense, Budget
from finance_app.forms import LoginForm, RegistrationForm, IncomeForm, ExpenseForm, BudgetForm
from datetime import datetime
import pandas as pd
import calendar
import os

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Kullanıcının toplam geliri
    total_income = db.session.query(db.func.sum(Income.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Kullanıcının toplam gideri
    total_expense = db.session.query(db.func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Kullanıcının kalan bakiyesi
    balance = total_income - total_expense
    
    # Son 5 gelir
    recent_incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).limit(5).all()
    
    # Son 5 gider
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).limit(5).all()
    
    # Kategori bazlı giderler
    expenses_by_category = db.session.query(
        Expense.category, db.func.sum(Expense.amount)
    ).filter_by(user_id=current_user.id).group_by(Expense.category).all()
    
    # Kategori bazlı gelirler
    incomes_by_category = db.session.query(
        Income.category, db.func.sum(Income.amount)
    ).filter_by(user_id=current_user.id).group_by(Income.category).all()
    
    return render_template(
        'dashboard.html', 
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        recent_incomes=recent_incomes,
        recent_expenses=recent_expenses,
        expenses_by_category=expenses_by_category,
        incomes_by_category=incomes_by_category
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Giriş başarısız. Lütfen email ve şifrenizi kontrol edin.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/incomes', methods=['GET', 'POST'])
@login_required
def incomes():
    form = IncomeForm()
    if form.validate_on_submit():
        income = Income(
            amount=form.amount.data,
            description=form.description.data,
            category=form.category.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(income)
        db.session.commit()
        flash('Gelir başarıyla eklendi!', 'success')
        return redirect(url_for('incomes'))
    
    # Tüm gelirler
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()
    
    return render_template('incomes.html', form=form, incomes=incomes)

@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def expenses():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            amount=form.amount.data,
            description=form.description.data,
            category=form.category.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(expense)
        db.session.commit()
        flash('Gider başarıyla eklendi!', 'success')
        return redirect(url_for('expenses'))
    
    # Tüm giderler
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    
    return render_template('expenses.html', form=form, expenses=expenses)

@app.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():
    form = BudgetForm()
    if form.validate_on_submit():
        # Mevcut bütçe kontrolü
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            category=form.category.data,
            month=form.month.data,
            year=form.year.data
        ).first()
        
        if existing_budget:
            existing_budget.amount = form.amount.data
            flash('Bütçe güncellendi!', 'success')
        else:
            budget = Budget(
                category=form.category.data,
                amount=form.amount.data,
                month=form.month.data,
                year=form.year.data,
                user_id=current_user.id
            )
            db.session.add(budget)
            flash('Bütçe başarıyla oluşturuldu!', 'success')
        
        db.session.commit()
        return redirect(url_for('budget'))
    
    # Mevcut ay ve yıl
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Form için varsayılan değerler
    form.month.data = current_month
    form.year.data = current_year
    
    # Kullanıcının bütçeleri
    budgets = Budget.query.filter_by(
        user_id=current_user.id,
        month=current_month,
        year=current_year
    ).all()
    
    # Kategori bazlı harcama toplamları
    expenses_this_month = db.session.query(
        Expense.category, db.func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id,
        db.extract('month', Expense.date) == current_month,
        db.extract('year', Expense.date) == current_year
    ).group_by(Expense.category).all()
    
    # Bütçe-harcama karşılaştırması
    budget_comparison = []
    for budget in budgets:
        expense_amount = 0
        for expense_category, amount in expenses_this_month:
            if expense_category == budget.category:
                expense_amount = amount
                break
        
        remaining = budget.amount - expense_amount
        percentage = (expense_amount / budget.amount * 100) if budget.amount > 0 else 0
        
        budget_comparison.append({
            'category': budget.category,
            'budget_amount': budget.amount,
            'expense_amount': expense_amount,
            'remaining': remaining,
            'percentage': percentage
        })
    
    return render_template(
        'budget.html', 
        form=form, 
        budgets=budgets,
        budget_comparison=budget_comparison,
        current_month=calendar.month_name[current_month],
        current_year=current_year
    )

@app.route('/reports')
@login_required
def reports():
    # Mevcut ay ve yıl
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Tüm gelirler
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    
    # Tüm giderler
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    
    # Aylık gelir toplamları
    monthly_incomes = db.session.query(
        db.extract('year', Income.date).label('year'),
        db.extract('month', Income.date).label('month'),
        db.func.sum(Income.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by('year', 'month').all()
    
    # Aylık gider toplamları
    monthly_expenses = db.session.query(
        db.extract('year', Expense.date).label('year'),
        db.extract('month', Expense.date).label('month'),
        db.func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by('year', 'month').all()
    
    # Aylık bütçe karşılaştırması
    monthly_budget_vs_expense = []
    for year, month, expense_total in monthly_expenses:
        # Ay için toplam bütçe
        total_budget = db.session.query(db.func.sum(Budget.amount)).filter_by(
            user_id=current_user.id,
            month=int(month),
            year=int(year)
        ).scalar() or 0
        
        month_name = calendar.month_name[int(month)]
        
        monthly_budget_vs_expense.append({
            'month': f"{month_name} {int(year)}",
            'budget': total_budget,
            'expense': expense_total,
            'difference': total_budget - expense_total
        })
    
    # Kategori bazlı gider yüzdeleri
    category_expenses = db.session.query(
        Expense.category, db.func.sum(Expense.amount).label('total')
    ).filter_by(user_id=current_user.id).group_by(Expense.category).all()
    
    total_expense = sum(amount for _, amount in category_expenses)
    
    category_percentages = []
    for category, amount in category_expenses:
        percentage = (amount / total_expense * 100) if total_expense > 0 else 0
        category_percentages.append({
            'category': category,
            'percentage': round(percentage, 2),
            'amount': amount
        })
    
    return render_template(
        'reports.html',
        monthly_incomes=monthly_incomes,
        monthly_expenses=monthly_expenses,
        monthly_budget_vs_expense=monthly_budget_vs_expense,
        category_percentages=category_percentages
    )

@app.route('/delete_income/<int:id>', methods=['POST'])
@login_required
def delete_income(id):
    income = Income.query.get_or_404(id)
    if income.user_id != current_user.id:
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('incomes'))
    
    db.session.delete(income)
    db.session.commit()
    flash('Gelir başarıyla silindi!', 'success')
    return redirect(url_for('incomes'))

@app.route('/delete_expense/<int:id>', methods=['POST'])
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('expenses'))
    
    db.session.delete(expense)
    db.session.commit()
    flash('Gider başarıyla silindi!', 'success')
    return redirect(url_for('expenses'))

@app.route('/delete_budget/<int:id>', methods=['POST'])
@login_required
def delete_budget(id):
    budget = Budget.query.get_or_404(id)
    if budget.user_id != current_user.id:
        flash('Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('budget'))
    
    db.session.delete(budget)
    db.session.commit()
    flash('Bütçe başarıyla silindi!', 'success')
    return redirect(url_for('budget'))

@app.route('/export_data', methods=['GET'])
@login_required
def export_data():
    data_type = request.args.get('type', 'incomes')
    
    # Statik klasörü oluştur (yoksa)
    static_dir = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    if data_type == 'incomes':
        data = Income.query.filter_by(user_id=current_user.id).all()
        df = pd.DataFrame([{
            'ID': income.id,
            'Miktar': income.amount,
            'Açıklama': income.description,
            'Kategori': income.category,
            'Tarih': income.date.strftime('%Y-%m-%d')
        } for income in data])
        filename = f"gelirler_{datetime.now().strftime('%Y%m%d')}.csv"
    
    elif data_type == 'expenses':
        data = Expense.query.filter_by(user_id=current_user.id).all()
        df = pd.DataFrame([{
            'ID': expense.id,
            'Miktar': expense.amount,
            'Açıklama': expense.description,
            'Kategori': expense.category,
            'Tarih': expense.date.strftime('%Y-%m-%d')
        } for expense in data])
        filename = f"giderler_{datetime.now().strftime('%Y%m%d')}.csv"
    
    elif data_type == 'budgets':
        data = Budget.query.filter_by(user_id=current_user.id).all()
        df = pd.DataFrame([{
            'ID': budget.id,
            'Kategori': budget.category,
            'Miktar': budget.amount,
            'Ay': calendar.month_name[budget.month],
            'Yıl': budget.year
        } for budget in data])
        filename = f"butceler_{datetime.now().strftime('%Y%m%d')}.csv"
    
    else:
        flash('Geçersiz veri tipi!', 'danger')
        return redirect(url_for('dashboard'))
    
    # CSV dosyası oluştur
    csv_path = os.path.join(static_dir, filename)
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    # Dosyayı indir
    flash(f'{filename} başarıyla oluşturuldu!', 'success')
    return send_file(csv_path, as_attachment=True, download_name=filename) 
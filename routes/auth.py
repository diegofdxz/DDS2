from urllib.parse import urlparse
from db import get_users_connection, hash_password
from flask import request, redirect, render_template, session, flash
from server import app
@app.route('/login', methods=['GET', 'POST'])
def login():
   
    if 'username' in session:
        return redirect(url_for('dashboard'))

    
    raw_next_url = request.args.get('next')
    next_url = '/dashboard'  # Valor seguro por defecto

    if raw_next_url:
        parsed_url = urlparse(raw_next_url)
        
        if not parsed_url.netloc and parsed_url.path.startswith('/'):
            next_url = raw_next_url

   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_users_connection()
        
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        user = conn.execute(query, (username, hash_password(password))).fetchone()
        conn.close()
        
        if user:
           
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['company_id'] = user['company_id']
            session.permanent = True
            
            return redirect(next_url)
        else:
            flash("Invalid username or password", "danger")
            return render_template('auth/login.html', next_url=next_url)

    return render_template('auth/login.html', next_url=next_url)


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))
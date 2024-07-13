from flask import Flask, request, redirect, url_for, render_template_string, session

app = Flask(__name__)
app.secret_key = 'bvfdhfvla'  # Use a strong, random value in production
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',
)


users = {
    'admin': {
        'username': 'admin',
        'password': 'adminpass'  # In a real application, use hashed passwords
    }
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile Management Service</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; }
        input, button { padding: 10px; margin-top: 10px; }
        form { margin-bottom: 20px; }
    </style>
</head>
<body>
    {{content|safe}}
</body>
</html>
'''

@app.route('/')
def index():
    if 'authenticated' in session:
        content_html = f'''
            <h1>Welcome, {users['admin']['username']}</h1>
            <p>Change your password or username below:</p>
            <form action="/update-password" method="POST">
                <input type="text" name="new_password" placeholder="Enter new password">
                <button type="submit">Update Password</button>
            </form>
            
            <form action="/update-username" method="POST">
                <input type="text" name="new_username" placeholder="Enter new username">
                <button type="submit">Change Username</button>
            </form>
            <a href="/logout">Logout</a>
        '''
        return render_template_string(HTML_TEMPLATE, content=content_html)
    else:
        return render_template_string(HTML_TEMPLATE, content='''
        <h1>Login</h1>
        <form action="/login" method="POST">
            <input type="password" name="password" placeholder="Password">
            <button type="submit">Login as Admin</button>
        </form>
        ''')

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    print(users['admin']['password'])
    if password == users['admin']['password']:
        session['authenticated'] = True
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

@app.route('/update-password', methods=['GET', 'POST'])
def update_password():
    if 'authenticated' not in session:
        print('not authenticated')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Access form data for POST requests
        new_password = request.form.get('new_password', '')
    else:
        # Access query parameters for GET requests
        new_password = request.args.get('new_password', '')
    
    users['admin']['password'] = new_password
    print(f"New password: {new_password}")
    return redirect(url_for('index'))


@app.route('/update-username', methods=['POST'])
def update_username():
    if 'authenticated' not in session:
        return redirect(url_for('index'))
    
    new_username = request.form.get('new_username', '')
    # XSS vulnerability if any JavaScript is passed as a new username:
    users['admin']['username'] = new_username
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

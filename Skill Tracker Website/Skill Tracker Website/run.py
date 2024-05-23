from app import app

app.secret_key = 'cooperwashere'
if __name__ == '__main__':
    app.run(debug=True)
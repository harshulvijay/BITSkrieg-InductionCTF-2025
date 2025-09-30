from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if username == 'bitskrieg' and password == 'MD5':
            return "InductionCTF{MD5_15_UN54F3}"
       
        
    return render_template('default.html')


if __name__ == '__main__':
    app.run(debug=False)  # Set to False in production

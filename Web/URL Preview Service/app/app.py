from flask import Flask, render_template, request
import requests
from urllib.parse import urlparse
import socket

app = Flask(__name__)

BLOCKED_DOMAINS = ['localhost', '127.0.0.1', '0.0.0.0', '10.', '172.', '192.168.']

def is_blocked_url(url):
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        port = parsed.port
        
        if not hostname:
            return True, "Invalid hostname"

        for blocked in BLOCKED_DOMAINS:
            if blocked.lower() in hostname.lower():
                return True, f"Blocked domain: {blocked}"
        try:
            ip = socket.gethostbyname(hostname)
            if ip.startswith('127.') or ip.startswith('10.') or ip.startswith('192.168.'):
                return True, f"Private IP detected: {ip}"
        except:
            pass
        return False, "URL allowed"
        
    except Exception as e:
        return True, f"Error parsing URL: {str(e)}"

def fetch_url_preview(url):
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        return {'status': 'success', 'content': response.text}
    except Exception as e:
        return {'status': 'error', 'message': f'Error: {str(e)}'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview')
def preview_url():
    url = request.args.get('url', '').strip()
    if not url:
        return render_template('preview.html', error='No URL provided')
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    blocked, reason = is_blocked_url(url)
    if blocked:
        return render_template('preview.html', error=reason, url=url)
    
    result = fetch_url_preview(url)
    return render_template('preview.html', result=result, url=url)

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=3000, debug=False)

from flask import Flask, request, send_file, jsonify
import os
import io
import qrcode
from functools import wraps

app = Flask(__name__)

# In-memory database of valid API keys (replace with a real database in production)
VALID_API_KEYS = {'your_paid_user_api_key'}

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.args.get('api_key')
        if api_key in VALID_API_KEYS:
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid or missing API key'}), 403
    return decorated

@app.route('/')
def home():
    return '''
    <h1>Welcome to the QR Code Generator SaaS App</h1>
    <p>Use the <code>/generate_qr</code> endpoint with your API key and data to generate a QR code.</p>
    <p>Example: <a href="/generate_qr?api_key=your_paid_user_api_key&data=HelloWorld">Generate QR Code</a></p>
    '''

@app.route('/generate_qr')
@require_api_key
def generate_qr():
    data = request.args.get('data')
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Get the port from the environment or default to 5000
    #app.run()
    app.run(host='0.0.0.0', port=port)

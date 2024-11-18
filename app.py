from flask import Flask, jsonify, make_response
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 
                            'http://localhost:3000,https://staging.olitt.com,https://beta.olitt.com,https://app.olitt.com,https://olitt.com'
                            ).split(',')

CORS(app, supports_credentials=True, origins=ALLOWED_ORIGINS)

@app.route("/check-cookies")
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Check Third Party Cookies</h1>
        <script>
            // Try to set a test cookie
            document.cookie = "test_cookie=1; SameSite=None; Secure";
            
            // Check if we can read the cookie
            const cookiesEnabled = document.cookie.indexOf('test_cookie=1') !== -1;
            
            // Send result to parent window
            window.parent.postMessage({ cookiesEnabled }, '*');
        </script>
    </body>
    </html>
    """
    
    response = make_response(html)
    response.headers['Content-Type'] = 'text/html'
    
    # Set CORS headers
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Cookie check service is running'
    })

if __name__ == '__main__':
    app.run(debug=True)
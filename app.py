from flask import Flask, jsonify, make_response, render_template, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get allowed origins from environment variable
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')

# Configure CORS
CORS(app,{
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
)
# CORS(app, supports_credentials=True)

@app.route("/check-cookies")
def index():
    print("Received cookies:", request.cookies)
    if 'ngrok-skip-browser-warning' in request.headers:
        has_cookie = request.cookies.get('test_cookie') is not None
        html = """
        <!DOCTYPE html>
        <html>
        <body>
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
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    else:
        return ""

# @app.route('/check-cookies')
# def check_cookies():
#     # Log cookies for debugging
#     print("Received cookies:", request.cookies)
    
#     # Check if the test cookie exists
#     has_cookie = request.cookies.get('testcookie') == '1'
#     print(has_cookie)
    
#     # Create response
#     response = jsonify({
#         'cookiesEnabled': has_cookie,
#         'receivedCookies': dict(request.cookies)  # For debugging
#     })
    
#     # Set CORS headers
#     origin = request.headers.get('Origin')
#     print("origin", origin)
#     if origin in ALLOWED_ORIGINS:
#         response.headers['Access-Control-Allow-Origin'] = origin
#         response.headers['Access-Control-Allow-Credentials'] = 'true'
#     print(response)
    
#     return response

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Cookie check service is running'
    })

if __name__ == '__main__':
    app.run(debug=True)
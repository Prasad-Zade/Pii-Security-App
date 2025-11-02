import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pii_privacy_handler_app', 'backend'))

from pii_privacy_handler_app.backend.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
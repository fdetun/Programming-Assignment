#!/usr/bin/python3
"""
Programming Assignment - iCompaas API
"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from v1.sanitized import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/v1/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)



if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5006, threaded=True)

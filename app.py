from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    # Serve the main game page
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    # Serve static files like JS and CSS
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Run the Flask app on all interfaces at port 5000
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template
import yaml

app = Flask(__name__)

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

@app.route('/')
def index():
    return render_template('index.html', config = config)

@app.route('/student_mental_health.html')
def student_mental_health():
    return render_template('projects/student_mental_health.html', config = config)

@app.route('/spotify_data_analysis.html')
def spotify_data_analysis():
    return render_template('projects/spotify_data_analysis.html', config = config)

@app.route('/indian_food_data_analysis.html')
def indian_food_data_analysis():
    return render_template('projects/indian_food_data_analysis.html', config = config)

@app.route('/ultra_marathons_data_analysis.html')
def ultra_marathons_data_analysis():
    return render_template('projects/ultra_marathons_data_analysis.html', config = config)

@app.route('/audio_library_organizer.html')
def audio_library_organizer():
    return render_template('projects/audio_library_organizer.html', config = config)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ =='__main__':
    app.run(debug=True)

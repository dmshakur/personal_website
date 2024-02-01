from ast import literal_eval as str_to_dict
import yaml

from flask import Flask, render_template, request


app = Flask(__name__)

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)



@app.route('/')
def index():
    return render_template('index.html', config = config)



@app.route('/projects/<project_url>.html')
def open_project_view(project_url):
    project_name = request.args.get('project_name')
    github_data = str_to_dict(request.args.get('github_data'))
    if github_data['raw_file_display']:
        if type(github_data['files']) is str:
            github_data['files'] = [github_data['files']]
    else:
        if type(github_data['notebooks']) is str:
            github_data['notebooks'] = [github_data['notebooks']]
    

    return render_template(
        'project_view.html', 
        config = config, 
        project_name = project_name,
        github_data = github_data
    )



@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response



if __name__ =='__main__':
    app.run(debug=True)

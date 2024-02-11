from ast import literal_eval as str_to_dict
from importlib import import_module
import json
import yaml

from flask import Flask, render_template, request
from markdown import markdown
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import requests


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

@app.route('/readme')
def readme():
    github_data = request.args.get('github_data')
    github_data = json.loads(github_data)
    readme_url = f'https://raw.githubusercontent.com/dmshakur/{github_data["repo_name"]}/{github_data["branch"]}/README.md'

    readme = requests.get(readme_url)
    readme_html = markdown(readme.text)

    return readme_html, 200


@app.route('/dashboard')
def dashboard():
    github_data  = request.args.get('github_data')
    repo_name = json.loads(github_data)["repo_name"]

    module_path = f'dashboards.{repo_name}.{repo_name}_dashboard'
    dash_module = import_module(module_path)
    dash_app = dash_module.dash_app


    return render_template(
        'dashboard.html',
        dash_app = dash_app
    )


@app.route('/code')
def code():
    github_data = request.args.get('github_data')
    github_data = json.loads(github_data)

    if github_data['raw_file_display']:
        formatter = HtmlFormatter(style = 'friendly', full = True, cssclass = 'pygments')

        title = github_data['repo_name'].replace('_', ' ').capitalize()
        h3_title = f'<h3>{title}</h3>'
        html = [h3_title]

        for i, file in enumerate(github_data['files']):
            file_url = f'https://raw.githubusercontent.com/dmshakur/{github_data["repo_name"]}/{github_data["branch"]}/{file}'
            python_file = requests.get(file_url)
            highlighted_file = highlight(python_file.text, PythonLexer(), formatter)

            
            html.extend([
                f'<h5>File {i + 1}: {file}</h5>',
                '<hr>' + highlighted_file + '<hr>'
            ])
        
        css = formatter.get_style_defs('.pygments')
        style = f'<style>{" ".join(css)}</style>'
        html = ' '.join(html)

        return style + html, 200

    return render_template(
        'code.html',
        github_data = github_data
    )



@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response



if __name__ =='__main__':
    app.run(debug=False)

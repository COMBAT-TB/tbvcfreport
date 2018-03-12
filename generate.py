from jinja2 import Environment, FileSystemLoader
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))

j2_env = Environment(loader=FileSystemLoader(
    os.path.join(CURR_DIR, "templates")),
    trim_blocks=True
)


def render_template(template, data):
    return j2_env.get_template(template).render(data)


def create_report(data=None):
    output = 'output.html'
    title = 'VCFReport'
    context = {
        'title': title,
        'data': data,
    }
    with open(output, 'w') as f:
        html = render_template('report-layout.html', context)
        f.write(html)

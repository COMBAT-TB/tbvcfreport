import os
from jinja2 import Environment, FileSystemLoader

jinja_env = Environment(loader=FileSystemLoader(
    os.path.join(os.getcwd(), "templates")),
    trim_blocks=True
)


def render_template(template, data):
    return jinja_env.get_template(template).render(data)


def render_report(file_name, data):
    try:
        output = '{file_name}.html'.format(file_name=file_name)
        context = {
            'file_name': file_name,
            'data': data,
        }
        with open(output, 'w') as f:
            html = render_template('report-layout.html', context)
            f.write(html)

        return output
    except Exception as e:
        raise e

"""
Interface to Jinja
"""
import os

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

jinja_env = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")),
    trim_blocks=True
)


def render_template(template, data):
    """
    Render HTML template
    :param template:
    :param data:
    :return:
    """
    return jinja_env.get_template(template).render(data)


def generate_report(file_name, data):
    """
    Write and render HTML report
    :param file_name:
    :param data:
    :return:
    """
    try:

        output = '{file_name}.html'.format(file_name=file_name)
        context = {
            'file_name': file_name,
            'data': data,
        }
        html = render_template('report-layout.html', context)
        with open(output, 'w') as f:
            f.write(html)

        # PDF output
        pdf_output = '{file_name}.pdf'.format(file_name=file_name)
        HTML(string=html).write_pdf(pdf_output)

        return output
    except Exception as e:
        raise e


def generate_drug_resistance_report(file_name, data):
    """
    Write and render HTML report
    :param file_name:
    :param data:
    :return:
    """
    try:

        output = '{file_name}_drug_resistance.html'.format(file_name=file_name)
        context = {
            'file_name': file_name,
            'data': data,
        }
        html = render_template('drug_resistance_report.html', context)
        with open(output, 'w') as f:
            f.write(html)

        # PDF output
        pdf_output = '{file_name}_drug_resistance.pdf'.format(
            file_name=file_name)
        HTML(string=html).write_pdf(pdf_output)

        return output
    except Exception as e:
        raise e

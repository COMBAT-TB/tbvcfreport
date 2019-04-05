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
        generate_txt_report(file_name, data)
        output = '{file_name}_variants_report.html'.format(file_name=file_name)
        context = {
            'file_name': file_name,
            'data': data,
        }
        html = render_template('report-layout.html', context)
        with open(output, 'w') as f:
            f.write(html)
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
        generate_dr_txt_report(file_name, data)
        output = '{file_name}_drug_resistance_report.html'.format(
            file_name=file_name)
        context = {
            'file_name': file_name,
            'data': data,
        }
        html = render_template('drug_resistance_report.html', context)
        with open(output, 'w') as f:
            f.write(html)

        # PDF output
        pdf_output = '{file_name}_drug_resistance_report.pdf'.format(
            file_name=file_name)
        HTML(string=html).write_pdf(pdf_output)

        return output
    except Exception as e:
        raise e


def generate_txt_report(file_name, data):

    txt_output = '{file_name}_variants_report.txt'.format(file_name=file_name)

    agreement = "{}%".format(data['lineage'].get('percent_agreement', ''))
    lineage_header = ['Species', 'Lineage', 'Sub-lineage', 'Agreement']
    lineage_data = [[data['lineage'].get('species', ''),
                     data['lineage'].get('lineage', ''),
                     data['lineage'].get('sublineage', ''), agreement]
                    ]
    # pdf tables required nested lists
    # lineage_data.insert(0, lineage_header)
    variants_header = ['CHR', 'GENE', 'IDENTIFIER', 'PRODUCT', 'TYPE',
                       'ANNOTATION', 'POS', 'REF', 'ALT', 'CONSEQUENCE',
                       'IMPACT', 'PATHAWAY']
    snp_data = data.get('variants')
    variants = [[s[16], s[3], s[4],
                 s[21]['protein']['uniquename'] if s[21]['protein'] else '',
                 s[19], s[1], str(s[17]), s[18], s[0], s[10], s[2],
                 ','.join([p['name'] for p in s[21]['pathway']]
                          ) if s[21]['pathway'] and len(s[21]['pathway']) >= 1 else ''
                 ]
                for s in snp_data]
    # pdf tables required nested lists
    # variants.insert(0, variants_header)
    with open(txt_output, 'w') as f:
        f.write("#{} Report\n".format(file_name))
        f.write("#{}\n".format('\t'.join(lineage_header)))
        for data in lineage_data:
            f.write("{}\n".format('\t'.join(data)))
        f.write("\n#{}\n".format('\t'.join(variants_header)))
        for data in variants:
            f.write("{}\n".format('\t'.join(data)))
    return True


def generate_dr_txt_report(file_name, data):
    txt_output = '{file_name}_drug_resistance_report.txt'.format(
        file_name=file_name)
    agreement = "{}%".format(data['lineage'].get('percent_agreement', ''))
    lineage_data = [['Species', 'Lineage', 'Sub-lineage', 'Agreement'],
                    [data['lineage'].get('species', ''),
                     data['lineage'].get('lineage', ''),
                     data['lineage'].get('sublineage', ''), agreement]
                    ]
    with open(txt_output, 'w') as f:
        f.write("#{} Report\n".format(file_name))
        f.write("#{}\n".format('\t'.join(lineage_data[0])))
        for entry in lineage_data[1:]:
            f.write("{}\n".format('\t'.join(entry)))
        f.write("\n#TBProfiler Drug Resistance Report\n")
        f.write("\n#{}\n".format(
            '\t'.join(['Drug', 'Resistance', 'Supporting Mutations'])))
        for entry in data['dr_data']:
            resistant = "R" if entry['resistant'] else "S"
            drug = entry['drug_human_name']
            mutations = ["{}({}-{})".format(mutation[0], str(mutation[2]), mutation[1])
                         for mutation in entry['variants']] if entry.get('variants') else ""
            f.write("{}\n".format(
                '\t'.join([drug, resistant, ','.join(mutations)])))
        f.write("\n#Drug resistance predictions are for research purposes only and are produced by the TBProfiler software.\n")

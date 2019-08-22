"""Interface to Jinja."""
import os

from jinja2 import Environment, FileSystemLoader

jinja_env = Environment(loader=FileSystemLoader(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")),
    trim_blocks=True
)


def render_template(template, data):
    """Render HTML template.

    :param template:
    :param data:
    :return:
    """
    return jinja_env.get_template(template).render(data)


def generate_report(file_name, data):
    """Write and render HTML report.

    :param file_name:
    :param data:
    :return:
    """
    try:
        generate_txt_report(file_name, data)

        context = {
            'file_name': file_name,
            'data': data,
        }
        # variants report
        output = '{file_name}_variants_report.html'.format(file_name=file_name)
        html = render_template('report-layout.html', context)
        with open(output, 'w') as v_report:
            v_report.write(html)

        # drug_resistance_report
        if data.get('dr_data') and len(data['dr_data']) > 0:
            dr_output = '{file_name}_drug_resistance_report.html'.format(
                file_name=file_name)
            dr_html = render_template('drug_resistance_report.html', context)
            with open(dr_output, 'w') as dr_output:
                dr_output.write(dr_html)
    except Exception as e:
        raise e


def generate_txt_report(file_name, data):
    """Generate text reports.

    :param file_name:
    :param data:
    :return:
    """
    v_txt_output = '{file_name}_variants_report.txt'.format(
        file_name=file_name)

    agreement = "{}%".format(data['lineage'].get('percent_agreement', ''))
    lineage_header = ['Species', 'Lineage', 'Sub-lineage', 'Agreement']
    lineage_data = [[data['lineage'].get('species', ''),
                     data['lineage'].get('lineage', ''),
                     data['lineage'].get('sublineage', ''), agreement]
                    ]
    variants_header = ['CHR', 'GENE', 'IDENTIFIER', 'PRODUCT', 'TYPE',
                       'ANNOTATION', 'POS', 'REF', 'ALT', 'CONSEQUENCE',
                       'IMPACT', 'PATHAWAY']
    snp_data = data.get('variants')
    variants = [
        [
            s[16], s[3], s[4],
            s[21]['protein']['uniquename'] if s[21]['protein'] else '',
            s[19], s[1], str(s[17]), s[18], s[0], s[10], s[2],
            ','.join(map(str, [p['name'] for p in s[21]['pathway']]))
            if s[21].get('pathway') and len(s[21]['pathway']) >= 1 else ''
        ]
        for s in snp_data
    ]
    with open(v_txt_output, 'w') as _variants_report:
        _variants_report.write("#{} Report\n".format(file_name.capitalize()))

        _variants_report.write("#{}\n".format('\t'.join(lineage_header)))
        for l_data in lineage_data:
            _variants_report.write("{}\n".format('\t'.join(l_data)))

        _variants_report.write("\n#{}\n".format('\t'.join(variants_header)))
        for variant in variants:
            _variants_report.write("{}\n".format('\t'.join(variant)))

    if data.get('dr_data') and len(data['dr_data']) > 0:
        dr_txt_output = '{file_name}_drug_resistance_report.txt'.format(
            file_name=file_name)
        with open(dr_txt_output, 'w') as dr_report:
            dr_report.write("#{} Report\n".format(file_name.capitalize()))

            dr_report.write("#{}\n".format('\t'.join(lineage_header)))
            for l_data in lineage_data:
                dr_report.write("{}\n".format('\t'.join(l_data)))

            dr_report.write("\n#TBProfiler Drug Resistance Report\n")
            dr_report.write("\n#{}\n".format(
                '\t'.join(['Drug', 'Resistance', 'Supporting Mutations'])))
            for entry in data['dr_data']:
                resistant = "R" if entry['resistant'] else "S"
                drug = entry['drug_human_name']
                mutations = [
                    "{}({}-{})".format(mutation[0],
                                       str(mutation[2]), mutation[1])
                    for mutation in entry['variants']
                ] if entry.get('variants') else ""
                dr_report.write("{}\n".format(
                    '\t'.join([drug, resistant, ','.join(mutations)])))
            dr_report.write(
                "\n#Drug resistance predictions are for research purposes only and are produced by the TBProfiler software.\n")

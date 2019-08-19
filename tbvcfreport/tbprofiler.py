"""Interface to TBProfiler report."""

import json

import click

drug_list = ['isoniazid', 'rifampicin', 'ethambutol',
             'pyrazinamide', 'streptomycin', 'ethionamide',
             'fluoroquinolones', 'amikacin', 'capreomycin',
             'kanamycin', 'para-aminosalicylic_acid',
             'cycloserine', 'delaminid', 'linezolid',
             'clofazimine', 'bedaquiline'
             ]

drug_names = {
    'isoniazid': 'Isoniazid',
    'rifampicin': 'Rifampicin',
    'ethambutol': 'Ethambutol',
    'pyrazinamide': 'Pyrazinamide',
    'streptomycin': 'Streptomycin',
    'ethionamide': 'Ethionamide',
    'fluoroquinolones': 'Fluoroquinolones',
    'amikacin': 'Amikacin',
    'capreomycin': 'Capreomycin',
    'kanamycin': 'Kanamycin',
    'para-aminosalicylic_acid': 'Para-aminosalicylic acid',
    'linezolid': 'Linezolid',
    'cycloserine': 'Cycloserine',
    'delaminid': 'Delaminid',
    'clofazimine': 'Clofazimine',
    'bedaquiline': 'Bedaquiline'
}


def get_tb_profiler_data(tbprofiler_report, variants):
    """Get TBProfiler data."""
    drug_resistance_list, drug_resistance = [], {}
    call_positions, dr_calls_seen = set(), set()
    rrs_start, rrs_end = 1471846, 1473382
    rrs_variant_count = 0
    for variant_record in variants:
        POS = int(variant_record[17])
        if POS >= rrs_start and POS <= rrs_end:
            rrs_variant_count += 1
        call_positions.add(POS)
    tbprofiler_data = json.load(tbprofiler_report)
    dr_data = tbprofiler_data['dr_variants']
    for record in dr_data:
        drug_name = record['drug']
        if record['genome_pos'] in dr_calls_seen:
            continue
        dr_calls_seen.add(record['genome_pos'])
        if drug_name not in drug_list:
            click.secho(f"Unknown drug: {drug_name}\n", fg='yellow')
            continue
        dr_record = drug_resistance.get(drug_name, {
            'drug': drug_name,
            'drug_human_name': drug_names[drug_name],
            'resistant': True,
            'snippy_agreement': True, 'variants': []})
        if record['genome_pos'] not in call_positions:
            dr_record['snippy_agreement'] = False
        dr_record['variants'].append((
            record['gene'], record['change'], round(record['freq'], 2)
        ))
        drug_resistance[drug_name] = dr_record
    for drug_name in drug_names:
        if drug_name in drug_resistance:
            drug_resistance_list.append(drug_resistance[drug_name])
        else:
            drug_resistance_list.append({
                'drug_name': drug_name,
                'drug_human_name': drug_names[drug_name],
                'resistant': False})
    return (drug_resistance_list, rrs_variant_count)

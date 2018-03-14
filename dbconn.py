from py2neo import Graph, watch

import configparser

watch('neo4j.bolt')

config = configparser.ConfigParser()
config.read('config.ini')

DB = config['DEFAULT']['DB']

graph = Graph(host=DB, bolt=True, password="")


def get_gene_data(q):
    # WHERE g.uniquename IN {q}
    # where_statement = "WHERE gene.name =~'(?i){0}.*' \
    # OR gene.uniquename=~'gene:(?i){0}.*'".format(q)
    where_statement = "WHERE gene.uniquename='gene:{0}'".format(q)
    try:

        data = graph.run(
            "MATCH (gene:Gene) {where_statement} "
            "OPTIONAL MATCH (protein:Protein)<-[:ENCODES]-(gene) "
            "OPTIONAL MATCH (pathway:Pathway)<-[:INVOLVED_IN]-(protein) "
            "RETURN gene, protein, "
            "collect(distinct(pathway)) as pathway "
            "order by gene.uniquename asc"
            .format(where_statement=where_statement)).data()
        if data:
            return data[0]
        else:
            return {}
    except Exception as e:
        raise e

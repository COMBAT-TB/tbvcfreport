"""
Interface to Graph Database
"""
import os

from py2neo import Graph


DB_HOST = os.environ.get("DATABASE_URI", "combattb.sanbi.ac.za")

graph = Graph(host=DB_HOST, bolt=True, http_port=7474, password="")


def get_gene_data(q):
    """
    Query DB
    :param q:
    :return:
    """
    # WHERE g.uniquename IN {q}
    # where_statement = "WHERE gene.name =~'(?i){0}.*' \
    # OR gene.uniquename=~'gene:(?i){0}.*'".format(q)
    where_statement = "WHERE gene.uniquename='{0}'".format(q)
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

"""Interface to Graph Database."""
import os

from py2neo import Graph

DB_HOST = os.environ.get("DATABASE_URI", "neodb.sanbi.ac.za")
SECURE = True if DB_HOST == "neodb.sanbi.ac.za" else os.environ.get(
    "SECURE", False)

graph = Graph(host=DB_HOST, password="", secure=SECURE)


def get_gene_data(q):
    """Query DB.

    :param q:
    :return:
    """
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


def query_by_gene_list(genes):
    """Query DB.

    :param genes: list
    :return:
    """
    where_statement = "WHERE gene.uniquename IN {0}".format(genes)
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
            return data
        else:
            return {}
    except Exception as e:
        raise e

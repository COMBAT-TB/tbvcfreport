"""Interface to Graph Database."""
from neo4j import GraphDatabase


class CombatTbDb:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    @staticmethod
    def _count_genes_tx(tx):
        result = tx.run("MATCH (g:Gene) return count(g)")
        return result.single()[0]

    def count_genes(self):
        with self.driver.session() as session:
            count = session.read_transaction(self._count_genes_tx)
        return count

    @staticmethod
    def _get_gene_table_tx(tx, genes=None):
        if not genes:
            where_clause = ""
        else:
            where_clause = "WHERE gene.uniquename IN {} ".format(genes)
        query = (
            "MATCH (gene:Gene) {} OPTIONAL MATCH (protein:Protein)<-[:ENCODES]-(gene) "
            "OPTIONAL MATCH (pathway:Pathway)<-[:INVOLVED_IN]-(protein) "
            "RETURN gene, protein, "
            "collect(distinct(pathway)) as pathway "
            "order by gene.uniquename asc"
        ).format(where_clause)
        result = tx.run(query)
        return result.values()

    def query_by_gene_list(self, gene_list):
        with self.driver.session() as session:
            values = session.read_transaction(self._get_gene_table_tx, gene_list)
        return values

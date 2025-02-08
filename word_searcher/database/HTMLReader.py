import os
from bs4 import BeautifulSoup
import pandas as pd
from word_searcher.database.DBConnector import DBConnector


class HTMLReader:
    def __init__(self, db_connector: DBConnector):
        self._db_connector = db_connector
        self._html_path = os.path.expanduser("word_searcher/raw_data/")
        self._exclusions = {" ", "-", "'", "/", "*", ":"}
        self.html_to_database()

    def html_to_database(self):

        file_list = self._get_all_html_files()
        master_definitions = list()

        for file_name in file_list:

            file_path = self._html_path + file_name
            soup = self._read_html_file(file_path)
            definitions = self._extract_definitions(soup)
            master_definitions.extend(definitions)

        master_definitions = list(set(master_definitions)) # remove all remaining dupes

        lengths = [len(w) for w in master_definitions]
        df = pd.DataFrame({"word": master_definitions, "length": lengths})
        self._create_dictionary_table(df)
        self._test_db_creation()

    def _get_all_html_files(self) -> list:
        all_files = os.listdir(self._html_path)
        htmls = list()

        for file in all_files:
            if file.endswith(".html"):
                htmls.append(file)

        return htmls

    @staticmethod
    def _read_html_file(file_path: os.path) -> BeautifulSoup:

        if not os.path.exists(file_path):
            raise KeyError(f"{file_path} not found")
        else:
            print(f"reading {file_path}...")

        with open(file_path, 'rb') as file:
            file_content = file.read()

        soup = BeautifulSoup(file_content)

        return soup

    def _extract_definitions(self, soup: BeautifulSoup) -> list:

        all_definitions = soup.body.find_all("b")
        definitions_to_keep = list()

        for definition in all_definitions:

            if set(definition.text).isdisjoint(self._exclusions):
                definitions_to_keep.append(definition.text)

        definitions_to_keep = list(set(definitions_to_keep))    # drop duplicates

        return definitions_to_keep

    def _create_dictionary_table(self, df: pd.DataFrame):

        query_cleanup = "DROP TABLE IF EXISTS dictionary"
        self._db_connector.execute_query(query_cleanup)

        query_table = "CREATE TABLE dictionary(word text, length integer)"
        self._db_connector.execute_query(query_table)

        conn = self._db_connector.create_sqa_connection()
        df.to_sql(name="dictionary", con=conn, if_exists="append", index=False)
        conn.dispose()

        query_index = "CREATE INDEX idx_dictionary_length on dictionary(length)"
        self._db_connector.execute_query(query_index)

    def _test_db_creation(self) -> None:

        query = "SELECT count(*), count(distinct length) from dictionary"

        print(self._db_connector.execute_query(query))



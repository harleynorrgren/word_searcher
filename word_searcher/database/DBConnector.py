from dotenv import load_dotenv
import os
import psycopg2
from sqlalchemy import create_engine
from word_searcher.user_input.QueryObject import QueryObject


class DBConnector:

    def __init__(self):
        self._db_creds = dict()
        self._set_db_creds()
        self._can_connect = False
        self.contains_dictionary_table = False
        self._test_connection()

    def execute_query(self, query: str) -> list:

        conn = None
        response = ["ERROR"]

        try:

            conn = self.create_connection()
            cur = conn.cursor()

            cur.execute(query)
            response = cur.fetchall()
            cur.close()

        except psycopg2.DatabaseError as error:
            print(error)

        finally:
            if conn is not None:
                conn.close()
                return response

    def create_connection(self):

        conn = psycopg2.connect(
            host=self._db_creds["host"],
            dbname=self._db_creds["dbname"],
            user=self._db_creds["user"],
            password=self._db_creds["password"],
            port=self._db_creds["port"]
        )
        return conn

    def _set_db_creds(self):
        load_dotenv()
        self._db_creds["host"] = os.getenv("DB_HOSTNAME")
        self._db_creds["dbname"] = os.getenv("DB_NAME")
        self._db_creds["user"] = os.getenv("DB_USERNAME")
        self._db_creds["password"] = os.getenv("DB_PASSWORD")
        self._db_creds["port"] = os.getenv("DB_PORT")

    def _test_connection(self) -> bool:
        query = "SELECT * FROM pg_catalog.pg_tables;"
        print("testing connection...")
        response = self.execute_query(query)
        self._check_dictionary_table(response)

        if response == ["ERROR"]:
            self._can_connect = False
            raise ValueError("Unable to connect to database")
        else:
            print("...OK!")
            self._can_connect = True
        return self._can_connect

    def _check_dictionary_table(self, table_list: list) -> bool:
        self.contains_dictionary_table = False

        for table in table_list:
            if table[1] == "dictionary":
                self.contains_dictionary_table = True

        return self.contains_dictionary_table

    def create_sqa_connection(self):
        conn_string = f"postgresql://{self._db_creds['user']}:{self._db_creds['password']}@{self._db_creds['host']}:{self._db_creds['port']}/{self._db_creds['dbname']}"
        engine = create_engine(conn_string)
        return engine

    def submit_query_object(self, query_object: QueryObject):

        query = query_object.get_query()
        result = self.execute_query(query)

        return result

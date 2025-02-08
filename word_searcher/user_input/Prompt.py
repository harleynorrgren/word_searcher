from word_searcher.database.DBConnector import DBConnector
from word_searcher.user_input.QueryObject import QueryObject


class Prompt:
    def __init__(self, db_connector: DBConnector):
        self._db_connector = db_connector
        self.prompt_for_input()

    def prompt_for_input(self):

        should_quit = False
        print("Enter your query below, type /q to quit")
        while not should_quit:
            user_query = input("Query: ")

            if user_query == "/q":
                should_quit = True
                print(f"Bye!")
                break

            else:
                print(f"Checking {user_query}")
                query_object = QueryObject(user_query)
                result = self._db_connector.submit_query_object(query_object)
                self._pretty_print_result(result)

    @staticmethod
    def _pretty_print_result(result: list) -> None:
        result_list = list()

        if len(result) > 0:
            print("Words Found:")

        for r in result:

            result_list.append(r[0])

        w = 0
        while w < len(result_list):
            end = min(w+5, len(result_list))
            print(", ".join(result_list[w:end]))
            w += 5

        print("\n")







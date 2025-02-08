from word_searcher.database.DBConnector import DBConnector
from word_searcher.database.HTMLReader import HTMLReader
from word_searcher.user_input.Prompt import Prompt

def main():

    db_connector = DBConnector()

    if not db_connector.contains_dictionary_table:
        print("Dictionary table not found, creating one")
        html_reader = HTMLReader(db_connector)

    prompt = Prompt(db_connector)





if __name__ == "__main__":
    main()

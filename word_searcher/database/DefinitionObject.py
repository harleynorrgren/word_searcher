class DefinitionObject:
    def __init__(self, definition: str):
        self.word = definition
        self.length = len(definition)

    def to_dict(self):
        return {

            "word": self.word,
            "length": self.length

        }
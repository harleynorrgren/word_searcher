

class QueryObject:

    def __init__(self, query_string: str):
        # example string: "5 .a.t. r1,f3 ghijk"
        self._query_string = query_string.lower()
        self.length = self.parse_length()
        self.known_positions = self.parse_known_positions()
        self.contains = self.parse_contains()
        self.excludes = self.parse_exclude()

    def get_query(self) -> str:
        query = f"""
            SELECT
                lower(word)
            from dictionary
            WHERE length = {self.length}
            {self.known_positions}
            {self.contains}
            {self.excludes}
        """

        return query

    def parse_length(self) -> int:
        try:
            length = self._query_string.split(" ")[0]
            length = int(length)

            return length

        except TypeError as error:
            raise TypeError(f"first argument must be an integer... {self._query_string}")

    def parse_known_positions(self) -> str:
        known = self._query_string.split(" ")[1]

        if len(known) != self.length:
            raise ValueError(f"word is {self.length} characters, you have provided {len(self._query_string)} known values")

        known_str = f"""
            AND lower(word) ~ '{known}'\n
        """
        return known_str

    def parse_contains(self) -> str:
        contains = self._query_string.split(" ")[2]

        if contains == ".":
            return ""

        contains = contains.split(",")

        query = ""

        for c in contains:
            try:
                char = c[0]
                position = int(c[1:])
                if position > self.length:
                    raise ValueError(f"provided positional indicator {position} is greater than word length {self.length}")

                regex = "." * self.length
                regex = list(regex)
                regex[position] = char
                regex = "".join(regex)

                query += f"AND lower(word) like '%{char}%'\n"
                query += f"AND lower(word) !~ '{regex}'\n"

            except TypeError as e:
                raise TypeError(f"positional argument for {char} is not an integer, you provided {position}")

        return query

    def parse_exclude(self) -> str:
        excludes = self._query_string.split(" ")
        query = ""
        if len(excludes) == 4:
            excludes = list(excludes[3])
            for e in excludes:
                query += f"AND lower(word) not like '%{e}%'\n"

        return query


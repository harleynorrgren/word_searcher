# Word Searcher

Love Wordles, Quordles, Octordles and Crypticles, but hate memorising the dictionary? 
Let's find those words...

## Initial Project Setup
* git clone from repo
* `pipx install poetry` if you don't have it already.
* `poetry install`

## DB Setup
* `brew install postgresql`
* `brew services start postgresql@14` N.B. do check your postgres version/launch instructions after brew install...
* `createdb dictionary`

### To Test:
* `psql -h localhost -d dictionary` to open postgres
* `\du+` to get your username
* `ALTER ROLE {YOUR USERNAME} PASSWORD '{NEW PASSWORD}'` to add a password
* `\q` to quit

### Connection Params
Add your connection params to a `.env` in your project root, the file should look like:
```
DB_HOSTNAME = "localhost"
DB_NAME = "dictionary"
DB_USERNAME = "{YOUR USERNAME}"
DB_PASSWORD = "{NEW PASSWORD}"
DB_PORT = "5432"
```

## Dictionary Data
Download and extract all `.html` files into the `raw_data` folder:
* https://www.mso.anu.edu.au/%7Eralph/OPTED/optedv003.hqx

# How to run
`poetry run python3 main.py`
With each run, the code will try to detect the dictionary database, and set it up if it's not found.

You will then be asked to enter a query which is specified as follows:

`{number of letters} {known positions} {letters contained} {exclusions}`

e.g. `5 .r... d2,n1 ghkl`

Where:
* Number of letters is an integer, e.g. `5`
* Known positions are letters for which you know the locations, specified as a `.` for any unknown positions and the actual letter for any known ones. For example if you know that the second letter is an r you would write `.r...`. The total number of characters here has to match the {number of letters} parameter.
* Letters contained are letters which you know are in the word, just not their positions. For example you tried the letter d in the third position but it was a partial match. These letters are specified as the letter and the position you tried it in (zero indexed), separated by commas like so: `d2,n1`.
* Exclusions are letters which you know *aren't* in the word, specified as a list of characters like `ghkl`.

Queries return all matches from the dictionary.


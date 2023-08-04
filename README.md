# JSON Lines Formatter

Simple tool to format [JSON Lines] files into pretty printed ones.

## Usage

```bash
# via Python
python -m jsonl_formatter file_1 [... file_N]

# via Docker
docker run -v $PWD:/mnt/pwd seznam/jsonl-formatter file_1 [... file_N]

# via hash-bang
./jsonl_formatter.py file_1 [... file_N]
```

### Input

```json lines
{"id": 1, "father": "Mark", "mother": "Charlotte", "children": ["Tom"]}
{"id": 2, "father": "John", "mother": "Ann", "children": ["Jessika", "Antony", "Jack"]}
{"id": 3, "father": "Bob", "mother": "Monika", "children": ["Jerry", "Karol"]}
```

### Output

```json lines
{"id": 1, "father": "Mark", "mother": "Charlotte", "children": ["Tom"]}
{"id": 2, "father": "John", "mother": "Ann",       "children": ["Jessika", "Antony", "Jack"]}
{"id": 3, "father": "Bob",  "mother": "Monika",    "children": ["Jerry",   "Karol"]}
```

## Installation (optional)

* Copy [`jsonl_formatter.py`](jsonl_formatter.py) into `$PYTHONPATH`,
* or make Docker `make docker` and create an alias for Docker `alias jsonl-formatter='docker run -v $PWD:/mnt/pwd seznam/jsonl-formatter'`,
* or create a symlink into `$PATH`, f.e. `sudo ln -s $PWD/jsonl_formatter.py /usr/local/bin/jsonl-formatter`.

## Contribution notes

Firstly, thanks for your interest!

We are using [Conventional Commits](https://conventionalcommits.org) (format of `category: message`), notably for generating changelogs.
Once your work is ready for merge, please rebase to latest version, as we strongly prefer to merge through fast-forward and keep the history clean.



[JSON Lines]:https://jsonlines.org/

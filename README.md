
1. fill env
2. Get chroma password by running `docker run --rm --entrypoint htpasswd httpd:2 -Bbn admin YOUR_PASSWORD > server.htpasswd`
3. `python src/database/init_rag.py`  for initting tables.

## load data to db
```
from database.fragments_db import load_fragments
from database.text_processor import split_into_fragments
fragments = split_into_fragments(data_path=path_project / "data/official_rules_fsm.pdf")
load_fragments(fragments)
```
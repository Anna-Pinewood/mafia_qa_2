
1. fill env
2. Get chroma password by running `docker run --rm --entrypoint htpasswd httpd:2 -Bbn admin YOUR_PASSWORD > server.htpasswd`
3. `python src/database/init_rag.py`  for initting tables.
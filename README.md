# zotero-google-scholar

a command line utility to add Google Scholar URL shortcuts to Zotero entries

## usage

```bash
$ uv run zotero-google-scholar print-collections
"4S6WU66T",  # "prompt optimization"
"78XST3VM",  # "compound AI systems"
"CSVC5D43",  # "single cell datasets"
"WCNJRL6T",  # "diffusion models"
...
```

```
$ uv run zotero-google-scholar add-google-scholar-links 4S6WU66T
...
2025-06-26 14:59:39,955 - zotero_google_scholar.core - INFO - processing item NQ8T4J6Z
2025-06-26 14:59:40,393 - httpx - INFO - HTTP Request: GET https://api.zotero.org/users/5539253/items/NQ8T4J6Z/children?locale=en-US&format=json&limit=100 "HTTP/1.1 200 OK"
2025-06-26 14:59:40,393 - zotero_google_scholar.core - INFO - adding google scholar link, url: https://scholar.google.com/scholar?q=DSPy%3A+Compiling+Declarative+Language+Model+Calls+into+State-of-the-Art+Pipelines+
2025-06-26 14:59:40,844 - httpx - INFO - HTTP Request: POST https://api.zotero.org/users/5539253/items "HTTP/1.1 200 OK"

```

## setup

### 1. get a zotero API key

first, set up a zotero API key at https://www.zotero.org/settings/keys.

### 2. set env vars

second, environment variables in one of two ways:

1. in a `.env` file (see `.env.template`; `cp .env.template .env` and edit accordingly)
2. manually:

```
export ZOTERO_API_KEY=""
export ZOTERO_LIBRARY_ID=""
```

### 3. install

```bash
uv sync
```

# rag — Page-cited search over PDF documents

**Purpose:** turn requirement documents, specifications and vendor guides into text that can be searched
and cited by page, so analysis quotes the source instead of guessing.
**Cost:** zero. No embeddings, no vector database, no network, no API calls. Regex retrieval over extracted
text is enough for a few thousand pages.
**Dependencies:** `pypdf` for `extract.py` (`tools/requirements.txt`). `query.py` is standard library only.

---

## 1. Use

```powershell
# Extract one PDF, or every PDF under a folder. Output defaults to .tmp\rag-corpus\ (gitignored).
python tools\rag\extract.py "New Task\Current Project\requirements.pdf"
python tools\rag\extract.py "New Task\Current Project" --noise "^\s*Acme Corp Confidential\s*$"

# Query it
python tools\rag\query.py docs                                   # what is in the corpus
python tools\rag\query.py find "session timeout"                 # ranked pages containing all terms
python tools\rag\query.py find "api user" --doc admin-guide      # one document only
python tools\rag\query.py page admin-guide 63-67                 # print a page range
python tools\rag\query.py toc admin-guide --level 2 --grep api   # filtered heading index
```

`--noise` takes a regex for whole lines to drop, such as a header or footer repeated on every page. The
default drops only `Page N of M` and bare page numbers.

## 2. What it writes

| File | Holds |
|---|---|
| `<slug>.md` | Full text with one `## [p<N>]` marker per page. Greppable, and the marker gives the page |
| `<slug>.headings.tsv` | Detected headings: page, level, text. The cheap way into a long document |
| `corpus.jsonl` | One `{"doc","page","text"}` object per page, for every PDF in the run |

The slug is the file name, lower-cased, with non-alphanumerics turned into `-`. `corpus.jsonl` holds only
the PDFs named in the current run, so pass every document you want searchable in one run.

## 3. Rules

- **Cite every fact as `<doc>:p<N>`**, for example `admin-guide:p63`. It maps to the printed page, so a
  reviewer can check it in seconds.
- ⛔ **Never read a large extracted `.md` linearly.** A read returns the first 2,000 lines with no error, so a
  truncated read looks complete. Check `wc -l` first, then use `query.py` or `.headings.tsv` to jump to
  the pages you need.
- The corpus is an intermediate, not a deliverable. It lives in `.tmp/` and is rebuilt from the PDFs.

## 4. Known extraction limits

- Text inside screenshots is not extracted. Such pages read `_(no extractable text - likely a screenshot)_`.
- Numbered and bulleted list markers can extract as orphaned `1.` or `•` lines ahead of their content.
- Table cells extract in reading order: readable, but not machine-parseable as a table.
- Heading detection is a heuristic (short, capitalised, unpunctuated lines). Treat the index as a map, not
  as the document's real outline.

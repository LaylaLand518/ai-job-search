"""
upload_pdf.py — inject a local PDF into a browser file input without a file picker.

Approach: split the base64 into ~40 KB chunks, append each to window.__pdfUpload
in separate JS calls, then materialise the File in a final call.
This keeps every individual JS call well under transport limits.

API
---
get_upload_chunks(pdf_path, var="__pdfUpload")
    → list[str]   # JS snippets to run IN ORDER via javascript_tool

get_commit_js(filename, input_index=0, var="__pdfUpload")
    → str         # final JS to run after all chunks; creates the File and sets input.files

get_upload_chunks_pair(cv_path, cl_path=None)
    → list[str]   # all chunks + commit calls for CV (index 1) and optional CL (index 2)

Standalone
----------
python upload_pdf.py cv/Liu_XXX_CV.pdf [cover_letters/Liu_XXX_CL.pdf]
  → prints JSON list of JS snippets to execute in order
"""

from __future__ import annotations
import base64
import json
import sys
from pathlib import Path

CHUNK_SIZE = 4_000    # characters per JS append call — kept small so Read tool can read each file


def _b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def get_upload_chunks(pdf_path: str, var: str = "__pdfUpload") -> list[str]:
    """Return JS snippets that accumulate the base64 in window[var]."""
    b64 = _b64(Path(pdf_path))
    chunks = [b64[i:i + CHUNK_SIZE] for i in range(0, len(b64), CHUNK_SIZE)]
    snippets: list[str] = []

    # Init
    snippets.append(f"window['{var}'] = ''; 'init {Path(pdf_path).name}'")

    # Append chunks
    for i, chunk in enumerate(chunks):
        snippets.append(f"window['{var}'] += '{chunk}'; 'chunk {i+1}/{len(chunks)}'")

    return snippets


def get_commit_js(filename: str, input_index: int = 0, var: str = "__pdfUpload") -> str:
    """Return JS that turns window[var] into a File and sets it on the Nth file input."""
    return f"""(function() {{
  const b64 = window['{var}'];
  if (!b64) return 'ERROR: {var} is empty — did all chunks run?';
  const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  const file = new File([bytes], '{filename}', {{type:'application/pdf'}});
  const dt = new DataTransfer();
  dt.items.add(file);
  const inputs = document.querySelectorAll('input[type="file"]');
  const input = inputs[{input_index}];
  if (!input) return 'INPUT NOT FOUND at index {input_index} (found ' + inputs.length + ')';
  input.files = dt.files;
  const nativeEvt = new Event('change', {{bubbles: true}});
  input.dispatchEvent(nativeEvt);
  // React fiber — call onChange with a full SyntheticEvent-like object
  const fk = Object.keys(input).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
  if (fk) {{
    let f = input[fk];
    while (f) {{
      const p = f.memoizedProps || f.pendingProps;
      if (p && p.onChange) {{
        p.onChange({{
          target: input, currentTarget: input,
          type: 'change', nativeEvent: nativeEvt,
          preventDefault: ()=>{{}}, stopPropagation: ()=>{{}},
          isPropagationStopped: ()=>false, isDefaultPrevented: ()=>false,
          persist: ()=>{{}}
        }});
        break;
      }}
      f = f.return;
    }}
  }}
  delete window['{var}'];
  return 'Uploaded [{input_index}]: {filename} (' + (bytes.length/1024).toFixed(1) + ' KB)';
}})()"""


def get_upload_chunks_pair(
    cv_path: str,
    cl_path: str | None = None,
) -> list[str]:
    """Return all JS snippets to upload CV (input index 1) and optional cover letter (index 2).

    Ashby file input layout:
      index 0 — hidden autofill-from-resume input (skip)
      index 1 — Resume / CV
      index 2 — Cover Letter (when present)
    """
    cv = Path(cv_path)
    snippets: list[str] = []

    snippets += get_upload_chunks(str(cv), var="__cvUpload")
    snippets.append(get_commit_js(cv.name, input_index=1, var="__cvUpload"))

    if cl_path:
        cl = Path(cl_path)
        if cl.exists():
            snippets += get_upload_chunks(str(cl), var="__clUpload")
            snippets.append(get_commit_js(cl.name, input_index=2, var="__clUpload"))

    return snippets


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    args = sys.argv[1:]
    cl = args[1] if len(args) >= 2 and args[1].endswith(".pdf") else None
    snippets = get_upload_chunks_pair(args[0], cl)
    print(json.dumps(snippets, indent=2))
    print(f"\n# {len(snippets)} JS calls total", file=sys.stderr)

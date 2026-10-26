# Current report build and render

`../README.md` is the editorial source. Preserve it; `complete_rubric.py` rebuilds from an older academic baseline and must not be used to reset this report. The catalog contains20 use cases; the separate delivery16 crosswalk and historical academic34 crosswalk have different purposes.

Use the bundled document Python and Node runtimes located by the Codex workspace dependency loader. On this workstation their prefix is `/Users/manus/.cache/codex-runtimes/codex-primary-runtime/dependencies`. Node diagram tools require `NODE_PATH=$prefix/node/node_modules`. Run from repository root:

```sh
"$prefix/python/bin/python3" docs/sa-report/refresh_current20_model.py
NODE_PATH="$prefix/node/node_modules" "$prefix/node/bin/node" docs/sa-report/render_current20_model.cjs
NODE_PATH="$prefix/node/node_modules" "$prefix/node/bin/node" docs/sa-report/render_state.cjs
"$prefix/python/bin/python3" docs/sa-report/render_business_process.py
"$prefix/python/bin/python3" docs/sa-report/sequence-diagrams/render.py
"$prefix/python/bin/python3" docs/sa-report/collaboration-diagrams/render.py
"$prefix/python/bin/python3" docs/sa-report/verify_structure.py
"$prefix/python/bin/python3" docs/sa-report/build_report.py
```

The current model metadata comes from the read-only disposable-stack query `sql/verify-current20-model.ts`. It verifies39 tables,91 foreign keys,25 enums and7 migrations. Partial unique indexes constrain only qualifying rows. Payroll payment history is1:N; the prepared/paid predicate permits at most one active payment per payroll record. Protected sample values are redacted, and empty tables retain honest empty evidence.

Render with the documents skill's `render_docx.py`, approved bundled headless LibreOffice override, and the published fontconfig file. The first render without explicit font discovery showed blank Thai body text. The following environment fixed the diagnostic and report; do not use desktop LibreOffice or claim that the first render passed:

```sh
export PATH="$prefix/bin/override:$PATH"
export FONTCONFIG_FILE="$PWD/docs/sa-report/evidence/haris-fonts.conf"
export SAL_FONTPATH=/System/Library/Fonts/Supplemental
"$prefix/python/bin/python3" "$documents_skill/render_docx.py" docs/sa-report/Haris-SA-Report.docx --output_dir "$render_dir" --emit_pdf
"$prefix/python/bin/python3" docs/sa-report/refresh_page_refs.py --pdf "$render_dir/Haris-SA-Report.pdf"
# Render again after updating cached page references; inspect every final page.
```

The fontconfig file is a workstation recipe; on another workstation resolve installed fonts and bundled runtime locations explicitly. It writes only a private temporary font cache. The document retains the existing Tahoma template. The final PDF must come from the final font-correct render after cached page references are verified. Raw browser traces, fixture credentials and bank exports stay in ignored evidence directories. Publication files are enumerated explicitly in the Task4 curated manifest.

# Cabo Verde (CV) — legislação em Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

**Partial repository.** Legislation of the Republic of Cabo Verde, in Portuguese, as offered for download by the
**Tribunal Constitucional** (Constitutional Court) in the "Legislação" section of its website: the Constitution
(2010 revision), the main codes (Civil, Civil Procedure, Penal, Criminal Procedure, Administrative Procedure), and
laws on the Constitutional Court, the referendum, political parties and the judicial organisation.

Retrieved 2026-10-13.

<!-- COUNTS -->
| Directory | Files |
|---|---|
| `codigos/` | 5 |
| `constituicao/` | 1 |
| `leis-organicas/` | 6 |
| `leis/` | 6 |
| **Total** | **18** |
<!-- /COUNTS -->

## Structure

```
constituicao/constituicao-2010.md   Lei Constitucional n.º 1/VII/2010 (3rd revision of the 1992 Constitution) with the
                                    republished text of the Constitution (Boletim Oficial, I Série, n.º 17, 3 May 2010)
codigos/                            codes (as given by the Court: some files are amending acts, e.g. "Código Penal — 4.ª e 5.ª alterações")
leis/                               laws on the Constitutional Court, referendum, political parties...
leis-organicas/                     organic laws of the courts and the Public Prosecutor's Office
```

File names follow the titles given by the Court. Front matter: `source` = download URL; `record` = listing page;
`status: unknown` except for the Constitution. The PDFs are Boletim Oficial pages laid out in two columns, split
automatically (column order errors are possible; running headers may remain).

## Source

| Source | URL |
|---|---|
| Tribunal Constitucional — Leis Constitucionais | https://www.tribunalconstitucional.cv/index.php/leis-constitucionais/ |
| Tribunal Constitucional — Legislação (Tribunal Constitucional) | https://www.tribunalconstitucional.cv/index.php/tribunal-constitucional/ |
| Tribunal Constitucional — Legislação complementar (Códigos, Orgânicas) | https://www.tribunalconstitucional.cv/index.php/complementar/ |

## Not covered / known gaps

* **No general collection of laws.** The official *Boletim Oficial* is sold/distributed by the Imprensa Nacional
  (incv.cv; its kiosk kiosk.incv.cv did not answer); the Parliament website (parlamento.cv) did not answer. The
  Legis-PALOP+TL database requires a paid subscription for full texts and its terms grant only a personal,
  non-transferable licence: not used.
* Skipped because the PDFs are scans without a usable text layer: Recurso de Amparo e de Habeas Data, Regime do
  Controlo Público da Riqueza dos Titulares de Cargos Políticos, Código Eleitoral (2010 version), Orgânica do
  Tribunal Fiscal e Aduaneiro, Orgânica do Tribunal Militar de Instância.
* Historical constitutional laws (1975–1999) and the Assembly's booklet edition of the Constitution are not
  included (the Boletim Oficial 2010 text is used).

## Copyright

Official texts of the Republic of Cabo Verde, published in the Boletim Oficial and made available by the
Constitutional Court without stated reuse restrictions; official legislative texts are generally not subject to
copyright. The Markdown conversion is provided as is; the authoritative text is the one published in the
*Boletim Oficial*.

## Regenerating

```sh
python3 scripts/cv_fetch.py    # downloads to ../_raw/cv/ (3 s between requests) and writes the Markdown
python3 scripts/cv_readme.py   # updates the counts table
```

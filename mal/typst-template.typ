// =============================================================================
// mal/typst-template.typ — dokumentmal for bostøtte-prognoseprosjektet
//
// Erstatter Quartos standardmal for typst-formatet (template-partials i YAML).
// Signaturen til article() er uendret, slik at Quartos typst-show.typ kaller
// den uten tilpasning; alt som er endret, er utseendet.
//
// Designvalg og begrunnelse:
//   * Bare fonter Typst har innebygd. Da ser PDF-en identisk ut på Windows,
//     macOS og i CI-container, og byggeloggen er fri for font-advarsler.
//     Hierarkiet i overskriftene lages med grad og vekt, ikke med fontbytte.
//   * Tabeller settes etter booktabs-prinsippet: linje over, linje under
//     hodet, linje under tabellen. Ingen vertikale streker og ingen
//     heldekkende rutenett: de bærer ingen informasjon og gjør brede tabeller
//     uleselige (jf. den forrige versjonen av dette dokumentet).
//   * Tall settes med tabularfigurer slik at sifrene flukter i kolonner.
//   * Ingenting i malen er tidsavhengig, slik at to renderinger av samme
//     kildefil gir identisk PDF.
// =============================================================================

// Kun fonter Typst har innebygd ("typst fonts --ignore-system-fonts" gir
// nøyaktig disse fire familiene). Det gir to ting en fontstabel ikke gir:
// identisk PDF på enhver maskin — Windows, macOS, CI-container — og null
// «unknown font family»-advarsler i byggeloggen.
#let brodfont   = "Libertinus Serif"
#let tittelfont = "Libertinus Serif"
#let kodefont   = "DejaVu Sans Mono"

#let aksent = rgb("#00505c")
#let grumt  = rgb("#5b646d")
#let linje  = rgb("#a3abb2")

#let article(
  title: none,
  subtitle: none,
  authors: none,
  date: none,
  abstract: none,
  abstract-title: none,
  cols: 1,
  margin: (top: 2.6cm, bottom: 2.4cm, left: 2.7cm, right: 2.7cm),
  paper: "a4",
  lang: "nb",
  region: "NO",
  font: brodfont,
  fontsize: 10.5pt,
  title-size: 21pt,
  subtitle-size: 13pt,
  heading-family: tittelfont,
  heading-weight: "bold",
  heading-style: "normal",
  heading-color: black,
  heading-line-height: 0.65em,
  sectionnumbering: none,
  pagenumbering: "1",
  toc: false,
  toc_title: none,
  toc_depth: none,
  toc_indent: 1.2em,
  doc,
) = {

  // --- Side ------------------------------------------------------------------
  set page(
    paper: paper,
    margin: margin,
    numbering: pagenumbering,
    number-align: center,
    header: context {
      // Ingen kolumnetittel på tittelside og innholdsside.
      if counter(page).get().first() > 2 {
        set text(size: 8.5pt, font: tittelfont, fill: grumt)
        if title != none { title }
        v(-7pt)
        line(length: 100%, stroke: 0.4pt + linje)
      }
    },
  )

  // --- Tekst -----------------------------------------------------------------
  set text(
    lang: lang,
    region: region,
    font: font,
    size: fontsize,
    hyphenate: true,
    number-type: "lining",
  )
  set par(justify: true, leading: 0.66em, spacing: 0.95em)

  // --- Overskrifter ----------------------------------------------------------
  set heading(numbering: sectionnumbering)
  show heading: set text(font: heading-family, fill: heading-color)
  show heading: set block(breakable: false)
  // Nytt kapittel starter på ny side. Vilkåret på numbering skiller
  // brødtekstens kapitler fra unummererte overskrifter som «Referanser»:
  // Quarto pakker dem i et block, og pagebreak er ulovlig inne i et block.
  show heading.where(level: 1): it => {
    if it.numbering != none { pagebreak(weak: true) }
    block(above: 0.2em, below: 1em, width: 100%)[
      #set text(size: 18pt, weight: "bold")
      #it
    ]
  }
  show heading.where(level: 2): it => block(above: 1.6em, below: 0.7em)[
    #set text(size: 12.5pt, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => block(above: 1.25em, below: 0.5em)[
    #set text(size: 10.8pt, weight: "bold")
    #it
  ]
  show heading.where(level: 4): it => block(above: 1em, below: 0.4em)[
    #set text(size: 10.5pt, weight: "regular", style: "italic")
    #it
  ]

  // --- Tabeller: booktabs ----------------------------------------------------
  // Quarto legger selv inn table.hline() under table.header(); malen tegner
  // linjen over og under tabellen, og fjerner alt annet strekverk.
  set table(inset: (x: 5pt, y: 3.2pt), stroke: none, align: left + top)
  show table: it => block(
    width: 100%,
    stroke: (top: 0.9pt + black, bottom: 0.9pt + black),
    inset: (top: 4pt, bottom: 4pt),
  )[
    // Ingen orddeling i tabeller: celletekst er korte merkelapper, og
    // «Sta-tus» over to linjer i en smal kolonne ser ut som en feil.
    #set text(size: 8.7pt, number-width: "tabular", hyphenate: false)
    #set par(justify: false, leading: 0.5em)
    #it
  ]
  show table.cell.where(y: 0): set text(weight: "bold")

  // --- Figur- og tabelltekster ----------------------------------------------
  show figure.caption: it => block(width: 100%, above: 0.6em, below: 0.6em)[
    #set align(left)
    #set text(size: 8.5pt, fill: grumt)
    #set par(justify: false, leading: 0.52em, hanging-indent: 0pt)
    #text(weight: "bold", fill: black, font: tittelfont)[
      #it.supplement #context it.counter.display(it.numbering)#it.separator
    ]#it.body
  ]
  // Lange tabeller får brekke over sidegrensen. Uten dette skyves en tabell som
  // ikke får plass, i sin helhet til neste side og etterlater en halvtom side.
  // Typst gjentar table.header() automatisk på ny side.
  show figure: set block(above: 1.5em, below: 1.5em, breakable: true)

  // --- Kode ------------------------------------------------------------------
  show raw: set text(font: kodefont, size: 8.5pt)
  show raw.where(block: true): it => block(
    width: 100%, fill: rgb("#f6f7f8"), inset: 8pt, radius: 2pt,
    stroke: 0.4pt + rgb("#e2e5e8"),
  )[#it]

  // --- Lenker og kryssreferanser --------------------------------------------
  show link: set text(fill: aksent)
  show ref: set text(fill: aksent)

  set math.equation(numbering: "(1)", supplement: none)

  // --- Tittelside ------------------------------------------------------------
  if title != none {
    v(4.5cm)
    block(width: 100%)[
      #set text(font: heading-family)
      #line(length: 36%, stroke: 2pt + aksent)
      #v(0.6em)
      #text(size: title-size, weight: "bold")[#title]
      #if subtitle != none {
        linebreak()
        v(0.3em)
        text(size: subtitle-size, weight: "regular", fill: grumt)[#subtitle]
      }
    ]
    v(1.3cm)
    if authors != none {
      set text(font: heading-family, size: 10.5pt)
      for a in authors {
        block(spacing: 0.4em)[#a.name]
        if a.affiliation != [] { block(spacing: 0.4em)[#text(fill: grumt)[#a.affiliation]] }
      }
    }
    if date != none {
      v(0.4em)
      text(font: heading-family, size: 10pt, fill: grumt)[#date]
    }
    if abstract != none {
      v(1.6cm)
      block(width: 90%)[
        #text(font: heading-family, size: 9.5pt, weight: "bold")[#abstract-title]
        #v(0.35em)
        #set text(size: 9.8pt)
        #abstract
      ]
    }
    pagebreak()
  }

  // --- Innholdsfortegnelse ---------------------------------------------------
  // Tittelen settes manuelt, ikke via outline(title: …): en outline-tittel er
  // en heading, og heading-regelen over inneholder pagebreak(), som Typst ikke
  // tillater inne i et block.
  if toc {
    if toc_title != none {
      block(above: 0em, below: 0.9em)[
        #set text(font: tittelfont, size: 15pt, weight: "bold")
        #toc_title
      ]
    }
    show outline.entry.where(level: 1): it => {
      v(9pt, weak: true)
      set text(font: tittelfont, weight: "bold", size: 10pt)
      it
    }
    show outline.entry: set text(font: tittelfont, size: 9.5pt)
    block(above: 0em, below: 2em)[
      #outline(title: none, depth: toc_depth, indent: toc_indent)
    ]
    pagebreak(weak: true)
  }

  if cols == 1 { doc } else { columns(cols, doc) }
}

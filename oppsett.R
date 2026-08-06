# =============================================================================
# oppsett.R — installerer det bostotte_oslo.qmd trenger, og sier fra hva som mangler
#
# Kjør denne ÉN gang før første render:
#     source("oppsett.R")
#
# Skriptet installerer bare det som faktisk mangler, og rapporterer til slutt
# om miljøet er klart. Det installerer ingenting uten å si hva og hvorfor.
# =============================================================================

PAKKER <- c(
  # kjerne
  "tidyverse",      # dplyr, ggplot2, purrr, tidyr, stringr, lubridate, readr
  "knitr",          # tabeller og chunk-motor
  "rmarkdown",      # kreves av Quarto for R-chunks
  # tidsserier
  "tsibble",        # tidsserie-tabeller
  "fable",          # ARIMA, ETS, naive-modeller
  "fabletools",     # modell-, prognose- og evalueringsrammeverk
  "feasts",         # seriediagnostikk (STL, enhetsrot, ACF)
  "urca",           # enhetsrottester (KPSS)
  "distributional"  # prediktive fordelinger
)

cat("Sjekker miljøet for bostotte_oslo.qmd\n")
cat(strrep("-", 62), "\n")
cat("R-versjon:", R.version.string, "\n")
if (getRversion() < "4.1.0") {
  cat("  ADVARSEL: dokumentet bruker \\(x)-lambdasyntaks og krever R >= 4.1.\n")
}

installert <- rownames(installed.packages())
mangler <- setdiff(PAKKER, installert)

if (length(mangler) == 0) {
  cat("Alle", length(PAKKER), "pakker er allerede installert.\n")
} else {
  cat("Mangler", length(mangler), "pakker:", paste(mangler, collapse = ", "), "\n")
  cat("Installerer nå. Dette kan ta noen minutter første gang.\n\n")
  install.packages(mangler)
  fortsatt <- setdiff(PAKKER, rownames(installed.packages()))
  if (length(fortsatt)) {
    cat("\nKLARTE IKKE å installere:", paste(fortsatt, collapse = ", "), "\n")
    cat("Prøv å installere dem enkeltvis for å se feilmeldingen:\n")
    cat("  install.packages(\"", fortsatt[1], "\")\n", sep = "")
  } else {
    cat("\nAlle pakker installert.\n")
  }
}

cat(strrep("-", 62), "\n")

# --- Kan pakkene faktisk lastes? -------------------------------------------
lastefeil <- character()
for (p in PAKKER) {
  if (!suppressWarnings(suppressPackageStartupMessages(
        requireNamespace(p, quietly = TRUE)))) lastefeil <- c(lastefeil, p)
}
if (length(lastefeil)) {
  cat("Installert, men lar seg ikke laste:", paste(lastefeil, collapse = ", "), "\n")
  cat("Start R på nytt og kjør source(\"oppsett.R\") igjen.\n")
} else {
  cat("Alle pakker lar seg laste.\n")
}

# --- Ligger filene der de skal? --------------------------------------------
cat(strrep("-", 62), "\n")
noedvendig <- c("bostotte_oslo.qmd", "referanser.bib", "mal/typst-template.typ",
                "velferdsetaten-data/scripts/velferdsetaten_data.R")
for (f in noedvendig) {
  cat(if (file.exists(f)) "  OK      " else "  MANGLER ", f, "\n", sep = "")
}
if (!file.exists("bostotte_oslo.qmd")) {
  cat("\n  Du står i feil mappe. Åpne Velferdsprosjekt.Rproj først,\n")
  cat("  eller sett arbeidsmappe med setwd() til repo-roten.\n")
  cat("  Nåværende mappe:", getwd(), "\n")
}

# --- Laster datapakken? ----------------------------------------------------
cat(strrep("-", 62), "\n")
if (file.exists("velferdsetaten-data/scripts/velferdsetaten_data.R")) {
  ok <- tryCatch({
    suppressPackageStartupMessages(source("velferdsetaten-data/scripts/velferdsetaten_data.R"))
    d <- last_alt("velferdsetaten-data")
    cat("Datapakken lastet:", length(d), "objekter,",
        format(nrow(d$oslo)), "månedsrader i Oslo-serien.\n")
    TRUE
  }, error = function(e) { cat("Datapakken feilet:\n  ", conditionMessage(e), "\n"); FALSE })
} else ok <- FALSE

# --- Quarto ----------------------------------------------------------------
cat(strrep("-", 62), "\n")
q <- tryCatch(system("quarto --version", intern = TRUE), error = function(e) NA)
if (all(is.na(q))) {
  cat("Fant ikke quarto på kommandolinjen.\n")
  cat("RStudio har egen innebygd Quarto — bruk Render-knappen i stedet for terminalen.\n")
} else {
  cat("Quarto:", q[1], "\n")
  if (package_version(q[1]) < "1.7.0") cat("  ADVARSEL: dokumentet er testet mot Quarto 1.7 eller nyere.\n")
}

cat(strrep("-", 62), "\n")
if (length(lastefeil) == 0 && ok) {
  cat("Klart. Render med Render-knappen i RStudio, eller:\n")
  cat("  quarto render bostotte_oslo.qmd\n")
  cat("Første kjøring tar rundt ti minutter. La den bli ferdig.\n")
} else {
  cat("Ikke klart ennå — se meldingene over.\n")
}

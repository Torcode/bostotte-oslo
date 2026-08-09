#| include: false

# =============================================================================
# Oppsett. Én chunk laster miljøet, datapakken og de avledede størrelsene som
# resten av dokumentet — inkludert løpende tekst — refererer til. Ingen tall i
# dette dokumentet er skrevet av for hånd; alle kommer herfra eller fra en
# chunk lenger nede, slik at teksten ikke kan komme i utakt med datapakken.
# =============================================================================

# Sjekk avhengigheter først, med en melding som sier hva som mangler og hva som
# fikser det. Uten dette feiler dokumentet nedstrøms med «could not find
# function \"ARIMA\"», som ikke forteller noen hva de skal gjøre.
.pakker <- c("tidyverse", "knitr", "tsibble", "fable", "fabletools",
             "feasts", "urca", "distributional")
.mangler <- .pakker[!vapply(.pakker, requireNamespace, logical(1), quietly = TRUE)]
if (length(.mangler)) {
  stop("\n\nManglende R-pakker: ", paste(.mangler, collapse = ", "),
       "\n\nKjør source(\"oppsett.R\") i repo-roten, eller:\n  install.packages(c(",
       paste0('\"', .mangler, '\"', collapse = ", "), "))\n", call. = FALSE)
}

suppressPackageStartupMessages({
  library(tidyverse)
  library(knitr)
  library(tsibble)
  library(fable)
  library(fabletools)
  library(feasts)
  library(urca)
  library(distributional)
})

knitr::opts_chunk$set(
  echo = FALSE, message = FALSE, warning = FALSE,
  fig.align = "center", dev = "svg"
)

# --- UTF-8 uavhengig av vertsmaskin ------------------------------------------
# Uten UTF-8 som native encoding konverterer R hver ikke-ASCII-streng til
# vertens tegnsett på vei ut, og skriver <U+00E5> der det skulle stått å. Da
# blir både tabeller og løpende tall uleselige. Locale-navnene er ulike på
# Unix og Windows, så vi prøver begge familier.
#
# Vakten STOPPER dersom UTF-8 ikke lar seg sette. Den forrige versjonen lot
# dokumentet fortsette, og produserte en PDF der hvert tusenskille sto som
# <U+00A0>. En vakt som ikke stopper er ingen vakt.
# Vi tester symptomet, ikke navnet paa locale: taaler en norsk bokstav og et
# hardt mellomrom en tur gjennom vertens tegnsett uten aa bli escape't? Det er
# noeyaktig det som avgjoer om PDF-en blir lesbar.
.tegnsett_ok <- function() {
  s <- "\u00e5\u00a0"
  !grepl("<U+", enc2native(s), fixed = TRUE)
}
if (!.tegnsett_ok()) {
  for (loc in c("nb_NO.UTF-8", "nb_NO.utf8",                   # Unix
                "Norwegian Bokmal_Norway.utf8",                # Windows
                "Norwegian_Norway.utf8", "Norwegian.utf8",
                "English_United States.utf8",
                "C.UTF-8", "C.utf8", "en_US.UTF-8")) {
    if (.tegnsett_ok()) break
    suppressWarnings(try(Sys.setlocale("LC_ALL", loc), silent = TRUE))
  }
}
if (!.tegnsett_ok()) {
  stop("\n\nR kjorer ikke med UTF-8 som tegnsett (locale: ",
       Sys.getlocale("LC_CTYPE"), ").",
       "\nDokumentet inneholder norske tegn, og uten UTF-8 skriver R dem",
       "\nsom <U+00E5> i tabeller og som <U+00A0> i hvert tusenskille.",
       "\nPDF-en ville blitt bygget, men vart uleselig.",
       "\n\nWindows: Innstillinger > Tid og sprak > Sprak >",
       "\n  Administrative sprakinnstillinger > Endre systemets",
       "\n  omradeinnstilling > kryss av for \"Beta: Bruk Unicode UTF-8\",",
       "\n  og start maskinen pa nytt.",
       "\nUnix: start R med LANG=nb_NO.UTF-8 eller LANG=C.UTF-8.",
       "\n\nRepoets .Rprofile forsoker dette automatisk ved oppstart. Slar",
       "\ndet feil, er det systeminnstillingen over som ma endres.\n",
       call. = FALSE)
}

# --- Formatering: norske tallkonvensjoner ------------------------------------
# Tusenskille er hardt mellomrom (U+00A0) slik at 20 849 ikke brekker over to
# linjer. Tegnet skrives som R-escape, ikke som byte i kildefila: en literal
# U+00A0 i koden gir en streng R kan komme til å escape'e på vei ut, og da
# står det <U+00A0> i PDF-en i stedet for et mellomrom.
NBSP <- "\u00a0"

# Ikke-endelige tall stopper byggingen framfor å bli trykt. Bakgrunnen er
# konkret: en 0/0 i sanntidskanten sto som NaN i løpende tekst i en tidligere
# PDF. Ni regnskapsidentiteter stoppet byggingen, men ingen av dem så på et
# enkelt inline-tall. Nå gjør formateringsfunksjonen selv den kontrollen.
#
# Aksemerker er unntaket, og det er et ekte unntak, ikke en lettvinthet:
# ggplot2 kaller merkefunksjonen med kandidatbrudd som kan ligge utenfor
# skalaen, og gir da NA med vilje. Derfor har akser sin egen tolerante
# formatering, `nb_akse()`, mens alt som havner i brødtekst og tabeller går
# gjennom den strenge. Skillet er poenget: en NA i en akse er normal, en NA i
# en setning er en feil.
.endelig <- function(x, hvor) {
  if (!all(is.finite(x)))
    stop("\n\n", hvor, "(): fikk en verdi som ikke er et tall: ",
         paste(utils::head(x[!is.finite(x)], 3), collapse = ", "),
         "\nEt tall i teksten er NA, NaN eller Inf. Rett kilden framfor",
         "\na trykke det.\n", call. = FALSE)
  invisible(TRUE)
}
nb_akse <- function(x, d = 0) {
  ut <- rep(NA_character_, length(x))
  e  <- is.finite(x)
  ut[e] <- formatC(x[e], format = "f", digits = d,
                   big.mark = NBSP, decimal.mark = ",")
  ut
}
pst_akse <- function(x, d = 0) {
  ut <- nb_akse(x, d)
  ifelse(is.na(ut), NA_character_, paste0(ut, NBSP, "%"))
}
nb  <- function(x, d = 0) {
  .endelig(x, "nb")
  formatC(x, format = "f", digits = d, big.mark = NBSP, decimal.mark = ",")
}
pst <- function(x, d = 1) paste0(nb(x, d), NBSP, "%")
mnd <- function(x) paste0(lubridate::year(x), "m", lubridate::month(x))
kab <- function(x, ...) {
  knitr::kable(x, format.args = list(big.mark = NBSP, decimal.mark = ","), ...)
}

# --- Datapakken ---------------------------------------------------------------
# Finn datapakken robust. Arbeidsmappa under rendering er ikke nødvendigvis den
# samme som dokumentets mappe — den avhenger av om det renderes fra konsollen,
# fra Render-knappen, fra «quarto preview» eller fra CI. Vi prøver arbeidsmappa
# først, deretter dokumentets egen mappe.
#
# Kandidaten må ikke bare finnes, den må la seg åpne. Ligger mappa i OneDrive
# kan file.exists() være sann for en fil som ennå ikke er lastet ned lokalt, og
# da feiler source() med «cannot open the connection» uten å si hvorfor. Vi
# prøver derfor å åpne fila, og skiller de to feilene i meldingen.
.leselig <- function(f) {
  con <- suppressWarnings(tryCatch(file(f, "r", encoding = "UTF-8"),
                                   error = function(e) NULL))
  if (is.null(con)) return(FALSE)
  on.exit(close(con), add = TRUE)
  isTRUE(tryCatch({ readLines(con, n = 1); TRUE }, error = function(e) FALSE))
}
.dokumentmappe <- tryCatch(dirname(knitr::current_input(dir = TRUE)),
                           error = function(e) getwd())
DATASTI <- NULL
.ulesbar <- character()
for (.k in unique(c("data",
                    file.path(.dokumentmappe, "data"),
                    file.path(getwd(), "data")))) {
  .f <- file.path(.k, "scripts", "last_datapakke.R")
  if (!file.exists(.f)) next
  if (.leselig(.f)) { DATASTI <- .k; break }
  .ulesbar <- c(.ulesbar, .f)
}
if (is.null(DATASTI)) {
  stop("\n\nFant ingen lesbar datapakke «data/».",
       "\n  Arbeidsmappe:       ", getwd(),
       "\n  Dokumentets mappe:  ", .dokumentmappe,
       if (length(.ulesbar))
         paste0("\n\nFila finnes, men lar seg ikke åpne:\n  ",
                paste(.ulesbar, collapse = "\n  "),
                "\n\nDet skjer når prosjektmappa ligger i OneDrive og filene bare",
                "\nfinnes i skyen. Høyreklikk mappa i Utforsker og velg",
                "\n«Behold alltid på denne enheten», og render på nytt.\n")
       else
         paste0("\n\nÅpne Velferdsprosjekt.Rproj i RStudio og render derfra, ",
                "eller kjør\n  quarto render bostotte_oslo.qmd\nfra repo-roten.\n"),
       call. = FALSE)
}
source(file.path(DATASTI, "scripts", "last_datapakke.R"))
d <- last_alt(DATASTI)

UTTREKKSDATO <- "4. august 2026"   # vintage; jf. avsnitt om proveniens
EST_START    <- as.Date("2017-01-01")

# --- Utfallsserien ------------------------------------------------------------
# Sanntidskanten (siste måned, der terminkjøringen ennå ikke er gjort og
# verdien derfor er en strukturell null) fjernes her. Det er vaskeinngrep V1,
# dokumentert i @tbl-vask.
oslo_raa <- d$oslo |>
  transmute(dato,
            M        = ant_husstander_termin,
            soknader = ant_soknader,
            avslag   = ant_avslag,
            snitt    = gjsnitt_bostotte)

kant_rader  <- oslo_raa |> filter(dato == max(dato), M == 0)
oslo_termin <- oslo_raa |> anti_join(kant_rader, by = "dato")
oslo_est    <- oslo_termin |> filter(dato >= EST_START)

# Landsserien trimmes etter samme regel som Oslo-serien (V1), og av samme grunn:
# siste rad er strukturell null i begge, og 0/0 gir NaN. Oslos andel av
# mottakerne nasjonalt brukes til aa skalere nasjonale forhaandsanslag ned til
# Oslo i M7 (@sec-met-prior), og maa derfor regnes paa terminer med data i begge.
nasj_raa    <- d$nasjonalt |> transmute(dato, M = ant_husstander_termin)
nasj_termin <- nasj_raa |>
  anti_join(nasj_raa |> filter(dato == max(dato), M == 0), by = "dato")

osloandel <- oslo_termin |>
  inner_join(nasj_termin |> rename(M_nasj = M), by = "dato") |>
  arrange(dato) |> tail(12) |>
  summarise(a = 100 * mean(M / M_nasj)) |> pull(a)
stopifnot(is.finite(osloandel), osloandel > 5, osloandel < 40)

# --- Skalarer som brukes i løpende tekst -------------------------------------
n_est     <- nrow(oslo_est)
est_fra   <- mnd(min(oslo_est$dato));  est_til <- mnd(max(oslo_est$dato))
serie_fra <- mnd(min(oslo_termin$dato)); serie_til <- mnd(max(oslo_termin$dato))
n_serie   <- nrow(oslo_termin)

M_snitt <- mean(oslo_est$M); M_sd <- sd(oslo_est$M)
M_cv    <- 100 * M_sd / M_snitt
M_min   <- min(oslo_est$M);  M_maks <- max(oslo_est$M)

topp      <- oslo_est |> slice_max(M, n = 1)
apr24     <- oslo_est |> filter(dato %in% as.Date(c("2024-03-01", "2024-04-01")))
apr24_pst <- 100 * (apr24$M[2] / apr24$M[1] - 1)

# Volatilitet: gjennomsnittlig absolutt månedsendring i prosent, før og etter
# skjermingen (termin januar 2025). Brukes i @sec-met-observasjoner og @fig-vol.
mad_pst <- function(x) {
  x <- arrange(x, dato)
  p <- abs(100 * (x$M / lag(x$M) - 1))
  c(for_ = mean(p[x$dato <  as.Date("2025-01-01")], na.rm = TRUE),
    etter = mean(p[x$dato >= as.Date("2025-01-01")], na.rm = TRUE))
}
vol_oslo <- mad_pst(oslo_est)

bg_est <- d$brukergruppe |>
  transmute(brukergruppe, dato, M = ant_husstander_termin) |>
  filter(dato >= EST_START, dato <= max(oslo_est$dato))

vol_bg <- bg_est |>
  group_split(brukergruppe) |>
  map_dfr(\(g) tibble(brukergruppe = g$brukergruppe[1],
                      for_ = mad_pst(g)[["for_"]], etter = mad_pst(g)[["etter"]])) |>
  mutate(faktor = for_ / etter)

BEH <- "Husstander med midlertidige trygdeytelser"
vol_beh   <- vol_bg |> filter(brukergruppe == BEH)
vol_andre <- vol_bg |> filter(brukergruppe != BEH)
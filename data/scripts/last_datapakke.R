# =============================================================================
# last_datapakke.R
# R-laster for datapakken til bostøtte-prognoseprosjektet (Velferdsetaten-prep)
# Bygget 4. august 2026. Full kildedokumentasjon: docs/datakilder.md i pakken.
#
# BRUK
#   source("last_datapakke.R")
#   d <- last_alt("sti/til/data")   # utpakket datapakke
#   d$oslo            # Oslo månedlig 2010-2026 (termin- og utbetalingskalender)
#   d$oslo_bydel      # 15 bydeler x måned
#   d$brukergruppe    # Oslo x brukergruppe x måned (skjermingens behandlingsgruppe)
#   d$arsrapport      # publiserte nasjonale årstall (ekstern validering)
#   sjekk_data(d)     # kjører de seks QA-kontrollene
#   plot_oslo(d)      # rask serieplott med intervensjonslinjer (krever ggplot2)
#
# Kjørt direkte (Rscript last_datapakke.R) lastes alt og QA-en kjøres.
#
# Avhengigheter: readr, dplyr, lubridate (tidyverse-kjernen). ggplot2 kun for plott.
# =============================================================================

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(lubridate)
})

# --- Finn datamappen -----------------------------------------------------------
# Leter etter utpakket datapakke i angitt sti og vanlige kandidater.
finn_datamappe <- function(sti = NULL) {
  kandidater <- c(sti, "data", ".", "..",
                  file.path(path.expand("~"), "data"))
  marker <- file.path("data", "raw", "husbanken_bostotte_oslo_manedlig.csv")
  for (k in kandidater) {
    if (!is.null(k) && file.exists(file.path(k, marker))) return(normalizePath(k))
  }
  stop("Fant ikke datapakken. Pakk ut zip-en og angi stien: last_alt('sti/til/data')")
}

# --- Husbanken-seriene (Qlik-uttrekk) -----------------------------------------
# Kolonner: ant_husstander_utbetaling (per UTBETALINGSMÅNED),
# ant_husstander_termin (per TERMINMÅNED = vedtaksmåneden; utbetales den 20. i
# måneden etter), søknader/avslag, beløp og snittstørrelser.
# NB: siste måned har termin = 0 fordi terminkjøringen ikke er gjort ennå
# (sanntidskant). Serien føres i appen med daglig reload -> vintage varierer.
les_husbanken <- function(fil) {
  hdr <- names(read_csv(fil, n_max = 0, show_col_types = FALSE))
  ct <- if ("kommunenr" %in% hdr) cols(kommunenr = col_character()) else cols()
  read_csv(fil, col_types = ct, show_col_types = FALSE) |>
    mutate(dato = make_date(aar, manedsnr, 1), .before = 1) |>
    arrange(across(any_of(c("kommunenr", "brukergruppe"))), dato)
}

# --- SSB-tabeller (PxWeb json-stat2, flatet ut) --------------------------------
parse_ssb_tid <- function(x) {
  ut <- rep(as.Date(NA), length(x))
  i <- grepl("^\\d{4}$", x)
  ut[i] <- make_date(as.integer(x[i]), 1, 1)
  i <- grepl("^\\d{4}M\\d{2}$", x)
  ut[i] <- make_date(as.integer(substr(x[i], 1, 4)), as.integer(substr(x[i], 6, 7)), 1)
  i <- grepl("^\\d{4}K\\d$", x)
  ut[i] <- make_date(as.integer(substr(x[i], 1, 4)), (as.integer(substr(x[i], 6, 6)) - 1L) * 3L + 1L, 1)
  ut
}

les_ssb <- function(fil) {
  # alt leses som tekst (koder som "01" skal ikke bli 1), verdi konverteres
  read_csv(fil, col_types = cols(.default = col_character()), show_col_types = FALSE) |>
    mutate(verdi = as.numeric(verdi), dato = parse_ssb_tid(Tid_kode)) |>
    relocate(dato) |>
    arrange(dato)
}

# --- Oslo kommunes statistikkbank (bydelstabeller, årlige) ---------------------
# Merk: *_kode-kolonnene er posisjonelle indekser fra API-et; bruk *_navn.
les_oslo_statbank <- function(fil) {
  x <- read_csv(fil, col_types = cols(.default = col_character()), show_col_types = FALSE) |>
    mutate(verdi = as.numeric(verdi))
  aarkol <- grep("r_navn$", names(x), value = TRUE)[1]  # "år_navn", locale-trygt oppslag
  if (!is.na(aarkol)) x <- mutate(x, aar = as.integer(.data[[aarkol]]), .before = 1)
  x
}

# --- Kuraterte tabeller --------------------------------------------------------
les_intervensjoner <- function(fil) {
  read_csv(fil, show_col_types = FALSE) |>
    mutate(across(c(dato_virkning, termin_fra, termin_til,
                    utbetaling_fra, utbetaling_til), ym))
}

les_stromstotte <- function(fil) {
  read_csv(fil, show_col_types = FALSE) |>
    mutate(dato_utbetaling = make_date(utbetalingsaar, utbetalingsmaned, 1), .before = 1)
}

# --- Last alt ------------------------------------------------------------------
last_alt <- function(sti = NULL) {
  m <- finn_datamappe(sti)
  raw <- file.path(m, "data", "raw")
  cln <- file.path(m, "data", "clean")
  list(
    # Kjerneserier (Husbanken, jan 2010 - jul 2026)
    oslo                     = les_husbanken(file.path(raw, "husbanken_bostotte_oslo_manedlig.csv")),
    oslo_bydel               = les_husbanken(file.path(raw, "husbanken_bostotte_oslo_bydel_manedlig.csv")),
    brukergruppe             = les_husbanken(file.path(raw, "husbanken_bostotte_oslo_brukergruppe_manedlig.csv")),
    nasjonalt                = les_husbanken(file.path(raw, "husbanken_bostotte_nasjonalt_manedlig.csv")),
    nasjonalt_brukergruppe   = les_husbanken(file.path(raw, "husbanken_bostotte_nasjonalt_brukergruppe_manedlig.csv")),
    # SSB-kovariater
    leiemarked               = les_ssb(file.path(cln, "ssb_09895_leiemarked_oslo.csv")),
    kpi_husleie              = les_ssb(file.path(cln, "ssb_03013_kpi_husleie.csv")),
    kpi_total                = les_ssb(file.path(cln, "ssb_14710_kpi_totalindeks.csv")),
    befolkning_oslo          = les_ssb(file.path(cln, "ssb_01222_befolkning_oslo_kvartal.csv")),
    # Oslo statistikkbank (bydel, årlig)
    aap_bydel                = les_oslo_statbank(file.path(cln, "oslo_sos001_aap_bydel.csv")),
    ufore_bydel              = les_oslo_statbank(file.path(cln, "oslo_sos006_uforetrygd_bydel.csv")),
    sosialhjelp_bydel        = les_oslo_statbank(file.path(cln, "oslo_sto013_sosialhjelp_bydel.csv")),
    sosialhjelp_andel_bydel  = les_oslo_statbank(file.path(cln, "oslo_sto020_sosialhjelp_andel_bydel.csv")),
    folkemengde_bydel_0819   = les_oslo_statbank(file.path(cln, "oslo_bef004_folkemengde_bydel.csv")),
    folkemengde_bydel_1726   = les_oslo_statbank(file.path(cln, "oslo_bef005_folkemengde_bydel.csv")),
    framskriving_bydel       = read_csv(file.path(cln, "oslo_bef036_framskriving_bydel.csv"),
                                        col_types = cols(husbanken_kommunenr = col_character(),
                                                         .default = col_guess()),
                                        show_col_types = FALSE),
    grunnbelop               = read_csv(file.path(cln, "grunnbelop_historisk.csv"), show_col_types = FALSE),
    # Kuraterte regel-/intervensjonstabeller
    intervensjoner           = les_intervensjoner(file.path(cln, "intervensjonstabell.csv")),
    parametre                = read_csv(file.path(cln, "regelparametre_gjeldende.csv"), show_col_types = FALSE),
    stromstotte              = les_stromstotte(file.path(cln, "stromstotte_manedlig.csv")),
    # Publiserte nasjonale årstall fra Husbankens årsrapport, brukt til ekstern
    # validering av Qlik-uttrekket (se metodekapitlets avsnitt om validering).
    arsrapport               = read_csv(file.path(cln, "arsrapport_nokkeltall.csv"),
                                        show_col_types = FALSE),
    # Daterte forhaands- og etterberegnede effektanslag per intervensjon. Brukes
    # som prior der regressoren ennaa ikke er estimerbar (modell M7).
    forhandsanslag           = read_csv(file.path(cln, "forhandsanslag.csv"),
                                        show_col_types = FALSE)
  )
}

# --- QA: de seks kontrollene fra byggedagen ------------------------------------
sjekk_data <- function(d) {
  ok <- function(navn, betingelse, detalj = "") {
    cat(sprintf("[%s] %s %s\n", if (isTRUE(betingelse)) "OK  " else "FEIL", navn, detalj))
    isTRUE(betingelse)
  }

  # 1) Vintage-konsistens: termin(m) == utbetaling(m+1)
  lag_sjekk <- d$oslo |>
    transmute(dato_neste = dato %m+% months(1), termin = ant_husstander_termin) |>
    inner_join(d$oslo |> select(dato, utb = ant_husstander_utbetaling),
               by = c("dato_neste" = "dato")) |>
    filter(termin > 0, utb > 0)
  ok("termin -> utbetaling-lag (Oslo)",
     all(lag_sjekk$termin == lag_sjekk$utb),
     sprintf("- %d/%d månedspar konsistente", sum(lag_sjekk$termin == lag_sjekk$utb), nrow(lag_sjekk)))

  # 2) Bydelssum = Oslo-total (juni 2026)
  s_byd <- d$oslo_bydel |> filter(dato == as.Date("2026-06-01")) |>
    summarise(s = sum(ant_husstander_utbetaling, na.rm = TRUE)) |> pull(s)
  tot <- d$oslo |> filter(dato == as.Date("2026-06-01")) |> pull(ant_husstander_utbetaling)
  ok("bydelssum = Oslo-total (jun 2026)", s_byd == tot, sprintf("- %d vs %d", s_byd, tot))

  # 3) Brukergruppesum = Oslo-total (juni 2026)
  s_bg <- d$brukergruppe |> filter(dato == as.Date("2026-06-01")) |>
    summarise(s = sum(ant_husstander_utbetaling, na.rm = TRUE)) |> pull(s)
  ok("brukergruppesum = Oslo-total (jun 2026)", s_bg == tot, sprintf("- %d vs %d", s_bg, tot))

  # 4) 2025-skjermingen demper volatiliteten i midlertidige trygdeytelser (nasjonalt)
  vol <- function(aaret) {
    x <- d$nasjonalt_brukergruppe |>
      filter(brukergruppe == "Husstander med midlertidige trygdeytelser",
             aar == aaret, ant_husstander_utbetaling > 0) |>
      arrange(dato) |> pull(ant_husstander_utbetaling)
    mean(abs(diff(x)))
  }
  v24 <- vol(2024); v25 <- vol(2025)
  ok("skjermingseffekt 2025 (volatilitetsfall)", v25 < v24 / 2,
     sprintf("- snitt |Δmnd| 2024=%.0f, 2025=%.0f", v24, v25))

  # 5) LMU-forankring: Oslo og Bærum (sone 01), 2 rom, mnd-leie 2025 = 15 260 kr
  #    (filtrerer på ASCII-koder, ikke navn med æøå -> locale-robust)
  lmu <- d$leiemarked |>
    filter(Soner2_kode == "01", AntRom_kode == "2",
           ContentsCode_kode == "Husleie", Tid_kode == "2025") |>
    pull(verdi)
  ok("LMU 2-roms Oslo/Bærum 2025 = 15 260", length(lmu) == 1 && lmu == 15260,
     sprintf("- verdi: %s", paste(lmu, collapse = ", ")))

  # 6) Sanntidskant: siste måned har utbetaling > 0 og termin = 0
  siste <- d$oslo |> slice_max(dato, n = 1)
  ok("sanntidskant (siste måned: termin ennå ikke kjørt)",
     siste$ant_husstander_utbetaling > 0 && siste$ant_husstander_termin == 0,
     sprintf("- %s: utbetaling=%d, termin=%d", format(siste$dato, "%Y-%m"),
             siste$ant_husstander_utbetaling, siste$ant_husstander_termin))

  invisible(d)
}

# --- Rask serieplott med intervensjonslinjer -----------------------------------
plot_oslo <- function(d, maal = "ant_husstander_utbetaling") {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("Installer ggplot2 for plott: install.packages('ggplot2')")
  }
  library(ggplot2)
  nokkel <- d$intervensjoner |>
    filter(id %in% c("I04", "I05", "I12", "I14", "I17")) |>
    mutate(dato = coalesce(utbetaling_fra, dato_virkning))
  ggplot(d$oslo, aes(dato, .data[[maal]])) +
    geom_vline(data = nokkel, aes(xintercept = dato),
               linetype = "dashed", colour = "grey55") +
    geom_line(linewidth = 0.6, colour = "#00505c") +
    geom_text(data = nokkel, aes(x = dato, y = Inf, label = id),
              vjust = 1.4, hjust = -0.15, size = 3, colour = "grey35") +
    labs(title = "Husstander med utbetalt statlig bostøtte i Oslo",
         subtitle = "Månedlig (utbetalingskalender), jan 2010 - jul 2026. Stiplede linjer = nøkkelintervensjoner (se intervensjonstabellen).",
         x = NULL, y = "Husstander",
         caption = "Kilde: Husbankens statistikkbank (uttrekk 4. aug 2026)") +
    theme_minimal(base_size = 11)
}

# --- Kjørt direkte: last alt og kjør QA ----------------------------------------
if (sys.nframe() == 0L) {
  d <- last_alt()
  cat("Lastet", length(d), "datasett:\n ", paste(names(d), collapse = ", "), "\n\n")
  sjekk_data(d)
  cat("\nOslo, siste 6 måneder:\n")
  print(d$oslo |> select(dato, ant_husstander_utbetaling, ant_husstander_termin,
                         ant_soknader, ant_avslag, gjsnitt_bostotte) |> tail(6), n = 6)
}

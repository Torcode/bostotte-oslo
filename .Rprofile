# =============================================================================
# .Rprofile — kjøres av R ved oppstart i denne mappa, også av den R-prosessen
# Quarto starter under rendering. Hensikten er én ting: sikre UTF-8.
#
# Bakgrunn. Uten UTF-8 som native encoding konverterer R hver ikke-ASCII-streng
# til vertens tegnsett på vei ut, og skriver «å» som <U+00E5> og hvert
# tusenskille som <U+00A0>. Dokumentet bygger, men PDF-en blir uleselig.
# Dessuten avgjør tegnsettet om «Å» er en gyldig bokstav i et R-navn: er det
# ikke det, stopper parseren midt i en tabell — det var feilen 6. august 2026.
#
# Locale-navnene er forskjellige på Unix og Windows, så vi prøver begge
# familier, og tester symptomet framfor navnet: tåler en UTF-8-merket streng
# turen gjennom vertens tegnsett uten å bli escape't?
# =============================================================================

local({
  # \u00e5 er aa, \u00a0 er hardt mellomrom. Skrevet som escape, ikke som byte:
  # en literal i kildefila blir lest som «unknown» encoding og slipper unna
  # testen, mens en escape alltid gir en UTF-8-merket streng — som er den
  # som faktisk kan bli escape't på vei ut.
  ok <- function() !grepl("<U+", enc2native("\u00e5\u00a0"), fixed = TRUE)
  if (ok()) return(invisible(NULL))
  for (loc in c("nb_NO.UTF-8", "nb_NO.utf8",                    # Unix
                "Norwegian Bokmal_Norway.utf8",                 # Windows
                "Norwegian_Norway.utf8", "Norwegian.utf8",
                "English_United States.utf8",
                "C.UTF-8", "C.utf8", "en_US.UTF-8")) {
    if (ok()) break
    suppressWarnings(try(Sys.setlocale("LC_ALL", loc), silent = TRUE))
  }
  if (!ok())
    message("MERK: klarte ikke aa sette UTF-8 (locale: ",
            Sys.getlocale("LC_CTYPE"), "). ",
            "bostotte_oslo.qmd stopper med en forklaring.")
})

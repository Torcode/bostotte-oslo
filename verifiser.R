# =============================================================================
# verifiser.R — statisk portabilitetssjekk av bostotte_oslo.qmd
#
#     source("verifiser.R")
#
# Sjekker at hver R-chunk og hvert inline-uttrykk lar seg parse i et rent
# C-tegnsett, altsa i det verste tilfellet en leser kan ha.
#
# Hvorfor dette er en egen kontroll. Om en ikke-ASCII bokstav er gyldig i et
# R-navn avgjores av locale. `transmute(Ar = ...)` med norsk A parser fint i en
# UTF-8-locale og stopper med «unexpected '<'» i en C-locale, fordi R da skriver
# bokstaven som escapen <U+00C5> og parseren ser vinkelparentesen. Feilen er
# usynlig for den som utvikler i UTF-8, og total for den som ikke gjor det.
# Den stoppet en render 6. august 2026; denne kontrollen ville fanget den for
# fila ble sendt videre.
#
# Kontrollen kjorer i en egen R-prosess med LC_ALL=C, slik at den tester det
# verste tilfellet uansett hva vertsmaskinen selv star i.
# =============================================================================

QMD <- "bostotte_oslo.qmd"

sjekk_i_c_locale <- function(qmd = QMD) {
  stopifnot(file.exists(qmd))
  snutt <- sprintf('
    invisible(suppressWarnings(try(Sys.setlocale("LC_ALL", "C"), silent = TRUE)))
    src <- readLines(%s, encoding = "UTF-8", warn = FALSE)

    # --- chunks --------------------------------------------------------------
    start <- grep("^```\\\\{r", src); slutt <- grep("^```\\\\s*$", src)
    feil <- character()
    for (s in start) {
      e <- slutt[slutt > s][1]
      if (is.na(e)) next
      kode <- src[(s + 1):(e - 1)]
      lab  <- sub(".*label:\\\\s*", "", grep("label:", kode, value = TRUE)[1])
      kode <- kode[!grepl("^\\\\s*#\\\\|", kode)]
      r <- tryCatch({ parse(text = kode); NULL },
                    error = function(err) conditionMessage(err))
      if (!is.null(r))
        feil <- c(feil, sprintf("chunk [%%s] (linje %%d): %%s",
                                if (is.na(lab)) "uten navn" else lab, s, r))
    }

    # --- inline-uttrykk ------------------------------------------------------
    tekst <- paste(src, collapse = "\\n")
    m <- gregexpr("`r [^`]+`", tekst)[[1]]
    if (m[1] != -1) {
      biter <- regmatches(tekst, gregexpr("`r [^`]+`", tekst))[[1]]
      for (b in biter) {
        kode <- sub("^`r ", "", sub("`$", "", b))
        r <- tryCatch({ parse(text = kode); NULL },
                      error = function(err) conditionMessage(err))
        if (!is.null(r))
          feil <- c(feil, sprintf("inline %%s: %%s", substr(b, 1, 60), r))
      }
      cat("inline-uttrykk sjekket: ", length(biter), "\\n", sep = "")
    }
    cat("chunks sjekket:         ", length(start), "\\n", sep = "")
    cat("locale under sjekk:      ", Sys.getlocale("LC_CTYPE"), "\\n", sep = "")
    if (length(feil)) {
      cat("\\nPARSEFEIL:\\n"); cat(paste0("  ", feil, collapse = "\\n"), "\\n")
      quit(status = 1)
    }
    cat("ingen parsefeil\\n")
  ', deparse(qmd))

  f <- tempfile(fileext = ".R"); on.exit(unlink(f))
  writeLines(snutt, f)
  rbin <- file.path(R.home("bin"), if (.Platform$OS.type == "windows")
                    "Rscript.exe" else "Rscript")
  status <- system2(rbin, c("--vanilla", shQuote(f)))
  invisible(status == 0)
}

cat("Portabilitetssjekk av ", QMD, "\n", sep = "")
cat(strrep("-", 62), "\n")
ok <- sjekk_i_c_locale()
cat(strrep("-", 62), "\n")
if (isTRUE(ok)) {
  cat("Klart: dokumentet parser ogsa i et rent C-tegnsett.\n")
} else {
  cat("Ikke klart. Sett de rapporterte navnene i bakoverfnutter (`navn`),\n")
  cat("eller bruk ASCII i R-navn. Norske tegn i strenger og kommentarer\n")
  cat("er uproblematiske - det er navnene som ma vaere trygge.\n")
}

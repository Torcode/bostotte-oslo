# Scenarionotat: nytt boutgiftstak basert på faktiske leiepriser

Skrevet 18. august 2026. Dette er forberedelse, ikke aktivering: ingen rader
er lagt i registrene, ingen kode er endret, ingen scenariobane er beregnet.
Notatet dokumenterer saksgrunnlaget med kilder og spesifiserer hvordan
forslaget ville kjøres som navngitt scenario i rammeverket den dagen eieren
beslutter det — eller forslaget blir vedtak.

## Saksgrunnlaget, med kildegrad per påstand

Hver påstand under bærer sin egen kildegrad: **[P]** verifisert primærkilde,
**[P?]** primærdokument identifisert men sitatet ikke kontrollert mot
dokumentteksten, **[S]** sekundærkilde. Graderingen følger samme disiplin som
`PLASSHOLDER`-systemet i bibliografien: det umerkede skal være kontrollert.

1. **[P]** Stortinget fattet 16. juni 2023 anmodningsvedtak nr. 931
   (2022–2023): «Stortinget ber regjeringen i statsbudsjettet for 2024 fremme
   forslag om endringer i bostøtteregelverket som gjør ordningen mer
   treffsikker for husholdninger med lave inntekter og høye boutgifter.»
   Sitert her fra kontroll- og konstitusjonskomiteens gjennomgang i
   Innst. 239 S (2023–2024), som også bemerker at forslag ikke kom i
   2024-budsjettet.
2. **[P]** Bestillingen om *leiepriser* er en flertallsmerknad, ikke et
   nummerert vedtak: i Innst. 447 S (2023–2024) (revidert nasjonalbudsjett
   2024, juni 2024) ba flertallet (Ap, Sp, SV) om at regjeringen «skal utrede
   endringer i boutgiftstaket innen revidert nasjonalbudsjett 2025», og at
   taket «bør gjenspeile de faktiske boutgiftene i landet, for eksempel med
   utgangspunkt i SSBs leiemarkedsundersøkelse». Presiseringen vedtak/merknad
   er bekreftet av departementets egen oppfølging, som viser til «merknaden».
3. **[P]** Kommunal- og distriktsdepartementet ga Husbanken oppdraget i
   supplerende tildelingsbrev nr. 2 for 2024 (1. juli 2024), oppdrag 13/2024
   «Mer treffsikker innretning av boutgiftstakene»: «I tråd med merknaden,
   ber vi Husbanken om å utrede en mer treffsikker innretning av
   boutgiftstakene innen 15. november 2024.»
4. **[S]** Husbanken leverte utredningen høsten 2024 med anbefaling om «bruk
   av oppdaterte leiedata til justering av boutgiftstaket». Selve leveransen
   er ikke funnet offentliggjort; det verifiserbare er oppdragsfristen
   15. november 2024 i punkt 3. Skal leveransens innhold brukes i et
   scenario, må dokumentet innhentes (innsyn/eInnsyn) først.
5. **[P?]** I revidert nasjonalbudsjett 2025 (Prop. 146 S (2024–2025),
   15. mai 2025) ble saken skjøvet til det ordinære budsjettarbeidet;
   formuleringen «vurderingene vil inngå i arbeidet med det ordinære
   statsbudsjettet» er sitert via sekundærkilde, proposisjonen er
   identifisert, sitatet ikke kontrollert i selve dokumentet.
6. **[P]** Forslaget ble ikke fulgt opp i 2026-budsjettet: Prop. 1 S
   (2025–2026) for KDD (15. oktober 2025) fremmer ikke nytt boutgiftstak, og
   verken proposisjonens vedtaksoversikt eller Meld. St. 4 (2025–2026)
   kap. 11 har noe åpent bostøttevedtak hos KDD. (Negativt funn i store
   dokumenter — kontrollert i to uavhengige lesninger, men verdt et manuelt
   tekstsøk før det siteres videre.)
7. **[P]** Regjeringen oppnevnte i statsråd 19. desember 2025 et offentlig
   bostøtteutvalg (leder: Kristin Aarland, OsloMet) som «skal levere sin
   rapport til Kommunal- og distriktsdepartementet innen 31. desember 2026».
   Mandatet drøfter boutgifter og leiemarked, men nevner ikke boutgiftstaket
   eller Husbankens utredning eksplisitt.
8. **[P]** Neste budsjettdokument er kunngjort: statsbudsjettet for 2027
   legges fram **7. oktober 2026** (regjeringens datoside, publisert
   17. august 2026, «med forbehold om endringer i Stortingets kalender»).
   Revidert nasjonalbudsjett 2026 (12. mai 2026) endret ikke boutgiftstaket
   (ingen omtale funnet).

## Hvorfor dette aldri kan ligge i basisbanen

Rammeverkets port er informasjonssettet, ikke kalenderen: et regelverkssteg
får bare virke framover i en prognose dersom det har dokumentert
`effect_known_from` ≤ prognoseopprinnelsen i `data/clean/regelverk_kunnskap.csv`.
Et forslag uten vedtak har ingen kunngjøringsdato å registrere — det finnes
ingen rad å skrive uten å dikte. Basisbanen beholder derfor
informasjonsstatusene `vedtatt_kalender` og `viderefort_regelverk` (slik de
står i prognoseartefakten) uberørt av denne saken, uansett hvor sannsynlig et
vedtak måtte virke. Det er samme
regel som holder M7-orakelet utenfor operative tall: informasjon uten dato er
ikke informasjon i denne prosessen.

## Slik kjøres det som navngitt scenario den dagen det aktiveres

- **Navn og bokføring.** Scenariet får en egen id-serie atskilt fra
  intervensjonene (forslag: `S01 boutgiftstak-leiepris`; I-serien er
  reservert faktiske hendelser). Definisjonen skrives i
  intervensjonstabellens kolonneformat (dato_virkning, termin_fra,
  mekanisme, forventet retning, kilde) men lagres atskilt fra
  `intervensjonstabell.csv`, som forblir ren fasit.
- **To deklarerte frihetsgrader.** (i) Nivå/profil på nye tak — kan ikke
  tallfestes før Husbankens leveranse (punkt 4) eller en proposisjon
  foreligger; (ii) ikrafttredelsestermin — tidligst realistisk er
  terminer etter et budsjettvedtak i desember 2026, typisk 2027m1 eller
  2027m7. Begge settes eksplisitt per scenariokjøring og trykkes sammen med
  resultatet.
- **Retning, ikke størrelse.** Mekanismen er kjent fra forskriften: høyere
  tak øker godkjente boutgifter for husstander som i dag ligger over taket,
  og trekker inn husstander som med høyere beregningsgrunnlag får positiv
  støtte. Eksponeringen er observerbar i datapakken (`ant_over_tak`).
  Størrelsen er ukjent inntil punkt 4 er innhentet; scenariet deklarerer
  retning og lar nivået være parameter.
- **Beregning og merking.** Scenariobanen kjøres med samme modellapparat som
  basisbanen (pålagt steg i regressoren), men publiseres aldri i
  prognoseartefakten eller README-tabellen: egen blokk, eget navn, egne
  forutsetninger. Konformale intervaller gjelder ikke for scenariosteget —
  det finnes ingen historiske feil for uvedtatte regler å kalibrere på — så
  banen merkes betinget beregning under oppgitte forutsetninger, i slekt med
  orakel-merkingen, ikke prognose.
- **Overgangen til basisbanen** skjer først når et vedtak med dato
  foreligger: da får steget rad i `regelverk_kunnskap.csv` med
  `effect_known_from` = kunngjøringsdato og primærkilde, scenariet
  pensjoneres, og steget behandles som enhver annen intervensjon.

## Kjente informasjonspunkter framover

7. oktober 2026 (Prop. 1 S (2026–2027)) er det neste daterte punktet der et
vedtak kan komme; bostøtteutvalgets NOU (frist 31. desember 2026) er det
neste der kunnskapsgrunnlaget kan endre seg vesentlig; deretter revidert
nasjonalbudsjett våren 2027. Sjekklisten ved hvert punkt: finnes vedtak med
ikrafttredelsesdato og beløpsprofil → registrer kunngjøringsdato i
kunnskapsregisteret; bare omtale/utredning → scenariet består som scenario.

## Kilder

- Innst. 239 S (2023–2024), kontroll- og konstitusjonskomiteen (vedtak 931-
  sitatet): stortinget.no/globalassets/pdf/innstillinger/stortinget/2023-2024/inns-202324-239s.pdf
- Innst. 447 S (2023–2024), finanskomiteen, RNB 2024 (flertallsmerknaden):
  stortinget.no/no/Saker-og-publikasjoner/Publikasjoner/Innstillinger/Stortinget/2023-2024/inns-202324-447s/
- Supplerende tildelingsbrev nr. 2 for 2024 til Husbanken, KDD 1. juli 2024
  (oppdrag 13/2024): regjeringen.no/contentassets/6ed06d0c878446889f5d59c96feb3fe6/supplerende-tb-nr.-2-for-2024-husbanken.pdf
- Prop. 146 S (2024–2025), RNB 2025: regjeringen.no/contentassets/8e93548da7cc44f2801f2613c24c2af3/no/pdfs/prp202420250146000dddpdfs.pdf
- Prop. 1 S (2025–2026) KDD: regjeringen.no/no/dokumenter/prop.-1-s-20252026/id3123723/
- Meld. St. 4 (2025–2026) kap. 11: regjeringen.no/no/dokumenter/meld.-st.-4-20252026/id3123751/?ch=11
- Offisielt frå statsrådet 19. desember 2025 (oppnevningen):
  regjeringen.no/no/aktuelt/offisielt-fra-statsradet-19.-desember-2025/id3143392/
- Bostøtteutvalgets mandat og nettside (NOU-fristen):
  regjeringen.no/contentassets/632b31ee3d1d444cac243b31da68159a/bostottemandat.pdf;
  nettsteder.regjeringen.no/bostotteutvalget/
- Statsbudsjettet: viktige datoer i 2026 (framleggingsdatoen 7. oktober):
  regjeringen.no/no/statsbudsjett/2026/statsbudsjettet-viktige-datoer-i-2026/id3148899/
- Bostøttealliansen (sekundærkildene i punkt 4 og 5):
  bostottealliansen.no/hovedsiden/nyheter/statsbudsjett-2026;
  bostottealliansen.no/hovedsiden/nyheter/kutt-og-underregulering-videreføres-i-revidert-budsjett-2025

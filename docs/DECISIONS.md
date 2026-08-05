# Beslutningslogg

Sist oppdatert: 2026-08-05

Statusverdier:

- **Vedtatt:** styrer arbeidet til en ny beslutning erstatter den.
- **Foreløpig:** arbeidshypotese som må godkjennes ved faseport.
- **Åpen:** beslutning mangler.

| ID | Status | Beslutning | Begrunnelse og konsekvens |
|---|---|---|---|
| D-001 | Vedtatt | GitHub-repoet er prosjektets kanoniske kode-, tekst- og beslutningshistorikk. | Chat og notebooks er arbeidsflater; godkjente endringer skal ende i issue, branch og PR. |
| D-002 | Vedtatt | Prosjektet deles i tre faser: data/revidde, modeller/ML og operasjonalisering/MLOps. | Hver fase har en port; senere teknologi skal ikke brukes som erstatning for dokumentert datakvalitet eller modellverdi. |
| D-003 | Vedtatt | Prosjektet er i fase 1. | Nåværende leveranse er datakvalitets- og mulighetsrapport, ikke en modellkonkurranse. |
| D-004 | Foreløpig | Månedlig antall husstander med positivt terminvedtak i Oslo, $M^T_t$, er arbeidende hovedserie. | Serien er tilgjengelig månedlig og følger regelverkskalenderen. Endelig fase-2-kontrakt krever eksplisitt godkjenning. |
| D-005 | Vedtatt | Termin- og utbetalingskalender holdes separat, med $M^U_{t+1}=M^T_t$ som datakontroll. | Sammenblanding gir feil datering av intervensjoner og tilgjengelig informasjon. |
| D-006 | Vedtatt | Husbanken-vintagen fra 2026-08-04 fryses som fase-1-grunnlag. | Kilden revideres bakover. Alle tall må knyttes til vintage; senere uttrekk skal ikke overskrive dette i stillhet. |
| D-007 | Vedtatt | Bare åpne aggregater brukes i repoet. | Ingen person-, register- eller Microdata.no-data skal lagres i Git. |
| D-008 | Vedtatt | Seasonal naïve med sesonglengde 12 er obligatorisk baseline, og evaluering skjer med rolling origin. | Tilfeldig split overvurderer ytelse og bryter tidsrekkefølgen. |
| D-009 | Vedtatt | Resultater rapporteres separat for horisont 1–12. | En modell kan være nyttig på korte og svak på lange horisonter; ett aggregert tall skjuler dette. |
| D-010 | Vedtatt | Fase-2-eksperimenter utføres i Google Colab, men gjenbrukbar logikk flyttes til testbar kode. | Colab gir lav terskel for ML, mens repoet gir reproduksjon og review. |
| D-011 | Vedtatt | Fase 3 starter bare dersom fase 2 dokumenterer stabil modellverdi. | MLOps skal løse et dokumentert driftsproblem, ikke fungere som porteføljepynt. |
| D-012 | Foreløpig | unt_1.qmd er arbeidende kanonisk rapport; 03-metode-del1.qmd behandles som en kilde/arbeidsfil til duplikatet er avklart. | Filene overlapper og kan ellers divergere. Ingen tekst slettes før sammenligning og godkjenning. |
| D-013 | Åpen | Primært tap og beslutningsvekter. | MAE og RMSE kan rapporteres, men modellrangering bør knyttes til faktisk bruk og asymmetriske kostnader hvis de finnes. |
| D-014 | Åpen | Bruk av bydels- og brukergruppehierarki i hovedmodell. | Datastrukturen finnes og summerer eksakt, men kompleksiteten må begrunnes av prognoseverdi og utvalgsstørrelse. |

## Endringsprosedyre

En metodisk beslutning endres ved å:

1. opprette eller oppdatere et GitHub-issue;
2. beskrive alternativene og hva de påvirker;
3. dokumentere data, test eller kilde som avgjør valget;
4. oppdatere denne loggen i samme PR som implementasjonen.

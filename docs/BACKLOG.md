# Prioritert backlog

Backloggen speiler GitHub-issues. Issue-teksten er autoritativ for leveranse og akseptansekriterier.

| Rekkefølge | Fase | Issue | Avhengighet | Hovedleveranse |
|---:|---|---|---|---|
| 1 | 1 | [#1 Prosjektkontrakt, README og QA-port](https://github.com/Torcode/bostotte-oslo/issues/1) | — | Kanoniske dokumenter, validator og første CI |
| 2 | 1 | [#2 Bibliografi og primærkilder](https://github.com/Torcode/bostotte-oslo/issues/2) | #1 | Verifiserte kilder uten skjulte plassholdere |
| 3 | 1 | [#3 Robust innhenting og låst miljø](https://github.com/Torcode/bostotte-oslo/issues/3) | #1 | Ren-checkout-kjørbar datainnhenting |
| 4 | 1 | [#4 Utvidet datakontrakt og negative tester](https://github.com/Torcode/bostotte-oslo/issues/4) | #1, #3 | QA for alle godkjente data og vintage-manifest |
| 5 | 1 | [#5 Fullfør fase-1-rapport](https://github.com/Torcode/bostotte-oslo/issues/5) | #2–#4 | Én kanonisk, renderbar mulighetsrapport |
| 6 | Port | [#6 Frys prognose- og evalueringskontrakt](https://github.com/Torcode/bostotte-oslo/issues/6) | #5 | Go/no-go og implementerbar fase-2-kontrakt |
| 7 | 2 | [#7 Seasonal naïve og rolling origin](https://github.com/Torcode/bostotte-oslo/issues/7) | #6 | Tidsriktig baseline per horisont |
| 8 | 2 | [#8 Colab: statistiske og ML-modeller](https://github.com/Torcode/bostotte-oslo/issues/8) | #7 | Lekkasjefri modell-sammenligning |
| 9 | 2 | [#9 Stabilitet, intervaller og regelbrudd](https://github.com/Torcode/bostotte-oslo/issues/9) | #7–#8 | Robusthetsrapport og fase-3 go/no-go |
| 10 | 3 | [#10 MLOps-mulighetsstudie](https://github.com/Torcode/bostotte-oslo/issues/10) | #9 og dokumentert modellverdi | Driftsdemonstrator og overvåkningsdesign |
| Parallelt | Hygiene | [#11 Rådata, binærfiler og artefakter](https://github.com/Torcode/bostotte-oslo/issues/11) | #1 | Reversibel opprydding og lagringspolicy |

## Arbeidsregel

- Én issue → én branch → én PR.
- Maksimalt ett stort faglig spørsmål per PR.
- Ingen fase-2-modeller før #6 er godkjent.
- Ingen fase-3-infrastruktur før #9 anbefaler go.
- Mekaniske kontroller automatiseres; menneskelig/AI-review prioriterer måling, lekkasje, identifikasjon, kilder og overclaiming.

## Fase-1-kritisk sti

#1 → (#2 + #3) → #4 → #5 → #6

#11 kan gjennomføres parallelt så lenge ingen råfil slettes uten dokumentert gjenoppretting og reproduksjonsvurdering.

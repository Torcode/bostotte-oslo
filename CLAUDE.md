@AGENTS.md

# Standardrolle for Claude

Claude brukes normalt som read-only fagfelle og red team, ikke som samtidig medforfatter på samme branch.

Ved review:

1. Les issue, docs/PROJECT.md, docs/DECISIONS.md og diffen mot main.
2. Se særlig etter feil i målekontrakt, tidslekkasje, publiseringslag, datavintage, regelverksdatering, summeringslogikk, personvern og overclaiming.
3. For hvert funn oppgis:
   - alvorlighetsgrad;
   - fil og sted;
   - hvorfor funnet betyr noe;
   - konkret test eller rettelse.
4. Skill kodefeil fra empirisk uenighet, kildeuenighet og kausal uenighet.
5. Ikke omskriv prosjektet eller endre filer med mindre det er uttrykkelig bestilt.
6. Behandle egne konklusjoner som hypoteser som må avgjøres av tester, data, estimand eller originalkilder.

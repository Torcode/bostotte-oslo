# Forhåndsregistrering, notebook 05: intervaller

**Denne filen er committet før noen modell i notebook 05 er kjørt.** Notebook 05
henter den fra `main` og viser commit-datoen ved siden av resultatene, slik at
rekkefølgen kan etterprøves framfor å hviles på en påstand. Notebook 03 og 04 hadde
forhåndsregistrering i selve notebooken, der filen ikke kunne bevise rekkefølgen; det
er den svakheten dette retter.

## Hullet notebook 05 skal fylle

Alle modellene i notebook 03 og 04 gir punktprognoser. Modellstigen i arbeidsverk 1 er
skåret på dekning og intervallskår i tillegg til MASE og RMSE, og på de to kolonnene
kan arbeidsverk 2 foreløpig ikke sammenliknes i det hele tatt. For en etat som
dimensjonerer kapasitet er det intervallet som er beslutningsgrunnlaget, ikke punktet.

Notebook 02 bygget det tidsgyldige konformale skjemaet — kalibrering bare på
prognosefeil som faktisk var realisert ved opprinnelsen. Notebook 05 bruker det, og
prøver å reparere svakheten notebook 02 målte: ved tolv måneders horisont finnes bare
19 kalibreringspunkter.

## Fire påstander

**P1 — Det tidsgyldige skjemaet underdekker, mest på lange horisonter.**
Notebook 02 målte 67,4 % dekning mot nominelle 80 på den naive modellen, med 30
kalibreringspunkter ved h = 1 og 19 ved h = 12. Samme skjema på en bedre punktmodell
skal fortsatt underdekke, og underdekningen skal være større ved lange horisonter enn
ved korte.
*Felles hvis samlet dekning lander innenfor to prosentpoeng av 80, eller hvis
underdekningen ikke er større ved h = 12 enn ved h = 1.*

**P2 — Kalibrering på bydelspanelet hjelper.**
Femten bydeler pluss Oslo gir opptil seksten ganger så mange kalibreringspunkter ved
hver kombinasjon av opprinnelse og horisont. Dekningen skal komme nærmere nominelt
nivå, og forbedringen skal være størst der grunnlaget var tynnest, altså på lange
horisonter.
*Felles hvis panelkalibrering ikke bedrer dekningen ved h = 12.*

**P3 — Ukorrigert panelkalibrering overdekker.**
Notebook 01 målte at restvariasjonen i bydelspanelet skalerer med bydelsstørrelse:
log(sd) = −0,11 − 0,60·log(n), R² 0,87. Bydelenes prognosefeil på logskala er derfor
systematisk større enn Oslos, og å slå dem sammen ukorrigert skal gi for vide
intervaller for Oslo-totalen. Med en størrelseskorreksjon estimert på de samme
prognosefeilene skal dekningen ligge nærmere nominelt nivå.
*Felles hvis ukorrigert panelkalibrering ikke gir høyere dekning enn korrigert.*

**P4 — Beste punktmodell er ikke automatisk best på intervallskår.**
Intervallskåren belønner smale intervaller og straffer bom med vekt 2/α = 10. En
modell kan ha lavere MASE og likevel dårligere intervallskår, dersom kalibreringen er
dårligere. Rangeringen på de to målene skal derfor ikke være identisk.
*Felles hvis rangeringen på intervallskår er den samme som rangeringen på MASE.*

## Hva som måles ved siden av

Størrelsesskaleringen estimeres på nytt, direkte på prognosefeilene i
kryssvalideringen, og sammenliknes med notebook 01s −0,60. De to måler ikke helt det
samme — notebook 01 så på restvariasjon etter at fellesbevegelsen var trukket ut,
notebook 05 ser på prognosefeil — så et avvik er ikke i seg selv en motsigelse. Men
sammenlikningen står i notebooken uansett hva den viser.

## Oppsett som er bestemt på forhånd

- Nominelt nivå 80 %, som i arbeidsverk 1. Intervallskår med straffevekt 10.
- Samme protokoll: 31 opprinnelser, h = 1–12, 372 punkter.
- Punktmodeller: L0 (beste modell i notebook 04), G2 (beste i notebook 03), og M0 som
  referanse.
- Konformale kvantiler krever minst tre kalibreringspunkter, som i notebook 02.
- Ingen hyperparametre justeres i notebook 05.

Alt som avviker fra dette, skal begrunnes i notebooken.

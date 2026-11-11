# Full de ruta

## v1 · Publicat
- Joc de cenyida amb 5 nivells + regata lliure, ruta ideal i resum de la regata.
- App instal·lable (PWA) a GitHub Pages, sense connexió.
- Perfils sense dades personals al codi, recompenses (estrelles, XP, garatge, repte del dia).
- Rànquing de família amb Supabase i codi de família.

## v2 · Regata completa · Publicat
Recorregut: sortida → cenyida → **través** → **popa** → **porta de sotavent** (dues boies) → **última cenyida** → arribada.
- Al través i a la popa el vaixell també navega sol; les decisions són: orsar o arribar, trasluchar (botó que canvia de nom segons el tram) i per quina boia de la porta passar.
- Ombra de vent a la popa (els de darrere tapen els de davant).
- La ruta ideal i el resum per trams, amb colors de sector (lila = millor, verd = bo).
- Fet com a mode nou («Regata completa»). Els 5 nivells i la regata lliure continuen sent només cenyida.

## v2.1 · Botiga i rànquing per prova · Publicat
- Monedes en lloc de desbloquejar per nivells: es compren vaixells, esteles, banderes i celebracions.
- Cinc nivells d'article: Normal, Rar, Mític, Llegendari i Ultrallegendari.
- Rànquing de família per prova (cada nivell i la regata completa).
- Triar on surts amb calma: el rellotge espera i hi ha botons per moure's per la línia.

## v2.2 · Que no compensi sempre anar a l'extrem · Publicat
- El vent ja no compleix sempre la previsió (rolada persistent i canvi de vent amb força i moment variables, i oscil·lacions a sobre).
- Ratxes més repartides i que es mouen de costat.
- Al resum, a més de la ruta ideal, el temps d'un bon regatista que no sap el futur.
- Comentari quan fas un extrem, amb dades de quantes vegades fa podi.
- Mesura (40 regates per nivell): la ruta ideal amb una sola virada a Persistent baixa de 33 a 5, i a Canvi de vent de 20 a 1. L'extrem guanya a Persistent 10 cops en lloc de 15, i a Canvi de vent 4 en lloc d'11.

## v3 · Competició · Publicat
- Dos modes: Entrenament (el joc d'abans) i Competició.
- Temporada: Campionat de Catalunya (40, passen 20) → Campionat d'Espanya (50, passen 10) → Europeu (50, passen 5) → Mundial (60).
- Recorregut complet, puntuació baixa, descart a l'Europeu i al Mundial, rivals fixos durant el campionat.
- Si no et classifiques, tornes a provar el campionat amb vents nous. En acabar el Mundial comença una temporada nova, amb més nivell.
- Premis en monedes, trofeus al garatge i pestanya Competició al rànquing de família.
- Calibratge (12 campionats per etapa, temporada 1, amb un bon regatista sense saber el futur al lloc del jugador): Catalunya sempre, Espanya la meitat de les vegades, Europeu 1 de cada 4, Mundial al voltant del 15è.

## v4 · Seus, lligues i reptes · Publicat
- Popa d'Optimist: gairebé en popa redona i poques trasluchades; la decisió és el costat.
- Lligues a cada nivell i a cada seu (Bronze, Plata, Or, Platí, Diamant): amb 3 estrelles es puja.
- Seus: Garda (Ora, l'Ora que entra, Pelèr), Saint-Raphaël (brisa tèrmica, mistral, canvi de vent), Palma (embat, embat a clapes, xaloc) i Barcelona/Maresme (garbí, llevant, terral). Primera versió, per revisar amb la Mia.
- Reptes entre germans amb vaixell fantasma i comparació per trams (esquema v4 executat a Supabase l'11/11/2026).
- Popa calibrada amb 1.300 popes reals (MetaSail, Cap d'Agde 2026): TWA mediana 164° i, sobretot, una sola amura.
- Menú nou: pantalla d'inici, apartats separats, barra d'onglets i rànquing amb tres pestanyes.

## v4.1 · Garda ben fet · Publicat
- Ora: el camp és sota els penya-segats, a la dreta. Més vent i gir a prop de la pedra, i la majoria de la flota hi va. Guanya la dreta gairebé sempre.
- Pelèr: guanya l'esquerra, amb més joc de rolades.
- Palma (embat): una mica millor l'esquerra. Barcelona (garbí): una mica més de vent a prop de terra, a la dreta.
- A totes les seus el camp queda muntat al vent.
- Per revisar amb la Mia: cap on gira el vent a prop de la pedra i quanta flota va a la dreta.

## v4.2 · Saint-Raphaël per a la CIP · Publicat
- Quatre dies: tèrmic de tarda, tèrmic fluix, mistral i vent d'est.
- Tèrmic de tarda: entra després de la calma del migdia i va pujant; sovint paga l'esquerra, a prop de la costa.
- Tèrmic fluix: no s'estableix, clapes i rolades grans.
- Mistral: de terra, amb menys vent i més irregular a prop de la platja.
- Vent d'est: el més freqüent, amb onada.
- Tret de cròniques de regates de Pasqua a la mateixa badia. Cal contrastar-ho amb algú que hi hagi regatejat.

## v4.3 · Els dies d'abril a Saint-Raphaël · Publicat
- Els quatre dies surten de dades reals de vent de la badia (19-26 d'abril, 2016-2026) i porten el seu percentatge: tèrmic del sud 49%, llevant 35%, mistral 9%, dia fluix 7%.
- «Un dia d'abril»: no saps quin dia toca, només veus els senyals d'abans de sortir. Al resum et diu quin era.
- «Com reconèixer el dia» a la pàgina de la seu: què es veu i com funciona cada vent.

## v4.4 · Els dies de febrer a Garda · Publicat
- Garda amb dades de vent de Riva de l'última setmana de febrer: Ora 62%, Ora fluixa 18%, vent del nord 13%, Pelèr de matí 7%.
- L'Ora d'hivern és més fluixa que la d'estiu i la dreta encara pesa més.
- «Un dia de febrer» i «Com reconèixer el dia», com a Saint-Raphaël.
- Els models no coincideixen en quanta Ora hi ha: cal contrastar-ho amb el que han vist a l'aigua.

## v4.5 · El mateix recorregut a tot arreu · Publicat
- A Garda el recorregut ja no està girat: través, popa i porta a l'esquerra, com sempre en Optimist.
- Amb l'Ora, la segona cenyida surt de l'esquerra, lluny de la pedra i amb menys vent.
- Pendent de parlar: què fa difícil la segona cenyida a Garda.

## v4.6 · Recorregut oficial, través real i Garraf · Publicat
- Recorregut amb les mides del trapezi oficial d'Optimist: través a 120° del vent, popa llarga fins a una porta per sota de la sortida i última cenyida curta.
- Través: anar recte és el més ràpid. Els rivals orsen per defensar-se i es barallen; qui pot anar recte guanya. Més ombra de vent al través.
- Seu nova: Garraf, amb els dies de finals de novembre (Ventolina, Terral, Garbí, Llevant), «Un dia de novembre» i «Com reconèixer el dia».
- Els temps i els rànquings antics de la regata completa i de les seus ja no són comparables.
- Per confirmar amb els nens: on és l'arribada i com de llarga és la popa.

## v4.7 · Palma al desembre · Publicat
- Palma amb els dies del Ciutat de Palma (primers de desembre): Calma i embat fluix 37%, Mestral 28%, Vent del nord 16%, Gregal 13%, Llebeig 6%.
- «Un dia de desembre» i «Com reconèixer el dia».
- Barcelona es queda com estava: és on entrenen.

## v4.8 · Més premis al garatge · Publicat (ara)
- Vaixells nous: de gel, de neó, de tempesta, Moth amb foils, Holandès Errant, Kraken, nebulosa i catamarà F50.
- Esteles noves: escuma, neu, tinta, neó i llamps.
- Celebracions noves: nevada, dofins, disco, onada gegant, volcà i tempesta amb trons.
- Premis que no es venen: Optimist de diamant (30 estrelles), estela de pols d'or (10 victòries), Copa de campió (un trofeu de la Competició) i Aurora boreal (passar el Campionat d'Espanya).
- Conjunts que fan joc (vaixell + estela + celebració), indicats a cada targeta.
- Els premis guanyats ja no es perden (abans l'Optimist daurat marxava si es trencava la ratxa).
- Per ajustar amb els nens: preus i quantes estrelles o victòries demana cada premi.

## v5 · Sortida real
- Compte enrere de 3 minuts accelerat; el vaixell es pot moure abans del senyal (accelerar, frenar, virar).
- OCS si ets a sobre de la línia al senyal, amb retorn obligatori.
- Lectura de la línia: costat afavorit segons el vent.

## v4 · Regles i creuaments
- Protestes simples quan hi ha contacte o no es cedeix el pas; gir de penalització de 720°.
- Rivals que tapen a propòsit (cobertura) i rivals que es deixen tapar.
- Zona de 3 eslores a les boies.

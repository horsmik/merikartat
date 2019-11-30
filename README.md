# merikartat

Tämä on harjoitelma OpenCPM merikarttojen luomiseen Liikenneviraston Avoimesta Datasta.

Disclaimer: Ei navigointiin

Karttojen Lähde: Liikennevirasto. Ei navigointikäyttöön. Ei täytä virallisen merikartan vaatimuksia.
https://www.liikennevirasto.fi/avoindata/kayttoehdot/avoimen-tietokannan-lisenssi#.WgCfiWiCxPY

Ainuttakaan ohjelman luomaa karttaa ei ole tarkistettu/varmistettu. Ne näyttävät olevan kunnossa, mutta näitä ei tule käyttää navigointiin. Ainakaan ainoana karttana :)

Ohjelmat luovat karttalehdet merikarttasarjoille A ja B.

Ohjelma luo bittikartat sekä niihin liittyvät konfiguraatiotiedostot. OpenCPN muunnokseen tarvitset lisäksi imgkap-ohjelman.

Scripti ei ole erityisen versioriippuvainen toiminee kaikilla 3.x pythoneilla. Tarvitset lisäksi muutaman kirjaston. 
Taustaa:
https://www.fe83.org/gallery/view_album.php?set_albumName=album675

Hyödyllistä myös asentaa imagemagic, jolla voi käsittellä haettujen bittikarttojen väripaletin ennen KAP konversiota. Ilman tuota karttojen värisävyt saattavat vaihdella (yksittäin tehtyjen imgkap.exe konversioiden jäljiltä)

Workflow:

Määrittele haluamasi karttapoiminnat csv-tiedostoon. Joko kokonana uusi poiminta tai poista tekemistäni tiedostoista kommenttimerkinnät haluamistasi karttalehdistä.

Aja scripti, esim:
python MK_A_data.csv

Scripti tekee myös BAT tiedoston, minkä voi ajaa suoraan (olettaa että KAP tiedostot kopioidaan alihakemistoon "128_Colors") tai mistä voi katsoa mallia, miten seuraavat vaiheet tehdään.

Konvertoi kartan väripaletti (esim.) komennolla:
magick kartan_nimi.png -remap palette.png kartan_uusi_nimi.png

Tuossa uudelle kartalle tulee palette.png tiedostossa olevat värisävyt. Jolloin kartat näyttävät yhdenmukaisilta.

Lopuksi tehdään png KAP knversio komennolla:
imgkap.exe kartan_nimi.png kartan_konfiguraatio_tiedosto.txt

...minkä lopputuloksena syntyy geokoodattu KAP tiedosto, minkä voi avata OpenCPN softalla.

Karttoja oikeellisuutta ei edelleenkään ole varmistettu mitenkään. Ne vaikuttavat olevan kunnossa, mutta tuosta ei ole mitään takuita. ei navigointiin.

Huom: En ole keksinyt miten KAP tiedostoihin saisi "Läpinäkyvän värin". Jos karttatiilien haku menee yli aineistorajan, karttaan syntyy valkoinen reunus, mikä näkyy myös lopullisessa KAP-kartassa. Tästä johtuen esimerkiksi erikoiskarttojen poiminnassa joutuu rajaamaan poiminnan sellaiseksi että mukaan otetaan vain kokonaan erikoiskartan sisään mahtuvat karttatiilet. 

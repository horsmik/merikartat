# merikartat

Tämä on harjoitelma OpenCPM merikarttojen luomiseen Liikenneviraston Avoimesta Datasta.

Disclaimer: Ei navigointiin

Karttojen Lähde: Liikennevirasto. Ei navigointikäyttöön. Ei täytä virallisen merikartan vaatimuksia.
https://www.liikennevirasto.fi/avoindata/kayttoehdot/avoimen-tietokannan-lisenssi#.WgCfiWiCxPY

Ainuttakaan ohjelman luomaa karttaa ei ole tarkistettu/varmistettu. Ne näyttävät olevan kunnossa, mutta näitä ei tule käyttää navigointiin. Ainakaan ainoana karttana :)


Ohjelma luo bittikartat sekä niihin liittyvät konfiguraatiotiedostot. OpenCPN muunnokseen tarvitset lisäksi imgkap-ohjelman.

Scripti ei ole erityisen versioriippuvainen ja toiminee kaikilla 3.x pythoneilla. Tarvitset lisäksi muutaman kirjaston. 

Taustaa:
https://www.fe83.org/gallery/view_album.php?set_albumName=album675

Hyödyllistä myös asentaa imagemagick, millä voi käsittellä haettujen bittikarttojen väripaletin ennen KAP konversiota. Ilman tuota karttojen värisävyt saattavat vaihdella paljonkin (yksittäin tehtyjen imgkap.exe konversioiden jäljiltä)


Workflow:

Määrittele haluamasi karttapoiminnat csv-tiedostoon. Joko kokonana uusi poiminta tai poista tekemistäni tiedostoista kommenttimerkinnät haluamistasi karttalehdistä.

Aja scripti, esim:

python MK_Get_Map_Tiles.py MK_A_data.csv
tai
python MK_Get_Map_Tiles_Multithread.py MK_A_data.csv

Scripti tekee myös makekap.BAT tiedoston, minkä voi ajaa suoraan (olettaa että KAP tiedostot kopioidaan alihakemistoon "128_Colors") tai mistä voi katsoa mallia, miten seuraavat vaiheet tehdään.

Konvertoi kartan väripaletti (esim.) komennolla:

magick kartan_nimi.png -remap palette.png kartan_uusi_nimi.png

Tuossa uudelle kartalle tulee palette.png tiedostossa olevat värisävyt, jolloin kaikki kartat näyttävät yhdenmukaisilta.

Lopuksi tehdään .png > .KAP -konversio komennolla:

imgkap.exe kartan_nimi.png kartan_konfiguraatio_tiedosto.txt

Poista lopuksi makekap.BAT (scripti sisää siihen aina uusia rivejä kun ohjelma ajetaan).

...minkä lopputuloksena syntyy geokoodattu KAP tiedosto, minkä voi avata OpenCPN softalla.

Ohjelma luo paljon WMTS_alkuisia.png tiedostoja (A, B, C ja D sarjoista näitä syntyy noin 80t kpl). Nämä voi huoleta poistaa konversion jälkeen. Ohjelman voi myös ajaa samalla lähtötiedolla useamman kerran (tällöin vain syntyy uudelleen saman nimiset aineistot). Ohjelman voi myös keskeyttää ja aloittaa uudelleen (huom. multithread ohjelmaa on vaikeampi keskeyttää, koska se ei juuri vastaa Ctrl-C komentoon).

Kannattanee harjoitella muutamalla karttalehdellä ja ehkä muutenkin poimia aineistot osissa. Yksittäisen karttalehteen joutuu hakemaan noin 1000 karttatiiltä, mihin kuluu aikaa ehkä reilu kymmenisen minuuttia. Multithread -versio tekee saman puolessa minuutissa.

Karttoja oikeellisuutta ei edelleenkään ole varmistettu mitenkään. Ne vaikuttavat olevan kunnossa, mutta tuosta ei ole mitään takuita. ei navigointiin.

Huom: En ole keksinyt miten KAP tiedostoihin saisi "Läpinäkyvän värin". Jos karttatiilien haku menee yli aineistorajan, karttaan syntyy valkoinen reunus, mikä näkyy myös lopullisessa KAP-kartassa. Tästä johtuen esimerkiksi erikoiskarttojen poiminnassa joutuu rajaamaan poiminnan sellaiseksi että mukaan otetaan vain kokonaan erikoiskartan sisään mahtuvat karttatiilet. 

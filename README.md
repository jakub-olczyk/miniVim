# miniVim

Bardzo prosty edytor tekstowy zainspirowany działaniem klasycznego edytora Vi.
Napisany jako projekt zaliczeniowy z przedmiotu "Wzorce projektowe" z
wykorzytaniem:

* modułu do Pythona `curses` 
* oryginalnego Vima

Wzorce projektowe wykorzystanie w projekcie:

* Polecenie
* Singleton 
* Most
* Dekorator

## Obsługa

Poruszanie się po buforze odbywa się za pomocą klawiszy:

		    ^
	< h  j  k  l >
		 v

Zgodnie z tym co na obrazku powyżej oraz sposobem poruszania się w oryginalnym
Vi.

Dodatkowo można przeskakiwać pomiędzy słowami. Jeśli jesteśmy w linijce jak ta
(`^` wskazuje na pozycję kursora):

	Linijka tekstu dla przykladu.
	  ^

Po wciśnięciu `ww` znajdziemy się:

	Linijka tekstu dla przykladu.
	               ^

Ponieważ ta komenda przeskakuje na początek następnego słowa w linijce.
Naciskając `b` sytuacja będzie wyglądać następująco:

	Linijka tekstu dla przykladu.
	        ^
`b` przeskakuje na tej samej zasadzie co `w` tylko w drugą stronę.

### Wprowadzanie tekstu

Aby wprowadzić tekst można skorzystać z komend `i`, `I`, `A` oraz `o`, które
działają tak jak w Vi.

* `i`, `I` wchodzą w tryb Insert. `I` przeskakuje do początku linii przed wejściem.
  `i` - pozwala na wejście w tryb wprowadzania tekstu pod kursorem.
* `A` pozwala na wprowadzenie tekstu po przeskoku do końca linii.
* `o` przeskakuje do następnej linii i wchodzi w tryb Insert

### Usuwanie tekstu

Służą do tego polecenia `d` oraz `D`. `D` usuwa tekst od kursora do końca
linii. Natomiast `d` potrzebuje jeszcze jednego argumentu przed wykonaniem, a
mianowicie kierunku. Zgodnie z komendami do poruszania.

#### Przykład. Usuwanie poziome

	Przykladowa linijka tekstu.
	    ^
(`^` wskazuje pozycję kursora w linii).

Można teraz wykonać dwa polecenia zmieniające obecną linijkę:
1. `dl` - usunie literę, na którą wskazuje kursor.
2. `dh` - usunie literę z przed kursora.

Po wykonaniu 1. 

	Przyladowa linijka tekstu.
	    ^

Po wykonaniu 2.

	Przkladowa linijka tekstu.
	   ^

### Podmiana tekstu

Komenda, która jest wywoływana w inny sposób w oryginalnym Vi -- `s` służy do
podmiany tekstu w obecnej linii. Po jej naciśnięciu w pasku na dole ekranu
pojawia się zachętka `s/`. Poprawna składnia komendy wygląda następująco:

	s/<stary_tekst>/<nowy_tekst>/

Przy czym ostatni `/` nie jest wymagany. Pierwsze wystąpienie <starego_tekstu>
jest podmieniane na <nowy_tekst>.

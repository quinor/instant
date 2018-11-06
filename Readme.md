# InstC

Kompilator języka Instant do LLVM oraz JVM.


## Uruchamianie
* Kompilator napisany jest w języku Python, nie wymaga więc budowania. Ponieważ jednak używa on
  zewnętrznych bibliotek, należy je zainstalować. Polecam użyć w tym celu narzędzia `venv`.
  Polecenie `make` zainicjalizuje takie środowisko wirtualne, które należy potem załadować
  poleceniem `. ./activate`.
* Polecenia `insc_llvm` i `insc_jvm` (kompilatory) nie będą działać, jeśli zostaną przeniesione
  do innego katalogu. Aby temu zapobiec, należałoby dodać bibliotekę `instc` do `PYTHONPATH`.
  Dodatkowo oba kompilatory mają wbudowane dodatkowe (niewymagane w zadaniu) argumenty i prostą
  pomoc dostępną po wywołaniu `insc_<target> -h`.

## Struktura kompilatorów i kwestie techniczne
* Ze względu na konwencje Pythona źródła nie są umieszczone w katalogu `src`, ale `instc`, będącym
  także nazwą biblioteki implementującej kompilatory.
* Do parsowania używam biblioteki `parsy`, będącej analogiem Hasellowej biblioteki `parsec`.
* W katalogu `lib` znajduje się narzędzie `jasmin.jar`, którego używam jako assemblera JVM.
* Poza wyżej wymienionymi narzędziami kompilator używa javy (polecenie `java`) oraz llvm'a
  (polecenie `llvm-as`).
* W pliku `instc/resources.py` znajdują się stałe kawałki kodu assemblera użwane do generowania
  plików wyjściowych.

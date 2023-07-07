# WFI_23L_Projekt_InvertedPendulum
Oto projekt *symulacja odwróconego wahadła* zaliczający przedmiot WFIT zaprezentowany w dniu 22.06.2023. 

## Autorzy 
- Anna Muszyńska
- Igor Czunikin-Krasowicki

## Działanie
Program otwiera interfejs użytkownika, który umożliwia edycję parametrów symulacji. Po kliknięciu przycisku "Symulacja", program generuje animację zapisywaną jako plik MP4 "Animacja.mp4" i automatycznie ją odtwarza.

## Dodatkowe informacje
Aby korzystać z programu, należy pobrać wszystkie niezbędne biblioteki. Wersja InvertedPendulumFast oferuje szybsze działanie poprzez uruchamianie renderowanie klatek symulacji w osobnych procesach, ale jako że pierwszy raz korzystałem z multiprocessingu jest to wersja nieco bardziej eksperymentalna (dodatkowa biblioteka: multiprocessing).

"""
Jesteś informatykiem w firmie Noe's Animals Redistribution Center.
Firma ta zajmuje się międzykontynentalnym przewozem zwierząt.
---------
Celem zadania jest przygotowanie funkcji pozwalającej na przetworzenie
pliku wejściowego zawierającego listę zwierząt do trasnportu.
Funkcja ma na celu wybranie par (samiec i samica) z każdego gatunku,
tak by łączny ładunek był jak najlżeszy (najmniejsza masa osobnika
rozpatrywana jest względem gatunku i płci).
---------
Na 1 pkt.
Funkcja ma tworzyć plik wyjściowy zwierający listę wybranych zwierząt
w formacie wejścia (takim samym jak w pliku wejściowym).
Wyjście ma być posortowane alfabetycznie względem gatunku,
a następnie względem nazwy zwierzęcia.
---------
Na +1 pkt.
Funkcja ma opcję zmiany formatu wejścia na:
"<id>_<gender>_<mass>"
(paramter "compressed") gdzie:
- "id" jest kodem zwierzęcia (uuid),
- "gender" to jedna litera (F/M)
- "mass" zapisana jest w kilogramach w notacji wykładniczej
z dokładnością do trzech miejsc po przecinku np. osobnik ważący 456 gramów
ma mieć masę zapisaną w postaci "4.560e-01"
---------
Na +1 pkt.
* Ilość pamięci zajmowanej przez program musi być stałą względem
liczby zwierząt.
* Ilość pamięci może rosnąć liniowo z ilością gatunków.
---------
UWAGA: Możliwe jest wykonanie tylko jednej opcji +1 pkt.
Otrzymuje się wtedy 2 pkt.
UWAGA 2: Wszystkie jednoski masy występują w przykładzie.
"""
from pathlib import Path
import pandas as pd


def select_animals(inputPath, outputPath, compressed=False):
    with open(inputPath) as _input:
        df = pd.read_csv(_input, delimiter=',', quotechar='*')
        mass = df['mass'].str.split(' ', n=1, expand=True)
        df['mass'] = mass[0].astype('float')
        df['unit'] = mass[1]

        units = {'kg': 1, 'g': 1e-3, 'mg': 1e-6, 'Mg': 1e3}
        for unit, scientificNotation in units.items():
            df.loc[df.unit == unit, 'mass'] = df['mass'] * scientificNotation
            df.loc[df.unit == unit, 'scientificNotation'] = scientificNotation

        df = df.loc[df.groupby(['genus', 'gender'])['mass'].idxmin()]
        if compressed:
            df['gender'] = df['gender'].map({'female': 'F', 'male': 'M'})
            df['uuid_gender_mass'] = df['id'] + '_' + df['gender'] + df['mass'].map(lambda x: '_{:.3e}'.format(x))
            df = df['uuid_gender_mass']
        else:
            df['mass'] = df['mass'] / df['scientificNotation']
            df['mass'] = df['mass'].astype(str) + ' ' + df['unit']
            df = df.drop(columns=['scientificNotation', 'unit'])

    with open(outputPath, 'w+', newline='') as _output:
        if compressed:
            df.to_csv(_output, index=False, header=True)
        else:
            df.to_csv(_output, index=False)


if __name__ == '__main__':
    input_path = Path('s_animals.txt')
    output_path = Path('s_animals_s.txt')
    select_animals(input_path, output_path)
    with open(output_path) as generated:
        with open('s_animals_se.txt') as expected:
            assert generated.read() == expected.read()

    output_path = Path('s_animals_sc.txt')
    select_animals(input_path, output_path, True)
    with open(output_path) as generated:
        with open('s_animals_sce.txt') as expected:
            assert generated.read() == expected.read()

/* jak komus cos nie pasuje to smialo mozecie poprawiac. To narazie tylko zarys mysle ze te varchary mozna zmniejszyc z 50/100
ewentualnie pozmieniac niektore nazwy bo czasami nie wiadomo o co chodzi */

CREATE TABLE pracownicy (
    id_pracownika INT AUTO_INCREMENT PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    numer_telefonu VARCHAR(12),
    kod_pocztowy VARCHAR(10),
    miasto VARCHAR(50),
    ulica  VARCHAR(100),
    wynagrodzenie DECIMAL(10,2)
);

CREATE TABLE sponsorzy (
    id_sponsora INT AUTO_INCREMENT PRIMARY KEY,
    nazwa_firmy VARCHAR(50),
    numer_telefonu VARCHAR(12)
);

CREATE TABLE  sponsorzy_umowy (
    id_umowy INT AUTO_INCREMENT PRIMARY KEY,
    id_sponsora INT,
    id_chomika INT, 
    rozpoczecie_umowy DATE,
    koniec_umowy DATE,
    kwota DECIMAL(10,2),
);

CREATE TABLE finansowanie (
    id_finansowania INT AUTO_INCREMENT PRIMARY KEY,
    zrodlo VARCHAR(100),
    kwota DECIMAL(10,2),
    data_finansowania DATE
);

CREATE TABLE zawody (
    id_zawodow INT AUTO_INCREMENT PRIMARY KEY,
    data_zawodow DATE,
    nazwa VARCHAR(200),
    lokalizacja VARCHAR(200),
    pula_nagrod DECIMAL(10,2)
);

CREATE TABLE konkurencje (
    id_konkurencji INT AUTO_INCREMENT PRIMARY KEY,
    nazwa_konkurencji VARCHAR(100),
    formula VARCHAR(200)
);

CREATE TABLE chomiki (
    id_chomika INT AUTO_INCREMENT PRIMARY KEY,
    data_urodzenia DATE,
    data_smierci DATE,
    imie VARCHAR(50),
    rasa VARCHAR(50),
    kolor VARCHAR(50),
    waga DECIMAL(5,2),
    wzrost DECIMAL(5,2),
    plec CHAR(1)
);

CREATE TABLE wyniki_zawodow (
    id_startu INT AUTO_INCREMENT PRIMARY KEY,
    id_zawodow INT,
    id_konkurencji INT,
    id_chomika INT,
    zajete_miejsce INT,
    czas DECIMAL(6,2),
    punkty INT
);

CREATE TABLE substancje_zakazane (
    id_substancji INT AUTO_INCREMENT PRIMARY KEY,
    nazwa VARCHAR(100)
);

CREATE TABLE kontrole (
    id_kontroli INT AUTO_INCREMENT PRIMARY KEY,
    id_zawodow INT,
    id_chomika INT,
    data_kontroli DATE,
    wynik_kontroli BOOLEAN
);

CREATE TABLE wyniki_kontroli (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_kontroli INT,
    id_substancji INT
);









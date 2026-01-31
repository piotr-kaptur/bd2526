CREATE TABLE Pracownicy (
    id_pracownika INT PRIMARY KEY AUTO_INCREMENT,
    imię VARCHAR(50),
    nazwisko VARCHAR(50),
    numer_telefonu VARCHAR(12),
    kod_pocztowy VARCHAR(10),
    miasto VARCHAR(50),
    ulica  VARCHAR(100),
    wynagrodzenie INT
);

CREATE TABLE Sponsorzy (
    id_sponsora INT PRIMARY KEY AUTO_INCREMENT,
    nazwa_firmy VARCHAR(50),
    numer_telefonu VARCHAR(12)
);

CREATE TABLE Umowy_Sponsorskie (
    id_umowy INT PRIMARY KEY AUTO_INCREMENT,
    id_sponsora INT,
    id_chomika INT,
    data_rozpoczęcia DATE,
    data_zakończenia DATE,
    kwota INT
);

CREATE TABLE Dofinansowania (
    id_dofinansowania INT PRIMARY KEY AUTO_INCREMENT,
    źródło VARCHAR(50),
    kwota INT,
    data_dofinansowania DATE
);

CREATE TABLE Zawody (
    id_zawodów INT PRIMARY KEY AUTO_INCREMENT,
    lokalizacja VARCHAR(50),
    pula_nagród INT,
    data_zawodów DATE
);

CREATE TABLE Konkurencje (
    id_konkurencji INT PRIMARY KEY AUTO_INCREMENT,
    nazwa VARCHAR(50),
    formuła VARCHAR(10)
);

CREATE TABLE Wyniki_Zawodów (
    id_wyniku INT PRIMARY KEY AUTO_INCREMENT,
    id_zawodów INT,
    id_konkurencji INT,
    id_chomika INT,
    zajęte_miejsce INT,
    czas TIME(2),
    punkty INT
);


CREATE TABLE Chomiki (
    id_chomika INT PRIMARY KEY AUTO_INCREMENT,
    data_urodzenia DATE,
    data_śmierci DATE,
    imię VARCHAR(50),
    rasa VARCHAR(20),
    kolor VARCHAR(20),
    waga INT,
    wzrost INT,
    płeć VARCHAR(1)
);

CREATE TABLE Zakazane_substancje (
    id_substancji INT PRIMARY KEY AUTO_INCREMENT,
    nazwa VARCHAR(50)

);

CREATE TABLE Kontrole (
    id_kontroli INT PRIMARY KEY AUTO_INCREMENT,
    id_zawodów INT,
    id_chomika INT,
    czy_pozytywny BOOLEAN

);

CREATE TABLE Wyniki_Kontroli (
    id_wyniku INT PRIMARY KEY AUTO_INCREMENT,
    id_kontroli INT,
    id_substancji INT

);


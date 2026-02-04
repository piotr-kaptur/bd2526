CREATE PROCEDURE generate_tables()
BEGIN
    DROP TABLE IF EXISTS
    `wyniki_kontroli`,
    `kontrole`,
    `substancje_zakazane`,
    `wyniki_zawodow`,
    `chomiki`,
    `konkurencje`,
    `zawody`,
    `finansowanie`,
    `sponsorzy_umowy`,
    `sponsorzy`,
    `pracownicy`;
    CREATE TABLE pracownicy (
        id_pracownika INT AUTO_INCREMENT PRIMARY KEY,
        imie VARCHAR(50),
        nazwisko VARCHAR(50),
        numer_telefonu VARCHAR(12),
        miasto VARCHAR(50),
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
        kwota DECIMAL(10,2)
    );

    CREATE TABLE finansowanie (
        id_finansowania INT AUTO_INCREMENT PRIMARY KEY,
        kwota DECIMAL(10,2),
        data_finansowania DATE
    );

    CREATE TABLE zawody (
        id_zawodow INT AUTO_INCREMENT PRIMARY KEY,
        id_konkurencji INT,
        nazwa VARCHAR(200),
        data_zawodow DATE,
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
        imie VARCHAR(50),
        rasa VARCHAR(50),
        kolor VARCHAR(50),
        waga DECIMAL(5,2),
        wzrost DECIMAL(5,2),
        plec CHAR(1),
        data_urodzenia DATE,
        data_smierci DATE
    );

    CREATE TABLE wyniki_zawodow (
        id_startu INT AUTO_INCREMENT PRIMARY KEY,
        id_zawodow INT,
        id_chomika INT,
        czas DECIMAL(6,2)
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
        substancje_zakazane VARCHAR(100)
    );
END



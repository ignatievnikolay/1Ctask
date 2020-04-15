DROP TABLE Room;
DROP TABLE User;
DROP TABLE Booking;

CREATE TABLE Room (
    id TEXT PRIMARY KEY,
    num INTEGER,
    floor INTEGER,
    num_seats INTEGER
);

INSERT INTO Room
VALUES (1, 101, 1, 10);

CREATE TABLE User (
    id TEXT PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50)
);

INSERT INTO User
VALUES (1, 'Vasya', 'Pupkin');

CREATE TABLE Booking (
    id TEXT PRIMARY KEY,
    room_id TEXT,
    time_begin TEXT,
    time_end TEXT,
    booker_id TEXT,
    num_people INTEGER
);
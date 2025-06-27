CREATE DATABASE gamingzone;
USE gamingzone;
CREATE TABLE Games (
    GameID INT PRIMARY KEY AUTO_INCREMENT,
    GameName VARCHAR(50),
    GameType VARCHAR(30),
    ChargePerHour DECIMAL(5,2)
);

CREATE TABLE Memberships (
    MembershipID INT PRIMARY KEY AUTO_INCREMENT,
    MembershipType VARCHAR(20), -- Yearly / Monthly / Daily
    TotalHours INT
);

CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT,
    MemberName VARCHAR(50),
    MembershipID INT,
    HoursSpent INT DEFAULT 0,
    FOREIGN KEY (MembershipID) REFERENCES Memberships(MembershipID)
);

CREATE TABLE GamePlay (
    PlayID INT PRIMARY KEY AUTO_INCREMENT,
    MemberID INT,
    GameID INT,
    HoursPlayed INT,
    PlayDate DATE,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (GameID) REFERENCES Games(GameID)
);

INSERT INTO Games (GameName, GameType, ChargePerHour)
VALUES 
('FIFA 22', 'Sports', 100.00),
('Call of Duty', 'Action', 150.00),
('Candy Crush', 'Puzzle', 50.00),
('Need for Speed', 'Racing', 120.00);

INSERT INTO Memberships (MembershipType, TotalHours)
VALUES 
('Yearly', 500),
('Monthly', 100),
('Daily', 10);

INSERT INTO Members (MemberName, MembershipID, HoursSpent)
VALUES 
('Alice', 1, 150),
('Bob', 2, 40),
('Charlie', 3, 5),
('David', 2, 70),
('Eva', 1, 200);

INSERT INTO GamePlay (MemberID, GameID, HoursPlayed, PlayDate)
VALUES 
(1, 1, 5, '2025-06-01'),
(2, 2, 2, '2025-06-02'),
(3, 3, 1, '2025-06-03'),
(4, 1, 3, '2025-06-04'),
(5, 4, 4, '2025-06-05'),
(1, 2, 2, '2025-06-06'),
(2, 1, 1, '2025-06-07'),
(5, 1, 3, '2025-06-08');

SHOW TABLES FROM gamingzone;

USE gamingzone;
SHOW TABLES;
DESC members;

CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    membership_id INT,
    hours_spent INT DEFAULT 0,
    FOREIGN KEY (membership_id) REFERENCES memberships(id)
);

CREATE TABLE play_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    game_id INT,
    hours_played INT,
    FOREIGN KEY (member_id) REFERENCES members(id),
    FOREIGN KEY (game_id) REFERENCES games(id)
);
CREATE TABLE play_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT,
    game_id INT,
    hours_played INT,
    FOREIGN KEY (member_id) REFERENCES members(MemberID),
    FOREIGN KEY (game_id) REFERENCES games(GameID)
);
DESC members;
DESC games;
DESC members;
DESC memberships;
SET SQL_SAFE_UPDATES = 0;

UPDATE members SET MemberName = 'Niha' WHERE MemberName = 'Bhavna';
UPDATE members SET MemberName = 'Jhara' WHERE MemberName = 'Sunidhi';

SET SQL_SAFE_UPDATES = 1;

SELECT * FROM gameplay WHERE MemberID = (
  SELECT MemberID FROM members WHERE MemberName = 'Niha'
);
SELECT * FROM gameplay 
WHERE MemberID IN (
  SELECT MemberID FROM members WHERE MemberName = 'Niha'
);
SELECT MemberID, MemberName FROM members WHERE MemberName = 'Niha';

CREATE DATABASE VirtualArtGalleryy;
USE VirtualArtGalleryy;

CREATE TABLE Artwork (
    ArtworkID INT PRIMARY KEY,
    Title VARCHAR(100),
    Description TEXT,
    CreationDate DATE,
    Medium VARCHAR(50),
    ImageURL VARCHAR(255),
    ArtistID INT,
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID)
);

CREATE TABLE Artist (
    ArtistID INT PRIMARY KEY,
    Name VARCHAR(100),
    Biography TEXT,
    BirthDate DATE,
    Nationality VARCHAR(50),
    Website VARCHAR(100),
    ContactInformation VARCHAR(100)
);

CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50),
    Password VARCHAR(50),
    Email VARCHAR(100),
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    ProfilePicture VARCHAR(255)
);

CREATE TABLE FavoriteArtworks (
    UserID INT,
    ArtworkID INT,
    PRIMARY KEY (UserID, ArtworkID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID)
);

CREATE TABLE Gallery (
    GalleryID INT PRIMARY KEY,
    Name VARCHAR(100),
    Description TEXT,
    Location VARCHAR(100),
    Curator INT,
    OpeningHours VARCHAR(100),
    FOREIGN KEY (Curator) REFERENCES Artist(ArtistID)
);
CREATE TABLE Artwork_Gallery (
    ArtworkID INT,
    GalleryID INT,
    PRIMARY KEY (ArtworkID, GalleryID),
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID),
    FOREIGN KEY (GalleryID) REFERENCES Gallery(GalleryID)
);

INSERT INTO Artist VALUES
(1, 'M.F. Husain', 'Modern Indian painter', '1915-09-17', 'Indian', 'https://mfhusain.com', 'contact@husain.com'),
(2, 'S.H. Raza', 'Known for spiritual abstract art', '1922-02-22', 'Indian', 'https://shraza.in', 'info@raza.com'),
(3, 'Jamini Roy', 'Folk and tribal art of India', '1887-04-11', 'Indian', 'https://jaminir.in', 'jamini@art.in'),
(4, 'Amrita Sher-Gil', 'Modern Indian artist with European influence', '1913-01-30', 'Indian', 'https://amritashergil.in', 'amrita@art.in'),
(5, 'Anjolie Ela Menon', 'Indian contemporary artist', '1940-07-17', 'Indian', 'https://anjoliemenon.in', 'anjolie@art.in');

INSERT INTO User VALUES
(1, 'ravi123', 'pass123', 'ravi@example.com', 'Ravi', 'Kumar', '1999-04-21', 'ravi.jpg'),
(2, 'anjali456', 'pass456', 'anjali@example.com', 'Anjali', 'Mehta', '1998-10-10', 'anjali.jpg'),
(3, 'nikita789', 'pass789', 'nikita@example.com', 'Nikita', 'Shah', '1997-07-15', 'nikita.jpg'),
(4, 'arjun321', 'pass321', 'arjun@example.com', 'Arjun', 'Verma', '2000-12-05', 'arjun.jpg'),
(5, 'neha654', 'pass654', 'neha@example.com', 'Neha', 'Iyer', '1995-03-25', 'neha.jpg');
DROP TABLE IF EXISTS Artwork;
DROP TABLE IF EXISTS FavoriteArtworks;
DROP TABLE IF EXISTS Artwork_Gallery;

DROP TABLE IF EXISTS Artwork;

INSERT INTO Artwork (
    ArtworkID, Title, Description, CreationDate, Medium, ImageURL, ArtistID
) VALUES
(101, 'Bharat Mata', 'Iconic nationalist painting', '1905-08-15', 'Watercolor', 'bharatmata.jpg', 1),
(102, 'Bindu', 'Spiritual abstract circle', '1980-01-01', 'Acrylic', 'bindu.jpg', 2),
(103, 'Mother Teresa', 'Modern painting tribute', '1990-04-25', 'Oil', 'motherteresa.jpg', 1),
(104, 'Three Pujarins', 'Folk women worshippers', '1940-05-01', 'Tempera', 'pujarins.jpg', 3),
(105, 'Self Portrait', 'Early expressionist piece', '1931-03-10', 'Oil', 'selfportrait.jpg', 4);

INSERT INTO FavoriteArtworks VALUES
(1, 101),
(2, 102),
(3, 103),
(4, 104),
(5, 105);

INSERT INTO Gallery VALUES
(1, 'National Gallery of Modern Art', 'India''s top modern art museum', 'New Delhi', 1, '10 AM - 6 PM'),
(2, 'Contemporary Canvas', 'Showcases digital art', 'Mumbai', 2, '11 AM - 7 PM'),
(3, 'Tribal Expressions', 'Focus on indigenous art', 'Kolkata', 3, '9 AM - 5 PM'),
(4, 'Urban Art Hub', 'Experimental art zone', 'Bangalore', 4, '10 AM - 8 PM'),
(5, 'Classic Visions', 'Gallery of timeless paintings', 'Chennai', 5, '11 AM - 6 PM');

INSERT INTO Artwork_Gallery VALUES
(101, 1),
(102, 2),
(103, 1),
(104, 3),
(105, 4);

SELECT * FROM Artwork;
SELECT * FROM Artist;
SELECT * FROM User;
SELECT * FROM FavoriteArtworks;
SELECT * FROM Gallery;
SELECT * FROM Artwork_Gallery;

SHOW TABLES;
RENAME TABLE Artist TO artist;
DROP TABLE artist;
SHOW DATABASES;
ALTER TABLE Artist MODIFY COLUMN ArtistID INT AUTO_INCREMENT PRIMARY KEY;
ALTER TABLE Artist MODIFY ArtistID INT AUTO_INCREMENT;
ALTER TABLE Artist MODIFY ArtistID INT AUTO_INCREMENT;
ALTER TABLE Gallery DROP FOREIGN KEY gallery_ibfk_1;
ALTER TABLE Artist MODIFY ArtistID INT AUTO_INCREMENT;
ALTER TABLE Gallery DROP FOREIGN KEY gallery_ibfk_1;
ALTER TABLE Artwork DROP FOREIGN KEY artwork_ibfk_1;
ALTER TABLE Artist MODIFY ArtistID INT AUTO_INCREMENT;
ALTER TABLE Gallery
ADD CONSTRAINT gallery_ibfk_1
FOREIGN KEY (Curator) REFERENCES Artist(ArtistID);

ALTER TABLE Artwork
ADD CONSTRAINT artwork_ibfk_1
FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID);
USE VirtualArtGalleryy;
SELECT * FROM Artist;
SELECT database();













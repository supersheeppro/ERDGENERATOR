DROP DATABASE IF EXISTS minecraft;
CREATE DATABASE minecraft;
USE minecraft;

CREATE TABLE Speler (
  SpelerID INT AUTO_INCREMENT NOT NULL,
  Gebruikersnaam VARCHAR(100) NOT NULL UNIQUE,
  UUID CHAR(36) NOT NULL UNIQUE,
  EersteLogin DATETIME NOT NULL,
  LaatsteLogin DATETIME,
  IsBanned BOOLEAN NOT NULL,
  Ervaring INT NOT NULL,
  Level INT NOT NULL,
  Health FLOAT NOT NULL,
  Mana FLOAT NOT NULL,
  PRIMARY KEY (SpelerID)
);

CREATE TABLE Wereld (
  WereldID INT AUTO_INCREMENT NOT NULL,
  Naam VARCHAR(100) NOT NULL UNIQUE,
  Seed BIGINT NOT NULL,
  Type VARCHAR(50) NOT NULL,
  CreatorSpelerID INT UNIQUE,
  Grootte VARCHAR(50),
  Moeilijkheidsgraad ENUM('Peaceful', 'Easy', 'Normal', 'Hard') NOT NULL,
  IsMultiplayer BOOLEAN NOT NULL,
  MaxSpelers INT,
  Tijdsinstelling ENUM('Dag', 'Nacht', 'Standaard'),
  PVPEnabled BOOLEAN NOT NULL,
  SpawnBeschermd BOOLEAN NOT NULL,
  PRIMARY KEY (WereldID),
  FOREIGN KEY (CreatorSpelerID) REFERENCES Speler(SpelerID)
);

CREATE TABLE Item (
  ItemID INT AUTO_INCREMENT NOT NULL,
  Naam VARCHAR(100) NOT NULL,
  ItemType VARCHAR(50) NOT NULL,
  MaxStack INT NOT NULL,
  Durability INT,
  PRIMARY KEY (ItemID)
);

CREATE TABLE SpelerInventaris (
  InventarisID INT AUTO_INCREMENT NOT NULL,
  SpelerID INT NOT NULL UNIQUE,
  ItemID INT NOT NULL,
  Aantal INT NOT NULL,
  PositieInInventaris INT NOT NULL,
  PRIMARY KEY (InventarisID),
  FOREIGN KEY (SpelerID) REFERENCES Speler(SpelerID),
  FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE Positie (
  PositieID INT AUTO_INCREMENT NOT NULL,
  SpelerID INT NOT NULL,
  WereldID INT NOT NULL,
  X FLOAT NOT NULL,
  Y FLOAT NOT NULL,
  Z FLOAT NOT NULL,
  Rotatie FLOAT,
  Timestamp DATETIME NOT NULL,
  PRIMARY KEY (PositieID),
  FOREIGN KEY (SpelerID) REFERENCES Speler(SpelerID),
  FOREIGN KEY (WereldID) REFERENCES Wereld(WereldID)
);

CREATE TABLE Ban (
  BanID INT AUTO_INCREMENT NOT NULL,
  SpelerID INT NOT NULL,
  Reden VARCHAR(255) NOT NULL,
  StartDatum DATETIME NOT NULL,
  EindDatum DATETIME,
  Permanent BOOLEAN NOT NULL,
  PRIMARY KEY (BanID),
  FOREIGN KEY (SpelerID) REFERENCES Speler(SpelerID)
);

CREATE TABLE CraftingRecept (
  ReceptID INT AUTO_INCREMENT NOT NULL,
  ResultaatItemID INT NOT NULL,
  Aantal INT NOT NULL,
  Beschrijving TEXT,
  PRIMARY KEY (ReceptID),
  FOREIGN KEY (ResultaatItemID) REFERENCES Item(ItemID)
);

CREATE TABLE CraftingReceptIngredient (
  ReceptIngredientID INT AUTO_INCREMENT NOT NULL,
  ReceptID INT NOT NULL,
  ItemID INT NOT NULL,
  Aantal INT NOT NULL,
  PRIMARY KEY (ReceptIngredientID),
  FOREIGN KEY (ReceptID) REFERENCES CraftingRecept(ReceptID),
  FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);

CREATE TABLE Structuur (
  StructuurID INT AUTO_INCREMENT NOT NULL,
  WereldID INT NOT NULL,
  Naam VARCHAR(100) NOT NULL,
  MakerSpelerID INT NOT NULL,
  LocatieX FLOAT NOT NULL,
  LocatieY FLOAT NOT NULL,
  LocatieZ FLOAT NOT NULL,
  DatumGemaakt DATETIME NOT NULL,
  PRIMARY KEY (StructuurID),
  FOREIGN KEY (WereldID) REFERENCES Wereld(WereldID),
  FOREIGN KEY (MakerSpelerID) REFERENCES Speler(SpelerID)
);

CREATE TABLE Achievement (
  AchievementID INT AUTO_INCREMENT NOT NULL,
  Naam VARCHAR(100) NOT NULL,
  Beschrijving TEXT,
  PRIMARY KEY (AchievementID)
);

CREATE TABLE SpelerAchievement (
  SpelerAchievementID INT AUTO_INCREMENT NOT NULL,
  SpelerID INT NOT NULL,
  AchievementID INT NOT NULL,
  DatumBehaald DATETIME NOT NULL,
  PRIMARY KEY (SpelerAchievementID),
  FOREIGN KEY (SpelerID) REFERENCES Speler(SpelerID),
  FOREIGN KEY (AchievementID) REFERENCES Achievement(AchievementID)
);

CREATE TABLE Vrienden (
  VriendschapID INT AUTO_INCREMENT NOT NULL,
  SpelerID1 INT NOT NULL,
  SpelerID2 INT NOT NULL,
  DatumToegevoegd DATETIME NOT NULL,
  Status VARCHAR(20) NOT NULL,
  PRIMARY KEY (VriendschapID),
  FOREIGN KEY (SpelerID1) REFERENCES Speler(SpelerID),
  FOREIGN KEY (SpelerID2) REFERENCES Speler(SpelerID)
);

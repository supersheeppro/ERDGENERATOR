-- Speler CRUD SQL
-- READ
SELECT * FROM Speler WHERE SpelerID = %s;

-- INSERT
INSERT INTO Speler (Gebruikersnaam, UUID, EersteLogin, LaatsteLogin, IsBanned, Ervaring, Level, Health, Mana) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);

-- UPDATE
UPDATE Speler SET Gebruikersnaam = %s, UUID = %s, EersteLogin = %s, LaatsteLogin = %s, IsBanned = %s, Ervaring = %s, Level = %s, Health = %s, Mana = %s WHERE SpelerID = %s;

-- DELETE
DELETE FROM Speler WHERE SpelerID = %s;

-- Wereld CRUD SQL
-- READ
SELECT * FROM Wereld WHERE WereldID = %s;

-- INSERT
INSERT INTO Wereld (Naam, Seed, Type, CreatorSpelerID, Grootte, Moeilijkheidsgraad, IsMultiplayer, MaxSpelers, Tijdsinstelling, PVPEnabled, SpawnBeschermd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

-- UPDATE
UPDATE Wereld SET Naam = %s, Seed = %s, Type = %s, CreatorSpelerID = %s, Grootte = %s, Moeilijkheidsgraad = %s, IsMultiplayer = %s, MaxSpelers = %s, Tijdsinstelling = %s, PVPEnabled = %s, SpawnBeschermd = %s WHERE WereldID = %s;

-- DELETE
DELETE FROM Wereld WHERE WereldID = %s;

-- Item CRUD SQL
-- READ
SELECT * FROM Item WHERE ItemID = %s;

-- INSERT
INSERT INTO Item (Naam, ItemType, MaxStack, Durability) VALUES (%s, %s, %s, %s);

-- UPDATE
UPDATE Item SET Naam = %s, ItemType = %s, MaxStack = %s, Durability = %s WHERE ItemID = %s;

-- DELETE
DELETE FROM Item WHERE ItemID = %s;

-- SpelerInventaris CRUD SQL
-- READ
SELECT * FROM SpelerInventaris WHERE InventarisID = %s;

-- INSERT
INSERT INTO SpelerInventaris (SpelerID, ItemID, Aantal, PositieInInventaris) VALUES (%s, %s, %s, %s);

-- UPDATE
UPDATE SpelerInventaris SET SpelerID = %s, ItemID = %s, Aantal = %s, PositieInInventaris = %s WHERE InventarisID = %s;

-- DELETE
DELETE FROM SpelerInventaris WHERE InventarisID = %s;

-- Positie CRUD SQL
-- READ
SELECT * FROM Positie WHERE PositieID = %s;

-- INSERT
INSERT INTO Positie (SpelerID, WereldID, X, Y, Z, Rotatie, Timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s);

-- UPDATE
UPDATE Positie SET SpelerID = %s, WereldID = %s, X = %s, Y = %s, Z = %s, Rotatie = %s, Timestamp = %s WHERE PositieID = %s;

-- DELETE
DELETE FROM Positie WHERE PositieID = %s;

-- Ban CRUD SQL
-- READ
SELECT * FROM Ban WHERE BanID = %s;

-- INSERT
INSERT INTO Ban (SpelerID, Reden, StartDatum, EindDatum, Permanent) VALUES (%s, %s, %s, %s, %s);

-- UPDATE
UPDATE Ban SET SpelerID = %s, Reden = %s, StartDatum = %s, EindDatum = %s, Permanent = %s WHERE BanID = %s;

-- DELETE
DELETE FROM Ban WHERE BanID = %s;

-- CraftingRecept CRUD SQL
-- READ
SELECT * FROM CraftingRecept WHERE ReceptID = %s;

-- INSERT
INSERT INTO CraftingRecept (ResultaatItemID, Aantal, Beschrijving) VALUES (%s, %s, %s);

-- UPDATE
UPDATE CraftingRecept SET ResultaatItemID = %s, Aantal = %s, Beschrijving = %s WHERE ReceptID = %s;

-- DELETE
DELETE FROM CraftingRecept WHERE ReceptID = %s;

-- CraftingReceptIngredient CRUD SQL
-- READ
SELECT * FROM CraftingReceptIngredient WHERE ReceptIngredientID = %s;

-- INSERT
INSERT INTO CraftingReceptIngredient (ReceptID, ItemID, Aantal) VALUES (%s, %s, %s);

-- UPDATE
UPDATE CraftingReceptIngredient SET ReceptID = %s, ItemID = %s, Aantal = %s WHERE ReceptIngredientID = %s;

-- DELETE
DELETE FROM CraftingReceptIngredient WHERE ReceptIngredientID = %s;

-- Structuur CRUD SQL
-- READ
SELECT * FROM Structuur WHERE StructuurID = %s;

-- INSERT
INSERT INTO Structuur (WereldID, Naam, MakerSpelerID, LocatieX, LocatieY, LocatieZ, DatumGemaakt) VALUES (%s, %s, %s, %s, %s, %s, %s);

-- UPDATE
UPDATE Structuur SET WereldID = %s, Naam = %s, MakerSpelerID = %s, LocatieX = %s, LocatieY = %s, LocatieZ = %s, DatumGemaakt = %s WHERE StructuurID = %s;

-- DELETE
DELETE FROM Structuur WHERE StructuurID = %s;

-- Achievement CRUD SQL
-- READ
SELECT * FROM Achievement WHERE AchievementID = %s;

-- INSERT
INSERT INTO Achievement (Naam, Beschrijving) VALUES (%s, %s);

-- UPDATE
UPDATE Achievement SET Naam = %s, Beschrijving = %s WHERE AchievementID = %s;

-- DELETE
DELETE FROM Achievement WHERE AchievementID = %s;

-- SpelerAchievement CRUD SQL
-- READ
SELECT * FROM SpelerAchievement WHERE SpelerAchievementID = %s;

-- INSERT
INSERT INTO SpelerAchievement (SpelerID, AchievementID, DatumBehaald) VALUES (%s, %s, %s);

-- UPDATE
UPDATE SpelerAchievement SET SpelerID = %s, AchievementID = %s, DatumBehaald = %s WHERE SpelerAchievementID = %s;

-- DELETE
DELETE FROM SpelerAchievement WHERE SpelerAchievementID = %s;

-- Vrienden CRUD SQL
-- READ
SELECT * FROM Vrienden WHERE VriendschapID = %s;

-- INSERT
INSERT INTO Vrienden (SpelerID1, SpelerID2, DatumToegevoegd, Status) VALUES (%s, %s, %s, %s);

-- UPDATE
UPDATE Vrienden SET SpelerID1 = %s, SpelerID2 = %s, DatumToegevoegd = %s, Status = %s WHERE VriendschapID = %s;

-- DELETE
DELETE FROM Vrienden WHERE VriendschapID = %s;


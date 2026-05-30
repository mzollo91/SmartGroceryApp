USE GroceryPlannerDB;
GO -- finish creating/selecting the database before running scripts.

IF OBJECT_ID(N'dbo.Stores',N'U') IS NULL BEGIN --OBJECT_ID looks at the internal 
CREATE TABLE Stores(StoreID INT PRIMARY KEY IDENTITY(1,1), -- IDENTITY handles the auto incrementing ID. (1,1) means that the starting value will be 1 and it will increment by 1 for each row.
					StoreName NVARCHAR(100) NOT NULL,
					StreetAddress NVARCHAR(255),
					City NVARCHAR(100),
					[State] NVARCHAR(50),
					ZipCode NVARCHAR(10)); -- Using NVARCHAR for zip codes to keep leading zeros.
END

IF OBJECT_ID(N'dbo.Items',N'U') IS NULL BEGIN
CREATE TABLE Items(ItemID INT PRIMARY KEY IDENTITY(1,1),
					ItemName NVARCHAR(255) NOT NULL UNIQUE, -- UNIQUE will prevent duplicate entries
					WeightOrCount DECIMAL(10,2), -- DECIMAL arguments refer to the total digits in the float and the number of decimal places. In this case, 10 digits down to 2 decimals.
					Units NVARCHAR(50),
					DepartmentLocation NVARCHAR(100));
END

IF OBJECT_ID(N'dbo.Prices',N'U') IS NULL BEGIN
CREATE TABLE Prices(PriceID INT PRIMARY KEY IDENTITY(1,1),
					ItemID INT NOT NULL,
					StoreID INT NOT NULL,
					Price DECIMAL(10,2) NOT NULL,
					DateRecorded DATE DEFAULT GETDATE(), -- Defaults to today's date.

					CONSTRAINT FK_Price_Item FOREIGN KEY(ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE, -- Defining the Foreing Keys to link back to the other tables.
					CONSTRAINT FK_Price_Store FOREIGN KEY(StoreID) REFERENCES Stores(StoreID) ON DELETE CASCADE);
END

IF OBJECT_ID(N'dbo.StoreDistances',N'U') IS NULL BEGIN
CREATE TABLE StoreDistances(DistanceID INT PRIMARY KEY IDENTITY(1,1),
					StoreA_ID INT NOT NULL,
					StoreB_ID INT NOT NULL,
					TravelDistance_Minutes FLOAT NOT NULL,

					CONSTRAINT FK_StoreA_ID FOREIGN KEY(StoreA_ID) REFERENCES Stores(StoreID) ON DELETE CASCADE, -- Defining the Foreing Keys to link back to the other tables.
					CONSTRAINT FK_StoreB_ID FOREIGN KEY(StoreB_ID) REFERENCES Stores(StoreID) ON DELETE NO ACTION,
					CONSTRAINT UQ_Route UNIQUE (StoreA_ID,StoreB_ID));
END

-- Commands to alter constraints on the created tables
ALTER TABLE Prices
DROP CONSTRAINT FK_Price_Item;

ALTER TABLE Prices
ADD CONSTRAINT FK_Price_Item FOREIGN KEY (ItemID) REFERENCES Items(ItemID) ON DELETE CASCADE;

ALTER TABLE Prices
DROP CONSTRAINT FK_Price_Store;

ALTER TABLE Prices
ADD CONSTRAINT FK_Price_Store FOREIGN KEY (StoreID) REFERENCES Stores(StoreID) ON DELETE CASCADE;

DROP TABLE dbo.StoreDistances;

SET IDENTITY_INSERT dbo.Stores ON;
INSERT INTO dbo.Stores (StoreID, StoreName, StreetAddress, City, State, ZipCode) VALUES(1,'Home','123 My Street','Shrewsbury','PA','17361');
SET IDENTITY_INSERT dbo.Stores OFF;

UPDATE dbo.Stores SET StoreName = 'Home', StreetAddress = '123 My Street', City = 'Shrewsbury', State = 'PA', ZipCode = '17361' WHERE StoreID = 1;

SELECT * FROM dbo.Stores;
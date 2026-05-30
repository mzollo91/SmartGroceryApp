USE GroceryPlannerDB;
GO

CREATE VIEW View_CurrentPrices AS SELECT i.ItemName,
										 s.StoreName,
										 p.Price,
										 p.DateRecorded,
										 i.Units,
										 (p.Price / NULLIF(i.WeightOrCount,0)) AS PricePerUnit

										 FROM Prices p
										 JOIN Items i ON p.ItemID = i.ItemID
										 JOIN Stores s ON p.StoreID = s.StoreID;
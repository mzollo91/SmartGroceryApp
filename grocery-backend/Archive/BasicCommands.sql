USE GroceryPlannerDB;
GO

INSERT INTO dbo.Items(ItemName, WeightOrCount,Units,DepartmentLocation)
VALUES('Bread',20.00,'oz','Aisles');

SELECT* FROM dbo.Items

DELETE dbo.Items WHERE ItemID>0;
DBCC CHECKIDENT('dbo.Items',RESEED,0);
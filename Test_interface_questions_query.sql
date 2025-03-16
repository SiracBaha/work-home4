-- From left to right, you can test the questions located on gradio interface with your database.

--1
SELECT p.ProductID, p.ProductName, p.Price, s.SupplierName, c.CategoryName
FROM Products p
JOIN Suppliers s ON p.SupplierID = s.SupplierID
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE p.Price > 100;


--2
SELECT o.OrderID, o.CustomerID, o.OrderDate, o.ShipperID
FROM Orders o
WHERE o.EmployeeID = 4;


--3
SELECT o.OrderID, o.OrderDate, c.CustomerName
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderDate >= DATE('now', '-7 days');


--4
SELECT p.ProductName, p.Price, s.SupplierName
FROM Products p
JOIN Suppliers s ON p.SupplierID = s.SupplierID
ORDER BY p.Price DESC
LIMIT 5;


--5
SELECT c.CustomerName, COUNT(o.OrderID) AS OrderCount, SUM(od.Quantity) AS TotalQuantity
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN OrderDetails od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID
ORDER BY OrderCount DESC
LIMIT 1;


--6
SELECT c.CategoryName, COUNT(DISTINCT od.OrderID) AS OrderCount
FROM Categories c
JOIN Products p ON c.CategoryID = p.CategoryID
JOIN OrderDetails od ON p.ProductID = od.ProductID
GROUP BY c.CategoryID
ORDER BY OrderCount DESC
LIMIT 5;


--7
SELECT c.CustomerName, COUNT(o.OrderID) AS OrderCount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
WHERE strftime('%Y', o.OrderDate) = '1997'
GROUP BY c.CustomerID;


--8
SELECT c.CategoryName, p.ProductName, s.SupplierName
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
JOIN Suppliers s ON p.SupplierID = s.SupplierID
ORDER BY c.CategoryName, p.ProductName;

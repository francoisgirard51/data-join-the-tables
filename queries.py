# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    db.execute("""
        SELECT Orders.OrderID, Customers.ContactName, Employees.FirstName
        FROM Orders
        JOIN Customers ON Orders.CustomerID = Customers.CustomerID
        JOIN Employees ON Orders.EmployeeID = Employees.EmployeeID
        ORDER BY Orders.OrderID
    """)
    return db.fetchall()

def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    db.execute("""
        SELECT Customers.ContactName,
               ROUND(SUM(OrderDetails.UnitPrice * OrderDetails.Quantity), 2) AS total_spent
        FROM Customers
        INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
        INNER JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
        GROUP BY Customers.ContactName
        HAVING total_spent IS NOT NULL
        ORDER BY total_spent ASC
    """)
    return db.fetchall()

def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee!
    By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like: ('FirstName', 'LastName',
    6000 (the sum of all purchase)). The order of the information is irrelevant'''
    db.execute("""
        SELECT Employees.FirstName, Employees.LastName,
               ROUND(SUM(OrderDetails.UnitPrice * OrderDetails.Quantity), 2) AS total_sales
        FROM Employees
        JOIN Orders ON Employees.EmployeeID = Orders.EmployeeID
        JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
        GROUP BY Employees.EmployeeID
        ORDER BY total_sales DESC
        LIMIT 1
    """)
    return db.fetchone()

def orders_per_customer(db):
    '''Return a list of tuples where each tuple contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    db.execute("""
        SELECT Customers.ContactName, COUNT(Orders.OrderID) as number_of_orders
        FROM Customers
        LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
        GROUP BY Customers.ContactName
        ORDER BY number_of_orders ASC
    """)
    return db.fetchall()

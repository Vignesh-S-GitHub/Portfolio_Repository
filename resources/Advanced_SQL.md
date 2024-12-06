For a **Data Engineering** role, understanding advanced SQL concepts is crucial as they help manage large-scale databases, perform complex queries, and optimize performance. Below are some advanced SQL topics relevant to Data Engineering:

### 1. **Window Functions**
   - **Description**: Window functions operate on a set of rows related to the current row, unlike aggregate functions which return a single result for the entire group.
   - **Examples**:
     - `ROW_NUMBER()`: Assigns a unique number to each row within a partition.
     - `RANK()`: Ranks rows within a partition with gaps in case of ties.
     - `DENSE_RANK()`: Similar to `RANK()`, but without gaps in the ranking.
     - `NTILE()`: Divides data into equal buckets.
     - `LEAD()`/`LAG()`: Access data from the next or previous row.
   - **Use Cases**: Ranking, moving averages, running totals, partitioning data.

   ```sql
   SELECT 
       customer_id,
       rental_date,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY rental_date) AS rental_order
   FROM rental;
   ```

---

### 2. **Common Table Expressions (CTEs) and Recursive Queries**
   - **Description**: CTEs allow for modular and readable SQL queries. Recursive CTEs help with hierarchical data structures (e.g., org charts).
   - **Examples**:
     - **Basic CTE**:
       ```sql
       WITH avg_rentals AS (
           SELECT customer_id, COUNT(*) AS rental_count
           FROM rental
           GROUP BY customer_id
       )
       SELECT * FROM avg_rentals WHERE rental_count > 5;
       ```
     - **Recursive CTE**:
       ```sql
       WITH RECURSIVE employee_hierarchy AS (
           SELECT employee_id, manager_id, 1 AS level
           FROM employees WHERE manager_id IS NULL
           UNION ALL
           SELECT e.employee_id, e.manager_id, eh.level + 1
           FROM employees e
           JOIN employee_hierarchy eh ON e.manager_id = eh.employee_id
       )
       SELECT * FROM employee_hierarchy;
       ```

---

### 3. **Partitioning**
   - **Description**: Partitioning divides a large table into smaller, more manageable pieces based on specific columns. This improves query performance, especially for large datasets.
   - **Types of Partitioning**:
     - **Range Partitioning**: Divides data into ranges (e.g., by date or price).
     - **List Partitioning**: Divides data based on a predefined set of values (e.g., geographical region).
     - **Hash Partitioning**: Distributes data evenly across partitions using a hash function.
   - **Use Case**: Improving query performance, especially for time-series or large datasets.

   ```sql
   CREATE TABLE sales (
       sales_id SERIAL,
       sales_date DATE,
       amount DECIMAL
   )
   PARTITION BY RANGE (sales_date);
   
   CREATE TABLE sales_2022 PARTITION OF sales
   FOR VALUES FROM ('2022-01-01') TO ('2023-01-01');
   ```

---

### 4. **Indexes and Performance Optimization**
   - **Description**: Indexes improve query performance by allowing the database to find rows faster.
   - **Types of Indexes**:
     - **B-tree Indexes**: Default index type, efficient for equality and range queries.
     - **Bitmap Indexes**: Good for columns with low cardinality.
     - **GIN/GIST Indexes**: Used for full-text search or non-standard data types like JSONB.
   - **Indexing Strategy**:
     - Create indexes on frequently queried columns.
     - Avoid over-indexing, which can slow down insert/update operations.

   ```sql
   CREATE INDEX idx_customer_id ON rental(customer_id);
   CREATE INDEX idx_rental_date ON rental(rental_date);
   ```

   - **Query Optimization**: Use `EXPLAIN` to analyze query execution plans.

---

### 5. **Materialized Views**
   - **Description**: Materialized views are like regular views, but they store the query results physically. They are useful when querying complex joins or aggregations, as they can significantly reduce query time.
   - **Use Case**: When you need to speed up repeated queries on expensive joins or aggregations.
   - **Example**:
     ```sql
     CREATE MATERIALIZED VIEW top_customers AS
     SELECT customer_id, COUNT(*) AS rental_count
     FROM rental
     GROUP BY customer_id
     ORDER BY rental_count DESC;
     
     REFRESH MATERIALIZED VIEW top_customers;
     ```

---

### 6. **Normalization and Denormalization**
   - **Normalization**: The process of organizing data to reduce redundancy. It's a key concept in OLTP systems.
   - **Denormalization**: The process of introducing redundancy to improve read performance. It's commonly used in OLAP and data warehouses.
   - **Use Cases**: Choose normalization for transactional systems, denormalization for analytics or reporting purposes.

---

### 7. **Advanced Join Types**
   - **Description**: Beyond standard inner and outer joins, SQL supports advanced join types.
   - **Examples**:
     - **Self Join**: A join where a table is joined with itself.
     - **Cross Join**: Returns a Cartesian product of two tables.
     - **Full Outer Join**: Returns all rows when there is a match in either left or right table.
   - **Use Case**: Reporting, advanced analytics, dealing with complex relationships.

   ```sql
   -- Self Join
   SELECT e1.employee_id, e2.employee_id AS manager_id
   FROM employees e1
   LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;
   ```

---

### 8. **JSON and JSONB**
   - **Description**: JSON and JSONB allow you to store and query semi-structured data directly within PostgreSQL.
   - **Operations**:
     - Extracting elements from a JSON/JSONB column: `json_column->'key'`.
     - Indexing JSONB data for fast querying.
   - **Use Case**: Storing metadata, logs, or data that doesn't fit into a relational schema.

   ```sql
   SELECT metadata->>'genre' FROM film_metadata WHERE metadata->>'rating' = 'PG';
   ```

---

### 9. **Triggers and Stored Procedures**
   - **Description**: Triggers automatically execute actions based on specific events (like insert, update, or delete), while stored procedures are predefined SQL logic stored in the database.
   - **Use Cases**: Enforcing business rules, automating tasks, maintaining data integrity.

   ```sql
   CREATE OR REPLACE FUNCTION update_inventory()
   RETURNS TRIGGER AS $$
   BEGIN
       UPDATE inventory SET stock = stock - 1 WHERE product_id = NEW.product_id;
       RETURN NEW;
   END;
   $$ LANGUAGE plpgsql;

   CREATE TRIGGER inventory_update
   AFTER INSERT ON sales
   FOR EACH ROW EXECUTE FUNCTION update_inventory();
   ```

---

### 10. **Transactional Integrity and ACID Properties**
   - **Description**: Understanding **ACID** (Atomicity, Consistency, Isolation, Durability) properties is crucial for data consistency in transactional systems.
   - **Use Cases**: Ensuring data consistency in systems with high concurrency or financial transactions.
   - **Example**:
     ```sql
     BEGIN;
     UPDATE account SET balance = balance - 100 WHERE account_id = 1;
     UPDATE account SET balance = balance + 100 WHERE account_id = 2;
     COMMIT;
     ```

---

### 11. **Data Warehouse Concepts**
   - **ETL (Extract, Transform, Load)**: Using SQL for data extraction, transformation, and loading into data warehouses.
   - **Star Schema and Snowflake Schema**: Logical designs of data warehouses to optimize querying.
   - **OLAP vs OLTP**: Understanding the difference between transactional systems (OLTP) and analytical systems (OLAP).

---

### 12. **Concurrency Control and Locks**
   - **Description**: When multiple transactions run concurrently, concurrency control mechanisms ensure data integrity.
   - **Types of Locks**:
     - **Row-level Locking**: Prevents other transactions from modifying the same row.
     - **Table-level Locking**: Prevents others from accessing the entire table.
   - **Isolation Levels**: Read Uncommitted, Read Committed, Repeatable Read, Serializable.

---
Here's an explanation of each advanced SQL topic mentioned in the provided content:

### 1. **Subqueries**
   - **Description**: A subquery is a query nested inside another query, typically inside the `WHERE`, `FROM`, or `SELECT` clause. It can be used to simplify complex queries by breaking them into smaller, more manageable parts.
   - **Example**:
     ```sql
     SELECT customer_name 
     FROM customers 
     WHERE customer_id IN (
         SELECT customer_id 
         FROM orders 
         WHERE order_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
     );
     ```
     **Explanation**: This query selects customer names from the `customers` table where their `customer_id` appears in the results of the subquery (customers who have placed an order in the last month).

### 2. **Joins**
   - **Description**: Joins are used to combine rows from two or more tables based on a related column. Different types of joins are used based on the required results.
     - **INNER JOIN**: Returns only matching rows.
     - **LEFT JOIN**: Includes all rows from the left table, with matching rows from the right table. If no match, NULL is returned for the right table.
     - **RIGHT JOIN**: Includes all rows from the right table, with matching rows from the left. If no match, NULL is returned for the left table.
     - **FULL JOIN**: Combines both left and right joins, returning all rows from both tables.
   - **Example**:
     ```sql
     SELECT table1.column1, table1.column2, table2.column1
     FROM table1
     INNER JOIN table2
     ON table1.matching_column = table2.matching_column;
     ```

### 3. **Union**
   - **Description**: The `UNION` operator combines the results of multiple `SELECT` statements into a single result set, removing duplicates by default.
   - **Example**:
     ```sql
     SELECT customer_name 
     FROM customers 
     WHERE country = 'USA'
     UNION
     SELECT customer_name 
     FROM customers 
     WHERE country = 'Canada';
     ```
     **Explanation**: This query combines customer names from the USA and Canada, removing any duplicates.

### 4. **Aggregate Functions**
   - **Description**: Aggregate functions operate on a group of rows and return a single value. Common aggregate functions include:
     - `COUNT()`: Counts the number of rows.
     - `SUM()`: Calculates the total sum.
     - `AVG()`: Calculates the average.
     - `MIN()`: Returns the minimum value.
     - `MAX()`: Returns the maximum value.
   - **Example**:
     ```sql
     SELECT product_category, SUM(order_amount) AS total_sales
     FROM orders
     GROUP BY product_category;
     ```

### 5. **Window Functions**
   - **Description**: Window functions perform calculations across a set of table rows that are somehow related to the current row. Unlike aggregate functions, they do not collapse rows.
     - Common functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, `LAG()`.
   - **Example**:
     ```sql
     SELECT customer_name, order_amount, 
            ROW_NUMBER() OVER (ORDER BY order_amount DESC) AS rank
     FROM orders;
     ```
     **Explanation**: This ranks customers by their order amount.

### 6. **Common Table Expressions (CTEs)**
   - **Description**: A CTE is a temporary result set defined within a `WITH` clause. It can be referenced multiple times in the main query.
   - **Example**:
     ```sql
     WITH customer_orders AS (
         SELECT customer_id, SUM(order_amount) AS total_amount
         FROM orders
         GROUP BY customer_id
     )
     SELECT customers.customer_name, customer_orders.total_amount
     FROM customers
     INNER JOIN customer_orders
     ON customers.customer_id = customer_orders.customer_id;
     ```

### 7. **Pivoting**
   - **Description**: Pivoting transforms data from a row format to a column format. It is commonly used for reporting and analytics.
   - **Example**:
     ```sql
     SELECT product,
            SUM(amount) AS Jan_Sales,
            SUM(amount) AS Feb_Sales,
            SUM(amount) AS Mar_Sales
     FROM sales
     PIVOT (
         SUM(amount) FOR month IN ('Jan', 'Feb', 'Mar')
     ) AS pivoted_data;
     ```

### 8. **Recursive Queries**
   - **Description**: Recursive queries are useful for querying hierarchical data (e.g., organizational structures). Recursive queries call themselves until a specific condition is met.
   - **Example**:
     ```sql
     WITH EmployeeHierarchy (id, name, manager_id, level) AS (
         SELECT id, name, manager_id, 1 AS level
         FROM employees
         WHERE manager_id IS NULL
         UNION ALL
         SELECT e.id, e.name, e.manager_id, h.level + 1
         FROM employees e
         INNER JOIN EmployeeHierarchy h ON e.manager_id = h.id
     )
     SELECT * FROM EmployeeHierarchy;
     ```

### 9. **String Manipulation**
   - **Description**: SQL provides various string functions like `CONCAT()`, `SUBSTRING()`, and `REPLACE()` to manipulate text data.
   - **Example**:
     ```sql
     SELECT CONCAT(first_name, ' ', last_name) AS full_name
     FROM employees;
     ```

### 10. **Date and Time Functions**
   - **Description**: SQL offers functions to manipulate and extract parts of date and time values.
   - **Example**:
     ```sql
     SELECT DATEPART(MONTH, order_date) AS order_month
     FROM orders;
     ```

### 11. **Case Statements**
   - **Description**: A `CASE` statement allows for conditional logic within SQL queries. It’s similar to an if-else construct in programming.
   - **Example**:
     ```sql
     SELECT customer_name, 
            CASE 
                WHEN total_order_amount >= 1000 THEN 'High Value'
                WHEN total_order_amount >= 500 THEN 'Medium Value'
                ELSE 'Low Value'
            END AS customer_category
     FROM customers;
     ```

### 12. **User-Defined Functions (UDFs)**
   - **Description**: UDFs allow you to extend the functionality of your database by creating custom functions. There are two types:
     - **Scalar Functions**: Return a single value.
     - **Table-Valued Functions**: Return a table (result set).
   - **Example**:
     ```sql
     CREATE FUNCTION calculate_discount(price DECIMAL(10,2), discount_rate INT)
     RETURNS DECIMAL(10,2)
     BEGIN
         DECLARE discount DECIMAL(10,2);
         SET discount = price * (discount_rate / 100.0);
         RETURN price - discount;
     END;
     ```

### 13. **Temporary Tables**
   - **Description**: Temporary tables exist only for the duration of the session and are used for intermediate storage of results.
   - **Example**:
     ```sql
     CREATE TEMPORARY TABLE temp_customer_orders (
         customer_id INT,
         total_order_amount DECIMAL(10,2),
         PRIMARY KEY (customer_id)
     );
     ```

### 14. **External Query Filter**
   - **Description**: External query filters involve pushing query operations down to external systems to filter data before transferring it to the SQL server, improving performance.
   - **Example**:
     ```sql
     CREATE VIEW active_customers AS
     SELECT customer_id, customer_name
     FROM crm_customers
     WHERE is_active = 1;
     
     SELECT o.order_id, o.customer_id, c.customer_name
     FROM orders o
     INNER JOIN active_customers c ON o.customer_id = c.customer_id;
     ```

### 15. **Query Optimization**
   - **Description**: Query optimization involves improving the performance of SQL queries by analyzing execution plans, proper indexing, and minimizing unnecessary data retrieval.
   - **Example**:
     ```sql
     CREATE INDEX IF NOT EXISTS idx_product_category_stock (category_id, quantity);
     SELECT *
     FROM products
     WHERE category_id = 1
     AND quantity > 0;
     ```
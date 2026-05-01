/* =========================================================================
   PROJECT: Superstore Profit Analytics
   AUTHOR: Bhoomika Ameta
   DATABASE: MS SQL Server
   DESCRIPTION: Advanced analytical queries to extract business KPIs, 
                customer segmentation, and geographical performance.
========================================================================= */

-- 1. What percentage of total orders were shipped on the same date?
SELECT 
    COUNT(*) AS TotalOrders, 
    SUM(CASE WHEN ship_date = order_date THEN 1 ELSE 0 END) AS SameShippedOrders,
    ROUND((CAST(SUM(CASE WHEN ship_date = order_date THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100, 2) AS PercentageOfTotalOrders
FROM [dbo].[superstore];

-- 2. Top 3 customers with highest total quantities of orders.
SELECT TOP 3 
    customer_name AS Top_3_Customers, 
    COUNT(*) AS Total_Orders
FROM [dbo].[superstore]
GROUP BY customer_name
ORDER BY Total_Orders DESC;

-- 3. Top 5 items with the highest average sales.
SELECT TOP 5 
    product_name AS Top_5_Items,  
    ROUND(AVG(sales), 2) AS Average_Sales
FROM [dbo].[superstore]
GROUP BY product_name
ORDER BY Average_Sales DESC;

-- 4. Average order value for each customer, ranked by average order value.
SELECT 
    customer_name,
    avg_sales,
    RANK() OVER (ORDER BY avg_sales DESC) AS Customer_Rank
FROM (
    SELECT customer_name, ROUND(AVG(sales), 2) AS avg_sales
    FROM [dbo].[superstore]
    GROUP BY customer_name
) AS Subquery
ORDER BY avg_sales DESC;

-- 5. Customers with highest and lowest orders from each city.
WITH CityOrderCounts AS (
    SELECT city, customer_name, COUNT(order_id) AS num_orders
    FROM [dbo].[superstore]
    GROUP BY city, customer_name
),
CityMinMax AS (
    SELECT city, MIN(num_orders) AS lowest_order, MAX(num_orders) AS highest_order
    FROM CityOrderCounts
    GROUP BY city
)
SELECT 
    a.city,
    STRING_AGG(CASE WHEN a.num_orders = b.lowest_order THEN a.customer_name ELSE NULL END, ',') AS Lowest_Order_Customers,
    STRING_AGG(CASE WHEN a.num_orders = b.highest_order THEN a.customer_name ELSE NULL END, ',') AS Highest_Order_Customers
FROM CityOrderCounts a
JOIN CityMinMax b ON a.city = b.city
WHERE a.num_orders = b.lowest_order OR a.num_orders = b.highest_order
GROUP BY a.city;

-- 6. Most demanded sub-category in the West region.
SELECT TOP 1 
    sub_category, 
    SUM(quantity) AS Total_Quantity
FROM [dbo].[superstore]
WHERE Region = 'West'
GROUP BY sub_category
ORDER BY Total_Quantity DESC;

-- 7. Order with the highest cumulative sales value.
SELECT TOP 1 
    order_id, 
    ROUND(SUM(sales), 2) AS Total_Sales
FROM [dbo].[superstore]
GROUP BY order_id
ORDER BY Total_Sales DESC;

-- 8. Average time for orders to get shipped.
SELECT 
    AVG(DATEDIFF(day, order_date, ship_date)) AS Avg_Shipping_Time_Days
FROM [dbo].[superstore];

-- 9. Segment placing the largest individual orders from each state.
WITH StateSegmentSales AS (
    SELECT state, segment, ROUND(SUM(sales), 2) AS total_sales
    FROM [dbo].[superstore]
    GROUP BY state, segment
), 
MaxStateSales AS (
    SELECT state, MAX(total_sales) AS max_sales
    FROM StateSegmentSales
    GROUP BY state
)
SELECT a.state, a.segment, a.total_sales
FROM StateSegmentSales AS a
JOIN MaxStateSales AS b ON a.state = b.state AND a.total_sales = b.max_sales
ORDER BY state;
USE fudgemart_v3
GO

WITH source AS (
    SELECT v.*, product_department, product_id
    FROM fm_vendors v JOIN fm_products p ON v.vendor_id=p.product_vendor_id
    WHERE product_department != 'Housewares'
)
SELECT * FROM source pivot (
    COUNT(product_id) FOR product_department IN 
    ([Clothing], [Electronics], [Hardware], [Sporting Goods])
) AS pvt

DROP index IF EXISTS ix_product_department ON fm_products
CREATE index ix_product_department ON fm_products(product_department)
INCLUDE (product_vendor_id)
GO

DROP index IF EXISTS ix_product_department ON fm_products
DROP index IF EXISTS ix_product_vendor ON fm_products
CREATE index ix_product_vendor_id ON fm_products(product_vendor_id)
INCLUDE (product_department)




USE payroll
GO

SELECT employee_id, employee_firstname, employee_lastname, employee_jobtitle
FROM employees
WHERE employee_jobtitle = 'Store Manager'
OR employee_jobtitle = 'Owner'

DROP index IF EXISTS ix_employee_jobtitle ON employees;
CREATE index ix_employee_jobtitle ON employees(employee_jobtitle);
GO

SELECT employee_id, employee_firstname, employee_lastname, employee_jobtitle
FROM employees
WHERE employee_jobtitle = 'Store Manager'
OR employee_jobtitle = 'Owner'

SELECT employee_jobtitle, COUNT(*) AS employee_count
FROM employees WITH (INDEX(ix_employee_jobtitle))
WHERE employee_jobtitle = 'Store Manager'
OR employee_jobtitle = 'Department Manager'
GROUP BY employee_jobtitle;
GO


USE vbay
GO

SELECT item_id, item_name, 
DENSE_RANK() OVER
    ( PARTITION BY item_name ORDER BY bid_datetime) AS bid_order, 
    bid_amount, 
    lag(user_firstname + ' ' + user_lastname) OVER
    (PARTITION BY item_name ORDER BY bid_datetime) AS prev_bidder,
    user_firstname + ' ' + user_lastname AS bidder, 
    LEAD(user_firstname + ' ' + user_lastname) OVER 
    (PARTITION BY item_name ORDER BY bid_datetime) AS next_bidder
    from vb_items
        JOIN vb_bids on item_id = bid_item_id
        JOIN vb_users on bid_user_id = user_id
    WHERE bid_status='ok'
GO 

DROP index IF EXISTS ix_vb_bids ON vb_bids;
CREATE index ix_vb_bids ON vb_bids(bid_item_id);
GO 

SELECT item_id, item_name, 
DENSE_RANK() OVER
    ( PARTITION BY item_name ORDER BY bid_datetime) AS bid_order, 
    bid_amount, 
    lag(user_firstname + ' ' + user_lastname) OVER
    (PARTITION BY item_name ORDER BY bid_datetime) AS prev_bidder,
    user_firstname + ' ' + user_lastname AS bidder, 
    LEAD(user_firstname + ' ' + user_lastname) OVER 
    (PARTITION BY item_name ORDER BY bid_datetime) AS next_bidder
    from vb_items
        JOIN vb_bids WITH (INDEX(ix_vb_bids)) on item_id = bid_item_id
        JOIN vb_users on bid_user_id = user_id
    WHERE bid_status='ok'
GO 


use fudgemart_v3
GO

CREATE VIEW dbo.v_orders
WITH SCHEMABINDING
AS
SELECT c.customer_state, c.customer_firstname + ' ' + c.customer_lastname AS customer_name, 
DATEPART(year, order_date) AS order_year, o.order_id, o.ship_via, 
od.order_qty AS order_detail_qty, od.order_qty*p.product_retail_price AS order_detailed_extd_price, 
p.product_id, p.product_name, p.product_department
FROM dbo.fm_orders o 
JOIN dbo.fm_customers c ON o.customer_id = c.customer_id
JOIN dbo.fm_order_details od ON o.order_id = od.order_id
JOIN dbo.fm_products p ON p.product_id = od.product_id
GO 

SELECT * 
FROM dbo.v_orders
WHERE customer_state = 'NY';
GO

DROP INDEX IF EXISTS ix_v_orders ON dbo.v_orders;
CREATE UNIQUE CLUSTERED INDEX ix_v_orders ON dbo.v_orders(order_id);
GO

SELECT * 
FROM dbo.v_orders;
GO

SELECT *
FROM dbo.v_orders 
WITH(NOEXPAND);



DROP VIEW if exists v_orders;
GO

CREATE VIEW dbo.v_orders
WITH SCHEMABINDING
AS
SELECT c.customer_state, c.customer_firstname + ' ' + c.customer_lastname AS customer_name, 
DATEPART(year, order_date) AS order_year, o.order_id, o.ship_via, 
od.order_qty AS order_detail_qty, od.order_qty*p.product_retail_price AS order_detailed_extd_price, 
p.product_id, p.product_name, p.product_department
FROM dbo.fm_orders o 
JOIN dbo.fm_customers c ON o.customer_id = c.customer_id
JOIN dbo.fm_order_details od ON o.order_id = od.order_id
JOIN dbo.fm_products p ON p.product_id = od.product_id
GO 

create unique clustered index ix_view_orders ON v_orders(order_id);
GO

CREATE NONCLUSTERED COLUMNSTORE INDEX ix_v_orders_Columnstore
ON dbo.v_orders (
    customer_state, 
    customer_name, 
    order_year, 
    order_id, 
    ship_via, 
    order_detail_qty, 
    order_detailed_extd_price, 
    product_id, 
    product_name, 
    product_department
);
GO



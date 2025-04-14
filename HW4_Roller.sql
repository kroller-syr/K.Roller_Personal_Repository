use vbay
GO

SELECT * FROM vb_items

SELECT item_name, item_type, item_reserve, item_soldamount FROM vb_items
    WHERE item_type='Collectables'
    ORDER BY item_name


SELECT * from vb_items
SELECT * from vb_users 

SELECT s.user_email, s.user_firstname, s.user_lastname, i.item_type, i.item_type
    FROM vb_items i
        JOIN vb_users s ON i.item_seller_user_id = s.user_id
        WHERE i.item_type = 'Antiques'

SELECT s.user_email as sellers_email, 
    b.user_email as buyers_email, 
    i.item_soldamount - i.item_reserve as item_margin, 
    i.*
    FROM vb_items i 
        JOIN vb_users s on s.user_id = i.item_seller_user_id
        JOIN vb_users b on b.user_id = i.item_buyer_user_id
    WHERE i.item_sold=1 
    ORDER BY item_margin DESC 

SELECT * FROM vb_users
SELECT * FROM vb_zip_codes

SELECT * FROM vb_users
    WHERE user_zip_code 
    LIKE '13%'


SELECT * FROM vb_users
SELECT * FROM vb_zip_codes

SELECT * FROM vb_users u 
SELECT * FROM vb_zip_codes z 

SELECT u.user_firstname, u.user_lastname, u.user_email, u.user_zip_code, z.zip_city, z.zip_state
FROM vb_users u
INNER JOIN vb_zip_codes z ON u.user_zip_code = z.zip_code
WHERE zip_state = 'NY'
ORDER BY z.zip_city, u.user_lastname, u.user_firstname

SELECT * FROM vb_items i 

SELECT item_id, item_name, item_type, item_reserve 
    FROM vb_items
    WHERE item_sold = '0' AND item_reserve >= 250.00
    ORDER BY item_reserve DESC


SELECT item_id, item_name, item_type, item_reserve, 
CASE 
    WHEN item_reserve > 250 then 'High Priced Item'
    WHEN item_reserve < 50 then 'Low Priced Item'
    ELSE 'Average Priced Item'
END AS item_price_market_value
FROM vb_items
WHERE item_type != 'All Other';



SELECT * FROM vb_bids b 
SELECT * FROM vb_users u 

SELECT u.user_firstname + ' ' + u.user_lastname AS user_fullname, u.user_email, b.bid_id, b.bid_datetime, b.bid_amount, b.bid_item_id
FROM vb_users u
LEFT JOIN vb_bids b on u.user_id = b.bid_user_id
WHERE b.bid_status = 'ok'
ORDER BY b.bid_datetime DESC

SELECT * FROM vb_items i 
SELECT * FROM vb_bids b 
SELECT * FROM vb_users u

SELECT u.user_firstname, u.user_lastname, u.user_email, u.user_id, b.bid_datetime, i.item_id, i.item_name
FROM vb_users u 
LEFT JOIN vb_bids b on u.user_id = b.bid_user_id
JOIN vb_items i on b.bid_item_id = i.item_id 
WHERE b.bid_status !='ok'
ORDER BY u.user_lastname, u.user_firstname, b.bid_datetime DESC 

SELECT * FROM vb_items i 
SELECT * FROM vb_bids b 
SELECT * FROM vb_users u 

SELECT i.item_id, i.item_name, i.item_type, u.user_firstname + ' ' + u.user_lastname AS user_fullname, i.item_reserve
FROM vb_items i
JOIN vb_users u on i.item_seller_user_id = u.user_id 
LEFT JOIN vb_bids b on i.item_id = b.bid_item_id
WHERE b.bid_item_id IS NULL;  

SELECT u2.user_firstname + ' ' + u2.user_lastname AS user_who_gave_rating, u.user_firstname + ' ' + u.user_lastname AS review_left_for_seller, r.rating_value, r.rating_comment
FROM vb_user_ratings r 
JOIN vb_users u on r.rating_for_user_id = u.user_id
JOIN vb_users u2 on r.rating_by_user_id = u2.user_id
WHERE rating_astype = 'Seller'


SELECT i.item_id,i.item_name, i.item_type, i.item_soldamount,
u.user_firstname + ' ' + u.user_lastname AS seller_fullname,
z.zip_city as sellers_city, z.zip_state as sellers_state,  
u2.user_firstname + ' ' + u2.user_lastname AS buyer_fullname,
z2.zip_city as buyers_city, z2.zip_state as buyers_state
FROM vb_items i
JOIN vb_users u on i.item_seller_user_id = u.user_id
JOIN vb_users u2 on i.item_buyer_user_id = u2.user_id
JOIN vb_zip_codes z on u.user_zip_code = z.zip_code
JOIN vb_zip_codes z2 on u2.user_zip_code = z2.zip_code
WHERE item_sold = '1'

SELECT u.user_firstname + ' ' + u.user_lastname AS user_fullname, u.user_email 
FROM vb_users u
LEFT JOIN vb_items i on u.user_id = i.item_buyer_user_id
LEFT JOIN vb_items i2 on u.user_id = i2.item_seller_user_id
LEFT JOIN vb_bids b on u.user_id = b.bid_user_id
WHERE i.item_buyer_user_id IS NULL AND i2.item_seller_user_id IS NULL AND b.bid_user_id IS NULL;
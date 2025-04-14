use vbay
GO

SELECT * FROM vb_items
SELECT * FROM vb_bids

SELECT item_name, item_reserve, min(bid_amount) as min_bid, max(bid_amount) as max_bid, item_soldamount
FROM vb_items
    JOIN vb_bids ON item_id=bid_item_id
    WHERE bid_status = 'ok'
    GROUP BY item_name, item_reserve, item_soldamount
    ORDER BY item_reserve DESC;
GO

WITH user_bids AS (
SELECT s.user_email, s.user_firstname, s.user_lastname, count(*) as bid_counts, 
    CASE WHEN count(*) BETWEEN 0 and 1 THEN 'Low'
     WHEN count(*) BETWEEN 2 and 4 THEN 'Moderate'
     ELSE 'High' END AS user_bid_activity
FROM vb_users s 
    LEFT JOIN vb_bids b ON b.bid_user_id = s.user_id
    WHERE b.bid_status = 'ok'
    GROUP BY s.user_email, s.user_firstname, s.user_lastname
)

SELECT user_bid_activity, count(*) as user_count
    FROM user_bids
    GROUP BY user_bid_activity
    ORDER BY user_count;
GO

SELECT item_name, item_type, item_reserve, item_soldamount 
FROM vb_items
WHERE item_type='Collectables'
ORDER BY item_name;

GO
 

SELECT * FROM vb_items i 

SELECT i.item_type, MIN(i.item_reserve) AS category_min_reserve, 
AVG(i.item_reserve) AS category_average_reserve, 
MAX(i.item_reserve) AS category_max_reserve, 
COUNT(i.item_type) AS item_type_count
FROM vb_items i
GROUP BY i.item_type;

GO 

SELECT i.item_name, i.item_type, i.item_reserve,
MIN(i.item_reserve) OVER (PARTITION BY i.item_type) AS item_min_reserve,
MAX(i.item_reserve) OVER (PARTITION BY i.item_type) AS item_max_reserve,
AVG(i.item_reserve) OVER (PARTITION BY i.item_type) AS item_average_reserve
FROM vb_items i
WHERE i.item_type='Antiques' OR i.item_type='Collectables';

GO


SELECT u.user_firstname, u.user_lastname,
COUNT(r.rating_for_user_id) as user_rating_count,
CAST(AVG(r.rating_value) as DECIMAL(2,1)) AS seller_average_rating
FROM vb_users u 
LEFT JOIN vb_user_ratings r ON r.rating_for_user_id = u.user_id
GROUP BY u.user_firstname, u.user_lastname, u.user_id;

GO 

SELECT i.item_name, 
COUNT(b.bid_item_id) as item_bid_count
FROM vb_items i 
LEFT JOIN vb_bids b on b.bid_item_id = i.item_id
WHERE i.item_type = 'Collectables'
GROUP BY i.item_name
ORDER BY item_bid_count DESC;

GO

SELECT i.item_id, i.item_name, b.bid_amount, u.user_firstname + ' ' + u.user_lastname AS bidder,
ROW_NUMBER() OVER (PARTITION BY i.item_id ORDER BY b.bid_datetime ASC) AS bid_order
FROM vb_bids b 
LEFT JOIN vb_items i ON i.item_id = b.bid_item_id
LEFT JOIN vb_users u ON u.user_id = b.bid_user_id
WHERE i.item_id = '6'
ORDER BY bid_order;

GO


SELECT i.item_id, i.item_name, b.bid_amount, u.user_firstname + ' ' + u.user_lastname AS bidder,
ROW_NUMBER() OVER (PARTITION BY i.item_id ORDER BY b.bid_datetime ASC) AS bid_order,
LAG(u.user_firstname+ ' ' + u.user_lastname) OVER (PARTITION BY i.item_id ORDER BY b.bid_datetime ASC) AS previous_bidder, 
LEAD(u.user_firstname + ' ' + u.user_lastname) OVER(PARTITION BY i.item_id ORDER BY b.bid_datetime ASC) AS next_bidder
FROM vb_bids b 
LEFT JOIN vb_items i ON i.item_id = b.bid_item_id
LEFT JOIN vb_users u ON u.user_id = b.bid_user_id
WHERE i.item_id = '6'
ORDER BY bid_order;

GO

WITH AverageRating AS (
    SELECT AVG(rating_value) AS AvgRating
    FROM vb_user_ratings
),
raw_ratings AS (
SELECT  u.user_firstname, u.user_lastname, u.user_email,r.rating_value, 
AvgRating,
COUNT(r.rating_by_user_id) OVER (PARTITION BY r.rating_by_user_id) AS number_of_reviews_left
FROM vb_user_ratings r
LEFT JOIN vb_users u ON u.user_id = r.rating_by_user_id
CROSS JOIN AverageRating
)
SELECT *
FROM raw_ratings
WHERE rating_value < AvgRating AND number_of_reviews_left > 2;

GO

WITH BidData AS (
    SELECT u.user_firstname, u.user_lastname, u.user_email, b.bid_user_id,
    COUNT(*) AS total_bids_by_user,
    COUNT(DISTINCT b.bid_item_id) AS total_items_bidded_on
    FROM vb_bids b
    LEFT JOIN vb_users u ON u.user_id = b.bid_user_id
    WHERE b.bid_status = 'ok'
    GROUP BY u.user_firstname, u.user_lastname, u.user_email, b.bid_user_id
)
SELECT user_firstname, user_lastname, user_email, bid_user_id,
       total_bids_by_user, total_items_bidded_on,
       CASE WHEN total_items_bidded_on > 0 THEN 
            CAST(total_bids_by_user AS FLOAT) / total_items_bidded_on
       ELSE 0 END AS bid_to_item_ratio
FROM BidData
ORDER BY bid_to_item_ratio DESC;

GO


SELECT i.item_name, b.highest_bid_for_item, u.user_firstname, u.user_lastname
FROM vb_items i
JOIN (
SELECT bid_item_id, MAX(bid_amount) AS highest_bid_for_item
FROM vb_bids
    WHERE bid_status = 'ok'
    GROUP BY bid_item_id
) b ON b.bid_item_id = i.item_id
LEFT JOIN vb_bids bb ON bb.bid_item_id = i.item_id AND bb.bid_amount = b.highest_bid_for_item
LEFT JOIN vb_users u ON u.user_id = bb.bid_user_id
WHERE i.item_sold = '0';

GO


WITH OverallAvgRating AS (
SELECT CAST(AVG(rating_value) AS DECIMAL(3,2)) AS overall_avg_rating
FROM vb_user_ratings
),
UserRatings AS (
SELECT u.user_firstname, u.user_lastname, u.user_id,
    COUNT(r.rating_for_user_id) AS user_rating_count,
    CAST(AVG(r.rating_value) AS DECIMAL(3,2)) AS seller_average_rating
FROM vb_users u 
LEFT JOIN vb_user_ratings r ON r.rating_for_user_id = u.user_id
GROUP BY u.user_firstname, u.user_lastname, u.user_id
)
SELECT ur.user_firstname, ur.user_lastname, ur.user_rating_count, ur.seller_average_rating, oar.overall_avg_rating,
(ur.seller_average_rating - oar.overall_avg_rating) AS rating_difference
FROM UserRatings ur
CROSS JOIN OverallAvgRating oar;

GO



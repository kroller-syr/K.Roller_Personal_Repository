USE tinyu
GO 

DROP PROCEDURE IF EXISTS dbo.p_upsert_major
GO

CREATE PROCEDURE dbo.p_upsert_major(
    @major_code CHAR(3),
    @major_name VARCHAR(50)
) AS BEGIN 
BEGIN TRY 
BEGIN TRANSACTION 
IF EXISTS(SELECT * FROM majors where major_code = @major_code) BEGIN 
    UPDATE majors set major_name = @major_name 
        WHERE major_code = @major_code 
        IF @@ROWCOUNT <> 1 throw 50001, 'p_upsert_major: Update Error', 1
    END
    ELSE BEGIN 
        DECLARE @id int= (SELECT max(major_id) from majors) + 1
        INSERT INTO majors (major_id, major_code, major_name)
            VALUES (@id, @major_code, @major_name)
        IF @@ROWCOUNT <> 1 throw 50002, 'p_upsert_major: Insert Error', 1
        END
        COMMIT
    END TRY 
    BEGIN CATCH 
        ROLLBACK;
        THROW
        END CATCH
END 

SELECT * FROM majors

DECLARE @major_code6 CHAR(3) = 'BSN';
DECLARE @major_name6 VARCHAR(50) = 'Economics';
EXEC dbo.p_upsert_major @major_code =@major_code6, @major_name= @major_name6;

SELECT * FROM majors

INSERT INTO majors(major_id, major_code, major_name)
VALUES 
(10,'TST','Testing1'),
(11, 'TST', 'Testing2');
GO

DECLARE @major_code CHAR(3) = 'TST';
DECLARE @major_name VARCHAR(50) = 'The Waters'

EXEC dbo.p_upsert_major @major_code = @major_code, @major_name = @major_name
GO


USE vbay
GO

DROP PROCEDURE IF EXISTS dbo.p_place_bid
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO
create procedure [dbo].[p_place_bid]
(
	@bid_item_id int,
	@bid_user_id int,
	@bid_amount money
)
as
begin
	declare @max_bid_amount money
	declare @item_seller_user_id int
	declare @bid_status varchar(20)
    DECLARE @new_bid_id INT
	
	-- be optimistic :-)
	set @bid_status = 'ok'

    BEGIN TRY
        BEGIN TRANSACTION;
	
	-- TODO: 5.5.1 set @max_bid_amount to the higest bid amount for that item id 
	set @max_bid_amount = (select max(bid_amount) from vb_bids where bid_item_id=@bid_item_id and bid_status='ok'); 
	
	-- TODO: 5.5.2 set @item_seller_user_id to the seller_user_id for the item id
	set @item_seller_user_id = (select item_seller_user_id from vb_items where item_id=@bid_item_id); 

	-- TODO: 5.5.3 if no bids then set the @max_bid_amount to the item_reserve amount for the item_id
	if (@max_bid_amount is null) 
		set @max_bid_amount = (select item_reserve from vb_items where item_id=@bid_item_id) ;
	
	-- if you're the item seller, set bid status
	if ( @item_seller_user_id = @bid_user_id)
		set @bid_status = 'item_seller';
	
	-- if the current bid lower or equal to the last bid, set bid status
	if ( @bid_amount <= @max_bid_amount)
		set @bid_status = 'low_bid';
		
	-- TODO: 5.5.4 insert the bid at this point and return the bid_id 		
	insert into vb_bids (bid_user_id, bid_item_id, bid_amount, bid_status)
		values (@bid_user_id, @bid_item_id, @bid_amount, @bid_status);
    SET @new_bid_id = SCOPE_IDENTITY();
    
	COMMIT;
    RETURN @new_bid_id;
    END TRY
    BEGIN CATCH 
    IF XACT_STATE() <> 0 
    BEGIN 
        ROLLBACK;
        THROW;
END 

   
    END CATCH;
    END; 
GO


DECLARE @bid_item_id INT = 36;
DECLARE @bid_user_id INT = 2;
DECLARE @bid_amount MONEY = '105'

EXEC [dbo].[p_place_bid] @bid_item_id=@bid_item_id, @bid_user_id=@bid_user_id, @bid_amount =@bid_amount
GO

SELECT * FROM vb_bids
GO


DROP PROCEDURE IF EXISTS [dbo].[p_rate_user]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER OFF
GO
create procedure [dbo].[p_rate_user]
(
	@rating_by_user_id int,
	@rating_for_user_id int,
	@rating_astype varchar(20),
	@rating_value int,
	@rating_comment varchar(250) 
)
as
begin
    BEGIN TRY 
    IF @rating_value < 1 OR @rating_value > 5 
    BEGIN;
        THROW 50003, 'p_rate_user: Rating must be between the values of 1 and 5 stars', 1;
    END

    IF @rating_by_user_id = @rating_for_user_id
    BEGIN; 
        THROW 50004, 'p_rate_user: Users cannot leave ratings for themselves.', 1;
    
    END

    BEGIN TRANSACTION;

	-- TODO: 5.3
	insert into vb_user_ratings (rating_by_user_id, rating_for_user_id, rating_astype, rating_value,rating_comment)
	values (@rating_by_user_id, @rating_for_user_id, @rating_astype, @rating_value, @rating_comment)

    COMMIT;
	
	return @@identity;  
end TRY 
BEGIN CATCH 
IF XACT_STATE() <> 0
BEGIN 
    ROLLBACK;
END; 

THROW;
END CATCH;
END;
GO


DECLARE @rating_by_user_id int = 1;
DECLARE @rating_for_user_id int= 2;
DECLARE	@rating_astype varchar(20)= 'seller_rating';
DECLARE	@rating_value int = 6;
DECLARE @rating_comment VARCHAR(250) = 'Many product with having good fit. Other orders in future making, best seller at pricing.'

EXEC [dbo].[p_rate_user] @rating_by_user_id = @rating_by_user_id, @rating_for_user_id= @rating_for_user_id, @rating_astype=@rating_astype,
                        @rating_value=@rating_value, @rating_comment=@rating_comment 
                    
GO


DECLARE @rating_by_user_id int = 1;
DECLARE @rating_for_user_id int= 1;
DECLARE	@rating_astype varchar(20)= 'seller_rating';
DECLARE	@rating_value int = 5;
DECLARE @rating_comment VARCHAR(250) = 'This seller is the best one on vbay. All the other sellers should go back to that e word knockoff. Best person ever.'

EXEC [dbo].[p_rate_user] @rating_by_user_id = @rating_by_user_id, @rating_for_user_id= @rating_for_user_id, @rating_astype=@rating_astype,
                        @rating_value=@rating_value, @rating_comment=@rating_comment 
                    
GO


USE tinyu
GO 

ALTER TABLE majors
ADD major_capacity INT NULL;

SELECT * FROM majors

UPDATE majors
SET major_capacity = 10
WHERE major_id = 1 

UPDATE majors
SET major_capacity = 8
WHERE major_id = 2

UPDATE majors
SET major_capacity = 14
WHERE major_id = 3

UPDATE majors
SET major_capacity = 15
WHERE major_id = 4

UPDATE majors
SET major_capacity = 9
WHERE major_id = 5

DROP TRIGGER IF EXISTS trg_maximum_major_cap;
GO


CREATE TRIGGER trg_maximum_major_cap
ON majors
INSTEAD OF INSERT, UPDATE
AS
BEGIN
    -- Handle INSERT operations
    IF EXISTS (SELECT * FROM inserted)
    BEGIN
        INSERT INTO majors (major_id, major_code, major_name, major_capacity)
        SELECT 
            major_id, 
            major_code, 
            major_name, 
            CASE 
                WHEN major_capacity > 15 THEN 15
                ELSE major_capacity
            END
        FROM inserted;
    END

    -- Handle UPDATE operations
    IF EXISTS (SELECT * FROM deleted)
    BEGIN
        UPDATE m
        SET 
            m.major_code = i.major_code,
            m.major_name = i.major_name,
            m.major_capacity = CASE 
                WHEN i.major_capacity > 15 THEN 15
                ELSE i.major_capacity
            END
        FROM majors m
        INNER JOIN inserted i ON m.major_id = i.major_id;
    END
END;


UPDATE majors 
SET major_capacity = 19
WHERE major_id = 1

SELECT * FROM majors 

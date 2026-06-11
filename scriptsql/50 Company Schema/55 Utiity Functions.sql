--
-- **************************
-- ** APPLICATION DATABASE **
-- **************************
--

-- Paolo De Stefani 01.2025

-- This script MUST be executed by postgres user or a postgres like user
-- Connected to a database ("postgres" database is OK)

---------------------------------
-- APPLICATION DB ARCHITECTURE --
---------------------------------

-- * one database {pyAppPgDataBase}
-- * one role that own the database {pyAppPgOwnerRole} without login privilege
-- * one login role {pyAppPgLoginRole} that inherit {pyAppPgOwnerRole} privileges

-- Every database has 4 schemas:
-- * system     for system objects
-- * common     for common objects that are shared with all companies
-- * company    for objects associated with a company
-- * temp       for temporary tables

-- This set of variables will be be resolved before executing the scripts:
-- {pyAppPgOwnerRole}           = PostgresSQL Role that own all db objects without login privilege
-- {pyAppPgDataBase}            = Postgres database name
-- {pyAppPgLoginRole}           = PostgresSQL Role used for standard login users
-- {pyAppPgLoginPassword}       = Password for pyAppPgLoginRole
-- {pyAppName}                  = Python application name
-- {pyAppDescription}           = Python application description
-- {pyAppVersionMajor}          = Application version major number
-- {pyAppVersionMinor}          = Application version minor number
-- {pyAppVersionPatch}          = Application version patch number
-- {pyAppVersionTag}            = Application version tag
-- {pyAppVersionDescription}    = Application version description
-- {pyAppPgDataBaseTS}          = Database table space (MUST be created before script execution)
-- {pyAppPgTablesTS}            = Tables table space (MUST be created before script execution)
-- {pyAppPgIndexesTS}           = Indexes table space (MUST be created before script execution)


---------------------------
-- COMMON SCHEMA OBJECTS --
---------------------------

SET search_path = company;


-- delete orders utility function
CREATE FUNCTION delete_event_order(in_event int) 
RETURNS VOID AS
$$
BEGIN
	-- delete event orders
	DELETE FROM company.order_header 
    WHERE event_id = in_event; -- event include company
	-- stock inventory update
	UPDATE company.inventory 
    SET unloaded = 0, ordered = 0 
    WHERE event_id = in_event; -- event include company
	-- delete from stock unload
	DELETE FROM company.ordered_delivered
    WHERE event_id = in_event; -- event include company
	-- delte from numbering
	DELETE FROM company.numbering 
    WHERE event_id = in_event; -- event include company
END;
$$ 
LANGUAGE plpgsql;
COMMENT ON FUNCTION delete_event_order(int) IS
    'Function for delete all orders';
ALTER FUNCTION delete_event_order(in_event int) 
    OWNER TO {pyAppPgOwnerRole};


-- set orders as processed utility function
CREATE FUNCTION set_order_as_processed(in_event int) 
RETURNS VOID AS
$$
BEGIN
	UPDATE order_header_department
    SET fulfillment_date = oh.date_time
    FROM order_header_department ohd
    JOIN order_header oh ON ohd.order_header_id = oh.order_header_id
    WHERE ohd.fulfillment_date is null
        AND oh.event_id = in_event; -- event include company
END;
$$ 
LANGUAGE plpgsql;
COMMENT ON FUNCTION set_order_as_processed(int) IS
    'Function for set all orders as processed';
ALTER FUNCTION set_order_as_processed(in_event int) 
    OWNER TO {pyAppPgOwnerRole};


-- rebuild inventory utility function
CREATE FUNCTION inventory_rebuild(in_event int) 
RETURNS VOID AS
$$
DECLARE
    odr         RECORD;         -- order detail dep record
    item        BIGINT;        -- item
    itempart    BIGINT;        -- item part
    partqty     numeric(12, 2); -- quantity for item part
BEGIN
    -- clear items inventory
    UPDATE company.inventory
    SET ordered = 0, unloaded = 0  
    WHERE event_id = in_event; -- event include company
    -- loop trough lines deps records
    FOR odr IN
        SELECT 
            l.company_id,
            l.event_id,
            l.event_date,
            l.day_part,
            l.item_id,
            i.item_type,
            l.ordered_quantity,
            l.delivered_quantity
        FROM company.order_line_department l
        JOIN company.order_header_department h ON l.order_header_department_id = h.order_header_department_id
        JOIN company.item i ON l.item_id = i.item_id -- item include company
        WHERE l.event_id = in_event -- event include company
    LOOP
       FOR item, itempart, partqty IN 
            SELECT 
                i.item, 
                i.part,
                i.qty
            FROM (
                -- normal item
                SELECT 
                    item_id  AS item,
                    item_id  AS part,
                    1        AS qty
                FROM company.item
                WHERE item_type = 'I'
                UNION
                -- kit
                SELECT 
                    item_id  AS item,
                    part_id  AS part,
                    quantity AS qty 
                FROM company.item_part 
                WHERE item_type = 'K'
                ) i
            WHERE i.item = odr.item_id 
        LOOP
            -- update inventory
            UPDATE company.inventory 
            SET unloaded = unloaded + odr.delivered_quantity * partqty,
                ordered = ordered + odr.ordered_quantity * partqty
            WHERE event_id = in_event -- event include company
                AND item_id = itempart;
        END LOOP;
    END LOOP;
    -- update stock and available
	UPDATE company.inventory
	SET stock = loaded - unloaded,
		available = loaded - unloaded - ordered
	WHERE event_id = in_event;
END;
$$ 
LANGUAGE plpgsql;
COMMENT ON FUNCTION inventory_rebuild(int) IS
    'Function for rebuild inventory';
ALTER FUNCTION inventory_rebuild(in_event int) 
    OWNER TO {pyAppPgOwnerRole};


-- rebuild ordered_delivered utility function
CREATE FUNCTION ordered_delivered_rebuild(in_event int) 
RETURNS VOID AS
$$
DECLARE
    odr         RECORD;             -- order detail dep record
BEGIN
    -- clear ordered_delivered
    DELETE FROM company.ordered_delivered 
    WHERE event_id = in_event; -- event include company
    -- loop trough lines deps records
    FOR odr IN
        SELECT 
            l.company_id,
            l.event_id,
            l.event_date,
            l.day_part,
            l.item_id,
            i.item_type,
            l.ordered_quantity,
            l.delivered_quantity
        FROM company.order_line_department l
        JOIN company.order_header_department h ON l.order_header_department_id = h.order_header_department_id
        JOIN company.item i ON l.item_id = i.item_id -- item include company
        WHERE l.event_id = in_event -- event include company
    LOOP
        -- only for normal items
		-- initialize values on not present/change day/change daypart
		IF NOT EXISTS(  SELECT ordered_delivered_id 
						FROM company.ordered_delivered 
						WHERE   event_id    = odr.event_id 
							AND event_date  = odr.event_date 
							AND day_part    = odr.day_part 
							AND item_id     = odr.item_id) THEN
			IF (SELECT has_delivered_control FROM company.item WHERE item_id = odr.item_id) THEN
				INSERT INTO company.ordered_delivered (company_id, event_id, event_date, day_part, item_id) 
				VALUES (odr.company_id,	odr.event_id, odr.event_date, odr.day_part,	odr.item_id);
			END IF;
		END IF;
		-- update ordered delivered
		UPDATE company.ordered_delivered
		SET ordered   = ordered + odr.ordered_quantity,
			delivered = delivered + odr.delivered_quantity
		WHERE   event_id    = odr.event_id 
			AND event_date  = odr.event_date 
			AND day_part    = odr.day_part 
			AND item_id     = odr.item_id;
    END LOOP;
END;
$$ 
LANGUAGE plpgsql;
COMMENT ON FUNCTION ordered_delivered_rebuild(int) IS
    'Function for ordered delivered rebuild';
ALTER FUNCTION ordered_delivered_rebuild(in_event int) 
    OWNER TO {pyAppPgOwnerRole};


-- numbering rebuild utility function
CREATE FUNCTION numbering_rebuild(in_event int) 
RETURNS VOID AS
$$
DECLARE 
    i           integer; 
BEGIN
    -- clear old values
    DELETE FROM company.numbering 
    WHERE event_id = in_event; -- event include company
    -- update identity
	i := (SELECT coalesce(max(numbering_id), 0) + 1 FROM company.numbering);
	EXECUTE format('ALTER TABLE company.numbering ALTER COLUMN numbering_id RESTART WITH %s', i);
    -- update numbering table
    INSERT INTO company.numbering (
		company_id,
		event_id,
		event_date,
		day_part,
		current_value,
		created_at,
		created_by,
		updated_at,
		updated_by,
		object_version)
	SELECT
		company_id,
		event_id,
		stat_order_date,
		stat_order_day_part,
		max(order_number) AS current_value,
		now(),
		system.pa_current_user(),
		now(),
		system.pa_current_user(),
		0
	FROM company.order_header
	WHERE event_id = in_event
	GROUP BY company_id, event_id, stat_order_date, stat_order_day_part;
END;
$$ 
LANGUAGE plpgsql;
COMMENT ON FUNCTION numbering_rebuild(int) IS
    'Function for numbering rebuild';
ALTER FUNCTION numbering_rebuild(in_event int) 
    OWNER TO {pyAppPgOwnerRole};


-- script that creates a trigger that decreases the quantity
-- of an item after adding a new order

CREATE TRIGGER decrement AFTER INSERT ON orders FROM EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;

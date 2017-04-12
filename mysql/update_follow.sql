drop trigger if exists update_follow;
DELIMITER $$

CREATE
    TRIGGER update_follow after INSERT
    ON user
    FOR EACH ROW
    BEGIN
    insert into follow (user_id, follower) values (NEW.user_id, New.user_id);
	  END$$

DELIMITER ;

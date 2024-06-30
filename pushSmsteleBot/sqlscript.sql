CREATE TABLE smsbot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    chatid VARCHAR(30) NOT NULL
);


#checking 
INSERT INTO smsbot (username, chatid)
VALUES ('ahied_mahi_SSL', '1387217956');



CREATE TABLE logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    chatid VARCHAR(30) NOT NULL, 
    username VARCHAR(100) NOT NULL,
    requestDetails VARCHAR(50),
    
);




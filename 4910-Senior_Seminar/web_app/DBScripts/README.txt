TO VIEW ALL THE DATA IN THE DATABASE, USE 'display.sql'
NOTE: Due to version discrepencies and permission issues with
the Clemson Buffet servers, the data could not be exported to
a seperate file, but it can still be viewed through the database
scripts.

How to run these:
*Be on campus network or open a VPN connection
1. Open file in VS Code
2. Install vscode-database extension in VS Code
3. Use CTRL-SHIFT-P to open command prompt
4. Enter SQL to find SQL commands
5. Connect to database
    5a. Select "Connect to MySQL Database"
    5b. Enter 'mysql1.cs.clemson.edu' for host
    5c. Enter 'aisner' for user
    5d. Enter 'WattTeam6' for password
    5e. Select DriverIncentiveDB
6. Reopen the command prompt (steps 3 and 4), and select Run file as Query
    Output will be printed in terminal

If you want a test user, use test1@email.com with password test1234
    make new users with the same format ^^ test#@email.com with password of test123 or user#   -- here substitute # for a number
	
	
STORED PROCEDURES: Currently, we have 2 stored procedures
1.sp_createUser
CREATE DEFINER=`aisner`@`%` PROCEDURE `sp_createUser`(
    IN p_username VARCHAR(30),
    IN p_password VARCHAR(100))
BEGIN
    if ( select exists (select 1 from ACCOUNT where Username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into ACCOUNT
        (
			Username,
            Pass
        )
        values
        (
            p_username,
            p_password
        );
     
    END IF;
END

2.sp_validateLogin
CREATE DEFINER=`aisner`@`%` PROCEDURE `sp_validateLogin`(
	IN p_username VARCHAR(30)
)
BEGIN
	select * from ACCOUNT where Username = p_username;
END
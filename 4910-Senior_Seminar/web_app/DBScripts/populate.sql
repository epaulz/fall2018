insert into ACCOUNT
values  (1,'driver','Imadriver','123 park rd','123-456-7890',0),
        (2,'sponsor','Imasponsor','456 park rd','987-654-3210',0),
        (3,'admin','Imanadmin','789 park rd','555-867-5309',0);

insert into ADMINS
values  (3,1);

insert into SPONSOR
values  (2,'Clemson University',1,3,100.00,1.00);

insert into DRIVER
values  (1,'Aidan','Isner', 'Good');

insert into WORKS_FOR
values  (2,1,10.0,'2018-09-20');

insert into ITEMS
values  (1,'Something','www.something.com',28.00,2);

insert into BUYS
values  (1,1,'2018-09-20');

insert into PAYCHECKS
values  (1,1.00,'2018-09-20',2,3);

insert into CONTACT_US
values  (0,'Someone','someone@gmail.com','someone wants something','2018-10-04');
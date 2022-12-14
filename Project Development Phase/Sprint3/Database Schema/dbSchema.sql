create table AGENT (
    ID integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    NAME varchar(225),
    EMAIL VARCHAR(225),
    PASSWORD VARCHAR(225),
    PRIMARY KEY (ID)
);

CREATE TABLE CUSTOMER(
    ID integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    NAME varchar(225),
    EMAIL VARCHAR(225),
    PASSWORD VARCHAR(225),
    PRIMARY KEY (ID)
);

CREATE TABLE TICKET(
    ID integer not null GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    ISSUE varchar(225),
    CUSTOMER_ID integer,
    AGENT_ID integer,
    STATUS VARCHAR(225),
    PRIMARY KEY (ID)
);

CREATE TABLE ADMIN(
    ID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) EMAIL VARCHAR(225),
    PASSWORD VARCHAR(225),
    NAME VARCHAR(225),
);
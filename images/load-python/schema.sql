use codetest;

drop table if exists people, places, countries, counties, cities;


create table places(
    id int not null auto_increment,
    city varchar(50),
    county varchar(50),
    country varchar(50),
    primary key (id)
)
;

create table countries(
    id int not null auto_increment,
    name varchar(50),
    primary key (id)
);

create table counties(
    id int not null auto_increment,
    name varchar(50),
    countryId int,
    primary key (id),
    foreign key (countryId) references countries (id)
);

create table cities(
    id int not null auto_increment,
    name varchar(50),
    countyId int,
    countryId int,
    primary key (id),
    foreign key (countyId) references counties (id),
    foreign key (countryId) references countries (id)
);

create table people(
    id int not null auto_increment,
    given_name varchar(50),
    family_name varchar(50),
    date_of_birth date,
    place_of_birth varchar(50),
    cityId int,
    primary key (id),
    foreign key (cityid) references cities(id)
)
;
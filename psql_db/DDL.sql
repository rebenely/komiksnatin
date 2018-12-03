create database komiksnatin;
\c komiksnatin;

drop table if exists account cascade;
drop table if exists komik cascade;
drop table if exists tag cascade;
drop table if exists tags cascade;
drop table if exists review cascade;
drop table if exists list cascade;
drop table if exists listrank cascade;
-- drop table if exists auth_user cascade;


--
-- create table if not exists auth_user (
--     id serial,
--     password varchar(128) not null,
--     last_login timestamp with time zone,
--     is_superuser boolean not null,
--     username varchar(150) not null,
--     first_name varchar(30) not null,
--     last_name varchar(150) not null,
--     email varchar(254) not null,
--     is_staff boolean not null,
--     is_active boolean not null,
--     date_joined timestamp with time zone not null,
--     primary key (id),
--     unique (username)
-- );


create table if not exists account (
    username varchar(20) check (length(username) > 4 and  username ~ '^[a-zA-Z0-9_\-]+$'),
    description varchar(200),
    accountType varchar(20) not null,
    user_id integer not null,
    -- foreign key (user_id) references auth_user on delete cascade,
    primary key (username)
);

create table if not exists komik (
    id serial,
    title varchar(100) not null check (title <> ''),
    description varchar(1000),
    rating numeric(3,2) check (rating >= 0 and rating <= 5) default 0,
    author varchar(100),
    image_url varchar(500) not null,
    primary key (id)
);


create table if not exists tag (
    id serial,
    name varchar(50) unique not null check (name <> ''),
    description varchar(500),
    primary key (id),
    unique (name)
);


create table if not exists review (
    id serial,
    user_id varchar(20) not null,
    komik_id integer not null,
    rating integer not null check (rating >= 0 and rating <= 5) default 0,
    created TIMESTAMP DEFAULT NOW(),
    comment varchar(1000),
    primary key (id),
    foreign key (user_id) references account on delete cascade,
    foreign key (komik_id) references komik,
    unique(komik_id, user_id)
);


create table if not exists tags (
    id serial,
    komik_id integer not null,
    tag_id integer not null,
    primary key (id),
    foreign key (komik_id) references komik on delete cascade,
    foreign key (tag_id) references tag on delete cascade
);

create table if not exists list (
    id serial,
    title varchar(50) not null check (title <> ''),
    description varchar(1000),
    list_size integer not null default 0,
    user_id varchar(20),
    created TIMESTAMP DEFAULT NOW(),
    foreign key (user_id) references account on delete cascade,
    primary key (id)
);

create table if not exists listrank (
    id serial,
    ranking integer not null,
    description varchar(1000),
    komik_id integer not null,
    list_id integer not null,
    primary key (id),
    foreign key (komik_id) references komik on delete cascade,
    foreign key (list_id) references list on delete cascade,
    unique (list_id, ranking),
    unique (list_id, komik_id)
);



-- Trigger for updating komik rating --
drop trigger if exists komik_rating_update on review;
drop trigger if exists komik_rating_delete on review;


CREATE OR REPLACE FUNCTION update_komik_rating()
RETURNS trigger AS
$BODY$
BEGIN
update komik set rating = (select round(coalesce(avg(rating), 0), 2) from review where komik_id = komik.id) where id = new.komik_id;
RETURN NEW;
END;
$BODY$  LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_komik_rating()
RETURNS trigger AS
$BODY$
BEGIN
update komik set rating = (select round(coalesce(avg(rating), 0), 2) from review where komik_id = komik.id) where id = old.komik_id;
RETURN NEW;
END;
$BODY$  LANGUAGE plpgsql;

create trigger komik_rating_update after insert or update on review
for each row
    execute procedure update_komik_rating();

create trigger komik_rating_delete after delete on review
for each row
    execute procedure delete_komik_rating();

-- Trigger for updtating list size --
drop trigger if exists list_size_update on listrank;
drop trigger if exists list_size_delete on listrank;


 CREATE OR REPLACE FUNCTION update_list_size()
   RETURNS trigger AS
 $BODY$
 BEGIN
  update list set list_size = (select coalesce(count(ranking), 0) from listrank where list_id = list.id) where id = new.list_id;
  RETURN NEW;
 END;
 $BODY$  LANGUAGE plpgsql;

  CREATE OR REPLACE FUNCTION delete_list_size()
   RETURNS trigger AS
 $BODY$
 BEGIN
  update list set list_size = (select coalesce(count(ranking), 0) from listrank where list_id = list.id) where id = old.list_id;
  RETURN NEW;
 END;
 $BODY$  LANGUAGE plpgsql;

create trigger list_size_update after insert or update on listrank
for each row
    execute procedure update_list_size();
create trigger list_size_delete after delete on listrank
for each row
    execute procedure delete_list_size();

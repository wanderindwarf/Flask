delete from entries;

insert into entries(date, title, content) values (now() - interval '10 days', 'First post!', 'This is first post by Denys Rekun!');
insert into entries(date, title, content) values (now() - interval '1 day', 'I love Flask', 'I am finding Flask incredibly fun.');
insert into entries(title, content) values ('Databases', 'My databases class is a lot of work, but I am enjoying it.');
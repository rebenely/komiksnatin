-- insert into account (username, password, description, isAdmin) values ('androgenic', 'amygdalar', 'enlightens', 0);
-- insert into account (username, password, description, isAdmin) values ('bedusted', 'bacchanals', 'Callum', 1);
-- insert into account (username, password, description, isAdmin) values ('cleverness', 'dauphins', 'galloons', 0);
-- insert into account (username, password, description, isAdmin) values ('gemmation', 'eggtimer', 'dahling', 1);
-- insert into account (username, password, description, isAdmin) values ('hitherward', 'fibrotic', 'elasticity', 0);

delete from account;
delete from komik;
delete from tag;
delete from tags;
delete from review;
delete from list;
delete from listrank;
delete from auth_user;

-- user: androgenic, password: amygdalar
insert into auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined) values (0, 'androgenic', 'pbkdf2_sha256$120000$I7Z1wx5hTL9x$sPyT+KXQYuHZewNsmr1L8Pwtz4w/rZCUWOrfaeC4x5c=', 'sql test', 'test', '', false, false, true, now());
insert into account (username, description, accountType, user_id) values ('androgenic', 'enlightens', 'basic', 0);

-- user: bedusted, password: bacchanals
insert into auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined) values (1, 'bedusted', 'pbkdf2_sha256$120000$xKUlpatdUY4L$7Sa6r8gK5pOsAX+nvf6u01AmmlCkgBK30OUDrbNCSeU=', 'sql test', 'test', '', false, false, true, now());
insert into account (username, description, accountType, user_id) values ('bedusted', 'Callum', 'basic', 1);

-- user: cleverness, password: dauphins
insert into auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined) values (2, 'cleverness', 'pbkdf2_sha256$120000$7EVCVrSC1W9x$lBbTEv0e2YBFVOshXxORyOY4ZsHRjby8zee8i+aHd7I=', 'sql test', 'test', '', false, false, true, now());
insert into account (username, description, accountType, user_id) values ('cleverness', 'galloons', 'basic', 2);

-- user: gemmation, password: eggtimer
insert into auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined) values (3, 'gemmation', 'pbkdf2_sha256$120000$0H8aR27xjgPO$Qv3a+UpchAFC0ZiCw+KGndaOglrmeGJ0ZF1tiIuD99c=', 'sql test', 'test', '', false, false, true, now());
insert into account (username, description, accountType, user_id) values ('gemmation', 'dahling', 'basic', 3);

-- user: hitherward, password: fibrotic
insert into auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined) values (4, 'hitherward', 'pbkdf2_sha256$120000$0H8aR27xjgPO$Qv3a+UpchAFC0ZiCw+KGndaOglrmeGJ0ZF1tiIuD99c=', 'sql test', 'test', '', false, false, true, now());
insert into account (username, description, accountType, user_id) values ('hitherward', 'elasticity', 'basic', 4);

-- user: panginoon, password: akinangmundo
insert into auth_user (id, username, password, first_name, last_name, email, is_superuser, is_staff, is_active, date_joined) values (5, 'panginoon', 'pbkdf2_sha256$120000$psww8Q506L5r$/BIU/bzbO3fbQjCmqZBxo0aiw4n/i+seVbPL8/I8AZk=', 'sql test', 'test', '', true, true, true, now());
insert into account (username, description, accountType, user_id) values ('panginoon', 'admin account', 'admin', 5);

-- set counter to max --
SELECT setval('auth_user_id_seq', (SELECT MAX(id) from "auth_user"));

-- komiks --
insert into komik (id, title, description, rating, image_url, author) values (0, 'Skyworld', 'Every legend hides a lie  A murdered Skygod re-emerges in modern-day Manila.  A Tikbalang prince plots vengeance for the death of his father.  And the Queen of the Asuang unleashes the mythical Bakunawa upon the streets of the city.  Caught in their age-old struggle is Andoy. a crippled orphan that discovers he is the fulfillment of a prophecy dating back to Lapu-Lapu himself', 0.0, 'skyworld.jpg', 'Mervin Ignacio, Ian Sta. Maria');
insert into komik (id, title, description, rating, image_url, author) values (1, 'Trese', 'When the sun sets in the city of Manila, don''t you dare make a wrong turn and end up in that dimly-lit side of the metro, where aswang run the most-wanted kidnapping rings, where kapre are the kingpins of crime, and engkantos slip through the cracks and steal your most precious possessions.  When crime takes a turn for the weird, the police call Alexandra Trese.', 0.0, 'trese.jpg', 'Budjette Tan, Kajo Baldisimo');
insert into komik (id, title, description, rating, image_url, author) values (2, 'Mythspace', 'Mythspace vol. 1 is a collection of six stories, each exploring a shared universe where Philippine folklore creatures -- Tikbalangs, Kapres, Manananggals -- were inspired by alien civilizations. Each creature is re-imagined and used to populate a science fiction universe that is rooted in Philippine oral tradition.', 0.0, 'mythspace.jpg', 'P. Chikiamco, K. Carreon, P. Quiroga, J. Gregorio, M. Dimagiba, C.R. Chua, B. Sinaban');
insert into komik (id, title, description, rating, image_url, author) values (3, 'Maktan 1521', 'nondesc', 0.0, 'maktan1521.jpg', 'Tepai Pascual');
insert into komik (id, title, description, rating, image_url, author) values (4, '14', 'nondesc', 0.0, '14.jpg', 'Manix Abrera');
insert into komik (id, title, description, rating, image_url, author) values (5, 'The Lost Journal of Alejandro Pardo: Creatures and Beasts of Philippine Folklore', 'His name was Alejandro Pardo, and this book is a strange door that contains words and pages from his writings, a strange door that leads to the truths behind the layers of rumor and misconception.  Are you ready to open it?', 0.0, 'pardo.jpg', 'Budjette Tan, David Hontiveros, Kajo Baldisimo, Bow Guerrero, Mervin Malonzo');
insert into komik (id, title, description, rating, image_url, author) values (6, 'Sixty Six', 'Kuwento ni Celestino Cabal. Kabebertdey niya lang. Mayroon siyang natanggap na regalo na ngayo''y unti-unti niyang binubuksan. Ika nga ng matatanda, ''Huli man daw at magaling''', 0.0, 'sixtysix.jpg', 'Russel Molina, Ian Sta. Maria');
insert into komik (id, title, description, rating, image_url, author) values (7, 'Numeros', 'NUMEROS is a Comic Book series published under FUM Magazine', 0.0, 'numeros.jpg', 'Ronjay Valdenor');
insert into komik (id, title, description, rating, image_url, author) values (8, 'The Mythology Class:A Graphic Novel', 'The story centers on University of the Philippines Anthropology student Nicole Lacson, a girl who holds a passionate love for Filipino myths passed down from her grandfather. Together with a motley assortment of companions, she meets the mysterious Mrs. Enkanta and races to recapture enkantos (supernatural creatures) who have escaped and are causing havoc in the human world. The story also references historical and mythological Filipino heroes like Kubin, Sulayman and Lam-ang.', 0.0, 'mythclass.jpg', 'Arnold Arre');
insert into komik (id, title, description, rating, image_url, author) values (9, 'Si Janus Silang at ang Tiyanak ng Tabon', 'Ang akala ni Janus, pangkaraniwang laro lang ang TALA Online. Sunod-sunod ang pagbabago sa buhay niya matapos ang kahindik-hindik na pangyayari sa RPG tournament sa sinalihan niya. Pero nang matuklasan niya ang tunay na kaugnayan ng larong ito sa alamat ng Tiyanak ng Tabon, wala na siyang magawa kundi ipagpatuloy ang paglalaro!', 0.0, 'janussilang.jpg', 'Edgar Calabia Samar, Carljoe Javier, Natasha Ringor');
insert into komik (id, title, description, rating, image_url, author) values (10, 'Elmer', 'Elmer is a window into a world where chickens have suddenly acquired the intelligence and consciousness of humans, where they can now consider themselves a race no different than browns, black, or whites. Recognizing themselves to be sentient, the inexplicably evolved chickens push to attain rights for themselves as the newest members of the human race.', 0.0, 'elmer.jpg', 'Gerry Alanguilan');
insert into komik (id, title, description, rating, image_url, author) values (11, 'P*cha, E ''Di Komiks', 'P*cha, E ''Di Komiks is a collection of comic strips, memes, and random artworks from creator Toto Madayag''s Facebook page, Libreng Komiks - with exclusive content found only in this book.', 0.0, 'edikomiks.jpg', 'Toto Madayag');
insert into komik (id, title, description, rating, image_url, author) values (12, 'Ang Subersibo', 'Oktubre 1881. Las Islas Filipinas. Maynila. Isang batang iskolar ang umuwi matapos ang pitong taong pag-aaral sa Alemanya upang simulan ang kaniyang buhay-propesiyonal bilang guro sa bayang sinilangan. Asawa, pamilya, at buhay na maayos at tahimik ang mga simpleng mithiin ng iskolar na ito, ngunit ang kasaysayan at tadhana ay may ibang mga plano.  Mula idealismo patungong terorismo, Ang Subersibo ay ang masalimuot, moral, at melodramatikong trahedya ng buhay ni Juan Crisostomo Ibarra y Magsalin.', 0.0, 'angsubersibo.jpg', 'Mervin Malonzo, Adam David');
insert into komik (id, title, description, rating, image_url, author) values (13, 'Ang Mundo ni Andong Agimat', 'Sa maniwala ka''t sa hindi, sabi ni Lolo, may panahon sa ating daigdig na naghari ang pinakamalakas at pinakamakapangyarihang mga nilalang sa balat ng lupa.  Ang ilan sa kanila''y naging tagapagtaguyod ng katarungan…Tagapagtanggol ng mga naapi.  Ang iba nama''y naging mga alagad ng kadiliman…Naparito upang maghasik ng lagim at salot sa sangkatauhan.  At mula sa daang taong pagtatagisan ng dalawa ay ipinanganak ang makulay na kuwento ng kagitingan at katapangan na humugis sa kanilang mundo.', 0.0, 'andongagimat.jpg', 'Arnold Arre');
insert into komik (id, title, description, rating, image_url, author) values (14, 'Agla', 'Agla [Bloodpaint Chronicles] is a historical fantasy set on the genesis of the very first of the Legendary Pintados Warriors amidst the violent politics between the Ancient Visayan Gods.', 0.0, 'agla.jpg', 'Kael Molo');
insert into komik (id, title, description, rating, image_url, author) values (15, 'Tabi Po', 'Isang lalake ang bigla na lamang nagising sa loob ng isang puno sa gitna ng kagubatan na walang alaala kung sino siya at saan siya nagmula. Ang tanging alaala lang niya ay isang imahe ng babae na nakikita niya sa kanyang panaginip, at ang tanging nararamdaman niya ay isang matinding gutom na mabilis na namumuo sa kanyang walang pusod na sikmura. Isang gutom na mapapawi lamang ng laman...at dugo.', 0.0, 'tabipo.jpg', 'Mervin Malonzo');
insert into komik (id, title, description, rating, image_url, author) values (16, 'Wasted', 'A story of love and tragedy. Jenny fell out of love from Eric. Eric started a killing spree out of desperation for the love of his life.', 0.0, 'wasted.jpg', 'Gerry Alanguilan');
insert into komik (id, title, description, rating, image_url, author) values (17, 'The Filipino Heroes League', 'Undermanned and under-funded, the Filipino Heroes League does what it can to fight against injustice.  It''s tough being a superhero but its even tougher being a third-world superhero.', 0.0, 'fhl.jpg', 'Paolo Fabregas');

-- set counter to max --
SELECT setval('komik_id_seq', (SELECT MAX(id) from "komik"));


-- tag --
insert into tag (id, name, description) values (0, 'Historical', 'Historical');
insert into tag (id, name, description) values (1, 'Crime', 'Crime');
insert into tag (id, name, description) values (2, 'Horror', 'Horror');
insert into tag (id, name, description) values (3, 'Action', 'Action');
insert into tag (id, name, description) values (4, 'Mythology', 'Mythology');
insert into tag (id, name, description) values (5, 'Comedy' , 'Comedy');
insert into tag (id, name, description) values (6, 'Romance', 'Romance');
insert into tag (id, name, description) values (7, 'Drama', 'Drama');

-- set counter to max --
SELECT setval('tag_id_seq', (SELECT MAX(id) from "tag"));


-- tags --
-- skyworld --
insert into tags (id, komik_id, tag_id) values (0, 0, 4);
insert into tags (id, komik_id, tag_id) values (1, 0, 3);
-- trese --
insert into tags (id, komik_id, tag_id) values (2, 1, 1);
insert into tags (id, komik_id, tag_id) values (3, 1, 4);
insert into tags (id, komik_id, tag_id) values (4, 1, 3);
-- mythspace --
insert into tags (id, komik_id, tag_id) values (5, 2, 4);
insert into tags (id, komik_id, tag_id) values (7, 2, 3);
insert into tags (id, komik_id, tag_id) values (8, 2, 1);
-- maktan --
insert into tags (id, komik_id, tag_id) values (9, 3, 3);
insert into tags (id, komik_id, tag_id) values (10, 3, 0);
-- 14 --
insert into tags (id, komik_id, tag_id) values (11, 4, 5);
-- lost Journal --
insert into tags (id, komik_id, tag_id) values (12, 5, 0);
insert into tags (id, komik_id, tag_id) values (13, 5, 4);
-- sixtysix --
insert into tags (id, komik_id, tag_id) values (14, 6, 3);
insert into tags (id, komik_id, tag_id) values (15, 6, 7);
-- numeros --
insert into tags (id, komik_id, tag_id) values (16, 7, 2);
-- myth class --
insert into tags (id, komik_id, tag_id) values (17, 8, 3);
insert into tags (id, komik_id, tag_id) values (18, 8, 4);
-- janus silang --
insert into tags (id, komik_id, tag_id) values (19, 9, 3);
insert into tags (id, komik_id, tag_id) values (20, 9, 4);
-- elmer --
insert into tags (id, komik_id, tag_id) values (21, 10, 7);
-- pocha --
insert into tags (id, komik_id, tag_id) values (22, 11, 5);
-- subersibo --
insert into tags (id, komik_id, tag_id) values (23, 12, 0);
-- andong --
insert into tags (id, komik_id, tag_id) values (24, 13, 3);
-- agla --
insert into tags (id, komik_id, tag_id) values (25, 14, 4);
-- tabi po --
insert into tags (id, komik_id, tag_id) values (26, 15, 4);
insert into tags (id, komik_id, tag_id) values (27, 15, 0);
-- wasted --
insert into tags (id, komik_id, tag_id) values (28, 16, 6);
insert into tags (id, komik_id, tag_id) values (29, 16, 7);
-- fhl --
insert into tags (id, komik_id, tag_id) values (30, 17, 1);
insert into tags (id, komik_id, tag_id) values (31, 17, 3);

-- set counter to max --
SELECT setval('tags_id_seq', (SELECT MAX(id) from "tags"));

-- reviews --
insert into review (id, rating, comment, komik_id, user_id) values (0, 5, 'Summer Komikon 2012 saw the launch of Mervin Ignacio and Ian Sta. Maria''s Skyworld as a two-volume trade paperback collection from National Bookstore which collected the graphic novel series originally self-published by the duo. I have the first three graphic novels, which were released in previous Komikons and of which I have done reviews here. A fourth one was unpublished but is included in the second volume of the collection.', 0, 'androgenic');
insert into review (id, rating, comment, komik_id, user_id) values (1, 2, 'I am rating this first volume (composed of Book 1: Apocrypha and Book 2: Testament) as if I have not read its second volume. The reason is that the second volume has the background of the story. I would have liked this first volume if parts of that background were somehow captured into the narration.', 0, 'bedusted');
insert into review (id, rating, comment, komik_id, user_id) values (2, 5, 'Trese rocks! It''s an anthology of stories created by Budjette Tan and Kajo Baldisimo featuring Alexandra Trese, bar owner and occult investigator. The local police in the stories make it a habit to call Trese when the case get even a hint of the supernatural. In this volume, she faces up aswangs, elementals and tikbalangs. Good things she''s got the Kambal backing her up.', 1, 'cleverness');
insert into review (id, rating, comment, komik_id, user_id) values (3, 4, 'One of the highly recommended Filipino books that was mentioned during the Filipino Fridays meme for ReaderCon was the Trese series. At first I hesitated in buying the books because they didn''t seem like my kind of thing, but several people attested to its greatness so I just went ahead and bought them.', 1, 'gemmation');
insert into review (id, rating, comment, komik_id, user_id) values (4, 4, 'Mythspace, Volume 1 is an anthology of related stories in the vein of science fiction mishmashed with Philippine folklore creating a new genre of its own. Currently, it is the only work of its kind, so its classified as speculative fiction but I really like the promise of local comic books that doesn''t use folklore in a horror setting but instead blazes a trail into a new frontier. The writer promotes this a space opera; I think a better description would be Star Wars and Folklore.', 2, 'hitherward');
insert into review (id, rating, comment, komik_id, user_id) values (5, 3, 'I appreciate this book that uses the less know facts about one of the most important Philippine heroes. Through this book, more young people would learn and appreciate what Lapu-Lapu contributed to what we are as a nation.', 3, 'hitherward');
insert into review (id, rating, comment, komik_id, user_id) values (6, 5, 'Look at all those chickens!', 10, 'gemmation');
insert into review (id, rating, comment, komik_id, user_id) values (7, 4, 'Super lolo, kaso bitin', 6, 'androgenic');
insert into review (id, rating, comment, komik_id, user_id) values (8, 4, 'Love, madness, death. This komiks is devastatingly real and violent but puts a balance into beautiful and heartbreaking. So many feelings burst inside. ', 16, 'bedusted');
insert into review (id, rating, comment, komik_id, user_id) values (9, 3, 'Super (heroes)hirap', 17, 'cleverness');

-- set counter to max --
SELECT setval('review_id_seq', (SELECT MAX(id) from "review"));

-- list --
insert into list (id, title, description, list_size, user_id) values (0, 'Top 10 Plot Twists', 'Will catch you off guard', 0, 'cleverness');
insert into list (id, title, description, list_size, user_id) values (1, 'Must read', 'Read this', 0, 'hitherward');
insert into list (id, title, description, list_size, user_id) values (2, 'Mga nabasa ko', 'Mga nabasa ko', 0, 'bedusted');
insert into list (id, title, description, list_size, user_id) values (3, 'Test List', 'Edit this', 0, 'panginoon');

-- set counter to max --
SELECT setval('list_id_seq', (SELECT MAX(id) from "list"));

-- listrank --
insert into listrank (id, ranking, description, komik_id, list_id) values (0, 1, 'YOU', 0, 0);
insert into listrank (id, ranking, description, komik_id, list_id) values (1, 2, 'LOST', 1, 0);
insert into listrank (id, ranking, description, komik_id, list_id) values (2, 3, 'THE', 2, 0);
insert into listrank (id, ranking, description, komik_id, list_id) values (3, 4, 'GAME', 3, 0);

insert into listrank (id, ranking, description, komik_id, list_id) values (4, 1, 'Never', 4, 1);
insert into listrank (id, ranking, description, komik_id, list_id) values (5, 2, 'Gonna', 5, 1);
insert into listrank (id, ranking, description, komik_id, list_id) values (6, 3, 'Give', 6, 1);
insert into listrank (id, ranking, description, komik_id, list_id) values (7, 4, 'You', 7, 1);
insert into listrank (id, ranking, description, komik_id, list_id) values (8, 5, 'Up', 8, 1);

insert into listrank (id, ranking, description, komik_id, list_id) values (9, 1, 'ranked as 1', 7, 2);
insert into listrank (id, ranking, description, komik_id, list_id) values (10, 2, 'ranked as 2', 14, 2);
insert into listrank (id, ranking, description, komik_id, list_id) values (11, 3, 'ranked as 3', 2, 2);
insert into listrank (id, ranking, description, komik_id, list_id) values (12, 4, 'ranked as 4', 4, 2);

insert into listrank (id, ranking, description, komik_id, list_id) values (13, 1, 'ranked as 1', 5, 3);
insert into listrank (id, ranking, description, komik_id, list_id) values (14, 2, 'ranked as 2', 4, 3);
insert into listrank (id, ranking, description, komik_id, list_id) values (15, 3, 'ranked as 3', 2, 3);
insert into listrank (id, ranking, description, komik_id, list_id) values (16, 4, 'ranked as 4', 8, 3);

-- set counter to max --
SELECT setval('listrank_id_seq', (SELECT MAX(id) from "listrank"));

    -- SELECT pg_terminate_backend (pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'cs165';
    -- \i C:/RE/School/CS 165/project/psql_db/DDL.sql'
    -- DROP SCHEMA public CASCADE;
    -- CREATE SCHEMA public;

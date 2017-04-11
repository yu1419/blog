DROP TABLE IF EXISTS blog.user;
create table blog.user (
  user_name varchar(30) UNIQUE,
  hashed_password varchar(500) not NULL,
  last_time datetime DEFAULT CURRENT_TIMESTAMP,
  user_id bigint NOT NULL AUTO_INCREMENT,
  real_user BOOLEAN DEFAULT 1,
  activated BOOLEAN DEFAULT 0,
  primary key (user_id)
)
;

Drop table if exists blog.category;
create table blog.category(
  category_name varchar(50) not NULL,
  post_id bigint,
  id int AUTO_INCREMENT,
  primary key(id)
);

DROP TABLE IF EXISTS blog.post;
create table blog.post (
  user_id bigint not NULL,
  content TEXT,
  title varchar(100),
  post_time datetime DEFAULT CURRENT_TIMESTAMP,
  last_modified datetime DEFAULT CURRENT_TIMESTAMP,
  post_id bigint NOT NULL AUTO_INCREMENT,
  primary key (post_id)
)
;
DROP TABLE IF EXISTS blog.comment;
create table blog.comment (
  user_id bigint not NULL,
  reply_to_id bigint default NULL,
  comment_content TEXT not NULL,
  comment_time datetime DEFAULT CURRENT_TIMESTAMP,
  comment_id bigint NOT NULL AUTO_INCREMENT,
  post_id bigint NOT NULL,
  primary key (comment_id)
)
;
DROP TABLE if EXISTS blog.tag;
create table blog.tag(
  post_id bigint default NULL,
  tag_name varchar(100) not NULL,
  pare_id bigint NOT NULL AUTO_INCREMENT,
  INDEX(tag_name),
  primary key (pare_id)
)

DROP TABLE if EXISTS blog.follow;
create table blog.follow(
  user_id bigint not NULL,
  follower bigint not NULL, #user_id who follow current user
  pare_id bigint NOT NULL AUTO_INCREMENT,
  follow_time datetime DEFAULT CURRENT_TIMESTAMP,
  primary key (pare_id)
)

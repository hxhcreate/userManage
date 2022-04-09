CREATE DATABASE `usermanage`;
use `usermanage`;
CREATE TABLE `user`
(
    `id`        int(11)      NOT NULL AUTO_INCREMENT,
    `username`  varchar(20)  NOT NULL,
    `password`  varchar(255) NOT NULL,
    `role`      tinyint(1)   NOT NULL DEFAULT 1,
    `sex`       tinyint(1)            DEFAULT NULL,
    `telephone` varchar(255) NOT NULL,
    `address`   varchar(255)          DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `telephone` (`telephone`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

-- id：用户id号，自增长
-- username：用户名
-- password：密码
-- role：用户角色，0表示管理员用户，1表示普通用户  默认普通用户
-- sex：性别，0表示男性，1表示女性，允许为空
-- telephone：手机号
-- address：联系地址，允许为空
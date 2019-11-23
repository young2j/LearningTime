```shell
odoo12/odoo-bin #启动服务
# 出错1
# psycopg2.OperationalError: could not connect to server: No such file or directory
#        Is the server running locally and accepting
#        connections on Unix domain socket "/tmp/.s.PGSQL.5432"? - - -

# 修改
sudo vim /etc/postgresql/9.5/main/postgresql.conf
unix_socket_directories = '/tmp'


# 出错2
# psycopg2.OperationalError: FATAL:  role "jge" does not exist
sudo su - postgres -c 'createuser [-s] jge' # -c command; -s superuser
```

# 创建角色并赋予权限

```pgp
CREATE ROLE  jge CreateDB  superuser Createrole Replication login;  #创建用户/角色并赋予权限
\du # 查看角色及属性
\q #退出 psql
```

# 权限管理

```pgp
# 授予权限
GRANT privilege [, ...]
ON object [, ...]
TO { PUBLIC | GROUP group | username }

# 收回权限
REVOKE privilege [, ...]
ON object [, ...]
FROM { PUBLIC | GROUP groupname | username }
```

* privilege − 值可以为：SELECT，INSERT，UPDATE，DELETE， RULE，ALL。

* object − 要授予访问权限的对象名称。可能的对象有： table， view，sequence。
  *  PUBLIC − 表示所有用户。
  * GROUP group − 为用户组授予权限。
  * username − 要授予权限的用户名。PUBLIC 是代表所有用户的简短形式。
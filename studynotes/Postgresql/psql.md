### install by tarball

```shell
1.  解压
2.  添加/bin到profile
3.  pgsql/bin/initdb -D pgsql/data
4.  pgsql/bin/pg_ctl -D /mnt/APPS/pgsql/data -l  /mnt/APPS/pgsql/data/logfile start #启动服务
5.  pgsql/bin/createdb test #创建数据库
6.  psql test # 进入sql shell

# 最好在环境变量里指定PGDATA路径
pg_ctl start [-D]
pg_ctl stop [-D]
pg_ctrl status [-D]

see more:
pg_ctl --help
```


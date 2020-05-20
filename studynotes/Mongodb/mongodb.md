## install by tarball
```shell
1. 解压 
2. 添加环境变量/bin
3. sudo mkdir -p /mnt/APPS/mongodb/data/db/
4. sudo mkdir -p /mnt/APPS/mongodb/data/log
5. sudo touch /mnt/APPS/mongodb/data/log/mongod.log
6. mongod --dbpath /mnt/APPS/mongodb/data/db/ --logpath /mnt/APPS/mongodb/data/log/mongod.log --fork
7. cat /mnt/APPS/mongodb/data/log/mongod.log 
```

### Start MongoDB

```shell
sudo service mongod start
```

### Verify that MongoDB has started successfully

```shell
sudo service mongod status
```

### Stop MongoDB

```shell
sudo service mongod stop
```

### Restart MongoDB

```shell
sudo service mongod restart
```

### Begin using MongoDB

```shell
mongo
```

### Uninstall MongoDB Community Edition

#### Stop MongoDB

```shell
sudo service mongod stop
```

#### Remove Packages

```shell
sudo apt-get purge mongodb-org*
```

#### Remove Data Directories

```shell
sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb
```

# mongod.conf

```python
#日志文件位置
logpath=/data/db/journal/mongodb.log　

# 以追加方式写入日志
logappend=true

# 是否以守护进程方式运行
fork = true

# 默认27017
#port = 27017

# 数据库文件位置
dbpath=/data/db

# 启用定期记录CPU利用率和 I/O 等待
#cpu = true

# 是否以安全认证方式运行，默认是不认证的非安全方式
#noauth = true
#auth = true

# 详细记录输出
#verbose = true

# Inspect all client data for validity on receipt (useful for
# developing drivers)用于开发驱动程序时验证客户端请求
#objcheck = true

# Enable db quota management
# 启用数据库配额管理
#quota = true
# 设置oplog记录等级
# Set oplogging level where n is
#   0=off (default)
#   1=W
#   2=R
#   3=both
#   7=W+some reads
#diaglog=0

# Diagnostic/debugging option 动态调试项
#nocursors = true

# Ignore query hints 忽略查询提示
#nohints = true
# 禁用http界面，默认为localhost：28017
#nohttpinterface = true

# 关闭服务器端脚本，这将极大的限制功能
# Turns off server-side scripting.  This will result in greatly limited
# functionality
#noscripting = true
# 关闭扫描表，任何查询将会是扫描失败
# Turns off table scans.  Any query that would do a table scan fails.
#notablescan = true
# 关闭数据文件预分配
# Disable data file preallocation.
#noprealloc = true
# 为新数据库指定.ns文件的大小，单位:MB
# Specify .ns file size for new databases.
# nssize =

# Replication Options 复制选项
# in replicated mongo databases, specify the replica set name here
#replSet=setname
# maximum size in megabytes for replication operation log
#oplogSize=1024
# path to a key file storing authentication info for connections
# between replica set members
#指定存储身份验证信息的密钥文件的路径
#keyFile=/path/to/keyfile
```

#### Failed to start mongod.service: Unit mongod.service not found.

```
[Unit]
Description=High-performance, schema-free document-oriented database
After=network.target
Documentation=https://docs.mongodb.org/manual

[Service]
User=jge
Group=root
ExecStart=/mnt/APPS/mongodb/bin/mongod --config /mnt/APPS/mongodb/conf/mongod.conf

[Install]
WantedBy=multi-user.target
```


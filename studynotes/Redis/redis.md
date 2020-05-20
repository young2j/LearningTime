# 安装
安装好后redis/src下会生成可执行文件redis-server/redis-cli等，并添加进了/usr/local/bin中；

```shell
sudo tar -zxvf redis.tar.gz
cd redis
sudo make
cd ./src
sudo make install 
```
> Makefile:293: recipe for target 'adlist.o' failed
> cd redis
> make clean
> make hiredis jemalloc linenoise lua geohash-int
> cd ./src && sudo make install

## 启动redis-server
```shell
redis-server [redis.conf]
```
## 启动redis-cli
```shell
    redis-cli
```

# redis数据库
* Redis支持多个数据库(数据字典)，并且每个数据库的数据是隔离的不能共享，并且基于单机才有，如果是集群就没有数据库的概念。
* 这些数据库更像是一种命名空间，而不适宜存储不同应用程序的数据，所以不同的应用应该使用不同的Redis实例存储数据.
* 数据库从0开始递增以数字命名，不支持自定义数据库的名字。
* Redis默认支持16个数据库（可以通过配置文件支持更多，无上限），可以通过配置databases来修改这一数字。
* Redis也不支持为每个数据库设置不同的访问密码，所以一个客户端要么可以访问全部数据库，要么连一个数据库也没有权限访问。
* 注意：FLUSHALL命令可以清空一个Redis实例中所有数据库中的数据。。


# redis配置
Redis 的配置文件位于 Redis 安装目录下，文件名为 redis.conf(Windows 名为 redis.windows.conf)。
各项配置含义：https://www.runoob.com/redis/redis-conf.html
```shell
config get name //获取配置信息
config get * //获取所有配置项

config set name value //设置配置项
```

# Redis数据类型
## string
* string类型最大存储512MB
```shell
set key value
get key
del key
```
## hash
* Redis hash 是一个键值(key=>value)对集合
* 每个 hash 可以存储 232 -1 键值对（40多亿）
```shell
hmset object k1 "v1" k2 "v2"
hmget object k1 k2
hget object k1
del object
```

## list
* Redis 列表是简单的字符串列表，按照插入顺序排序。你可以添加一个元素到列表
的头部（左边）或者尾部（右边）。
```shell
lpush listKey "v1" "v2"
rpush listKey "v3" "v4"
lrange listKey 0 3 //包含收尾，0 1 2 3
del listKey
```

## set
* Redis 的 Set 是 string 类型的无序集合。元素是唯一的。
* 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是 O(1)。
* 集合中最大的成员数为 232 - 1(4294967295, 每个集合可存储40多亿个成员)。
```shell
sadd setKey e1 e2 //设置成功返回元素个数
sadd setKey e1 //设置已存在元素，返回0
smembers setKey
del smembers
```
## zset (sorted set)
* Redis zset 和 set 一样也是string类型元素的集合,且不允许重复的成员。
* 每个元素都会关联一个double类型的分数score,redis正是通过分数来为集合中的成员进行从小到大的排序
```shell
zadd zsetKey 0 "zero"
zadd zsetKey 1 "one"
zadd zsetKey 2 "two"
zrange zsetKey 0 1
zrangebyscore zsetKey 0 2
del zsetKey
```
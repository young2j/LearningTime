# mysql8.0安装
1. 下载[mysql-apt-config_0.8.15-1_all.deb](https://dev.mysql.com/downloads/repo/apt/)
2. 安装
```shell
sudo dpkg -i mysql-apt-config_0.8.15-1_all.deb
sudo apt update
sudo apt install mysql-server [-y] # root-secret: jge520
```
3. 查看信息
```shell
sudo systemctl start mysql.service # wsl会报错，基本无解,就是systemctl不适合wsl

sudo systemctl status mysql.service 

sudo mysqladmin -u root version -p #简单查看信息

mysql -h host_name -u user -p password
```
3. 卸载
```shell
sudo systemctl stop mysql.service && sudo systemctl disable mysql.service

sudo apt purge mysql*
sudp apt autoremove
```

# 四种启动方式
1. mysqld
```shell
启动mysql服务器: 
./mysqld --defaults-file=/etc/my.cnf --user=root
客户端连接: 
mysql --defaults-file=/etc/my.cnf 或 mysql -S /tmp/mysql.sock
```
2. mysqld_safe
```shell
启动mysql服务器: 
./mysqld_safe --defaults-file=/etc/my.cnf --user=root &
客户端连接: 
mysql --defaults-file=/etc/my.cnf 或 mysql -S /tm/mysql.sock
```
3. mysql.server
```shell
cp -v /usr/local/mysql/support-files/mysql.server /etc/init.d/
chkconfig --add mysql.server
启动mysql服务器:
service mysql.server {start|stop|restart|reload|force-reload|status}
客户端连接: 同1、2
```
4.mysqld_multi
```shell
mkdir $MYSQL_BASE/data2
cat <<-EOF>> /etc/my.cnf
[mysqld_multi]
mysqld = /usr/local/mysql/bin/mysqld_safe
mysqladmin = /user/local/mysql/bin/mysqladmin
user = mysqladmin
password = mysqladmin

[mysqld3306]
port   = 3306
socket   = /tmp/mysql3306.sock
pid-file = /tmp/mysql3306.pid
skip-external-locking
key_buffer_size = 16M
max_allowed_packet = 1M
table_open_cache = 64
sort_buffer_size = 512K
net_buffer_length = 8K
read_buffer_size = 256K
read_rnd_buffer_size = 512K
myisam_sort_buffer_size = 8M
basedir = /usr/local/mysql
datadir = /usr/local/mysql/data

[mysqld3307]
port   = 3307
socket   = /tmp/mysql3307.sock
pid-file = /tmp/mysql3307.pid
skip-external-locking
key_buffer_size = 16M
max_allowed_packet = 1M
table_open_cache = 64
sort_buffer_size = 512K
net_buffer_length = 8K
read_buffer_size = 256K
read_rnd_buffer_size = 512K
myisam_sort_buffer_size = 8M
basedir = /usr/local/mysql
datadir = /usr/local/mysql/data2
EOF

#mysql -S /tmp/mysql3306.sock
mysql>GRANT SHUTDOWN ON *.* TO 'mysqladmin'@'localhost' identified by 'mysqladmin' with grant option;

#mysql -S /tmp/mysql3307.sock
mysql>GRANT SHUTDOWN ON *.* TO 'mysqladmin'@'localhost' identified by 'mysqladmin' with grant option;

启动mysql服务器:./mysqld_multi --defaults-file=/etc/my.cnf start 3306-3307
关闭mysql服务器:mysqladmin shutdown
```
# windows下启动关闭
```shell
启动： mysqld --console 或 net start mysql
关闭： mysqladmin -u root shutdown 或 net stop mysql
```
#linux下启动关闭
```shell
启动： service mysql start
停止: service mysql stop
重启服务: service mysql restart
```
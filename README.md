Its easy to restore binlogs using python 

Usage : 
-------

python3 restore_binlog.py --host localhost --user root --password rootpass --binlog-dir /var/lib/mysql --start-time "2026-02-18 10:00:00"

Alternative Method : 
--------------------

Step 1 : Create a sql format file for restore 

mysqlbinlog --start-datetime="2026-02-18 10:00:00" mysql-bin.000123 > filtered.sql 

Step 2 : Restore the file 

mysql -u root -p < filtered.sql

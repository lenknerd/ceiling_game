#!/usr/bin/python3
from datetime import datetime
import mysql.connector


# Connect
cnx = mysql.connector.connect(user='root', password='red6warm',
                              host='127.0.0.1',
                              database='ceiling_game')
cursor = cnx.cursor()

quer = '''
  set @lt=NULL;
  select min(b.distance) as min_d, event_idx, event_type from
  (
    SELECT @rn:=@rn+1 as event_idx, `t`, @lt last_t, @lt:=t curr_t, `event_type`
    from (
      select `t`, `event_type` FROM `events`
      order by `t`
    ) t1, (SELECT @rn:=-1) t2
  ) as a
  inner join distances as b
    on b.t > a.last_t
    and b.t < a.curr_t
  group by event_idx;
'''

for result in cursor.execute(quer, multi=True):
    if result.with_rows:
        print("Rows produced by statement '{}':".format(
            result.statement))
        print(result.fetchall())
    else:
        print("Number of rows affected by statement '{}': {}".format(
            result.statement, result.rowcount))

cnx.close()


# coding:utf-8
from MySQLdb import connect
from db_const import HOSTNAME, USERNAME, PASSWORD, DATABASE

class DB(object):
    def __init__(self,
                 username=USERNAME,
                 passwd=PASSWORD,
                 hostname=HOSTNAME,
                 db=DATABASE):
        self._con = connect(hostname, username, passwd, db)

    @staticmethod
    def Dict2Str(Dict):
        header = Dict.keys()
        # insert data must be include ''
        body = ['"' + Dict[key] + '"' for key in header]
        return header, body

    def execute(self, cmd, get_all=True):
        with self._con as cur:
            cur.execute(cmd)
            if get_all:
                return cur.fetchall()
            else:
                return cur.fetchone()

    def insert(self, table, Dict):
        header, body = self.Dict2Str(Dict)
        with self._con as cur:
            cmd = "insert into {table} ({head}) VALUES ({val});".format(
                table=table,
                head=u','.join(header).encode('utf-8'),
                val=u','.join(body).encode('utf-8')
            )
            cur.execute(cmd)

    def insert_all(self, table, Dict_list):
        cmd = "insert into {table} ({head}) VALUES ({val});"
        with self._con as cur:
            for each in Dict_list:
                header, body = self.Dict2Str(each)
                insert_cmd = cmd.format(
                    table=table,
                    head=u','.join(header).encode('utf-8'),
                    val=u','.join(body).encode('utf-8'))
                print insert_cmd
                cur.execute(cmd.format(
                    table=table,
                    head=u','.join(header).encode('utf-8'),
                    val=u','.join(body).encode('utf-8')
                ))

    def update(self, table, Dict, condDict):
        header, body = self.Dict2Str(Dict)
        updateList = []
        for head, val in zip(header, body):
            updateList.append(u'='.join([head, val]).encode('utf-8'))
        with self._con as cur:
            cmd = "update {table} set {update} WHERE {key}='{value}';".format(
                table=table,
                update=u','.join(updateList).encode('utf-8'),
                key=condDict.keys()[0],
                value=condDict.values()[0]
            )
            cur.execute(cmd)

    def delete(self, table, condDict):
        with self._con as cur:
            cmd = "delete from {table} WHERE {key}='{value}';".format(
                table=table,
                key=condDict.keys()[0],
                value=condDict.values()[0]
            )
            cur.execute(cmd)


if __name__ == '__main__':
    # test
    db = DB()
    db.insert_all('users', [{'username': 'chencheng',
                             'password': '123',
                             'email': '291552579@qq.com',
                             'create_at': '2017-11-28 16:02',
                             'is_active': 'Y',
                             'is_admin': 'Y'},
                            {'username': u'佳绩正',
                             'password': '123',
                             'email': 'jiajizhen@test.com',
                             'create_at': '2017-11-30 11:38',
                             'is_active': 'Y',
                             'snp_table': 'snp_mRNA_table',
                             'expr_table': 'expr_gene_pos',
                             'desc_table': 'locus_gene_mlocus'}])





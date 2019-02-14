#coding=utf-8
import MySQLdb

class ReportData:  
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='test',
            db='test',
            charset="utf8",
        )
    def changeDB(self,dbname):
        if dbname=='d_easyhin_card_center':
            self.conn.close()
            self.conn = MySQLdb.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='welcome123',
                db='d_easyhin_card_center',
                charset="utf8",
            )

        return 'change db to %s successfully' %(dbname)
    def __del__(self):
	    self.conn.close()
    def jdbc(self,sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            return results
        except:
            print "Error: unable to fecth data"
    #注册用户城市分布

    def get_his_finance_manage_daily_data(self,spot_id,group_flag):
        sql = """
  SELECT
  f_crt_date,
  f_spot,
  SUM(f_pay_cnt),
  SUM(f_tc_pay_cnt),
  SUM(f_eb_income),
  SUM(f_en_income),
  SUM(f_ebh_income),
  SUM(f_kq_income),
  SUM(f_yk_income),
  SUM(f_nfm_income),
  SUM(f_pf_income),
  SUM(f_yy_income),
  SUM(f_zy_income),
  SUM(f_yc_income),
  SUM(f_ym_income),
  SUM(f_nfm_sh_income),
  SUM(f_tck_income),
  SUM(f_hjk_income),
  SUM(f_other_income),
  IFNULL(SUM((f_eb_income+f_en_income+f_ebh_income+f_kq_income+f_yk_income+f_nfm_income+f_pf_income+f_yy_income+f_zy_income+f_ym_income+f_jy_income+f_tck_income+f_hjk_income+f_other_income+f_yc_income+f_nfm_sh_income)),0) AS f_total_income,
  IFNULL(ROUND(SUM(f_tol_income)/SUM(f_kdj_cnt),2),0) AS f_kdj,
  IFNULL(ROUND(SUM(f_tol_income)/SUM(f_kdj_kt_cnt),2),0) AS f_kdj_kt,
  SUM(f_vip_sale_cnt),
  SUM(f_vip_first_money),
  SUM(f_vip_again_money),
  SUM(f_vip_total),
  SUM(f_vip_cost),
  SUM(f_sf_tf),
  SUM(f_vip_xfth),
  SUM((f_vip_xfth+f_sf_tf)) AS f_total_tf,
  SUM((f_eb_income+f_en_income+f_ebh_income+f_kq_income+f_yk_income+f_nfm_income+f_pf_income+f_yy_income+f_zy_income+f_ym_income+f_jy_income+f_tck_income+f_hjk_income+f_other_income+f_vip_total+f_yc_income+f_nfm_sh_income)-f_vip_cost) AS f_total
FROM
  t_views_his_finance_manage_daily
  WHERE 
  f_crt_date>=DATE_FORMAT(DATE_SUB(CURRENT_DATE(),INTERVAL 1 DAY),'%Y-%m-01') AND f_crt_date<CURRENT_DATE()
  AND f_spot_id ="""+str(spot_id)
        if group_flag == 1:
            sql = sql + " GROUP BY f_crt_date"
        #print sql
        return self.jdbc(sql);

if __name__ == "__main__":
    rd=ReportData()
    rs=rd.get_his_discount_money(59)
    print rs[0]

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedStyle
import time
from threading import Thread
from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error
import requests
from tkcalendar import Calendar, DateEntry

#  ################ DATABASE ################

def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
 
    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return db

#  ################ MENU 1 ################

# อุบัติเหตุ
def menu1():    
    def ser1():
           
        db_config = read_db_config()

        qaccident1 = """INSERT IGNORE er_nursing_detail (vn,arrive_time)
                            SELECT nu.vn,CONCAT(nu.vstdate," ",nu.vsttime)
                            from
                            (SELECT
                            ovstdiag.hn,
                            ovstdiag.vn,
                            ovstdiag.vstdate,
                            ovstdiag.vsttime,
                            ovstdiag.icd10
                            FROM
                            ovstdiag
                            WHERE
                            ovstdiag.vn NOT IN (SELECT vn FROM er_nursing_detail) AND
                            ovstdiag.icd10 LIKE "%%V%%" OR
                            ovstdiag.icd10 LIKE "%%W%%" OR
                            ovstdiag.icd10 LIKE "%%X%%" OR
                            ovstdiag.icd10 LIKE "%%Y%%") as nu
                            WHERE nu.vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) """

        qaccident =  """UPDATE er_nursing_detail e INNER JOIN opdscreen o on o.vn=e.vn 
                            set e.arrive_time = CONCAT(o.vstdate," ",ADDTIME(o.vsttime,'00:00:59'));

                            UPDATE er_nursing_detail SET report_doctor_time = DATE(arrive_time);
                            UPDATE er_nursing_detail SET doctor_finish_time = DATE(arrive_time);
                            UPDATE er_nursing_detail SET trauma ='Y' WHERE bba ='N';
                            UPDATE er_nursing_detail SET trauma ='Y' WHERE trauma is null;
                            UPDATE er_nursing_detail SET gcs_e = '4' WHERE gcs_e = '0' or gcs_e is null;
                            UPDATE er_nursing_detail SET gcs_v = '5' WHERE gcs_v = '0' or gcs_v is null;
                            UPDATE er_nursing_detail SET gcs_m = '6' WHERE gcs_m = '0' or gcs_m is null;
                            UPDATE er_nursing_detail SET pupil_l ='3' WHERE pupil_l ='0' or pupil_l is null;
                            UPDATE er_nursing_detail SET pupil_r ='3' WHERE pupil_r ='0' or pupil_r is null;
                            UPDATE er_nursing_detail SET er_accident_type_id = '19' WHERE er_accident_type_id is null ;
                            UPDATE er_nursing_detail SET er_refer_sender_id = '6' WHERE er_refer_sender_id is null ;
                            UPDATE er_nursing_detail SET accident_transport_type_id = '99' WHERE accident_transport_type_id is null ;
                            UPDATE er_nursing_detail SET accident_place_type_id = '99' WHERE accident_place_type_id is null ;
                            UPDATE er_nursing_detail SET accident_person_type_id = '9' WHERE accident_person_type_id is null ;
                            UPDATE er_nursing_detail SET accident_alcohol_type_id = '2' WHERE accident_alcohol_type_id is null ;
                            UPDATE er_nursing_detail SET accident_drug_type_id = '2' WHERE accident_drug_type_id is null ;
                            UPDATE er_nursing_detail SET visit_type = '1' WHERE visit_type is null ;
                            UPDATE er_nursing_detail SET er_emergency_type = '4' WHERE er_emergency_type is null ;

                            UPDATE er_nursing_detail SET        accident_airway_type_id ='3'    WHERE accident_airway_type_id  is null;
                            UPDATE er_nursing_detail SET        accident_bleed_type_id ='2'     WHERE accident_bleed_type_id  is null;
                            UPDATE er_nursing_detail SET        accident_belt_type_id ='9'      WHERE accident_belt_type_id  is null;
                            UPDATE er_nursing_detail SET        accident_helmet_type_id ='9'    WHERE accident_helmet_type_id  is null;
                            UPDATE er_nursing_detail SET        accident_splint_type_id ='3'    WHERE accident_splint_type_id  is null;
                            UPDATE er_nursing_detail SET        accident_fluid_type_id ='3'     WHERE accident_fluid_type_id  is null;

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='1'  
                            WHERE od.icd10  BETWEEN 'V01' AND 'V8999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='2'  
                            WHERE od.icd10  BETWEEN 'W00' AND 'W1999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='3'  
                            WHERE od.icd10  BETWEEN 'W20' AND 'W4999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='4'  
                            WHERE od.icd10  BETWEEN 'W50' AND 'W6499';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='5'  
                            WHERE od.icd10  BETWEEN 'W65' AND 'W7499';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='6'  
                            WHERE od.icd10  BETWEEN 'W75' AND 'W8499';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='7' 
                            WHERE od.icd10  BETWEEN 'W85' AND 'W9999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='8'  
                            WHERE od.icd10  BETWEEN 'X00' AND 'X0999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='9'  
                            WHERE od.icd10  BETWEEN 'X10' AND 'X1999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='10'  
                            WHERE od.icd10  BETWEEN 'X20' AND 'X2999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='11'  
                            WHERE od.icd10  BETWEEN 'X30' AND 'X3999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='12'  
                            WHERE od.icd10  BETWEEN 'X40' AND 'X4999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='13'  
                            WHERE od.icd10  BETWEEN 'X50' AND 'X5799';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='14'  
                            WHERE od.icd10  BETWEEN 'X58' AND 'X5999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='15'  
                            WHERE od.icd10  BETWEEN 'X60' AND 'X8499';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='16'  
                            WHERE od.icd10  BETWEEN 'X85' AND 'Y0999';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='17'  
                            WHERE od.icd10  BETWEEN 'Y10' AND 'Y3399';

                            UPDATE er_nursing_detail er INNER JOIN ovstdiag od on od.vn=er.vn set er_accident_type_id ='18'  
                            WHERE od.icd10  BETWEEN 'Y35' AND 'Y3699';"""
            
             
        # connect to the database server
        conn = MySQLConnection(**db_config)
 
        # execute the query
        cursor1 = conn.cursor()
        cursor1.execute(qaccident1)
        conn.commit()
            
        # execute the multi query
        cursor = conn.cursor()
        for result in cursor.execute(qaccident, multi=True):
            pass
        conn.commit()
        time.sleep(2)       
            
        pacci =(cursor1.rowcount)
        paccident = (f'เพิ่มข้อมูลแล้ว จำนวน {pacci} เรคคอร์ด') 
        messagebox.showinfo("การดำเนินการ",paccident,parent=window)

        cursor.close()
        conn.close()

# ฝากครรภ์
    def ser2():

        db_config = read_db_config()
        qancid = """ALTER TABLE person_anc_other_precare MODIFY COLUMN person_anc_other_precare_id
                        int(11) NOT NULL AUTO_INCREMENT FIRST"""

        qancdrop = """DROP TABLE IF EXISTS nu_anc;
        
                            CREATE TABLE nu_anc (person_anc_id VARCHAR ( 255 ) DEFAULT NULL,
                                    no1 VARCHAR ( 255 ) DEFAULT NULL,
                                    n1 date DEFAULT NULL,
                                    no2 VARCHAR ( 255 ) DEFAULT NULL,
                                    n2 date DEFAULT NULL,
                                    no3 VARCHAR ( 255 ) DEFAULT NULL,
                                    n3 date DEFAULT NULL,
                                    no4 VARCHAR ( 255 ) DEFAULT NULL,
                                    n4 date DEFAULT NULL,
                                    no5 VARCHAR ( 255 ) DEFAULT NULL,
                                    n5 date DEFAULT NULL,
                                    hos VARCHAR ( 255 ) DEFAULT NULL,
                                    normal VARCHAR ( 255 ) DEFAULT NULL)
                                    ENGINE = INNODB DEFAULT CHARSET = tis620;"""

        qancdel = """DELETE from nu_anc ;"""

        qancinsert = """INSERT INTO nu_anc (person_anc_id,no1,n1,no2,n2,no3,n3,no4,n4,no5,n5,hos,normal)
                            SELECT
                            person_anc_id,
                            "1" AS no1,
                            CASE DAYOFWEEK(DATE_ADD(lmp,INTERVAL '10' WEEK))
                            WHEN 1 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '10' WEEK),INTERVAL 2 DAY)
                            WHEN 2 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '10' WEEK),INTERVAL 1 DAY)
                            WHEN 3 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '10' WEEK),INTERVAL 0 DAY)
                            WHEN 4 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '10' WEEK),INTERVAL -1 DAY)
                            WHEN 5 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '10' WEEK),INTERVAL -2 DAY)
                            WHEN 6 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '10' WEEK),INTERVAL -3 DAY)
                            WHEN 7 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '10' WEEK),INTERVAL -4 DAY)
                            else cast(lmp as date) end AS n1,
                            "2" AS no2,
                            CASE DAYOFWEEK(DATE_ADD(lmp,INTERVAL '16' WEEK))
                            WHEN 1 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '16' WEEK),INTERVAL 2 DAY)
                            WHEN 2 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '16' WEEK),INTERVAL 1 DAY)
                            WHEN 3 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '16' WEEK),INTERVAL 0 DAY)
                            WHEN 4 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '16' WEEK),INTERVAL -1 DAY)
                            WHEN 5 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '16' WEEK),INTERVAL -2 DAY)
                            WHEN 6 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '16' WEEK),INTERVAL -3 DAY)
                            WHEN 7 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '16' WEEK),INTERVAL -4 DAY)
                            else cast(lmp as date) end AS n2,
                            "3" AS no3,
                            CASE DAYOFWEEK(DATE_ADD(lmp,INTERVAL '23' WEEK))
                            WHEN 1 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '23' WEEK),INTERVAL 2 DAY)
                            WHEN 2 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '23' WEEK),INTERVAL 1 DAY)
                            WHEN 3 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '23' WEEK),INTERVAL 0 DAY)
                            WHEN 4 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '23' WEEK),INTERVAL -1 DAY)
                            WHEN 5 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '23' WEEK),INTERVAL -2 DAY)
                            WHEN 6 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '23' WEEK),INTERVAL -3 DAY)
                            WHEN 7 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '23' WEEK),INTERVAL -4 DAY)
                            else cast(lmp as date) end AS n3,
                            "4" AS no4,
                            CASE DAYOFWEEK(DATE_ADD(lmp,INTERVAL '29' WEEK))
                            WHEN 1 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '29' WEEK),INTERVAL 2 DAY)
                            WHEN 2 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '29' WEEK),INTERVAL 1 DAY)
                            WHEN 3 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '29' WEEK),INTERVAL 0 DAY)
                            WHEN 4 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '29' WEEK),INTERVAL -1 DAY)
                            WHEN 5 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '29' WEEK),INTERVAL -2 DAY)
                            WHEN 6 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '29' WEEK),INTERVAL -3 DAY)
                            WHEN 7 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '29' WEEK),INTERVAL -4 DAY)
                            else cast(lmp as date) end as n4,
                            "5" AS no5,
                            CASE DAYOFWEEK(DATE_ADD(lmp,INTERVAL '35' WEEK))
                            WHEN 1 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '35' WEEK),INTERVAL 2 DAY)
                            WHEN 2 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '35' WEEK),INTERVAL 1 DAY)
                            WHEN 3 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '35' WEEK),INTERVAL 0 DAY)
                            WHEN 4 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '35' WEEK),INTERVAL -1 DAY)
                            WHEN 5 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '35' WEEK),INTERVAL -2 DAY)
                            WHEN 6 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '35' WEEK),INTERVAL -3 DAY)
                            WHEN 7 THEN DATE_ADD(DATE_ADD(lmp,INTERVAL '35' WEEK),INTERVAL -4 DAY)
                            else cast(lmp as date) end AS n5,( SELECT hospitalcode FROM opdconfig ) as hos,"1" as normal
                            FROM person_anc WHERE lmp >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);"""

        qanc01 = """INSERT INTO person_anc_other_precare (person_anc_id,precare_date,precare_hospcode,precare_no,anc_result)
                            SELECT 
                            nu_anc.person_anc_id,
                            nu_anc.n1,
                            nu_anc.hos,
                            nu_anc.no1,
                            nu_anc.normal
                            FROM `nu_anc`;"""

        qanc02 ="""INSERT INTO person_anc_other_precare (person_anc_id,precare_date,precare_hospcode,precare_no,anc_result)
                            SELECT
                            nu_anc.person_anc_id,
                            nu_anc.n2,
                            nu_anc.hos,
                            nu_anc.no2,
                            nu_anc.normal
                            FROM `nu_anc`;"""

        qanc03 ="""INSERT INTO person_anc_other_precare (person_anc_id,precare_date,precare_hospcode,precare_no,anc_result)
                            SELECT
                            nu_anc.person_anc_id,
                            nu_anc.n3,
                            nu_anc.hos,
                            nu_anc.no3,
                            nu_anc.normal
                            FROM `nu_anc`;"""

        qanc04 ="""INSERT INTO person_anc_other_precare (person_anc_id,precare_date,precare_hospcode,precare_no,anc_result)
                            SELECT
                            nu_anc.person_anc_id,
                            nu_anc.n4,
                            nu_anc.hos,
                            nu_anc.no4,
                            nu_anc.normal
                            FROM `nu_anc`;"""

        qanc05 ="""INSERT INTO person_anc_other_precare (person_anc_id,precare_date,precare_hospcode,precare_no,anc_result)
                            SELECT
                            nu_anc.person_anc_id,
                            nu_anc.n5,
                            nu_anc.hos,
                            nu_anc.no5,
                            nu_anc.normal
                            FROM `nu_anc`;"""


        qancdel01 = """DELETE a1
                                FROM person_anc_other_precare as a1 , person_anc_other_precare as a2
                                WHERE a1.person_anc_id=a2.person_anc_id
                                and a1.precare_no=a2.precare_no
                                and a1.precare_hospcode=a2.precare_hospcode
                                and a1.person_anc_other_precare_id > a2.person_anc_other_precare_id """


        qancdel02 ="""DELETE pp
                                FROM person_anc_other_precare as pp
                                LEFT OUTER JOIN person_anc_service as pa on pa.person_anc_id=pp.person_anc_id
                                WHERE pp.precare_date=pa.anc_service_date;"""

        qancdelnow="""DELETE FROM person_anc_other_precare WHERE precare_date > NOW();""" 

                   
        # connect to the database server
        conn = MySQLConnection(**db_config)
 
        # execute the query id
        cursor = conn.cursor()
        cursor.execute(qancid)
        conn.commit()

        # execute the query drop & create
        cursor = conn.cursor()
        for result in cursor.execute(qancdrop, multi=True):
            pass
        conn.commit()

        # execute the query delete
        cursor = conn.cursor()
        cursor.execute(qancdel)
        conn.commit()

        # execute the query input
        cursor1 = conn.cursor()
        cursor1.execute(qancinsert)
        conn.commit()
            
                    # execute the query 01
        cursor01 = conn.cursor()
        cursor01.execute(qanc01)
        conn.commit()

                    # execute the query 02
        cursor02 = conn.cursor()
        cursor02.execute(qanc02)
        conn.commit()

                    # execute the query 03
        cursor03 = conn.cursor()
        cursor03.execute(qanc03)
        conn.commit()

                    # execute the query 04
        cursor04 = conn.cursor()
        cursor04.execute(qanc04)
        conn.commit()

                    # execute the query 05
        cursor05 = conn.cursor()
        cursor05.execute(qanc05)
        conn.commit()

            
            # execute the query del01
        cursordel01 = conn.cursor()
        cursordel01.execute(qancdel01)
        conn.commit()

            # execute the query del02
        cursordel02 = conn.cursor()
        cursordel02.execute(qancdel02)
        conn.commit()

                    # execute the query delnow
        cursornow = conn.cursor()
        cursornow.execute(qancdelnow)
        conn.commit()
        
        time.sleep(2)
                     
        panc001 =(cursor01.rowcount * 5)
        panc002 =(cursordel01.rowcount+cursordel02.rowcount+cursornow.rowcount)
        panc007 =(panc001-panc002)
        pancc01= (f'เพิ่มข้อมูลแล้วจำนวน {panc007} เรคคอร์ด') 
        messagebox.showinfo("การดำเนินการ",pancc01,parent=window)                    

        cursor.close()
        conn.close()

#  เยี่ยมหลังคลอด
    def ser3():
        db_config = read_db_config()
        qmph ="""ALTER TABLE `hosxp_pcu`.`person_anc_preg_care` 
                MODIFY COLUMN `person_anc_preg_care_id` int(11) NOT NULL AUTO_INCREMENT FIRST;

                DROP TABLE IF EXISTS `nu_mph`;
                CREATE TABLE `nu_mph` (
                  `person_anc_id` varchar(255) DEFAULT NULL,
                  `no1` varchar(255) DEFAULT NULL,
                  `n1` date DEFAULT NULL,
                  `no2` varchar(255) DEFAULT NULL,
                  `n2` date DEFAULT NULL,
                  `no3` varchar(255) DEFAULT NULL,
                  `n3` date DEFAULT NULL,
                  `hos` varchar(255) DEFAULT NULL,
                  `normal` varchar(255) DEFAULT NULL,
                  `time` time DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=tis620;

                DELETE FROM nu_mph ;


                INSERT INTO nu_mph (person_anc_id,no1,n1,no2,n2,no3,n3,hos,normal)
                SELECT
                person_anc_id,
                "1" AS no1,
                CASE DAYOFWEEK(DATE_ADD(labor_date,INTERVAL '1' WEEK))
                WHEN 1 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '1' WEEK),INTERVAL 2 DAY)
                WHEN 2 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '1' WEEK),INTERVAL 1 DAY)
                WHEN 3 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '1' WEEK),INTERVAL 0 DAY)
                WHEN 4 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '1' WEEK),INTERVAL -1 DAY)
                WHEN 5 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '1' WEEK),INTERVAL -2 DAY)
                WHEN 6 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '1' WEEK),INTERVAL -3 DAY)
                WHEN 7 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '1' WEEK),INTERVAL -4 DAY)
                else cast(labor_date as date) end AS n1,
                "2" AS no2,
                CASE DAYOFWEEK(DATE_ADD(labor_date,INTERVAL '2' WEEK))
                WHEN 1 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '2' WEEK),INTERVAL 2 DAY)
                WHEN 2 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '2' WEEK),INTERVAL 1 DAY)
                WHEN 3 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '2' WEEK),INTERVAL 0 DAY)
                WHEN 4 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '2' WEEK),INTERVAL -1 DAY)
                WHEN 5 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '2' WEEK),INTERVAL -2 DAY)
                WHEN 6 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '2' WEEK),INTERVAL -3 DAY)
                WHEN 7 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '2' WEEK),INTERVAL -4 DAY)
                else cast(labor_date as date) end AS n2,
                "3" AS no3,
                CASE DAYOFWEEK(DATE_ADD(labor_date,INTERVAL '4' WEEK))
                WHEN 1 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '4' WEEK),INTERVAL 2 DAY)
                WHEN 2 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '4' WEEK),INTERVAL 1 DAY)
                WHEN 3 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '4' WEEK),INTERVAL 0 DAY)
                WHEN 4 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '4' WEEK),INTERVAL -1 DAY)
                WHEN 5 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '4' WEEK),INTERVAL -2 DAY)
                WHEN 6 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '4' WEEK),INTERVAL -3 DAY)
                WHEN 7 THEN DATE_ADD(DATE_ADD(labor_date,INTERVAL '4' WEEK),INTERVAL -4 DAY)
                else cast(labor_date as date) end AS n3
                ,( SELECT hospitalcode FROM opdconfig ) as hos,"1" as normal
                FROM person_anc
                WHERE edc >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and labor_date <>'0';

                INSERT INTO person_anc_preg_care (
                person_anc_id,
                care_date,
                anc_preg_care_location_id,
                uterus_level_normal,
                lochia_normal,
                nipple_normal,
                albumin_level,
                sugar_level,
                perineum_normal,
                bps,
                bpd,
                rr,
                temperature,
                preg_care_number,
                hos_guid,
                vn,
                care_time,
                real_preg_care,
                doctor_code
                ) SELECT
                        person_anc_id AS person_anc_id,
                        n1 AS care_date,
                        '1' as anc_preg_care_location_id,
                        'Y' as uterus_level_normal,
                        'Y' as lochia_normal,
                        'Y' as nipple_normal,
                        'ปกติ' as albumin_level, 
                        'ปกติ' as sugar_level,
                        'Y' as perineum_normal,
                        '110' as bps ,
                        '70' as bpd ,
                        '82' as rr ,
                        '37' as temperature ,
                        no1 as preg_care_number,
                        upper(concat('{', uuid(), '}')) as hos_guid,
                        CONCAT(
                                DATE_FORMAT(
                                        DATE_ADD(n1, INTERVAL 543 YEAR),
                                        '%y%m%d'
                                ),
                                TIME_FORMAT(time, '%h%i%s')
                        ) as vn,
                CURTIME() as care_time,
                        'Y' as real_preg_care,
                        (SELECT code FROM doctor WHERE provider_type_code ='03' and active ='Y' and sex ='2' ORDER BY RAND() LIMIT 1) as doctor
                FROM
                        `nu_mph`;

                INSERT INTO person_anc_preg_care (
                person_anc_id,
                care_date,
                anc_preg_care_location_id,
                uterus_level_normal,
                lochia_normal,
                nipple_normal,
                albumin_level,
                sugar_level,
                perineum_normal,
                bps,
                bpd,
                rr,
                temperature,
                preg_care_number,
                hos_guid,
                vn,
                care_time,
                real_preg_care,
                doctor_code
                ) SELECT
                        person_anc_id AS person_anc_id,
                        n2 AS care_date,
                        '1' as anc_preg_care_location_id,
                        'Y' as uterus_level_normal,
                        'Y' as lochia_normal,
                        'Y' as nipple_normal,
                        'ปกติ' as albumin_level, 
                        'ปกติ' as sugar_level,
                        'Y' as perineum_normal,
                        '110' as bps ,
                        '70' as bpd ,
                        '82' as rr ,
                        '37' as temperature ,
                        no2 as preg_care_number,
                        upper(concat('{', uuid(), '}')) as hos_guid,
                        CONCAT(
                                DATE_FORMAT(
                                        DATE_ADD(n2, INTERVAL 543 YEAR),
                                        '%y%m%d'
                                ),
                                TIME_FORMAT(time, '%h%i%s')
                        ) as vn,
                CURTIME() as care_time,
                        'Y' as real_preg_care,
                        (SELECT code FROM doctor WHERE provider_type_code ='03' and active ='Y' and sex ='2' ORDER BY RAND() LIMIT 1) as doctor
                FROM
                        `nu_mph`;

                INSERT INTO person_anc_preg_care (
                person_anc_id,
                care_date,
                anc_preg_care_location_id,
                uterus_level_normal,
                lochia_normal,
                nipple_normal,
                albumin_level,
                sugar_level,
                perineum_normal,
                bps,
                bpd,
                rr,
                temperature,
                preg_care_number,
                hos_guid,
                vn,
                care_time,
                real_preg_care,
                doctor_code
                ) SELECT
                        person_anc_id AS person_anc_id,
                        n3 AS care_date,
                        '1' as anc_preg_care_location_id,
                        'Y' as uterus_level_normal,
                        'Y' as lochia_normal,
                        'Y' as nipple_normal,
                        'ปกติ' as albumin_level, 
                        'ปกติ' as sugar_level,
                        'Y' as perineum_normal,
                        '110' as bps ,
                        '70' as bpd ,
                        '82' as rr ,
                        '37' as temperature ,
                        no3 as preg_care_number,
                        upper(concat('{', uuid(), '}')) as hos_guid,
                        CONCAT(
                                DATE_FORMAT(
                                        DATE_ADD(n3, INTERVAL 543 YEAR),
                                        '%y%m%d'
                                ),
                                TIME_FORMAT(time, '%h%i%s')
                        ) as vn,
                CURTIME() as care_time,
                        'Y' as real_preg_care,
                        (SELECT code FROM doctor WHERE provider_type_code ='03' and active ='Y' and sex ='2' ORDER BY RAND() LIMIT 1) as doctor
                FROM
                        `nu_mph`;

                DELETE a1
                FROM person_anc_preg_care a1 , person_anc_preg_care a2
                WHERE a1.person_anc_id=a2.person_anc_id
                and a1.care_date=a2.care_date
                and a1.preg_care_number=a2.preg_care_number
                AND a1.person_anc_preg_care_id > a2.person_anc_preg_care_id;

                DELETE FROM person_anc_preg_care WHERE care_date > NOW();"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
 
            # execute the query multi
        cursor = conn.cursor()        
        for result in cursor.execute(qmph, multi=True):
            pass
            
        conn.commit()        
        cursor.close()
        conn.close()
        
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)

# เยี่ยมทารก        
    def ser4():

        db_config = read_db_config()
          
        qpp ="""ALTER TABLE `hosxp_pcu`.`person_wbc_post_care` 
                    MODIFY COLUMN `person_wbc_post_care_id` int(11) NOT NULL AUTO_INCREMENT FIRST;

                    DROP TABLE IF EXISTS `nu_cdc`;
                    CREATE TABLE `nu_cdc` (
                      `person_wbc_id` varchar(255) DEFAULT NULL,
                      `no1` varchar(255) DEFAULT NULL,
                      `n1` date DEFAULT NULL,
                      `no2` varchar(255) DEFAULT NULL,
                      `n2` date DEFAULT NULL,
                      `no3` varchar(255) DEFAULT NULL,
                      `n3` date DEFAULT NULL,
                      `a1` varchar(255) DEFAULT NULL,
                      `a2` varchar(255) DEFAULT NULL,
                      `a3` varchar(255) DEFAULT NULL,
                      `a4` varchar(255) DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=tis620;

                    DELETE FROM nu_cdc;

                    INSERT INTO nu_cdc(person_wbc_id,no1,n1,no2,n2,no3,n3,a1,a2,a3,a4)

                    SELECT
                    w.person_wbc_id,
                    "1" AS no1,
                    CASE DAYOFWEEK(DATE_ADD(p.birthdate,INTERVAL '1' WEEK))
                    WHEN 1 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL 2 DAY)
                    WHEN 2 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL 1 DAY)
                    WHEN 3 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL 0 DAY)
                    WHEN 4 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL -1 DAY)
                    WHEN 5 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL -2 DAY)
                    WHEN 6 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL -3 DAY)
                    WHEN 7 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL -4 DAY)
                    else cast(p.birthdate as date) end AS n1,
                    "2" AS no2,
                    CASE DAYOFWEEK(DATE_ADD(p.birthdate,INTERVAL '2' WEEK))
                    WHEN 1 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '2' WEEK),INTERVAL 2 DAY)
                    WHEN 2 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '2' WEEK),INTERVAL 1 DAY)
                    WHEN 3 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '2' WEEK),INTERVAL 0 DAY)
                    WHEN 4 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '2' WEEK),INTERVAL -1 DAY)
                    WHEN 5 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '2' WEEK),INTERVAL -2 DAY)
                    WHEN 6 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '2' WEEK),INTERVAL -3 DAY)
                    WHEN 7 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '2' WEEK),INTERVAL -4 DAY)
                    else cast(p.birthdate as date) end AS n2,
                    "3" AS no3,
                    CASE DAYOFWEEK(DATE_ADD(p.birthdate,INTERVAL '4' WEEK))
                    WHEN 1 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '4' WEEK),INTERVAL 2 DAY)
                    WHEN 2 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '4' WEEK),INTERVAL 1 DAY)
                    WHEN 3 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '4' WEEK),INTERVAL 0 DAY)
                    WHEN 4 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '4' WEEK),INTERVAL -1 DAY)
                    WHEN 5 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '4' WEEK),INTERVAL -2 DAY)
                    WHEN 6 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '1' WEEK),INTERVAL -3 DAY)
                    WHEN 7 THEN DATE_ADD(DATE_ADD(p.birthdate,INTERVAL '4' WEEK),INTERVAL -4 DAY)
                    else cast(p.birthdate as date) end AS n3,"2",(SELECT code FROM doctor
                    WHERE provider_type_code ='03' and active ='Y'  ORDER BY RAND() LIMIT 1),"1","1"as a1
                    FROM person_wbc as w
                    left outer join person as p on p.person_id=w.person_id;

                    INSERT IGNORE person_wbc_post_care
                    (person_wbc_id,care_date,anc_preg_care_location_id,doctor_code,care_number,
                    person_wbc_post_care_result_type_id,person_nutrition_food_type_id)
                    SELECT person_wbc_id,n1,a1,a2,no1,a3,a4 FROM nu_cdc;


                    INSERT IGNORE person_wbc_post_care
                    (person_wbc_id,care_date,anc_preg_care_location_id,doctor_code,care_number,
                    person_wbc_post_care_result_type_id,person_nutrition_food_type_id)
                    SELECT person_wbc_id,n2,a1,a2,no2,a3,a4 FROM nu_cdc;


                    INSERT IGNORE person_wbc_post_care
                    (person_wbc_id,care_date,anc_preg_care_location_id,doctor_code,care_number,
                    person_wbc_post_care_result_type_id,person_nutrition_food_type_id)
                    SELECT person_wbc_id,n3,a1,a2,no3,a3,a4 FROM nu_cdc;


                    DELETE w1
                    FROM person_wbc_post_care w1 , person_wbc_post_care w2
                    WHERE w1.person_wbc_id=w2.person_wbc_id
                    and w1.care_date=w2.care_date
                    and w1.care_number=w2.care_number
                    and w1.person_wbc_post_care_id>w2.person_wbc_post_care_id;

                    DELETE FROM person_wbc_post_care WHERE care_date > NOW();

                    INSERT IGNORE person_wbc_post_care_screen (person_wbc_post_care_id,post_care_screen_id,screen_value)
                    SELECT person_wbc_post_care_id,"1","Y" FROM person_wbc_post_care;

                    INSERT IGNORE person_wbc_post_care_screen (person_wbc_post_care_id,post_care_screen_id,screen_value)
                    SELECT person_wbc_post_care_id,"2","Y" FROM person_wbc_post_care;

                    INSERT IGNORE person_wbc_post_care_screen (person_wbc_post_care_id,post_care_screen_id,screen_value)
                    SELECT person_wbc_post_care_id,"3","Y" FROM person_wbc_post_care;

                    INSERT IGNORE person_wbc_post_care_screen (person_wbc_post_care_id,post_care_screen_id,screen_value)
                    SELECT person_wbc_post_care_id,"4","Y" FROM person_wbc_post_care;

                    INSERT IGNORE person_wbc_post_care_screen (person_wbc_post_care_id,post_care_screen_id,screen_value)
                    SELECT person_wbc_post_care_id,"5","Y" FROM person_wbc_post_care;

                    DELETE s1
                    FROM person_wbc_post_care_screen s1 , person_wbc_post_care_screen s2
                    WHERE s1.person_wbc_post_care_id=s2.person_wbc_post_care_id
                    AND s1.post_care_screen_id=s2.post_care_screen_id
                    and s1.person_wbc_post_care_screen_id>s2.person_wbc_post_care_screen_id;"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
 
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qpp, multi=True):
            pass
        conn.commit()
        cursor.close()
        conn.close()
        
        time.sleep(2)        
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)

# เยี่ยมบ้าน
    def ser5():
        
        db_config = read_db_config()

        qvisit ="""ALTER TABLE `hosxp_pcu`.`ovst_community_service` 
                    MODIFY COLUMN `ovst_community_service_id` int(11) NOT NULL AUTO_INCREMENT FIRST;

                    #239	1J:ให้ความรู้/ สุขศึกษาเกี่ยวกับโรคและการป้องกันโรคต่าง ๆ
                    INSERT INTO ovst_community_service (vn,ovst_community_service_type_id,doctor,entry_datetime)
                    SELECT vn,"239"
                    ,doctor,CONCAT(vstdate," ",vsttime)FROM ovstdiag 
                    WHERE vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    #240	1J:ให้ความรู้/ สุขศึกษาเกี่ยวกับโรคตามฤดูกาล
                    INSERT INTO ovst_community_service (vn,ovst_community_service_type_id,doctor,entry_datetime)
                    SELECT vn,"240"
                    ,doctor,CONCAT(vstdate," ",vsttime)FROM ovstdiag 
                    WHERE vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    #241	1J:แนะนำ / ให้ความรู้ เรื่องการใช้ยา
                    INSERT INTO ovst_community_service (vn,ovst_community_service_type_id,doctor,entry_datetime)
                    SELECT vn,"241"
                    ,doctor,CONCAT(vstdate," ",vsttime)FROM ovstdiag 
                    WHERE vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    #244	1J:ให้ความรู้ด้านโภชนาการ
                    INSERT INTO ovst_community_service (vn,ovst_community_service_type_id,doctor,entry_datetime)
                    SELECT vn,"244"
                    ,doctor,CONCAT(vstdate," ",vsttime)FROM ovstdiag 
                    WHERE vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    #245	1J:ให้ความรู้/ สุขศึกษาเกี่ยวกับสุขภาพอื่น ๆ  
                    INSERT INTO ovst_community_service (vn,ovst_community_service_type_id,doctor,entry_datetime)
                    SELECT vn,"245"
                    ,doctor,CONCAT(vstdate," ",vsttime)FROM ovstdiag 
                    WHERE vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    #246	1J:การเผยแพร่ความรู้/ให้สุขศึกษาแก่กลุ่มบุคคลทั่วไป  ไม่ระบุรายละเอียด
                    INSERT INTO ovst_community_service (vn,ovst_community_service_type_id,doctor,entry_datetime)
                    SELECT vn,"246"
                    ,doctor,CONCAT(vstdate," ",vsttime)FROM ovstdiag 
                    WHERE vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    #ลบค่าซ้ำในการเยี่ยมรายการเดียวกัน
                    delete c1
                    from ovst_community_service as c1, ovst_community_service as c2
                    where c1.vn=c2.vn 
                    and c1.ovst_community_service_type_id=c2.ovst_community_service_type_id
                    and c1.ovst_community_service_id > c2.ovst_community_service_id ;

                    #ลบค่าซ้ำในรายการส่งเสิรมสุขภาพ
                    DELETE p1
                    FROM pp_special as p1, pp_special as p2
                    WHERE p1.vn=p2.vn and p1.pp_special_type_id=p2.pp_special_type_id
                    and p1.pp_special_id > p2.pp_special_id;"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
 
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qvisit, multi=True):
            pass
        conn.commit()   
        cursor.close()
        conn.close()
        time.sleep(2)        
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)

# เยี่ยมบ้านเบาหวาน-ความดัน
    def ser6():
        db_config = read_db_config()

        qvisitdmht ="""ALTER TABLE `hosxp_pcu`.`ovst_community_service` 
                    MODIFY COLUMN `ovst_community_service_id` int(11) NOT NULL AUTO_INCREMENT FIRST;

                    #เยี่ยมบ้านผู้ป่วยเบาหวาน
                    INSERT INTO ovst_community_service (vn,doctor) SELECT vn,doctor FROM ovstdiag 
                    WHERE icd10 ='E119' AND vstdate >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    UPDATE ovst_community_service c INNER JOIN ovstdiag o on o.vn=c.vn
                    SET c.entry_datetime=CONCAT(o.vstdate," ",o.vsttime),
                    c.ovst_community_service_type_id='2' WHERE c.ovst_community_service_type_id is null;

                    #เยี่ยมบ้านผู้ป่วยความดัน
                    INSERT INTO ovst_community_service (vn,doctor) SELECT vn,doctor FROM ovstdiag 
                    WHERE icd10 ='I10' AND vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    UPDATE ovst_community_service c INNER JOIN ovstdiag o on o.vn=c.vn
                    SET c.entry_datetime=CONCAT(o.vstdate," ",o.vsttime),
                    c.ovst_community_service_type_id='1' WHERE c.ovst_community_service_type_id is null;

                    #ลบค่าซ้ำในการเยี่ยมรายการเดียวกัน
                    delete c1
                    from ovst_community_service as c1, ovst_community_service as c2
                    where c1.vn=c2.vn 
                    and c1.ovst_community_service_type_id=c2.ovst_community_service_type_id
                    and c1.ovst_community_service_id > c2.ovst_community_service_id ;

                    #ลบค่าซ้ำในรายการส่งเสิรมสุขภาพ
                    DELETE p1
                    FROM pp_special as p1, pp_special as p2
                    WHERE p1.vn=p2.vn and p1.pp_special_type_id=p2.pp_special_type_id
                    and p1.pp_special_id > p2.pp_special_id;"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qvisitdmht, multi=True):
            pass
        conn.commit()
        cursor.close()
        conn.close()
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)        

# ปรับความสมบูรณ์งานบริการ
    def ser7():
        db_config = read_db_config()
        qcomplete ="""#ปรับ การสกรีน หน้า 1 stop service
                    UPDATE opdscreen
                    SET advice1 = 'Y',
                     advice2 = 'Y',
                     advice3 = 'Y',
                     advice4 = 'Y',
                     advice5 = 'Y',
                     advice6 = 'Y',
                    advice8 = 'Y';

                    UPDATE opdscreen
                    SET pe_heent = 'N'
                    WHERE
                            pe_heent IS NULL;

                    UPDATE opdscreen
                    SET pe_heart = 'N'
                    WHERE
                            pe_heart IS NULL;

                    UPDATE opdscreen
                    SET pe_lung = 'N'
                    WHERE
                            pe_lung IS NULL;

                    UPDATE opdscreen
                    SET pe_ab = 'N'
                    WHERE
                            pe_ab IS NULL;

                    UPDATE opdscreen
                    SET pe_ext = 'N'
                    WHERE
                            pe_ext IS NULL;

                    UPDATE opdscreen
                    SET pe_neuro = 'N'
                    WHERE
                            pe_neuro IS NULL;

                    UPDATE opdscreen
                    SET checkup = 'Y';

                    UPDATE opdscreen
                    SET found_allergy = 'N'
                    WHERE
                            found_allergy IS NULL;

                    UPDATE opdscreen
                    SET temperature = '37'
                    WHERE
                            temperature IS NULL;

                    #UPDATE ovst SET ovstist = '01',  ovstost = '02';

                    UPDATE ovst
                    SET pt_subtype='1' WHERE pt_subtype is null;

                    UPDATE ovst
                    set spclty ='01' WHERE  spclty is NULL;


                    UPDATE opdscreen
                    SET pe = 'Normal'
                    WHERE
                            pe IS NULL;

                    UPDATE ovst
                    SET visit_type = 'I'
                    WHERE
                            vsttime BETWEEN '08:30:00'
                    AND '16:30:00';

                    UPDATE ovst
                    SET visit_type = 'O'
                    WHERE
                            vsttime BETWEEN '16:30:01'
                    AND '23:59:59';

                    UPDATE ovst
                    SET visit_type = 'O'
                    WHERE
                            vsttime BETWEEN '00:00:00'
                    AND '08:29:59';

                    UPDATE ovst
                    SET cur_dep = '019'
                    WHERE
                            cur_dep IS NULL;

                    #ตั้งค่าให้การสูบบุหรี่ เป็น ไม่สูบ
                    UPDATE opdscreen
                    SET smoking_type_id = '1'
                    WHERE
                            smoking_type_id IS NULL;

                    #ตั้งค่าให้การดื่มสุรา เป็น ไม่ดื่ม
                    UPDATE opdscreen
                    SET drinking_type_id = '1'
                    WHERE  drinking_type_id IS NULL;

                    # แก้แผนก
                    #UPDATE ovst set spclty ='16' WHERE  spclty ='12';

                    #ความเร่งด่วน
                    UPDATE ovst o INNER JOIN ovstdiag d on d.vn=o.vn
                    SET o.pt_priority='0'
                    WHERE o.vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);

                    UPDATE ovst o INNER JOIN ovstdiag d on d.vn=o.vn
                    SET o.pt_priority='1'
                    WHERE o.vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH)
                    and d.icd10 LIKE "%%S%%"
                    or d.icd10 LIKE "%%T%%"
                    or d.icd10 LIKE "%%V%%"
                    or d.icd10 LIKE "%%X%%"
                    or d.icd10 LIKE "%%Y%%";

                    #สภาพผู้ป่วย เดินมา
                    UPDATE opdscreen o INNER JOIN ovstdiag d on d.vn=o.vn
                    SET o.walk_id='1'
                    WHERE o.vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and o.walk_id is null;

                    #SEQ
                    update ovst_seq set nhso_seq_id=seq_id WHERE seq_id<>nhso_seq_id AND vn like "62%";

                    UPDATE ovstdiag set icd10 = CONCAT(icd10,'09') WHERE LENGTH(icd10)= '3' and vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and icd10 LIKE "%%V%%" ;
                    UPDATE ovstdiag set icd10 = CONCAT(icd10,'09') WHERE LENGTH(icd10)= '3' and vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and icd10 LIKE "%%W%%" ;
                    UPDATE ovstdiag set icd10 = CONCAT(icd10,'09') WHERE LENGTH(icd10)= '3' and vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and icd10 LIKE "%%X%%" ;
                    UPDATE ovstdiag set icd10 = CONCAT(icd10,'09') WHERE LENGTH(icd10)= '3' and vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and icd10 LIKE "%%Y%%" ;
                    UPDATE ovstdiag set icd10 = CONCAT(icd10,'09') WHERE LENGTH(icd10)= '3' and vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and icd10 LIKE "%%M%%" ;

                    UPDATE opdscreen SET hpi=cc WHERE  vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and hpi is null or hpi ='';


                    UPDATE opdscreen SET cc=REPLACE(cc, 'ก่อน', 'เป็น') WHERE  vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) ;

                    UPDATE opdscreen SET cc=REPLACE(cc, 'เป็นเป็น', 'เป็นก่อน') WHERE  vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH)  ;

                    UPDATE opdscreen SET hpi=REPLACE(hpi, 'เป็น', 'ก่อน') WHERE  vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH);


                    UPDATE opdscreen SET hpi=CONCAT(hpi,"  ยังไม่รักษาที่ใด  จึงมา รพ.สต.") WHERE  vstdate  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and hpi LIKE '%%ก่อน%%' 
                    and hpi NOT LIKE '%%รพ%%'
                    and hpi NOT LIKE '%%สต%%'
                    and hpi NOT LIKE '%%ที่นี้%%'
                    and hpi NOT LIKE '%%จึงมา%%'
                    and hpi NOT LIKE '%%ที่ใด%%'
                    and hpi NOT LIKE '%%โรงพยาบาล%%'
                    and hpi NOT LIKE '%%ซื้อยา%%'
                    and hpi NOT LIKE '%%คลินิก%%'
                    and hpi NOT LIKE '%%คลินิค%%';

                    SET @ost = (SELECT ovstost FROM ovstost WHERE name like '%%ตรวจแล้ว%%');
                    UPDATE ovst SET  ovstost = @ost; 
                    """

            # connect to the database server
        conn = MySQLConnection(**db_config)
 
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qcomplete, multi=True):
            pass
        conn.commit()
           
        cursor.close()
        conn.close()
        time.sleep(2)        
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)

# พัฒนาการบัญชี 3-4
    def ser8():
        db_config = read_db_config()           
        qvisitdmht ="""UPDATE person_development_list set age_month =	'1'	WHERE development_id=	'1'	;
            UPDATE person_development_list set age_month =	'1'	WHERE development_id=	'2'	;
            UPDATE person_development_list set age_month =	'1'	WHERE development_id=	'3'	;
            UPDATE person_development_list set age_month =	'1'	WHERE development_id=	'4'	;
            UPDATE person_development_list set age_month =	'2'	WHERE development_id=	'5'	;
            UPDATE person_development_list set age_month =	'2'	WHERE development_id=	'6'	;
            UPDATE person_development_list set age_month =	'2'	WHERE development_id=	'7'	;
            UPDATE person_development_list set age_month =	'2'	WHERE development_id=	'8'	;
            UPDATE person_development_list set age_month =	'4'	WHERE development_id=	'9'	;
            UPDATE person_development_list set age_month =	'4'	WHERE development_id=	'10'	;
            UPDATE person_development_list set age_month =	'4'	WHERE development_id=	'11'	;
            UPDATE person_development_list set age_month =	'4'	WHERE development_id=	'12'	;
            UPDATE person_development_list set age_month =	'6'	WHERE development_id=	'13'	;
            UPDATE person_development_list set age_month =	'6'	WHERE development_id=	'14'	;
            UPDATE person_development_list set age_month =	'6'	WHERE development_id=	'15'	;
            UPDATE person_development_list set age_month =	'6'	WHERE development_id=	'16'	;
            UPDATE person_development_list set age_month =	'9'	WHERE development_id=	'17'	;
            UPDATE person_development_list set age_month =	'9'	WHERE development_id=	'18'	;
            UPDATE person_development_list set age_month =	'9'	WHERE development_id=	'19'	;
            UPDATE person_development_list set age_month =	'9'	WHERE development_id=	'20'	;
            UPDATE person_development_list set age_month =	'12'	WHERE development_id=	'21'	;
            UPDATE person_development_list set age_month =	'12'	WHERE development_id=	'22'	;
            UPDATE person_development_list set age_month =	'12'	WHERE development_id=	'23'	;
            UPDATE person_development_list set age_month =	'12'	WHERE development_id=	'24'	;
            UPDATE person_development_list set age_month =	'12'	WHERE development_id=	'25'	;
            UPDATE person_development_list set age_month =	'18'	WHERE development_id=	'26'	;
            UPDATE person_development_list set age_month =	'18'	WHERE development_id=	'27'	;
            UPDATE person_development_list set age_month =	'18'	WHERE development_id=	'28'	;
            UPDATE person_development_list set age_month =	'18'	WHERE development_id=	'29'	;
            UPDATE person_development_list set age_month =	'18'	WHERE development_id=	'30'	;
            UPDATE person_development_list set age_month =	'24'	WHERE development_id=	'31'	;
            UPDATE person_development_list set age_month =	'24'	WHERE development_id=	'32'	;
            UPDATE person_development_list set age_month =	'24'	WHERE development_id=	'33'	;
            UPDATE person_development_list set age_month =	'24'	WHERE development_id=	'34'	;
            UPDATE person_development_list set age_month =	'24'	WHERE development_id=	'35'	;
            UPDATE person_development_list set age_month =	'36'	WHERE development_id=	'36'	;
            UPDATE person_development_list set age_month =	'36'	WHERE development_id=	'37'	;
            UPDATE person_development_list set age_month =	'36'	WHERE development_id=	'38'	;
            UPDATE person_development_list set age_month =	'36'	WHERE development_id=	'39'	;
            UPDATE person_development_list set age_month =	'36'	WHERE development_id=	'40'	;
            UPDATE person_development_list set age_month =	'48'	WHERE development_id=	'41'	;
            UPDATE person_development_list set age_month =	'48'	WHERE development_id=	'42'	;
            UPDATE person_development_list set age_month =	'48'	WHERE development_id=	'43'	;
            UPDATE person_development_list set age_month =	'48'	WHERE development_id=	'44'	;
            UPDATE person_development_list set age_month =	'48'	WHERE development_id=	'45'	;
            UPDATE person_development_list set age_month =	'48'	WHERE development_id=	'46'	;
            UPDATE person_development_list set age_month =	'61'	WHERE development_id=	'47'	;
            UPDATE person_development_list set age_month =	'61'	WHERE development_id=	'48'	;

            update person_development_list set development_status='Y';"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qvisitdmht, multi=True):
            pass
        conn.commit()
        cursor.close()
        conn.close()
        time.sleep(2)        
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)
       
# 0-6 เดือนดื่มนมแม่
    def ser9():
        db_config = read_db_config()            
        qvisitdmht ="""UPDATE person_wbc_nutrition SET person_nutrition_childdevelop_type_id = '1',
            person_nutrition_food_type_id ='1', person_nutrition_bottle_type_id ='2',nutrition_level ='3',
            height_level ='3', bmi_level ='3',nutrition_low_level_yr_count ='0',nutrition_high_level_yr_count='0',
            doctor_code = (SELECT code FROM doctor WHERE provider_type_code ='03' and active ='Y' ORDER BY RAND() LIMIT 1)"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qvisitdmht, multi=True):
            pass
        conn.commit()
            
        cursor.close()
        conn.close()
        time.sleep(2)    
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)
 

    def show_and_run(func, btn):
        # Save current button color and change it to green
        oldcolor = btn['bg']
        btn['bg'] = 'green'

        # Call the function
        func()

        # Restore original button color
        btn['bg'] = oldcolor

    def run_function(func, btn):
        # Disable all buttons
        for b in buttons.values():
            b['state'] = 'disabled'

        processing_bar.start(interval=10)
        show_and_run(func, btn)
        processing_bar.stop()

        # Enable all buttons
        for b in buttons.values():
            b['state'] = 'normal'

    def clicked(func, btn):
        Thread(target=run_function, args=(func, btn)).start()

    #window = Tk()
    window = Toplevel()
    window.title('เพิ่มข้อมูลการให้บริการ')
    
    window.iconbitmap('imake.ico')
    window.grab_set()
    style = ThemedStyle(window)
    style.set_theme("plastik")
    

    topFrame = Frame(window)

    # Tell the Frame to fill the whole window
    topFrame.pack(fill=BOTH, expand=1)

    # Make the Frame grid contents expand & contract with the window
    topFrame.columnconfigure(0, weight=1)
    for i in range(4):
        topFrame.rowconfigure(i, weight=1)

    button_data = (
        ('ลงบันทึกอุบัติเหตุจาก ICD10 V W X Y', ser1),
        ('ลงบริการตรวจครรภ์ 5 ครั้ง อิงจาก LMP', ser2),
        ('ลงเยี่ยมมารดาหลังคลอด 3 ครั้ง อิงจาก วันที่คลอด', ser3),
        ('ลงเยี่ยมทารกหลังคลอด 3 ครั้ง อิงจาก วันเกิด', ser4),
        ('ลงเยี่ยมบ้านทั่วไป', ser5),
        ('ลงเยี่ยมบ้านโรคเรื้องรัง อิงจาก ICD10 E11x,I1x', ser6),
        ('ปรับความสมบูรณ์งานบริการ 1 Stop Service', ser7),
        ('ตรวจพัฒนาการ ในบัญชี 3,4', ser8),
        ('เด็ก 0 - 6 เดือน ดื่มนมแม่อย่างเดียว', ser9),
        #('All', all_func),
    )

    # Make all the buttons and save them in a dict
    buttons = {}
    for row, (name, func) in enumerate(button_data):
        btn = Button(topFrame, text=name)
        btn.config(command=lambda f=func, b=btn: clicked(f, b))
        btn.grid(row=row, column=0, columnspan=1, sticky='EWNS')
        buttons[name] = btn
    row += 1

    processing_bar = ttk.Progressbar(topFrame, 
        orient='horizontal', mode='indeterminate')
    processing_bar.grid(row=row, column=0, columnspan=1, sticky='EWNS')

    window.mainloop()

#  ################ MENU 2 ################
def menu2():

# ปรับข้อมูลประชากร
    def ser1():
        db_config = read_db_config()
            
        qcomp ="""update person set person_house_position_id='2' where person_house_position_id is null;
            update house set house_type_id='1' where house_type_id=' ' or house_type_id is null ;
            update house set location_area_id='2' where location_area_id=' ' or location_area_id is null;
            UPDATE person SET education='0' where education is NULL and age_y<4;
            UPDATE person SET education='1' where education is NULL and age_y BETWEEN 4 and 6;
            UPDATE person SET education='2' where education is NULL and age_y BETWEEN 7 and 12;
            UPDATE person SET education='3' where education is NULL and age_y BETWEEN 13 and 18;
            UPDATE person SET education='9' where education=' ' or education is NULL ;
            update person  set occupation='001' where occupation=' ' or occupation is null;
            update person set religion='01' where religion='00';
            update person set religion='01' where religion='' or religion is null;
            update person set marrystatus='9' where marrystatus =' ' or marrystatus is null;
            update person set marrystatus='9'  where marrystatus not in('1','2','3','4','5','6','9');
            update person set marrystatus='6' where pttype='76';

            UPDATE village v,person p SET p.house_regist_type_id="4" WHERE v.village_id=p.village_id and v.village_moo='0' and p.house_regist_type_id in("1","2","3");
            UPDATE village v,person p SET p.house_regist_type_id="3" WHERE v.village_id=p.village_id and v.village_moo<>'0' and p.house_regist_type_id="4";
            UPDATE village v,person p SET p.house_regist_type_id="1" WHERE v.village_id=p.village_id and v.village_moo<>'0' and (p.house_regist_type_id is null or p.house_regist_type_id=" ");
            UPDATE village v,person p SET p.house_regist_type_id="4" WHERE v.village_id=p.village_id and v.village_moo='0' and (p.house_regist_type_id is null or p.house_regist_type_id=" ");

            UPDATE person set person_discharge_id='1' WHERE death='Y' and (person_discharge_id='' or person_discharge_id is NULL);
            UPDATE person set person_discharge_id='9' WHERE death in('N','') and (person_discharge_id='' or person_discharge_id is NULL);

            update  person_anc  set discharge='Y' where current_preg_age between 49 and 1000;
               
            update person_women set child_alive_count='0' where child_alive_count is null;

            update person_women pw inner join person p  on pw.person_id=p.person_id    set  pw.women_birth_control_id=1 ,pw.nofp_type_id =''
            where  p.marrystatus='2' and pw.women_birth_control_id is null;

            update person_women pw inner join person p  on pw.person_id=p.person_id    set  pw.women_birth_control_id=8,pw.nofp_type_id=3
            where  p.marrystatus='1' and pw.women_birth_control_id is null;

            update  person_women pw inner join person p  on pw.person_id=p.person_id    set p.marrystatus='2' ,pw.nofp_type_id =''
            where  p.marrystatus='1' and pw.women_birth_control_id !=8;

            update person_women pw inner join person p  on pw.person_id=p.person_id    set  pw.women_birth_control_id=8 ,pw.nofp_type_id =3
            where  p.marrystatus not in ('1','2') and pw.women_birth_control_id is null;

            update person_women  set nofp_type_id =3 where women_birth_control_id='8'  and nofp_type_id is null;
            UPDATE person_women set nofp_type_id=' '  where women_birth_control_id<>'8'  and nofp_type_id=3;
            UPDATE person_women set nofp_type_id='3' WHERE women_birth_control_id=8 and nofp_type_id=' ';
            UPDATE person_women SET total_child_count=child_alive_count  where total_child_count is null ;
            UPDATE person_women SET total_child_count=child_alive_count  where total_child_count=' ' ;

            UPDATE vn_stat SET pdx='A099' where pdx='A09' and vstdate>'2013-11-30'; 
            UPDATE ovstdiag SET icd10='A099' where icd10='A09' and vstdate>'2013-11-30';
            UPDATE vn_stat SET pdx='Z00' where pdx='Z001' and age_y>12 and vstdate>'2013-11-30';
            UPDATE ovstdiag o,vn_stat v SET o.icd10='Z00' where o.icd10='Z001' and v.age_y>12 and o.vstdate>'2013-11-30' and o.vn=v.vn;

            delete  from house WHERE house_id not in(SELECT house_id FROM person);

            update house h,village v set h.house_subtype_id='1' where h.village_id=v.village_id and v.village_moo<>0 and h.house_subtype_id is null;
            update house h,village v set h.house_subtype_id='9' where h.village_id=v.village_id and v.village_moo=0 and h.house_subtype_id is null;

            update house SET census_id=REPLACE(census_id,"-","");"""

            
            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qcomp, multi=True):
            pass
        conn.commit()
        cursor.close()
        conn.close()
        time.sleep(2)        
        messagebox.showinfo("การดำเนินการ","ปรับปรุงข้อมูลแล้ว...",parent=window)        

# ปรับสถานะคนเสียชีวิต
    def ser2():

        db_config = read_db_config()            
        qcomp ="""UPDATE person SET death ='Y' WHERE person_discharge_id ='1';

                UPDATE patient p INNER JOIN person s on s.cid=p.cid
                SET p.death=s.death;

                UPDATE `clinicmember` c INNER JOIN patient p on p.hn=c.hn
                SET c.discharge='Y',c.clinic_member_status_id='2' WHERE p.death ='Y'"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qcomp, multi=True):
            pass
        conn.commit()       
        cursor.close()
        conn.close()
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","ปรับปรุงข้อมูลแล้ว...",parent=window)
        
# โอนรูปจากเวชระเบียนไปบัญชี 1
    def ser3():
        db_config = read_db_config()
        qcomp ="""INSERT INTO person_image ( person_image, person_id )
            SELECT patient_image.image, person.person_id
            FROM person INNER JOIN (patient INNER JOIN patient_image ON patient.hn = patient_image.hn) ON person.cid = patient.cid
            WHERE (((person.person_id) Not In (select person_id from person_image)));"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qcomp, multi=True):
            pass
        conn.commit()
            
        cursor.close()
        conn.close()
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)

# บังคับส่งออกแฟ้ม PRENATAL
    def ser4():
        db_config = read_db_config()

        qcomp ="""UPDATE person_anc set force_complete_date = LAST_DAY(CURRENT_DATE) 
WHERE lmp >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and discharge ='N'
and labor_date is null;

UPDATE person_anc set force_complete_date = LAST_DAY(labor_date) 
WHERE lmp >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and discharge ='N'
and labor_date is not null;

UPDATE person_anc set force_complete_export ='Y' WHERE force_complete_date IS NOT NULL and discharge ='N';
"""

            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qcomp, multi=True):
            pass
        conn.commit()
            
        cursor.close()
        conn.close()
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)
        
# เพิ่มข้อมูลแฟ้ม pp_special กิจกรรมส่งเสริม/ป้องกัน ตามมาตรฐาน 43 แฟ้ม ปี 63
    def ser5():
        db_config = read_db_config()
        qpp_pp ="""INSERT IGNORE INTO pp_special_code VALUES
            ('1B0030','1B0030 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลปกติ ผู้รับบริการเคยตรวจด้วยตนเองได้ผลปกติ',null,null),
            ('1B0031','1B0031 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลปกติ ผู้รับบริการเคยตรวจด้วยตนเองได้ผลผิดปกติ',null,null),
            ('1B0032','1B0032 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลปกติ ผู้รับบริการไม่เคยตรวจด้วยตนเอง',null,null),
            ('1B0033','1B0033 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลปกติ ไม่ระบุว่าผู้รับบริการเคยตรวจด้วยตนเองหรือไม่',null,null),
            ('1B0034','1B0034 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลผิดปกติ ผู้รับบริการเคยตรวจด้วยตนเองได้ผลปกติ',null,null),
            ('1B0035','1B0035 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลผิดปกติ ผู้รับบริการเคยตรวจด้วยตนเองได้ผลผิดปกติ',null,null),
            ('1B0036','1B0036 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลผิดปกติ ผู้รับบริการไม่เคยตรวจด้วยตนเอง',null,null),
            ('1B0037','1B0037 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งเต้านมได้ผลผิดปกติ ไม่ระบุว่าผู้รับบริการเคยตรวจด้วยตนเองหรือไม่',null,null),
            ('1B0039','1B0039 ตรวจคัดกรองมะเร็งเต้านม ไม่ระบุรายละเอียด',null,null),
            ('1B0040','1B0040 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งปากมดลูก ด้วยวิธี VIA ได้ผลลบ',null,null),
            ('1B0041 ','1B0041  ตรวจคัดกรองความเสี่ยง/โรคมะเร็งปากมดลูก ด้วยวิธี VIA ได้ผลบวก ไม่ให้การรักษา',null,null),
            ('1B0042','1B0042 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งปากมดลูก ด้วยวิธี VIA ได้ผลบวก และให้การรักษา ',null,null),
            ('1B0043 ','1B0043  ตรวจคัดกรองความเสี่ยง/โรคมะเร็งปากมดลูก ด้วยวิธี VIA ไม่ระบุผลการตรวจ',null,null),
            ('1B0044','1B0044 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งปากมดลูก ด้วยวิธี Pap (ยังไม่ทราบผล)',null,null),
            ('1B0045','1B0045 การคัดกรองมะเร็งปากมดลูก ด้วยวิธี VIA ผลตรวจเป็นมะเร็งปากมดลูก',null,null),
            ('1B0046','1B0046 การคัดกรองมะเร็งปากมดลูก ด้วยวิธี HPV Genotype Testing',null,null),
            ('1B0048','1B0048 ตรวจคัดกรองมะเร็งปากมดลูก วิธีอื่น (ระบุวิธี)',null,null),
            ('1B0049','1B0049 ตรวจคัดกรองมะเร็งปากมดลูก ไม่ระบุวิธี',null,null),
            ('1B0060','1B0060 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งลำไส้ ได้ผลลบ',null,null),
            ('1B0061','1B0061 ตรวจคัดกรองความเสี่ยง/โรคมะเร็งลำไส้ ได้ผลบวก',null,null),
            ('1B0260','1B0260 การประเมินภาวะซึมเศร้าด้วยแบบประเมิน 9Q พบว่าผลปกติ ',null,null),
            ('1B0261','1B0261 การประเมินภาวะซึมเศร้าด้วยแบบประเมิน 9Q พบว่าซึมเศร้าน้อย (คะแนน 7-12)',null,null),
            ('1B0262','1B0262 การประเมินภาวะซึมเศร้าด้วยแบบประเมิน 9Q พบว่าซึมเศร้าปานกลาง (คะแนน 13-18)',null,null),
            ('1B0263','1B0263 การประเมินภาวะซึมเศร้าด้วยแบบประเมิน 9Q พบว่าซึมเศร้ารุนแรง (คะแนน≥19)',null,null),
            ('1B0269','1B0269 การประเมินภาวะซึมเศร้าด้วยแบบประเมิน 9Q ไม่ระบุรายละเอียด',null,null),
            ('1B0270','1B0270 การประเมินการฆ่าตัวตายด้วยแบบประเมิน 8Q พบว่าไม่มีแนวโน้มการฆ่าตัวตาย ',null,null),
            ('1B0271','1B0271 การประเมินการฆ่าตัวตายด้วยแบบประเมิน 8Q พบว่ามีแนวโน้มที่จะฆ่าตัวตายระดับน้อย (คะแนน 1-8) ',null,null),
            ('1B0272','1B0272 การประเมินการฆ่าตัวตายด้วยแบบประเมิน 8Q พบว่ามีแนวโน้มที่จะฆ่าตัวตายระดับปานกลาง (คะแนน 9-16)',null,null),
            ('1B0273','1B0273 การประเมินการฆ่าตัวตายด้วยแบบประเมิน 8Q พบว่ามีแนวโน้มที่จะฆ่าตัวตายระดับรุนแรง (คะแนน ≥17)',null,null),
            ('1B0279','1B0279 การประเมินการฆ่าตัวตายด้วยแบบประเมิน 8Q ไม่ระบุรายละเอียด ',null,null),
            ('1B0280','1B0280 การตรวจคัดกรองโรคซึมเศร้าในผู้สูงอายุด้วยแบบคัดกรอง 2Q พบว่าผลปกติ',null,null),
            ('1B0281','1B0281 การตรวจคัดกรองโรคซึมเศร้าในผู้สูงอายุด้วยแบบคัดกรอง 2Q พบว่าผลผิดปกติ',null,null),
            ('1B0282','1B0282 การตรวจคัดกรองโรคซึมเศร้าในผู้สูงอายุด้วยแบบคัดกรอง 9Q พบว่าผลปกติ',null,null),
            ('1B0283','1B0283 การตรวจคัดกรองโรคซึมเศร้าในผู้สูงอายุด้วยแบบคัดกรอง 9Q พบว่าซึมเศร้าน้อย (คะแนน 7-12)',null,null),
            ('1B0284','1B0284 การตรวจคัดกรองโรคซึมเศร้าในผู้สูงอายุด้วยแบบคัดกรอง 9Q พบว่าซึมเศร้าปานกลาง (คะแนน 13-18)',null,null),
            ('1B0285','1B0285 การตรวจคัดกรองโรคซึมเศร้าในผู้สูงอายุด้วยแบบคัดกรอง 9Q พบว่าซึมเศร้ารุนแรง (คะแนน ≥19)',null,null),
            ('1B0286','1B0286 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้สูงอายุ พบว่าผลปกติ',null,null),
            ('1B0287','1B0287 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้สูงอายุ พบว่าผลผิดปกติ',null,null),
            ('1B0289','1B0289 การตรวจคัดกรองโรคซึมเศร้า/ประเมินความเครียดในผู้สูงอายุ ไม่ระบุรายละเอียด',null,null),
            ('1B030','1B030 การคัดกรองผู้ป่วยจิตเวชที่มีความเสี่ยงสูง พบมีประวัติทำร้ายตนเองด้วยวิธีรุนแรง มุ่งหวังให้เสียชีวิต',null,null),
            ('1B031','1B031 การคัดกรองผู้ป่วยจิตเวชที่มีความเสี่ยงสูง พบมีประวัติทำร้ายผู้อื่นด้วยวิธีรุนแรง/ก่อเหตุการณ์รุนแรงในชุมชน',null,null),
            ('1B032','1B032 การคัดกรองผู้ป่วยจิตเวชที่มีความเสี่ยงสูง พบมีอาการหลงผิด มีความคิดทำร้ายผู้อื่นให้ถึงกับชีวิตหรือมุ่งร้ายผู้อื่นแบบเฉพาะเจาะจง เช่น ระบุชื่อคนที่จะมุ่งร้าย',null,null),
            ('1B033','1B033 การคัดกรองผู้ป่วยจิตเวชที่มีความเสี่ยงสูง พบเคยมีประวัติก่อคดีอาญารุนแรง (ฆ่า พยายามฆ่า ข่มขืน วางเพลิง)',null,null),
            ('1B034','1B034 การคัดกรองผู้ป่วยจิตเวชที่มีความเสี่ยงสูง พบมีอาการหลงผิด มีความคิดหมกมุ่นผิดปกติที่เกี่ยวข้องแบบเฉพาะเจาะจงกับราชวงศ์ จนเกิดพฤติกรรมวุ่นวาย รบกวนในงานพิธีสำคัญ',null,null),
            ('1B1130','1B1130 การตรวจคัดกรองสมรรถภาพการมองเห็น ผลเหมาะสมกับลักษณะงาน',null,null),
            ('1B1131','1B1131 การตรวจคัดกรองสมรรถภาพการมองเห็น ผลไม่เหมาะสมกับลักษณะงาน',null,null),
            ('1B1139','1B1139 การตรวจคัดกรองสมรรถภาพการมองเห็น ไม่ระบุรายละเอียด',null,null),
            ('1B1140','1B1140 การตรวจคัดกรองสมรรถภาพการได้ยินของการตรวจที่มีผลครั้งเดียว มีผลปกติ (ระดับการได้ยินของหูทั้ง 2 ข้าง ไม่เกิน 25 เดซิเบล ทุกความถี่)',null,null),
            ('1B1141','1B1141 การตรวจคัดกรองสมรรถภาพการได้ยินของการตรวจที่มีผลครั้งเดียว มีผลตรวจระดับการได้ยินมากกว่า 25 เดซิเบล ที่ความถี่ใด ความถี่หนึ่งของหูข้างใดข้างหนึ่ง',null,null),
            ('1B1142','1B1142 การตรวจคัดกรองสมรรถภาพการได้ยิน มีผลผ่านเกณฑ์ เมื่อเทียบผลการตรวจกับ Baseline audiogram (ไม่พบ 15 dB-shift หรือ ไม่พบ 15 dB-shift Twice ทุกความถี่) ',null,null),
            ('1B1143','1B1143 การตรวจคัดกรองสมรรถภาพการได้ยิน มีผลไม่ผ่านเกณฑ์ เมื่อเทียบผลการตรวจกับ Baseline audiogram (พบ 15 dB-shift Twice หลังจากตรวจยืนยัน: Confirmation audiogram ภายใน 30 วัน)',null,null),
            ('1B1144','1B1144 การตรวจคัดกรองสมรรถภาพการได้ยิน เมื่อเทียบผลการตรวจกับ Baseline audiogram (พบ 15 dB-shift และไม่ได้รับการตรวจยืนยัน: Confirmation audiogram ภายใน 30 วัน)',null,null),
            ('1B1149','1B1149 การตรวจคัดกรองสมรรถภาพการได้ยิน ไม่ระบุรายละเอียด',null,null),
            ('1B1150','1B1150 การตรวจคัดกรองสมรรถภาพปอด ผลปกติ',null,null),
            ('1B1151','1B1151 การตรวจคัดกรองสมรรถภาพปอด ผลต่ำกว่าค่าคาดคะเนชนิดหลอดลมอุดกั้น',null,null),
            ('1B1152','1B1152 การตรวจคัดกรองสมรรถภาพปอด ผลต่ำกว่าค่าคาดคะเนชนิดจำกัดการขยายตัว',null,null),
            ('1B1153','1B1153 การตรวจคัดกรองสมรรถภาพปอด ผลต่ำกว่าค่าคาดคะเนชนิดหลอดลมอุดกั้นและจำกัดการขยายตัว (ผสม)',null,null),
            ('1B1159','1B1159 การตรวจคัดกรองสมรรถภาพปอด ไม่ระบุรายละเอียด',null,null),
            ('1B1160','1B1160 การตรวจเอ็กซเรย์ปอดฟิล์มใหญ่ในวัยทำงาน ผลปกติระดับ 0/0',null,null),
            ('1B1161','1B1161 การตรวจเอ็กซเรย์ปอดฟิล์มใหญ่ในวัยทำงาน ผลผิดปกติตั้งแต่ระดับ 0/1 – 1/0 ',null,null),
            ('1B1162','1B1162 การตรวจเอ็กซเรย์ปอดฟิล์มใหญ่ในวัยทำงาน ผลผิดปกติตั้งแต่ระดับ 1/1 ขึ้นไป ',null,null),
            ('1B1169','1B1169 การตรวจเอ็กซเรย์ปอดฟิล์มใหญ่ในวัยทำงาน ไม่ระบุรายละเอียด',null,null),
            ('1B1170','1B1170 การตรวจคัดกรองเพื่อหาความเสี่ยงจากสารกำจัดศัตรูพืช ผลปกติ',null,null),
            ('1B1171','1B1171 การตรวจคัดกรองเพื่อหาความเสี่ยงจากสารกำจัดศัตรูพืช ผลปลอดภัย',null,null),
            ('1B1172','1B1172 การตรวจคัดกรองเพื่อหาความเสี่ยงจากสารกำจัดศัตรูพืช ผลมีความเสี่ยง',null,null),
            ('1B1173','1B1173 การตรวจคัดกรองเพื่อหาความเสี่ยงจากสารกำจัดศัตรูพืช ผลไม่ปลอดภัย',null,null),
            ('1B1179','1B1179 การตรวจคัดกรองเพื่อหาความเสี่ยงจากสารกำจัดศัตรูพืช ไม่ระบุรายละเอียด',null,null),
            ('1B1200','1B1200 การตรวจคัดกรองผู้สูงอายุที่มีภาวะหกล้ม พบว่าไม่มีความเสี่ยง',null,null),
            ('1B1201','1B1201 การตรวจคัดกรองผู้สูงอายุที่มีภาวะหกล้ม พบว่ามีความเสี่ยง ให้คำแนะนำและรักษา',null,null),
            ('1B1202','1B1202 การตรวจคัดกรองผู้สูงอายุที่มีภาวะหกล้ม พบว่ามีความเสี่ยงส่งรักษาต่อ',null,null),
            ('1B1209','1B1209 การตรวจคัดกรองผู้สูงอายุที่เสี่ยงภาวะหกล้มไม่ระบุรายละเอียด',null,null),
            ('1B1220','1B1220 การตรวจคัดกรองสมรรถภาพสมอง (ภาวะสมองเสื่อม) โดยแบบAMT ในผู้สูงอายุพบว่าปกติ',null,null),
            ('1B1221','1B1221 การตรวจคัดกรองสมรรถภาพสมอง (ภาวะสมองเสื่อม) โดยแบบ AMT ในผู้สูงอายุพบว่าผิดปกติ ให้คำแนะนำและรักษา',null,null),
            ('1B1223','1B1223 การตรวจคัดกรองสมรรถภาพสมอง (ภาวะสมองเสื่อม) โดยแบบ AMT ในผู้สูงอายุพบว่าผิดปกติและส่งไปรักษาต่อ',null,null),
            ('1B1224','1B1224 การตรวจคัดกรองสมรรถภาพสมอง (ภาวะสมองเสื่อม) โดยแบบ MMSE-T 2002 ในผู้สูงอายุพบว่าปกติ',null,null),
            ('1B1225','1B1225 การตรวจคัดกรองสมรรถภาพสมอง (ภาวะสมองเสื่อม) โดยแบบ MMSE-T 2002 ในผู้สูงอายุพบว่าผิดปกติ ให้คำแนะนำและรักษา',null,null),
            ('1B1226','1B1226 การตรวจคัดกรองสมรรถภาพสมอง (ภาวะสมองเสื่อม) โดยแบบ MMSE-T 2002 ในผู้สูงอายุพบว่าผิดปกติและส่งไปรักษาต่อ',null,null),
            ('1B1229','1B1229 การตรวจคัดกรองสมรรถภาพสมอง (ภาวะสมองเสื่อม) โดยแบบ AMT/ MMSE-T 2002 ในผู้สูงอายุ ไม่ระบุรายละเอียด',null,null),
            ('1B1230','1B1230 การตรวจคัดกรองความเสี่ยงโรคหัวใจและหลอดเลือดสมองในผู้สูงอายุ พบว่าไม่มีความเสี่ยง',null,null),
            ('1B1231','1B1231 การตรวจคัดกรองความเสี่ยงโรคหัวใจและหลอดเลือดสมองในผู้สูงอายุ พบว่ามีความเสี่ยง',null,null),
            ('1B1232','1B1232 การตรวจคัดกรองความเสี่ยงโรคหัวใจและหลอดเลือดสมองในผู้สูงอายุ พบว่ามีความเสี่ยงสูง',null,null),
            ('1B1234','1B1234 การตรวจคัดกรองความเสี่ยงโรคหัวใจและหลอดเลือดสมองในผู้สูงอายุ พบว่ามีความเสี่ยงสูงมาก ให้คำแนะนำ / รักษา',null,null),
            ('1B1235','1B1235 การตรวจคัดกรองความเสี่ยงโรคหัวใจและหลอดเลือดสมองในผู้สูงอายุพบว่ามีความเสี่ยงสูงมาก รักษาต่อ',null,null),
            ('1B1239','1B1239 การตรวจคัดกรองความเสี่ยงโรคหัวใจและหลอดเลือดสมองในผู้สูงอายุ  ไม่ระบุรายละเอียด',null,null),
            ('1B1240','1B1240 การตรวจคัดกรองสายตาระยะใกล้ในผู้สูงอายุพบว่าไม่มีปัญหา',null,null),
            ('1B1241','1B1241 การตรวจคัดกรองสายตาระยะใกล้ในผู้สูงอายุพบว่ามีปัญหาให้คำแนะนำและรักษา',null,null),
            ('1B1242','1B1242 การตรวจคัดกรองสายตาระยะใกล้ในผู้สูงอายุพบว่ามีปัญหาส่งไปรักษาต่อ',null,null),
            ('1B1243','1B1243 การตรวจคัดกรองสายตาระยะไกลในผู้สูงอายุพบว่าไม่มีปัญหา',null,null),
            ('1B1244','1B1244 การตรวจคัดกรองสายตาระยะไกลในผู้สูงอายุพบว่ามีปัญหาให้คำแนะนำและรักษา',null,null),
            ('1B1245','1B1245 การตรวจคัดกรองสายตาระยะไกลในผู้สูงอายุพบว่ามีปัญหาส่งไปรักษาต่อ',null,null),
            ('1B1249','1B1249 การตรวจคัดกรองสายตาระยะใกล้/ระยะไกลในผู้สูงอายุไม่ระบุรายละเอียด',null,null),
            ('1B1250','1B1250 การตรวจคัดกรองความเสี่ยงต้อกระจกในผู้สูงอายุพบว่าไม่มีปัญหา',null,null),
            ('1B1251','1B1251 การตรวจคัดกรองความเสี่ยงต้อกระจกในผู้สูงอายุพบว่ามีปัญหาให้คำแนะนำและรักษา',null,null),
            ('1B1252','1B1252 การตรวจคัดกรองความเสี่ยงต้อกระจกในผู้สูงอายุพบว่ามีปัญหาส่งไปรักษาต่อ',null,null),
            ('1B1253','1B1253 การตรวจคัดกรองความเสี่ยงต้อหินในผู้สูงอายุพบว่าไม่มีปัญหา',null,null),
            ('1B1254','1B1254 การตรวจคัดกรองความเสี่ยงต้อหินในผู้สูงอายุพบว่ามีปัญหาให้คำแนะนำและรักษา',null,null),
            ('1B1255','1B1255 การตรวจคัดกรองความเสี่ยงต้อหินในผู้สูงอายุพบว่ามีปัญหาส่งไปรักษาต่อ',null,null),
            ('1B1256','1B1256 การตรวจคัดกรองความเสี่ยงโรคจอประสาทตาเสื่อมจากอายุในผู้สูงอายุพบว่าไม่มีปัญหา',null,null),
            ('1B1257','1B1257 การตรวจคัดกรองความเสี่ยงโรคจอประสาทตาเสื่อมจากอายุในผู้สูงอายุพบว่ามีปัญหาให้คำแนะนำ และรักษา',null,null),
            ('1B1258','1B1258 การตรวจคัดกรองความเสี่ยงโรคจอประสาทตาเสื่อมจากอายุในผู้สูงอายุพบว่ามีปัญหา ส่งไปรักษาต่อ',null,null),
            ('1B1259','1B1259 การตรวจคัดกรองความเสี่ยงต้อกระจก  / ต้อหิน / จอประสาทตาเสื่อมจากอายุ ในผู้สูงอายุ ไม่ระบุรายละเอียด',null,null),
            ('1B1260','1B1260 การตรวจคัดกรองพฤติกรรมเสี่ยงต่อสุขภาพช่องปากในผู้สูงอายุพบว่าพฤติกรรมเหมาะสม',null,null),
            ('1B1261','1B1261 การตรวจคัดกรองพฤติกรรมเสี่ยงต่อสุขภาพช่องปากในผู้สูงอายุพบว่าพฤติกรรมไม่เหมาะสม และแนะนำให้ความรู้',null,null),
            ('1B1269','1B1269 การตรวจคัดกรองพฤติกรรมเสี่ยงต่อสุขภาพช่องปากในผู้สูงอายุไม่ระบุรายละเอียด',null,null),
            ('1B1270','1B1270 การตรวจคัดกรองข้อเข่าเสื่อมทางคลินิกในผู้สูงอายุพบว่าปกติ',null,null),
            ('1B1271','1B1271 การตรวจคัดกรองข้อเข่าเสื่อมทางคลินิกในผู้สูงอายุพบว่าผิดปกติ ให้คำแนะนำและรักษา',null,null),
            ('1B1272','1B1272 การตรวจคัดกรองข้อเข่าเสื่อมทางคลินิกในผู้สูงอายุพบว่าผิดปกติและส่งรักษาต่อ',null,null),
            ('1B1273','1B1273 การตรวจคัดกรองสมรรถนะผู้สูงอายุเกี่ยวกับการดูแลระยะยาวพบว่าไม่ต้องดูแลระยะยาว',null,null),
            ('1B1274','1B1274 การตรวจคัดกรองสมรรถนะผู้สูงอายุเกี่ยวกับการดูแลระยะยาวพบว่าต้องเฝ้าระวัง ให้คำแนะนำและติดตาม',null,null),
            ('1B1275','1B1275 การตรวจคัดกรองสมรรถนะผู้สูงอายุเกี่ยวกับการดูแลระยะยาวพบว่าต้องดูแลระยะยาว ให้คำแนะนำและดูแลต่อเนื่อง',null,null),
            ('1B1279','1B1279 การตรวจคัดกรองข้อเข่าเสื่อมทางคลินิก ในผู้สูงอายุ / สมรรถนะผู้สูงอายุเกี่ยวกับการดูแลระยะยาว ไม่ระบุรายละเอียด',null,null),
            ('1B1280','1B1280 การตรวจคัดกรองสมรรถนะผู้สูงอายุเกี่ยวกับความสามารถในการทำกิจวัตรประจำวันพบว่าช่วยเหลือตัวเองได้ /ติดสังคม (ADL 12-20 คะแนน) และได้รับการจัดทำ Care Plan',null,null),
            ('1B1281','1B1281 การตรวจคัดกรองสมรรถนะผู้สูงอายุเกี่ยวกับความสามารถในการทำกิจวัตรประจำวันพบว่าช่วยเหลือตัวเองได้บ้าง / บางส่วน /ติดบ้าน (ADL 5-11 คะแนน) และได้รับการจัดทำ Care Plan',null,null),
            ('1B1282','1B1282 การตรวจคัดกรองสมรรถนะผู้สูงอายุเกี่ยวกับความสามารถในการทำกิจวัตรประจำวัน พบว่าช่วยเหลือตัวเองได้น้อย / ไม่ได้เลย /ภาวะติดเตียง (ADL 0-4 คะแนน) และได้รับการจัดทำ Care Plan',null,null),
            ('1B1283','1B1283 การตรวจคัดกรองภาวะกลั้นปัสสาวะในผู้สูงอายุ',null,null),
            ('1B1284','1B1284 การตรวจคัดกรองภาวะกลั้นปัสสาวะในผู้สูงอายุ ไม่มีปัญหา',null,null),
            ('1B1285','1B1285 การตรวจคัดกรองภาวะกลั้นปัสสาวะในผู้สูงอายุ มีปัญหา',null,null),
            ('1B1289','1B1289 การตรวจคัดกรองสมรรถนะผู้สูงอายุเกี่ยวกับความสามารถในการทำกิจวัตรประจำวันไม่ระบุรายละเอียด',null,null),
            ('1B130','1B130 การตรวจคัดกรองโรคซึมเศร้าในผู้ป่วยโรคเรื้อรังด้วยแบบคัดกรอง 2Q พบว่าผลปกติ',null,null),
            ('1B131','1B131 การตรวจคัดกรองโรคซึมเศร้าในผู้ป่วยโรคเรื้อรังด้วยแบบคัดกรอง 2Q พบว่าผลผิดปกติ',null,null),
            ('1B132','1B132 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้ป่วยโรคเรื้อรังพบว่าผลปกติ (0 – 4 คะแนน)',null,null),
            ('1B133','1B133 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้ป่วยโรคเรื้อรังพบว่ามีปัญหาความเครียด (5 – 7 คะแนน) ',null,null),
            ('1B134','1B134 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้ป่วยโรคเรื้อรังพบว่ามีความเครียดสูง (8 คะแนนขึ้นไป)',null,null),
            ('1B139','1B139 การตรวจคัดกรองโรคซึมเศร้า/ประเมินความเครียดในผู้ป่วยโรคเรื้อรังไม่ระบุรายละเอียด',null,null),
            ('1B140','1B140 การตรวจคัดกรองโรคซึมเศร้าในหญิงตั้งครรภ์/หลังคลอดด้วยแบบคัดกรอง 2Q พบว่าผลปกติ',null,null),
            ('1B141','1B141 การตรวจคัดกรองโรคซึมเศร้าในหญิงตั้งครรภ์/หลังคลอดด้วยแบบคัดกรอง 2Q พบว่าผลผิดปกติ',null,null),
            ('1B142','1B142 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในหญิงตั้งครรภ์/หลังคลอดพบว่าผลปกติ (0 – 4 คะแนน) ',null,null),
            ('1B143','1B143 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในหญิงตั้งครรภ์/หลังคลอดพบว่ามีปัญหาความเครียด  (5 – 7 คะแนน)',null,null),
            ('1B144','1B144 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในหญิงตั้งครรภ์/หลังคลอดพบว่ามีความเครียดสูง (8 คะแนนขึ้นไป) ',null,null),
            ('1B149','1B149 การตรวจคัดกรองโรคซึมเศร้า/ประเมินความเครียดในหญิงตั้งครรภ์/หลังคลอด ไม่ระบุรายละเอียด',null,null),
            ('1B150','1B150 การตรวจคัดกรองโรคซึมเศร้าในผู้มีปัญหาสุรา/สารเสพติดด้วยแบบคัดกรอง 2Q พบว่าผลปกติ',null,null),
            ('1B151','1B151 การตรวจคัดกรองโรคซึมเศร้าในผู้มีปัญหาสุรา/สารเสพติดด้วยแบบคัดกรอง 2Q พบว่าผลผิดปกติ',null,null),
            ('1B152','1B152 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้มีปัญหาสุรา/สารเสพติดพบว่าผลปกติ (0 – 4 คะแนน)',null,null),
            ('1B153','1B153 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้มีปัญหาสุรา/สารเสพติดพบว่ามีปัญหาความเครียด (5 – 7 คะแนน)',null,null),
            ('1B154','1B154 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้มีปัญหาสุรา/สารเสพติดพบว่ามีความเครียดสูง (8 คะแนนขึ้นไป)',null,null),
            ('1B159','1B159 การตรวจคัดกรองโรคซึมเศร้า/ประเมินความเครียดในผู้มีปัญหาสุรา/สารเสพติดไม่ระบุรายละเอียด',null,null),
            ('1B160','1B160 การตรวจคัดกรองโรคซึมเศร้าในกลุ่มที่มีอาการซึมเศร้าชัดเจนด้วยแบบคัดกรอง 2Q พบว่าผลปกติ',null,null),
            ('1B161','1B161 การตรวจคัดกรองโรคซึมเศร้าในกลุ่มที่มีอาการซึมเศร้าชัดเจนด้วยแบบคัดกรอง 2Q พบว่าผลผิดปกติ',null,null),
            ('1B162','1B162 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในกลุ่มที่มีอาการซึมเศร้าชัดเจนพบว่าผลปกติ (0 – 4 คะแนน)',null,null),
            ('1B163','1B163 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในกลุ่มที่มีอาการซึมเศร้าชัดเจนพบว่ามีปัญหาความเครียด (5 – 7 คะแนน)',null,null),
            ('1B164','1B164 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในกลุ่มที่มีอาการซึมเศร้าชัดเจนพบว่ามีความเครียดสูง (8 คะแนนขึ้นไป)',null,null),
            ('1B169','1B169 การตรวจคัดกรองโรคซึมเศร้า/ประเมินความเครียดในกลุ่มที่มีอาการซึมเศร้า ชัดเจน ไม่ระบุรายละเอียด',null,null),
            ('1B170','1B170 การตรวจคัดกรองโรคซึมเศร้าในผู้ที่มีอาการทางกายเรื้อรังหลายอาการที่หาสาเหตุไม่ได้ด้วยแบบคัดกรอง 2Q พบว่าผลปกติ',null,null),
            ('1B171','1B171 การตรวจคัดกรองโรคซึมเศร้าในผู้ที่มีอาการทางกายเรื้อรังหลายอาการที่หาสาเหตุไม่ได้ด้วยแบบคัดกรอง 2Q พบว่าผลผิดปกติ',null,null),
            ('1B172','1B172 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในกลุ่มที่มีอาการซึมเศร้ในผู้ที่มีอาการทางกายเรื้อรังหลายอาการที่หาสาเหตุไม่ได้ พบว่าผลปกติ (0 – 4 คะแนน)',null,null),
            ('1B173','1B173 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้ที่มีอาการทางกายเรื้อรังหลายอาการที่หาสาเหตุไม่ได้ พบว่ามีปัญหาความเครียด (5 – 7 คะแนน)',null,null),
            ('1B174 ','1B174  การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในผู้ที่มีอาการทางกายเรื้อรังหลายอาการที่หาสาเหตุไม่ได้ พบว่ามีความเครียดสูง (8 คะแนนขึ้นไป)',null,null),
            ('1B179','1B179 การตรวจคัดกรองโรคซึมเศร้า/ประเมินความเครียดในผู้ที่มีอาการทางกายเรื้อรังหลายอาการที่หาสาเหตุไม่ได้  ไม่ระบุรายละเอียด',null,null),
            ('1B180','1B180 การตรวจคัดกรองโรคซึมเศร้าในกลุ่มที่มีการสูญเสีย  ด้วยแบบคัดกรอง 2Q พบว่าผลปกติ',null,null),
            ('1B181','1B181 การตรวจคัดกรองโรคซึมเศร้าในกลุ่มที่มีการสูญเสีย ด้วยแบบคัดกรอง 2Q พบว่าผลผิดปกติ',null,null),
            ('1B182','1B182 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในกลุ่มที่มีการสูญเสีย พบว่าผลปกติ (0 – 4 คะแนน)',null,null),
            ('1B183','1B183 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในกลุ่มที่มีการสูญเสีย พบว่าปัญหาความเครียด (5 – 7 คะแนน)',null,null),
            ('1B184','1B184 การประเมินความเครียดด้วยแบบคัดกรอง ST5 ในกลุ่มที่มีการสูญเสีย พบว่ามีความเครียดสูง (8 คะแนนขึ้นไป)',null,null),
            ('1B189','1B189 การตรวจคัดกรองโรคซึมเศร้า/ประเมินความเครียดในกลุ่มที่มีการสูญเสีย  ไม่ระบุรายละเอียด',null,null),
            ('1B200','1B200 การตรวจคัดกรองพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B201','1B201 การตรวจคัดกรองพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B202','1B202 การตรวจคัดกรองพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B203','1B203 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B204','1B204 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B205','1B205 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B206','1B206 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DAIM ผลปกติ',null,null),
            ('1B207','1B207 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DAIM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B209','1B209 การตรวจคัดกรอง/แบบเฝ้าระวังพัฒนาการสมวัยด้านการเคลื่อนไหวโดยเครื่องมือ DSPM และ หรือ DAIM ไม่ระบุรายละเอียด',null,null),
            ('1B210','1B210 การตรวจคัดกรองพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B211','1B211 การตรวจคัดกรองพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B212','1B212 การตรวจคัดกรองพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B213','1B213 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B214','1B214 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B215','1B215 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B216','1B216 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DAIM ผลปกติ',null,null),
            ('1B217','1B217 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DAIM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B219','1B219 การตรวจคัดกรอง/แบบเฝ้าระวังพัฒนาการสมวัยด้านกล้ามเนื้อมัดเล็กและสติปัญญาโดยเครื่องมือ DSPM และหรือ DAIM ไม่ระบุรายละเอียด',null,null),
            ('1B220','1B220 การตรวจคัดกรองพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B221','1B221 การตรวจคัดกรองพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B222','1B222 การตรวจคัดกรองพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B223','1B223 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B224','1B224 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B225','1B225 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B226','1B226 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DAIM ผลปกติ',null,null),
            ('1B227','1B227 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DAIM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B229','1B229 การตรวจคัดกรอง/แบบเฝ้าระวังพัฒนาการสมวัยด้านการเข้าใจภาษาโดยเครื่องมือ DSPM และหรือ DAIM ไม่ระบุรายละเอียด',null,null),
            ('1B230','1B230 การตรวจคัดกรองพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B231','1B231 การตรวจคัดกรองพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B232','1B232 การตรวจคัดกรองพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B233','1B233 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B234','1B234 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B235','1B235 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B236','1B236 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DAIM ผลปกติ',null,null),
            ('1B237','1B237 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DAIM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B239','1B239 การตรวจคัดกรอง/แบบเฝ้าระวังพัฒนาการสมวัยด้านการใช้ภาษาโดยเครื่องมือ DSPM และหรือ DAIM ไม่ระบุรายละเอียด',null,null),
            ('1B240','1B240 การตรวจคัดกรองพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B241','1B241 การตรวจคัดกรองพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B242','1B242 การตรวจคัดกรองพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DSPM ผลล่าช้าส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B243','1B243 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B244','1B244 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B245','1B245 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการใช้ภาด้านการช่วยเหลือตัวเองและสังคม โดยเครื่องมือ DSPM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B246','1B246 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DAIM ผลปกติ',null,null),
            ('1B247','1B247 การตรวจแบบเฝ้าระวังพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DAIM ผลล่าช้า ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B249','1B249 การตรวจคัดกรอง/แบบเฝ้าระวังพัฒนาการสมวัยด้านการช่วยเหลือตัวเองและสังคมโดยเครื่องมือ DSPMและหรือ DAIM ไม่ระบุรายละเอียด',null,null),
            ('1B250','1B250 การตรวจประเมินระบบประสาทและพัฒนาการอายุแรกเกิด โดยเครื่องมือ DAIM ข้อที่ 1-3 (ตรวจปฏิกิริยา ตรวจความตึงตัวของกล้ามเนื้อ และตรวจข้อเท้า) ผ่าน',null,null),
            ('1B251','1B251 การตรวจประเมินระบบประสาทและพัฒนาการอายุแรกเกิด โดยเครื่องมือ DAIMข้อที่ 1-3 (ตรวจปฏิกิริยา ตรวจความตึงตัวของกล้ามเนื้อ และตรวจข้อเท้า) ไม่ผ่าน ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B252','1B252 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 1 เดือน โดยเครื่องมือ DAIM ข้อที่ 4 (ตรวจการเหยียดแขนและขา) ผ่าน',null,null),
            ('1B253','1B253 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 1 เดือน โดยเครื่องมือ DAIM ข้อที่ 4 (ตรวจการเหยียดแขนและขา) ไม่ผ่าน ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B254','1B254 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 3-4 เดือน โดยเครื่องมือ DAIM ข้อที่ 5 (ตรวจการกำมือ) ผ่าน',null,null),
            ('1B255','1B255 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 3-4 เดือน โดยเครื่องมือ DAIM ข้อที่ 5 (ตรวจการกำมือ) ไม่ผ่าน ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B256','1B256 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 10-12 เดือน โดยเครื่องมือ DAIM ข้อที่ 6 (ตรวจการกางแขน) ผ่าน',null,null),
            ('1B257','1B257 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 10-12 เดือน โดยเครื่องมือ DAIM ข้อที่ 6 (ตรวจการกางแขน) ไม่ผ่าน ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B258','1B258 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 55-60 เดือน โดยเครื่องมือ DAIM ข้อที่ 7 (เดินต่อส้นเท้า) ผ่าน',null,null),
            ('1B259','1B259 การตรวจประเมินระบบประสาทและพัฒนาการอายุ 55-60 เดือน โดยเครื่องมือ DAIM ข้อที่ 7 (เดินต่อส้นเท้า) ไม่ผ่าน ส่งเพื่อประเมิน/รักษาต่อ',null,null),
            ('1B260','1B260 ผลการตรวจคัดกรองพัฒนาการสมวัยโดยเครื่องมือ DSPM ผลปกติ',null,null),
            ('1B261','1B261 ผลการตรวจคัดกรองพัฒนาการสมวัยโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งเสริมพัฒนาการใน 1 เดือน',null,null),
            ('1B262','1B262 ผลการตรวจคัดกรองพัฒนาการสมวัยโดยเครื่องมือ DSPM สงสัยล่าช้า ส่งต่อทันที',null,null),
            ('1B270','1B270 การกระตุ้นพัฒนาการเด็กล่าช้าโดยเครื่องมือ TEDA4I ผลปกติ',null,null),
            ('1B271','1B271 การกระตุ้นพัฒนาการเด็กล่าช้าโดยเครื่องมือ TEDA4I ผลล่าช้า ด้านการเคลื่อนไหว',null,null),
            ('1B272','1B272 การกระตุ้นพัฒนาการเด็กล่าช้าโดยเครื่องมือ TEDA4I ผลล่าช้า ด้านกล้ามเนื้อมัดเล็กและสติปัญญา',null,null),
            ('1B273','1B273 การกระตุ้นพัฒนาการเด็กล่าช้าโดยเครื่องมือ TEDA4I ผลล่าช้า ด้านความเข้าใจภาษา',null,null),
            ('1B274','1B274 การกระตุ้นพัฒนาการเด็กล่าช้าโดยเครื่องมือ TEDA4I ผลล่าช้า ด้านการใช้ภาษา',null,null),
            ('1B275','1B275 การกระตุ้นพัฒนาการเด็กล่าช้าโดยเครื่องมือ TEDA4I ผลล่าช้า ด้านการช่วยเหลือตนเองและสังคม',null,null),
            ('1B30','1B30 ผลการตรวจคัดกรองมะเร็งปากมดลูก ผลปกติ',null,null),
            ('1B31','1B31 ผลการตรวจคัดกรองธาลาสซีเมีย ผลปกติ',null,null),
            ('1B40','1B40 ผลการตรวจคัดกรองมะเร็งปากมดลูก ผลผิดปกติ',null,null),
            ('1B41','1B41 ผลการตรวจคัดกรองธาลาสซีเมีย ผลผิดปกติ',null,null),
            ('1B501','1B501 ผู้มารับบริการมีพฤติกรรมสูบบุหรี่ 1-10 มวนต่อวัน',null,null),
            ('1B502','1B502 ผู้มารับบริการมีพฤติกรรมสูบบุหรี่ 11-19 มวนต่อวัน',null,null),
            ('1B503','1B503 ผู้มารับบริการมีพฤติกรรมสูบบุหรี่ 20 มวนขึ้นไปต่อวัน',null,null),
            ('1B504','1B504 ผู้มารับบริการมีพฤติกรรมสูบบุหรี่มวนแรกหลังตื่นนอน น้อยกว่า 30 นาที',null,null),
            ('1B505','1B505 ผู้มารับบริการมีพฤติกรรมสูบบุหรี่มวนแรกหลังตื่นนอน มากกว่า 30 นาที แต่น้อยกว่า 1 ชั่วโมง',null,null),
            ('1B506','1B506 ผู้มารับบริการมีพฤติกรรมสูบบุหรี่มวนแรกหลังตื่นนอน 1 ชั่วโมง หรือมากกว่า',null,null),
            ('1B509','1B509 ผู้มารับบริการมีพฤติกรรมสูบบุหรี่ ไม่ระบุรายละเอียด',null,null),
            ('1B51','1B51 ผู้มารับบริการมีพฤติกรรมเคยสูบบุหรี่แต่เลิกแล้ว',null,null),
            ('1B52','1B52 ผู้มารับบริการมีพฤติกรรมไม่เคยสูบบุหรี่',null,null),
            ('1B530','1B530 การให้คำแนะนำผู้ติดบุหรี่แบบสั้น (Brief Advice)',null,null),
            ('1B531','1B531 การให้คำปรึกษาเพื่อการเลิกบุหรี่ (Counseling Advice)',null,null),
            ('1B532','1B532 การให้คำปรึกษาและให้ยาเพื่อเลิกบุหรี่ (Counseling Advice + Medicine)',null,null),
            ('1B540','1B540 การติดตามผู้ติดบุหรี่ ระยะเวลา 1 เดือน ผลยังสูบอยู่ปริมาณ/จำนวนมวน เท่าเดิม',null,null),
            ('1B541','1B541 การติดตามผู้ติดบุหรี่ ระยะเวลา 1 เดือน ผลลดปริมาณ/จำนวนมวนที่สูบลงได้',null,null),
            ('1B542','1B542 การติดตามผู้ติดบุหรี่ ระยะเวลา 1 เดือน ผลไม่สูบแล้ว',null,null),
            ('1B550','1B550 การติดตามผู้ติดบุหรี่ ระยะเวลา 3 เดือน ผลยังสูบบุหรี่อยู่ปริมาณ/จำนวนมวนเท่าเดิม',null,null),
            ('1B551','1B551 การติดตามผู้ติดบุหรี่ ระยะเวลา 3 เดือน ผลลดปริมาณ/จำนวนมวนที่สูบลงได้',null,null),
            ('1B552','1B552 การติดตามผู้ติดบุหรี่ ระยะเวลา 3 เดือน ผลไม่สูบแล้ว',null,null),
            ('1B560','1B560 การติดตามผู้ติดบุหรี่ ระยะเวลา 6 เดือน ผลยังสูบบุหรี่อยู่ปริมาณ/จำนวนมวนเท่าเดิม',null,null),
            ('1B561','1B561 การติดตามผู้ติดบุหรี่ ระยะเวลา 6 เดือน ผลลดปริมาณ/จำนวนมวนที่สูบลงได้',null,null),
            ('1B562','1B562 การติดตามผู้ติดบุหรี่ ระยะเวลา 6 เดือน ผลไม่สูบแล้ว',null,null),
            ('1B600','1B600 ผู้มารับบริการไม่เคยดื่มเครื่องดื่มแอลกอฮอล์ ตลอดชีวิตที่ผ่านมา ',null,null),
            ('1B601','1B601 ผู้มารับบริการเคยดื่มเครื่องดื่มแอลกอฮอล์ แต่เลิกดื่มมาแล้ว 1 ปีขึ้นไป',null,null),
            ('1B602','1B602 ผู้มารับบริการดื่มเครื่องดื่มแอลกอฮอล์ในระดับเสี่ยงต่ำ (คะแนน 0-10)',null,null),
            ('1B603','1B603 ผู้มารับบริการดื่มเครื่องดื่มแอลกอฮอล์ในระดับเสี่ยงปานกลาง (คะแนน 11-26)',null,null),
            ('1B604','1B604 ผู้มารับบริการดื่มเครื่องดื่มแอลกอฮอล์ในระดับเสี่ยงสูง (คะแนนตั้งแต่ 27 ขึ้นไป)',null,null),
            ('1B609','1B609 ผู้มารับบริการดื่มเครื่องดื่มแอลกอฮอล์ ไม่ระบุรายละเอียด',null,null),
            ('1B610','1B610 การให้คำแนะนำ (brief advice)',null,null),
            ('1B611','1B611 การให้คำปรึกษาแบบสั้น (brief counseling)',null,null),
            ('1B612','1B612 การส่งต่อเพื่อรับการประเมินและการบำบัดโดยผู้เชี่ยวชาญ (refer)',null,null),
            ('1B620','1B620 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 1 เดือน ไม่ดื่มเลย',null,null),
            ('1B621','1B621 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 1 เดือน ดื่มลดลง',null,null),
            ('1B622','1B622 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 1 เดือน ดื่มเท่าเดิม',null,null),
            ('1B623','1B623 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 1 เดือน ดื่มมากขึ้น',null,null),
            ('1B630','1B630 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 3 เดือน ไม่ดื่มเลย',null,null),
            ('1B631','1B631 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 3 เดือน ดื่มลดลง',null,null),
            ('1B632','1B632 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 3 เดือน ดื่มเท่าเดิม',null,null),
            ('1B633','1B633 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 3 เดือน ดื่มมากขึ้น',null,null),
            ('1B640','1B640 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 6 เดือน ไม่ดื่มเลย',null,null),
            ('1B641','1B641 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 6 เดือน ดื่มลดลง',null,null),
            ('1B642','1B642 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 6 เดือน ดื่มเท่าเดิม',null,null),
            ('1B643','1B643 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 6 เดือน ดื่มมากขึ้น',null,null),
            ('1B650','1B650 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 12 เดือน ไม่ดื่มเลย',null,null),
            ('1B651','1B651 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 12 เดือน ดื่มลดลง',null,null),
            ('1B652','1B652 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 12 เดือน ดื่มเท่าเดิม',null,null),
            ('1B653','1B653 การติดตามผู้มีพฤติกรรมการดื่มสุราแบบเสี่ยงสูง (ผู้ติดสุรา) ระยะเวลา 12 เดือน ดื่มมากขึ้น',null,null),
            ('1F301','1F301 การให้คำปรึกษาด้านสุขภาพ กลุ่มชายที่มีเพศสัมพันธ์กับชาย',null,null),
            ('1F302','1F302 การให้คำปรึกษาด้านสุขภาพ กลุ่มสาวประเภทสอง',null,null),
            ('1F31','1F31 การให้คำปรึกษาด้านสุขภาพ กลุ่มที่มีคู่นอนหลายคนเชิงพาณิชย์',null,null),
            ('1F32','1F32 การให้คำปรึกษาด้านสุขภาพ กลุ่มผู้ใช้ยาเสพติดประเภทฉีด',null,null),
            ('1F33','1F33 การให้คำปรึกษาด้านสุขภาพ กลุ่มคู่ผู้ติดเชื้อ',null,null),
            ('1F38','1F38 การให้คำปรึกษาด้านสุขภาพ กลุ่มอื่น ๆ',null,null);
            
            ALTER TABLE hosxp_pcu.pp_special_type 
            MODIFY COLUMN pp_special_type_id int(11) NOT NULL AUTO_INCREMENT FIRST;

            INSERT INTO pp_special_type (pp_special_type_name,pp_special_code)
            SELECT name,code FROM pp_special_code WHERE `code` not in (SELECT pp_special_code FROM pp_special_type);

            """

            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qpp_pp, multi=True):
            pass
        conn.commit()
        cursor.close()
        conn.close()            
        time.sleep(2)    
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)
        
# เพิ่มข้อมูลแฟ้ม community_service เยี่ยมบ้าน ตามมาตรฐาน 43 แฟ้ม ปี 63
    def ser6():
        db_config = read_db_config()

        qovst_com ="""DROP TABLE IF EXISTS `nu_community_service`;

            CREATE TABLE `nu_community_service`  (
              `code` varchar(255) CHARACTER SET tis620 COLLATE tis620_thai_ci NULL DEFAULT NULL,
              `name` varchar(255) CHARACTER SET tis620 COLLATE tis620_thai_ci NULL DEFAULT NULL
            ) ENGINE = MyISAM CHARACTER SET = tis620 COLLATE = tis620_thai_ci ROW_FORMAT = Dynamic;

            INSERT INTO `nu_community_service` VALUES ('1A000', 'เยี่ยมผู้ป่วยโรคความดันโลหิตสูง');
            INSERT INTO `nu_community_service` VALUES ('1A001', 'เยี่ยมผู้ป่วยโรคเบาหวาน ');
            INSERT INTO `nu_community_service` VALUES ('1A002', 'เยี่ยมผู้ป่วยโรคมะเร็ง');
            INSERT INTO `nu_community_service` VALUES ('1A003', 'เยี่ยมผู้ป่วยโรคระบบทางเดินหายใจ');
            INSERT INTO `nu_community_service` VALUES ('1A004', 'เยี่ยมผู้ป่วยโรคสมองเสื่อม');
            INSERT INTO `nu_community_service` VALUES ('1A005', 'เยี่ยมผู้ป่วยโรคหลอดเลือดสมอง');
            INSERT INTO `nu_community_service` VALUES ('1A008', 'เยี่ยมผู้ป่วยโรคเรื้อรังอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1A009', 'เยี่ยมผู้ป่วยโรคเรื้อรังที่ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A010', 'เยี่ยมผู้ป่วยโรคไข้เลือดออก');
            INSERT INTO `nu_community_service` VALUES ('1A011', 'เยี่ยมผู้ป่วยโรคอุจจาระร่วง ');
            INSERT INTO `nu_community_service` VALUES ('1A012', 'เยี่ยมผู้ป่วยโรคไข้หวัดใหญ่ 2009');
            INSERT INTO `nu_community_service` VALUES ('1A013', 'เยี่ยมผู้ป่วยโรคไข้หวัดใหญ่อื่นๆ หรือไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A014', 'เยี่ยมผู้ป่วยโรควัณโรค ');
            INSERT INTO `nu_community_service` VALUES ('1A015', 'เยี่ยมผู้ป่วย/ผู้สัมผัสโรคติดต่อทางเพศสัมพันธ์');
            INSERT INTO `nu_community_service` VALUES ('1A016', 'เยี่ยมผู้ป่วยโรคเอดส์');
            INSERT INTO `nu_community_service` VALUES ('1A018', 'เยี่ยมผู้ป่วยโรคติดต่ออื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1A019', 'เยี่ยมผู้ป่วยโรคติดต่อที่ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A020', 'เยี่ยมผู้ป่วยโรคจิต');
            INSERT INTO `nu_community_service` VALUES ('1A021', 'เยี่ยมผู้ป่วยโรควิตกกังวล');
            INSERT INTO `nu_community_service` VALUES ('1A022', 'เยี่ยมผู้ป่วยโรคซึมเศร้า');
            INSERT INTO `nu_community_service` VALUES ('1A023', 'เยี่ยมผู้ป่วยโรคปัญญาอ่อน');
            INSERT INTO `nu_community_service` VALUES ('1A024', 'เยี่ยมผู้ป่วยโรคลมชัก');
            INSERT INTO `nu_community_service` VALUES ('1A025', 'เยี่ยมผู้พยายามฆ่าตัวตาย');
            INSERT INTO `nu_community_service` VALUES ('1A028', 'เยี่ยมผู้ป่วยโรคจิตและปัญหาสุขภาพจิตอื่นๆ');
            INSERT INTO `nu_community_service` VALUES ('1A029', 'เยี่ยมผู้ป่วยโรคจิตและปัญหาสุขภาพจิต ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A030', 'เยี่ยมผู้ป่วยที่ได้รับบาดเจ็บจากอุบัติเหตุ');
            INSERT INTO `nu_community_service` VALUES ('1A031', 'เยี่ยมผู้ป่วยที่ได้รับบาดเจ็บจากการถูกทำร้ายโดยคน');
            INSERT INTO `nu_community_service` VALUES ('1A032', 'เยี่ยมผู้ป่วยที่ได้รับบาดเจ็บจากการถูกทำร้ายโดยสัตว์');
            INSERT INTO `nu_community_service` VALUES ('1A038', 'เยี่ยมผู้ป่วยที่ได้รับบาดเจ็บจากสาเหตุภายนอกอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1A039', 'เยี่ยมผู้ป่วยที่ได้รับบาดเจ็บจากสาเหตุภายนอกที่ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A10', 'เยี่ยมผู้ป่วยหลังผ่าตัด');
            INSERT INTO `nu_community_service` VALUES ('1A11', 'เยี่ยมผู้ป่วยที่มีใบติดตามจากโรงพยาบาล');
            INSERT INTO `nu_community_service` VALUES ('1A12', 'เยี่ยมผู้ป่วยที่ต้องการดูแลอย่างต่อเนื่องจากโรงพยาบาล');
            INSERT INTO `nu_community_service` VALUES ('1A13', 'เยี่ยมติดตามผู้ป่วยขาดนัด');
            INSERT INTO `nu_community_service` VALUES ('1A14', 'เยี่ยมผู้ป่วยหลังจากรับ/ส่งต่อ (refer) จากโรงพยาบาล');
            INSERT INTO `nu_community_service` VALUES ('1A18', 'เยี่ยมผู้ป่วยหลังได้รับการรักษาอื่นๆ');
            INSERT INTO `nu_community_service` VALUES ('1A19', 'เยี่ยมผู้ป่วยหลังได้รับการรักษา  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A200', 'เยี่ยมหญิงตั้งครรภ์แรก');
            INSERT INTO `nu_community_service` VALUES ('1A201', 'เยี่ยมหญิงตั้งครรภ์น้ำหนักน้อยกว่าเกณฑ์');
            INSERT INTO `nu_community_service` VALUES ('1A202', 'เยี่ยมหญิงตั้งครรภ์ที่มีภาวะเสี่ยง ');
            INSERT INTO `nu_community_service` VALUES ('1A203', 'เยี่ยมหญิงตั้งครรภ์ที่แยกทางกับสามี');
            INSERT INTO `nu_community_service` VALUES ('1A208', 'เยี่ยมหญิงตั้งครรภ์กิจกรรมอื่นๆ');
            INSERT INTO `nu_community_service` VALUES ('1A209', 'เยี่ยมหญิงตั้งครรภ์  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A210', 'เยี่ยมหญิงหลังคลอด ครั้งที่ 1 (1-2 สัปดาห์)  ที่ไม่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A211', 'เยี่ยมหญิงหลังคลอด ครั้งที่ 1 (1-2 สัปดาห์)  ที่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A212', 'เยี่ยมหญิงหลังคลอด ครั้งที่ 1 (1-2 สัปดาห์)  ไม่ระบุรายละเอียด ');
            INSERT INTO `nu_community_service` VALUES ('1A213', 'เยี่ยมหญิงหลังคลอด ครั้งที่ 2 (4-6 สัปดาห์) ที่ไม่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A214', 'เยี่ยมหญิงหลังคลอด ครั้งที่ 2 (4-6 สัปดาห์)  ที่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A215', 'เยี่ยมหญิงหลังคลอด ครั้งที่ 2 (4-6 สัปดาห์)  ไม่ระบุรายละเอียด ');
            INSERT INTO `nu_community_service` VALUES ('1A216', 'เยี่ยมหญิงหลังคลอด ครั้งอื่น  ที่ไม่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A217', 'เยี่ยมหญิงหลังคลอด ครั้งอื่น  ที่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A218', 'เยี่ยมหญิงหลังคลอด ครั้งอื่น  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A219', 'เยี่ยมหญิงหลังคลอด  ไม่ระบุรายละเอียด ');
            INSERT INTO `nu_community_service` VALUES ('1A220', 'เยี่ยมทารกแรกเกิด ครั้งที่ 1 (1-2 สัปดาห์)  ที่ไม่มีภาวะผิดปกติ  ');
            INSERT INTO `nu_community_service` VALUES ('1A221', 'เยี่ยมทารกแรกเกิด ครั้งที่ 1 (1-2 สัปดาห์)  ที่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A222', 'เยี่ยมทารกแรกเกิด ครั้งที่ 1 (1-2 สัปดาห์)  ไม่ระบุรายละเอียด ');
            INSERT INTO `nu_community_service` VALUES ('1A223', 'เยี่ยมทารกแรกเกิด ครั้งที่ 2 (4-6 สัปดาห์)');
            INSERT INTO `nu_community_service` VALUES ('1A224', 'เยี่ยมทารกแรกเกิด ครั้งที่ 2 (4-6 สัปดาห์)  ที่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A225', 'เยี่ยมทารกแรกเกิด ครั้งที่ 2 (4-6 สัปดาห์)  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A226', 'เยี่ยมทารกแรกเกิด ครั้งอื่น  ที่ไม่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A227', 'เยี่ยมทารกแรกเกิด ครั้งอื่น  ที่มีภาวะผิดปกติ');
            INSERT INTO `nu_community_service` VALUES ('1A228', 'เยี่ยมทารกแรกเกิด ครั้งอื่น  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A229', 'เยี่ยมทารกแรกเกิด ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A30', 'เยี่ยมผู้พิการทางการมองเห็น');
            INSERT INTO `nu_community_service` VALUES ('1A31', 'เยี่ยมผู้พิการทางการได้ยินหรือสื่อความหมาย');
            INSERT INTO `nu_community_service` VALUES ('1A32', 'เยี่ยมผู้พิการทางการเคลื่อนไหวหรือทางร่างกาย');
            INSERT INTO `nu_community_service` VALUES ('1A33', 'เยี่ยมผู้พิการทางจิตใจหรือพฤติกรรม หรือออทิสติก');
            INSERT INTO `nu_community_service` VALUES ('1A34', 'เยี่ยมผู้พิการทางสติปัญญา');
            INSERT INTO `nu_community_service` VALUES ('1A35', 'เยี่ยมผู้พิการทางการเรียนรู้');
            INSERT INTO `nu_community_service` VALUES ('1A39', 'เยี่ยมผู้ที่ความพิการยังไม่ได้รับการวินิจฉัยยืนยัน');
            INSERT INTO `nu_community_service` VALUES ('1A400', 'เยี่ยมเด็กอายุ 0 ? 5 ปี ขาดอาหาร ');
            INSERT INTO `nu_community_service` VALUES ('1A401', 'เยี่ยมเด็กอายุ 0 ? 5 ปี  อ้วน  ');
            INSERT INTO `nu_community_service` VALUES ('1A402', 'เยี่ยมเด็กอายุ 0 ? 5 ปี กลุ่มเสี่ยง(ค่อนข้างเตี้ย ค่อนข้างผอม น้ำหนักค่อนข้างน้อย ท้วม)');
            INSERT INTO `nu_community_service` VALUES ('1A403', 'เยี่ยมเด็กอายุ 0 ? 5 ปี ที่มีการเจริญเติบโตดีแต่แนวโน้มการเจริญเติบโตไม่ดี');
            INSERT INTO `nu_community_service` VALUES ('1A404', 'เยี่ยมเด็กอายุ 0 ? 5 ปี เพื่อติดตามพัฒนาการเด็กที่บกพร่อง / พัฒนาการไม่สมวัย');
            INSERT INTO `nu_community_service` VALUES ('1A405', 'เยี่ยมเด็กอายุ 0 ? 5 ปี เพื่อติดตามเด็กที่มีโรคประจำตัว/ โรคร้ายแรง/ โรคที่ต้องเฝ้าระวัง');
            INSERT INTO `nu_community_service` VALUES ('1A406', 'เยี่ยมเด็กอายุ 0 ? 5 ปี เพื่อติดตามเด็กให้ได้รับวัคซีนครบตามเกณฑ์/ เด็กขาดการรับวัคซีนตามนัด');
            INSERT INTO `nu_community_service` VALUES ('1A407', 'เยี่ยมเด็กอายุ 0 ? 5 ปี เพื่อแนะนำผู้ปกครอง เรื่อง การแปรงฟันที่ถูกต้อง ด้วยยาสีฟันผสมฟลูออไรด์');
            INSERT INTO `nu_community_service` VALUES ('1A408', 'เยี่ยมเด็กอายุ 0 ? 5 ปี กิจกรรมการให้บริการอื่น');
            INSERT INTO `nu_community_service` VALUES ('1A409', 'เยี่ยมเด็กอายุ 0 ? 5 ปี  ไม่ระบุกิจกรรม');
            INSERT INTO `nu_community_service` VALUES ('1A410', 'เยี่ยมเด็กอายุ 6 - 18 ปี ขาดอาหาร');
            INSERT INTO `nu_community_service` VALUES ('1A411', 'เยี่ยมเด็กอายุ 6 - 18 ปี อ้วน  ');
            INSERT INTO `nu_community_service` VALUES ('1A412', 'เยี่ยมเด็กอายุ 6 - 18 ปี อยู่ในกลุ่มเสี่ยง (ค่อนข้างเตี้ย ค่อนข้างผอม น้ำหนักค่อนข้างน้อย ท้วม)');
            INSERT INTO `nu_community_service` VALUES ('1A413', 'เยี่ยมเด็กอายุ 6 - 18 ปี ที่มีการเจริญเติบโตดีแต่แนวโน้มการเจริญเติบโตไม่ดี');
            INSERT INTO `nu_community_service` VALUES ('1A418', 'เยี่ยมเด็กอายุ 6 - 18 ปี กลุ่มอื่น');
            INSERT INTO `nu_community_service` VALUES ('1A419', 'เยี่ยมเด็กอายุ 6 ? 18 ปี  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A420', 'เยี่ยมกลุ่มวัยแรงงานเพื่อติดตามภาวะเสี่ยงในการทำงาน ด้านการเกษตร  ');
            INSERT INTO `nu_community_service` VALUES ('1A421', 'เยี่ยมกลุ่มวัยแรงงานเพื่อติดตามภาวะเสี่ยงในการทำงาน ในโรงงานอุตสาหกรรม');
            INSERT INTO `nu_community_service` VALUES ('1A422', 'เยี่ยมกลุ่มวัยแรงงานเพื่อติดตามภาวะเสี่ยงในการทำงานด้านอุตสาหกรรมในครัวเรือน');
            INSERT INTO `nu_community_service` VALUES ('1A428', 'เยี่ยมกลุ่มวัยแรงงานเพื่อติดตามภาวะเสี่ยงในการทำงานด้านอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1A429', 'เยี่ยมกลุ่มวัยแรงงาน  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A430', 'เยี่ยมผู้สูงอายุที่อยู่เพียงลำพัง');
            INSERT INTO `nu_community_service` VALUES ('1A431', 'เยี่ยมผู้สูงอายุที่ไม่อยู่เพียงลำพัง');
            INSERT INTO `nu_community_service` VALUES ('1A439', 'เยี่ยมผู้สูงอายุ  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A50', 'เยี่ยมผู้ประสบภัยพิบัติทางธรรมชาติ');
            INSERT INTO `nu_community_service` VALUES ('1A51', 'เยี่ยมผู้ประสบภัยพิบัติที่เกิดจากไฟ');
            INSERT INTO `nu_community_service` VALUES ('1A52', 'เยี่ยมผู้ประสบภัยพิบัติทางสงคราม');
            INSERT INTO `nu_community_service` VALUES ('1A53', 'เยี่ยมและเยียวยาผู้ประสบภัยพิบัติจากการเข้าแทรกแซงตามกฎหมาย');
            INSERT INTO `nu_community_service` VALUES ('1A54', 'เยี่ยมและเยียวยาผู้ประสบภัยพิบัติจากการก่อการร้าย/จลาจล');
            INSERT INTO `nu_community_service` VALUES ('1A58', 'เยี่ยมและเยียวยาผู้ประสบภัยพิบัติอื่น ๆ  ');
            INSERT INTO `nu_community_service` VALUES ('1A59', 'เยี่ยมและเยียวยาผู้ประสบภัยพิบัติที่ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1A90', 'เยี่ยมบ้านประชาชนสุขภาพดีเพื่อกิจกรรมการให้บริการเฉพาะเรื่อง');
            INSERT INTO `nu_community_service` VALUES ('1A99', 'เยี่ยมบ้านประชาชนสุขภาพดีทั่วไป');
            INSERT INTO `nu_community_service` VALUES ('1B000', 'การตรวจคัดกรองความเสี่ยง / โรคเบาหวาน');
            INSERT INTO `nu_community_service` VALUES ('1B001', 'การตรวจคัดกรองความเสี่ยง / โรคความดันโลหิตสูง');
            INSERT INTO `nu_community_service` VALUES ('1B002', 'การตรวจคัดกรองความเสี่ยง / โรคหัวใจและหลอดเลือด');
            INSERT INTO `nu_community_service` VALUES ('1B003', 'การตรวจคัดกรองความเสี่ยง / โรคมะเร็งเต้านม ');
            INSERT INTO `nu_community_service` VALUES ('1B004', 'การตรวจคัดกรองความเสี่ยง / โรคมะเร็งปากมดลูก  ');
            INSERT INTO `nu_community_service` VALUES ('1B005', 'การตรวจคัดกรองความเสี่ยง / โรคธาลาสซีเมีย');
            INSERT INTO `nu_community_service` VALUES ('1B008', 'การตรวจคัดกรองความเสี่ยง / โรคเรื้อรัง อื่นๆ');
            INSERT INTO `nu_community_service` VALUES ('1B009', 'การตรวจคัดกรองความเสี่ยง ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1B01', 'การตรวจคัดกรองความเสี่ยง / โรคติดต่อ');
            INSERT INTO `nu_community_service` VALUES ('1B020', 'การตรวจคัดกรองโรคจิต');
            INSERT INTO `nu_community_service` VALUES ('1B021', 'การตรวจคัดกรองโรคซึมเศร้า');
            INSERT INTO `nu_community_service` VALUES ('1B022', 'การตรวจคัดกรองโรคออทิสติก ในเด็กอายุ 0 ? 6 ปี ');
            INSERT INTO `nu_community_service` VALUES ('1B023', 'การตรวจคัดกรองภาวะเครียด ');
            INSERT INTO `nu_community_service` VALUES ('1B024', 'ดัชนีชี้วัดสุขภาพจิตคนไทย');
            INSERT INTO `nu_community_service` VALUES ('1B025', 'ดัชนีชี้วัดความสุขคนไทย');
            INSERT INTO `nu_community_service` VALUES ('1B028', 'การตรวจคัดกรองความเสี่ยง / โรคทางจิตเวช อื่น ๆ  ');
            INSERT INTO `nu_community_service` VALUES ('1B029', 'การตรวจคัดกรองความเสี่ยง  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1B100', 'การตรวจคัดกรองเพื่อค้นหาเด็กพิการทางกายและทางจิต ');
            INSERT INTO `nu_community_service` VALUES ('1B101', 'การตรวจคัดกรองเพื่อค้นหาเด็กพัฒนาการช้า');
            INSERT INTO `nu_community_service` VALUES ('1B102', 'การตรวจคัดกรองเพื่อค้นหาเด็กกระดูกสันหลังคด');
            INSERT INTO `nu_community_service` VALUES ('1B103', 'การตรวจคัดกรองเพื่อค้นหาเด็กอ้วนที่มีกิจกรรมทางกายต่ำ');
            INSERT INTO `nu_community_service` VALUES ('1B108', 'การตรวจคัดกรองความเสี่ยง / เฝ้าระวัง ในเด็ก อื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1B109', 'การตรวจคัดกรองความเสี่ยง / เฝ้าระวัง ในเด็ก  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1B110', 'การตรวจคัดกรองเพื่อค้นหาผู้ที่อาจมีภาวะเสี่ยงต่อการบาดเจ็บจากการทำงาน');
            INSERT INTO `nu_community_service` VALUES ('1B111', 'การตรวจคัดกรองเพื่อค้นหาคนทำงานที่มีกิจกรรมทางกายต่ำ');
            INSERT INTO `nu_community_service` VALUES ('1B112', 'การตรวจคัดกรองเพื่อติดตามโรคทางจิต');
            INSERT INTO `nu_community_service` VALUES ('1B129', 'การตรวจคัดกรองความเสี่ยง / เฝ้าระวังในผู้สูงอายุ  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1C00', 'การปรับเปลี่ยนพฤติกรรมเพื่อการเลิกสุรา');
            INSERT INTO `nu_community_service` VALUES ('1C01', 'การปรับเปลี่ยนพฤติกรรมเพื่อการเลิกบุหรี่');
            INSERT INTO `nu_community_service` VALUES ('1C02', 'การปรับเปลี่ยนพฤติกรรมเพื่อการเลิกยาเสพติด');
            INSERT INTO `nu_community_service` VALUES ('1C10', 'การฝึกทักษะการออกกำลังกาย');
            INSERT INTO `nu_community_service` VALUES ('1C11', 'การฝึกทักษะการออกกำลังกายเพื่อการฟื้นฟูสภาพ');
            INSERT INTO `nu_community_service` VALUES ('1C20', 'การติดตามพฤติกรรมเสี่ยงในการบริโภคของกลุ่มวัยแรงงาน');
            INSERT INTO `nu_community_service` VALUES ('1C3', 'การปรับเปลี่ยนพฤติกรรมความเสี่ยงโรคความดันโลหิตสูง');
            INSERT INTO `nu_community_service` VALUES ('1C4', 'การปรับเปลี่ยนพฤติกรรมความเสี่ยงโรคเบาหวาน');
            INSERT INTO `nu_community_service` VALUES ('1D00', 'ทาฟลูออไรด์ในเด็กอายุ 0-2 ปี');
            INSERT INTO `nu_community_service` VALUES ('1D01', 'แจกแปรงสีฟันในเด็กอายุ 18 เดือน');
            INSERT INTO `nu_community_service` VALUES ('1D02', 'ให้ทันตสุขศึกษาหญิงตั้งครรภ์');
            INSERT INTO `nu_community_service` VALUES ('1D03', 'สอน/แนะนำ ให้ผู้ดูแลหรือผู้พิการ แปรงฟัน ถูกวิธี ตามสภาพของตัวผู้พิการด้วยยาสีฟันผสมฟลูออไรด์');
            INSERT INTO `nu_community_service` VALUES ('1D04', 'สอน/แนะนำ ให้ผู้ดูแลหรือผู้สูงอายุ แปรงฟัน ถูกวิธี ตามสภาพของตัวผู้สูงอายุด้วยยาสีฟันผสมฟลูออไรด์ ');
            INSERT INTO `nu_community_service` VALUES ('1D05', 'ฝึกแปรงฟันด้วยยาสีฟันผสมฟลูออไรด์โดยผู้ปกครองแปรงให้เด็กเป็นรายคน ');
            INSERT INTO `nu_community_service` VALUES ('1D08', 'การให้บริการทันตสาธารณสุขอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1D09', 'การให้บริการทันตสาธารณสุข  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1D10', 'ตรวจรอยโรคฟันผุในเด็กอายุ 3-5 ปี ');
            INSERT INTO `nu_community_service` VALUES ('1D11', 'ตรวจความสะอาดช่องปากในเด็กอายุ 3-5 ปี');
            INSERT INTO `nu_community_service` VALUES ('1D12', 'ตรวจรอยโรคฟันผุหญิงตั้งครรภ์');
            INSERT INTO `nu_community_service` VALUES ('1D13', 'ตรวจสภาพเหงือกหญิงตั้งครรภ์');
            INSERT INTO `nu_community_service` VALUES ('1D18', 'ตรวจสุขภาพช่องปากอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1D19', 'ตรวจสุขภาพช่องปาก  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1D20', 'การตรวจ และคัดกรองรอยโรคก่อมะเร็งในช่องปาก');
            INSERT INTO `nu_community_service` VALUES ('1D21', 'การตรวจรอยโรคมะเร็งในช่องปาก');
            INSERT INTO `nu_community_service` VALUES ('1D28', 'การตรวจ และคัดกรองมะเร็งช่องปากอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1E00', 'การเฝ้าระวังโภชนาการในหญิงตั้งครรภ์');
            INSERT INTO `nu_community_service` VALUES ('1E01', 'การประเมินสารไอโอดีนในหญิงตั้งครรภ์ ');
            INSERT INTO `nu_community_service` VALUES ('1E10', 'การเฝ้าระวังการเจริญเติบโตของเด็กในกลุ่มอายุ 0-5 ปี');
            INSERT INTO `nu_community_service` VALUES ('1E11', 'การตรวจคัดกรองภาวะอ้วนในประชาชนอายุ 15 ปีขึ้นไป โดยการวัดเส้นรอบเอว หรือประเมินค่าดัชนีมวลกาย');
            INSERT INTO `nu_community_service` VALUES ('1E12', 'การตรวจคัดกรองภาวะอ้วนในประชาชนอายุ 15 ปีขึ้นไป ที่มีภาวะอ้วนลงพุง (โดยการวัดเส้นรอบเอว)');
            INSERT INTO `nu_community_service` VALUES ('1E13', 'การตรวจคัดกรองภาวะอ้วนในประชาชนอายุ 15 ปีขึ้นไป ที่มีภาวะอ้วน (ประเมินค่าดัชนีมวลกาย)');
            INSERT INTO `nu_community_service` VALUES ('1E18', 'กิจกรรมโภชนาการเฉพาะเรื่อง / เฉพาะกลุ่มอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1F00', 'การให้บริการปรึกษาทางด้านสุขภาพจิตทางโทรศัพท์');
            INSERT INTO `nu_community_service` VALUES ('1F08', 'การให้บริการปรึกษาทางด้านจิตเวชอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1F09', 'การให้บริการปรึกษาทางด้านจิตเวช  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1F10', 'การให้บริการปรึกษา/ให้ความรู้ ผู้ที่ติดสุราเพื่อลด/เลิกสุรา');
            INSERT INTO `nu_community_service` VALUES ('1F11', 'การให้บริการปรึกษา/ให้ความรู้ ผู้ที่ติดบุหรี่เพื่อลด/เลิกบุหรี่');
            INSERT INTO `nu_community_service` VALUES ('1F12', 'การให้บริการปรึกษา/ให้ความรู้ ผู้ที่ติดยาเสพติดเพื่อลด/เลิกยาเสพติด');
            INSERT INTO `nu_community_service` VALUES ('1F18', 'การให้บริการปรึกษา/ให้ความรู้ ทางด้านสารเสพติดอื่นๆ');
            INSERT INTO `nu_community_service` VALUES ('1F19', 'การให้บริการปรึกษา/ให้ความรู้ ทางด้านสารเสพติด  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1F20', 'การให้บริการปรึกษา/ให้ความรู้ เรื่องเพศสัมพันธ์');
            INSERT INTO `nu_community_service` VALUES ('1F21', 'การให้บริการปรึกษาเรื่องปัญหาครอบครัว');
            INSERT INTO `nu_community_service` VALUES ('1F28', 'การให้บริการปรึกษาในวัยรุ่นเรื่องสุขภาพอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1F29', 'การให้บริการปรึกษาในวัยรุ่น  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1G00', 'การให้บริการกิจกรรมกายภาพบำบัด');
            INSERT INTO `nu_community_service` VALUES ('1G01', 'การให้บริการผู้ป่วยร่วมกับหน่วยงานอื่น / สหวิชาชีพ');
            INSERT INTO `nu_community_service` VALUES ('1G08', 'การให้บริการอื่นที่ระบุรายละเอียดแก่ผู้ป่วยในชุมชน');
            INSERT INTO `nu_community_service` VALUES ('1G09', 'การให้บริการผู้ป่วยในชุมชน  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1G10', 'การให้คำแนะนำญาติที่ดูแลผู้ป่วยใส่สายให้อาหาร (NG tube)');
            INSERT INTO `nu_community_service` VALUES ('1G11', 'การให้คำแนะนำญาติที่ดูแลผู้ป่วยใส่ท่อหลอดลม คอ และการดูดเสมหะ');
            INSERT INTO `nu_community_service` VALUES ('1G12', 'การให้คำแนะนำญาติที่ดูแลผู้ป่วยใส่สายสวนปัสสาวะ');
            INSERT INTO `nu_community_service` VALUES ('1G13', 'การให้คำแนะนำญาติที่ดูแลผู้ป่วยที่มียาฉีด เช่น อินซูลิน ฯลฯ');
            INSERT INTO `nu_community_service` VALUES ('1G14', 'การให้คำแนะนำญาติที่ดูแลผู้ป่วยที่มีบาดแผล');
            INSERT INTO `nu_community_service` VALUES ('1G18', 'การให้คำแนะนำญาติที่ดูแลผู้ป่วยอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1G19', 'การให้คำแนะนำญาติที่ดูแลผู้ป่วย  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1H000', 'ตรวจรอยโรคฟันผุในนักเรียนชั้นประถมศึกษาปีที่ 1 (อายุ 6-7 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H001', 'ตรวจรอยโรคฟันผุในนักเรียนชั้นประถมศึกษาปีที่ 3 (อายุ 7-8 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H010', 'การให้บริการ Need for Sealant ในนักเรียนชั้นประถมศึกษาปีที่ 1 (อายุ 6-7 ปี) ');
            INSERT INTO `nu_community_service` VALUES ('1H020', 'การให้บริการ Need for E-application ในนักเรียนชั้นประถมศึกษาปีที่ 1 (อายุ 6-7 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H030', 'ตรวจการยึดติดไม่สมบูรณ์ของสารเคลือบหลุมร่องฟัน ในนักเรียนชั้นประถมศึกษา (อายุ 6-12 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H040', 'ตรวจเหงือกตามระบบเฝ้าระวังทันตสุขภาพ ในนักเรียนชั้นประถมศึกษา (อายุ 6-12 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H041', 'ตรวจเหงือกตามระบบเฝ้าระวังทันตสุขภาพ ในนักเรียนชั้นมัธยมศึกษา (อายุ 13-18 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H050', 'ตรวจฟันผุตามระบบเฝ้าระวังทันตสุขภาพ ในนักเรียนชั้นประถมศึกษา (อายุ 6-12 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H051', 'ตรวจฟันผุตามระบบเฝ้าระวังทันตสุขภาพ ในนักเรียนชั้นมัธยมศึกษา (อายุ 13-18 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H060', 'ตรวจฟันตกกระตามระบบเฝ้าระวังทันตสุขภาพ  ในนักเรียนชั้นประถมศึกษา (อายุ 6-12 ปี) ');
            INSERT INTO `nu_community_service` VALUES ('1H061', 'ตรวจฟันตกกระตามระบบเฝ้าระวังทันตสุขภาพ  ในนักเรียนชั้นมัธยมศึกษา (อายุ 13-18 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H070', 'ตรวจสุขภาพช่องปากตามเกณฑ์โรงเรียนส่งเสริมสุขภาพในนักเรียนชั้นประถมศึกษา (อายุ 6-12 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H071', 'ตรวจสุขภาพช่องปากตามเกณฑ์โรงเรียนส่งเสริมสุขภาพในนักเรียนชั้นมัธยมศึกษา (อายุ 13-18 ปี)');
            INSERT INTO `nu_community_service` VALUES ('1H08', 'การให้บริการสุขภาพช่องปากอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1H10', 'ติดตามภาวะทางจิตในกลุ่มวัยเรียนอายุ 6 - 18 ปี และเด็กวัยรุ่น');
            INSERT INTO `nu_community_service` VALUES ('1H18', 'การให้บริการทางด้านจิตเวชอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1H19', 'การให้บริการด้านจิตเวช  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1H200', 'ตรวจหูในนักเรียนชั้นประถมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H201', 'ตรวจหูในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H202', 'แก้ไขโรคของหูในนักเรียนชั้นประถมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H203', 'แก้ไขโรคของหูในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H204', 'ตรวจการได้ยินในนักเรียนชั้นประถมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H205', 'ตรวจการได้ยินในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H206', 'แก้ไขอาการผิดปกติของการได้ยินในนักเรียนชั้นประถมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H207', 'แก้ไขอาการผิดปกติของการได้ยินในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H2080', 'การตรวจคัดกรองการได้ยิน ปกติทั้ง 2 ข้าง');
            INSERT INTO `nu_community_service` VALUES ('1H2081', 'การตรวจคัดกรองการได้ยินผิดปกติทั้ง 2 ข้างหรือข้างใดข้างหนึ่ง ได้รับการรักษา');
            INSERT INTO `nu_community_service` VALUES ('1H2082', 'การตรวจคัดกรองการได้ยินผิดปกติทั้ง 2 ข้างหรือข้างใดข้างหนึ่ง ได้รับการส่งต่อ');
            INSERT INTO `nu_community_service` VALUES ('1H2083', 'การตรวจคัดกรองการได้ยินผิดปกติทั้ง 2 ข้างหรือข้างใดข้างหนึ่ง ไม่ได้ส่งต่อและรักษา');
            INSERT INTO `nu_community_service` VALUES ('1H210', 'ตรวจตาในนักเรียนชั้นประถมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H211', 'ตรวจตาในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H212', 'แก้ไขโรคตาในนักเรียนชั้นประถมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H213', 'แก้ไขโรคตาในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H214', 'ตรวจสายตาในนักเรียนชั้นประถมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H215', 'ตรวจสายตาในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H216', 'แก้ไขอาการสายตาผิดปกติในนักเรียนชั้นประถมศึกษา ');
            INSERT INTO `nu_community_service` VALUES ('1H217', 'แก้ไขอาการสายตาผิดปกติในนักเรียนชั้นมัธยมศึกษา');
            INSERT INTO `nu_community_service` VALUES ('1H2180', 'การตรวจคัดกรองสายตา ปกติทั้ง 2 ข้าง');
            INSERT INTO `nu_community_service` VALUES ('1H2181', 'การตรวจคัดกรองสายตา ผิดปกติทั้ง 2 ข้างหรือข้างใดข้างหนึ่ง (VA<20/40) ได้รับการรักษา');
            INSERT INTO `nu_community_service` VALUES ('1H2182', 'การตรวจคัดกรองสายตา ผิดปกติทั้ง 2 ข้างหรือข้างใดข้างหนึ่ง (VA<20/40) ได้รับการส่งต่อ');
            INSERT INTO `nu_community_service` VALUES ('1H2183', 'การตรวจคัดกรองสายตา ผิดปกติทั้ง 2 ข้างหรือข้างใดข้างหนึ่ง (VA<20/40) ไม่ได้ส่งต่อและรักษา');
            INSERT INTO `nu_community_service` VALUES ('1H280', 'นักเรียนที่ได้รับยาถ่ายพยาธิ');
            INSERT INTO `nu_community_service` VALUES ('1H281', 'นักเรียนที่ได้รับการตรวจเหาและได้รับการแก้ไข');
            INSERT INTO `nu_community_service` VALUES ('1H288', 'นักเรียนที่ได้รับการตรวจสุขภาพประจำปีอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1H300', 'นักเรียนได้รับการเฝ้าระวังการเจริญเติบโต');
            INSERT INTO `nu_community_service` VALUES ('1H301', 'นักเรียนได้รับการตรวจภาวะโลหิตจาง');
            INSERT INTO `nu_community_service` VALUES ('1H3010', 'ตรวจคัดกรองระดับความเข้มข้นของเม็ดเลือดแดง (HB) หรือปริมาณเม็ดเลือดแดงอัดแน่น (HCT) พบปกติ ');
            INSERT INTO `nu_community_service` VALUES ('1H3011', 'ตรวจคัดกรองระดับความเข้มข้นของเม็ดเลือดแดง (HB) หรือปริมาณเม็ดเลือดแดงอัดแน่น (HCT) พบผิดปกติ และได้ยาเสริมธาตุเหล็กเพื่อรักษา');
            INSERT INTO `nu_community_service` VALUES ('1H3012', 'ติดตามผลการตรวจคัดกรองระดับความเข้มข้นของเม็ดเลือดแดง (HB) หรือปริมาณเม็ดเลือดแดงอัดแน่น (HCT) หลังรับประทานยา 1 เดือน ผลปกติ');
            INSERT INTO `nu_community_service` VALUES ('1H3013', 'ติดตามผลการตรวจคัดกรองระดับความเข้มข้นของเม็ดเลือดแดง (HB) หรือปริมาณเม็ดเลือดแดงอัดแน่น (HCT) หลังรับประทานยา 1 เดือน ผลผิดปกติและส่งต่อ');
            INSERT INTO `nu_community_service` VALUES ('1H302', 'นักเรียนได้รับการตรวจคอพอก');
            INSERT INTO `nu_community_service` VALUES ('1H3030', 'นักเรียนได้รับการตรวจคัดกรองเด็กอ้วนกลุ่มเสี่ยง Obesity Sign ไม่พบ Obesity Sign');
            INSERT INTO `nu_community_service` VALUES ('1H3031', 'นักเรียนได้รับการตรวจคัดกรองเด็กอ้วนกลุ่มเสี่ยง พบ Obesity Sign 3 ใน 4 ข้อ ส่งต่อรักษา');
            INSERT INTO `nu_community_service` VALUES ('1H3032', 'นักเรียนได้รับการตรวจคัดกรองเด็กอ้วนกลุ่มเสี่ยง พบ Obesity Sign 3 ใน 4 ข้อ ไม่ได้ส่งต่อรักษา');
            INSERT INTO `nu_community_service` VALUES ('1H308', 'นักเรียนได้รับการเฝ้าระวังการเจริญเติบโตอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1I00', 'ผู้ป่วยได้รับการนวดเพื่อการรักษาที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I01', 'การบริการนวดเพื่อการส่งเสริมสุขภาพที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I02', 'ผู้ป่วยได้รับการประคบสมุนไพรเพื่อการรักษาที่บ้าน ');
            INSERT INTO `nu_community_service` VALUES ('1I020', 'การบริการประคบสมุนไพรเพื่อการส่งเสริมสุขภาพที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I03', 'ผู้ป่วยได้รับการอบสมุนไพรเพื่อการรักษาที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I04', 'การบริการอบสมุนไพรเพื่อการส่งเสริมสุขภาพที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I05', 'การบริการหญิงหลังคลอดด้วยการอบสมุนไพรที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I050', 'การบริการหญิงหลังคลอดด้วยการอาบสมุนไพรที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I051', 'การบริการหญิงหลังคลอดด้วยการประคบสมุนไพรที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I052', 'การบริการหญิงหลังคลอดด้วยการนวดที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I053', 'การบริการหญิงหลังคลอดด้วยการนวดเต้านมที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I058', 'การบริการหญิงหลังคลอดด้วยวิธีอื่น ที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I06', 'การบริการหญิงหลังคลอดด้วยการทับหม้อเกลือที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I060', 'การบริการหญิงหลังคลอดด้วยการนั่งถ่านที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I07', 'การให้คำแนะนำ การสอน สาธิตด้านการแพทย์แผนไทย');
            INSERT INTO `nu_community_service` VALUES ('1I070', 'การให้คำแนะนำ การสอน สาธิตการบริหารร่างกายด้วยมณีเวชที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I071', 'การให้คำแนะนำ หญิงหลังคลอด และการบริบาลทารกด้านการแพทย์แผนไทยที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I08', 'การให้บริการการแพทย์แผนไทยอื่นๆ ที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I080', 'การให้บริการพอกยาสมุนไพร ที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I081', 'การให้บริการแช่ยาสมุนไพร ที่บ้าน');
            INSERT INTO `nu_community_service` VALUES ('1I100', 'การให้บริการกดจุดบำบัด (Acupressure)');
            INSERT INTO `nu_community_service` VALUES ('1I101', 'การให้บริการนวดปรับสมดุลร่างกาย');
            INSERT INTO `nu_community_service` VALUES ('1I102', 'การให้บริการสมาธิบำบัด');
            INSERT INTO `nu_community_service` VALUES ('1I103', 'การให้บริการนวดสวีดิช (Swedish Massage)');
            INSERT INTO `nu_community_service` VALUES ('1I104', 'การให้บริการนวดเพื่อสุขภาพแบบเนิฟว์แอสซิสต์ (Nerve Assist)');
            INSERT INTO `nu_community_service` VALUES ('1I105', 'การให้บริการกดจุดสะท้อนเท้า (Foot Reflexology)');
            INSERT INTO `nu_community_service` VALUES ('1I110', 'การให้บริการเกอร์สันบำบัด (Gerson Therapy)');
            INSERT INTO `nu_community_service` VALUES ('1I111', 'การให้บริการคีโตเจนิคไดเอต (Ketogenic Diet) /อาหารพร่องแป้ง (Low-Carbohydrate Diet)');
            INSERT INTO `nu_community_service` VALUES ('1I112', 'การให้บริการแมคโครไบโอติกส์ (Macrobiotics)');
            INSERT INTO `nu_community_service` VALUES ('1I113', 'การให้บริการอาหารปรับสมดุลฤทธิ์ ร้อน ? เย็น');
            INSERT INTO `nu_community_service` VALUES ('1I180', 'การให้บริการจินตภาพบำบัด (Visualization Therapy)');
            INSERT INTO `nu_community_service` VALUES ('1I181', 'การให้สมาธิบำบัด/พลังบำบัด');
            INSERT INTO `nu_community_service` VALUES ('1I182', 'การให้บริการกัวซา (Guasa)');
            INSERT INTO `nu_community_service` VALUES ('1I183', 'การให้บริการการแพทย์ทางเลือกวิถีธรรม');
            INSERT INTO `nu_community_service` VALUES ('1J00', 'ให้ความรู้/ สุขศึกษาเกี่ยวกับโรคและการป้องกันโรคต่าง ๆ');
            INSERT INTO `nu_community_service` VALUES ('1J01', 'ให้ความรู้/ สุขศึกษาเกี่ยวกับโรคตามฤดูกาล');
            INSERT INTO `nu_community_service` VALUES ('1J02', 'แนะนำ / ให้ความรู้ เรื่องการใช้ยา');
            INSERT INTO `nu_community_service` VALUES ('1J03', 'ให้ความรู้และจัดกิจกรรมการออกกำลังกายที่ถูกต้องและเหมาะสม');
            INSERT INTO `nu_community_service` VALUES ('1J04', 'ให้สุขศึกษาในแหล่งแพร่กามโรค');
            INSERT INTO `nu_community_service` VALUES ('1J05', 'ให้ความรู้ด้านโภชนาการ');
            INSERT INTO `nu_community_service` VALUES ('1J08', 'ให้ความรู้/ สุขศึกษาเกี่ยวกับสุขภาพอื่น ๆ  ');
            INSERT INTO `nu_community_service` VALUES ('1J09', 'การเผยแพร่ความรู้/ให้สุขศึกษาแก่กลุ่มบุคคลทั่วไป  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1J10', 'ให้ความรู้/ สุขศึกษาแก่หญิงขายบริการ');
            INSERT INTO `nu_community_service` VALUES ('1J11', 'ให้ความรู้เกี่ยวกับการดูแลเท้าในผู้ป่วยเบาหวาน');
            INSERT INTO `nu_community_service` VALUES ('1J18', 'ให้ความรู้/ สุขศึกษาบุคคลเฉพาะกลุ่มอื่น ๆ');
            INSERT INTO `nu_community_service` VALUES ('1J19', 'การเผยแพร่ความรู้/ให้สุขศึกษาแก่บุคคลเฉพาะกลุ่ม  ไม่ระบุรายละเอียด');
            INSERT INTO `nu_community_service` VALUES ('1J20', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับผู้ป่วยโรคเรื้อรัง');
            INSERT INTO `nu_community_service` VALUES ('1J21', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับผู้ป่วยที่มีปัญหาทางระบบทางเดินหายใจ เช่น ปอดอุดกั้นเรื้อรัง หอบหืด');
            INSERT INTO `nu_community_service` VALUES ('1J22', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับผู้ป่วยที่มีปัญหาทางระบบหัวใจหลอดเลือด');
            INSERT INTO `nu_community_service` VALUES ('1J23', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับเด็กอ้วนที่มีกิจกรรมทางกายต่ำ');
            INSERT INTO `nu_community_service` VALUES ('1J24', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับหญิงตั้งครรภ์และหลังคลอด');
            INSERT INTO `nu_community_service` VALUES ('1J25', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับประชากรกลุ่มเสี่ยงต่อการบาดเจ็บจากการทำงาน');
            INSERT INTO `nu_community_service` VALUES ('1J26', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับกลุ่มคนทำงานที่มีกิจกรรมทางกายต่ำ');
            INSERT INTO `nu_community_service` VALUES ('1J27', 'ให้ความรู้และจัดกิจกรรมออกกำลังกายที่เหมาะสมสำหรับผู้สูงอายุที่เสี่ยงต่อการหกล้ม');
            INSERT INTO `nu_community_service` VALUES ('1J28', 'ให้ความรู้บุคคลทั่วไปที่มีสุขภาพดีเกี่ยวกับท่าทางการทำงานและท่าทางในชีวิตประจำวัน');


            ALTER TABLE hosxp_pcu.ovst_community_service_type
            MODIFY COLUMN ovst_community_service_type_id int(11) NOT NULL AUTO_INCREMENT FIRST;

            INSERT into ovst_community_service_type (ovst_community_service_type_name,ovst_community_service_type_code)
            SELECT name,code FROM nu_community_service WHERE `code` not in (SELECT ovst_community_service_type_code FROM ovst_community_service_type);"""


            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qovst_com, multi=True):
            pass
        conn.commit()
        cursor.close()
        conn.close()
        time.sleep(2)    
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)

# เพิ่มข้อมูลแฟ้ม comactivity กิจกรรมในชุมชน ตามมาตรฐาน 43 แฟ้ม ปี 63
    def ser7():
        db_config = read_db_config()

        qvil_com ="""INSERT IGNORE INTO provis_comactivity  VALUES
            ('2A00','เก็บตัวอย่าง/ตรวจสารปนเปื้อนในอาหาร ผัก และผลไม้ทุกชนิด',null,null),
            ('2A01','ตรวจร้านค้าของชำ',null,null),
            ('2A02','ตรวจให้คำแนะนำสถานที่ผลิตอาหาร ',null,null),
            ('2A03','ตรวจสถานที่จำหน่ายบุหรี่/แอลกอฮอล์ ',null,null),
            ('2A04','ตรวจร้านก๋วยเตี๋ยว/หม้อก๋วยเตี๋ยว',null,null),
            ('2A08','กิจกรรมการให้บริการชุมชนด้านการคุ้มครองผู้บริโภคอื่น ๆ',null,null),
            ('2A09 ','กิจกรรมการให้บริการชุมชนด้านการคุ้มครองผู้บริโภค   ไม่ระบุรายละเอียด',null,null),
            ('2B00','การกำจัดน้ำเสีย/ขยะ/มูลสัตว์',null,null),
            ('2B01','ตรวจโรงฆ่าสัตว์ ',null,null),
            ('2B02','ตรวจเรือนจำ',null,null),
            ('2B03','ตรวจคุณภาพน้ำ',null,null),
            ('2B04','ตรวจโรงงาน / ตรวจสุขภาพพนักงาน',null,null),
            ('2B05','ตรวจเยี่ยมสถานประกอบกิจการ',null,null),
            ('2B06 ','การพัฒนา/การจัดการส้วมให้ถูกสุขลักษณะ',null,null),
            ('2B08','กิจกรรมการให้บริการชุมชนอื่น ๆ ด้านการสุขาภิบาลสิ่งแวดล้อม',null,null),
            ('2B09 ','กิจกรรมการให้บริการชุมชนด้านการสุขาภิบาลสิ่งแวดล้อม ไม่ระบุรายละเอียด',null,null),
            ('2C00','ตรวจสุขาภิบาลร้านอาหารในตลาดสด',null,null),
            ('2C01','ตรวจสุขาภิบาลร้านอาหารแผงลอย',null,null),
            ('2C02','ตรวจสุขาภิบาลร้านอาหารในโรงเรียน',null,null),
            ('2C08','ตรวจสุขาภิบาลอาหารอื่น ๆ  ',null,null),
            ('2D000','การพ่นหมอกควันเพื่อกำจัดยุงลาย',null,null),
            ('2D001','การหยอดทรายอะเบทเพื่อกำจัดยุงลาย',null,null),
            ('2D002','รณรงค์การเลี้ยงปลาหางนกยูงการกำจัดลูกน้ำ ยุงลาย',null,null),
            ('2D003','รณรงค์การปิดภาชนะ/คว่ำภาชนะ เพื่อกำจัดยุงลาย',null,null),
            ('2D01','การกำจัดแมลงและสัตว์นำโรคต่าง ๆ',null,null),
            ('2D02','การสอบสวนโรคและควบคุมโรคระบาดในชุมชน',null,null),
            ('2D03','ตรวจประเมินสถานการณ์การประสบภัยพิบัติในชุมชน',null,null),
            ('2D040','รณรงค์การแนะนําการใช้สมุนไพรควบคุมป้องกันโรค',null,null),
            ('2D041','รณรงค์การ/แนะนําการใช้สมุนไพรในโรงเรียน',null,null),
            ('2D08','กิจกรรมการให้บริการชุมชนอื่น ๆ ด้านการควบคุมป้องกันโรค',null,null),
            ('2D080','ให้ความรู้/สถานที่ตรวจบริการ ด้านเอชไอวีโรคติดต่อทางเพศสัมพันธ์ และ หรือ Harm Reduction',null,null),
            ('2D081','ให้อุปกรณ์ป้องกันการติดเชื้อเอชไอวี และโรคติดต่อทางเพศสัมพันธ์ (ถุงยางอนามัย สารหล่อลื่น และ หรือ กระบอกฉีดและเข็มสะอาด)',null,null),
            ('2E00','การตรวจสอบคุณภาพเกลือเสริมไอโอดีนในชุมชน',null,null),
            ('2E01','จัดนิทรรศการด้านโภชนาการ',null,null),
            ('2E02','รณรงค์ด้านโภชนาการ',null,null),
            ('2E03','ประกวดด้านโภชนาการ',null,null),
            ('2F00','การให้ความรู้/ข้อมูลด้านโภชนาการ',null,null),
            ('2F08','การให้ความรู้และสุขศึกษาเรื่องสุขภาพอื่น ๆ',null,null),
            ('2F09','การให้ความรู้และสุขศึกษาเรื่องสุขภาพ ไม่ระบุรายละเอียด',null,null),
            ('2F1','ออกหน่วยสุขศึกษาและหน่วยเคลื่อนที่ในชุมชน ',null,null),
            ('2F20','จัดอบรมให้ความรู้ด้านการส่งเสริมป้องกันโรคแก่ อสม. / แกนนำชุมชน',null,null),
            ('2F21','จัดอบรมให้ความรู้ด้านการส่งเสริมป้องกันโรคแก่ประชาชนกลุ่มเป้าหมาย',null,null),
            ('2F22','จัดอบรมให้ความรู้ด้านโภชนาการ',null,null),
            ('2F23','จัดอบรมให้ความรู้ด้านทันตสุขภาพแก่แกนนำ/ กลุ่มผู้ป่วย/ ชมรม',null,null),
            ('2F24','จัดอบรมให้ความรู้ด้านทันตสุขภาพแก่ /อสม./ผู้ดูแลเด็ก (ผดด.)  ',null,null),
            ('2F25','จัดอบรมให้ความรู้ด้านทันตสุขภาพแก่แกนนำนักเรียน/ครู  ',null,null),
            ('2F28','จัดอบรมให้ความรู้เรื่องสุขภาพอื่น ๆ  ',null,null),
            ('2F29','จัดอบรมให้ความรู้เรื่องสุขภาพ ไม่ระบุรายละเอียด',null,null),
            ('2F301','แมคโครไบโอติกส์ (Macrobiotics) ',null,null),
            ('2F302','มังสวิรัติ',null,null),
            ('2F303','คีโตเจนิค ไดเอต (Ketogenic Diet) / อาหารพร่องแป้ง (Low-Carbohydrate Diet)',null,null),
            ('2F304','อาหารปรับสมดุลฤทธิ์ร้อน-เย็น/อาหารสุขภาพ/เกอร์สันบำบัด (Gerson Therapy)',null,null),
            ('2F310','การให้ความรู้ เรื่อง การนำหลักธรรมศาสนามาปฏิบัติในชีวิตประจำวัน',null,null),
            ('2F311','การให้ความรู้ เรื่อง การปรับสมดุลร่างกาย / ดุลยภาพบำบัด',null,null),
            ('2F312','การให้ความรู้ เรื่อง กายและจิต (Mind and Body Intervention) / การออกกำลังกาย',null,null),
            ('2F313','การให้ความรู้ เรื่อง สวดมนต์บำบัดและ/หรือสมาธิบำบัด',null,null),
            ('2F314','การให้ความรู้ เรื่อง สมุนไพรในการดูแลสุขภาพ',null,null),
            ('2F315','การให้ความรู้ เรื่อง พลังบำบัด',null,null),
            ('2G00','ออกหน่วยบริการทางการแพทย์/ทันตกรรม เคลื่อนที่ในชุมชน',null,null),
            ('2G01','ออกหน่วยบริการทางการแพทย์/ทันตกรรม พอ.สว. เคลื่อนที่ในชุมชน',null,null),
            ('2G1','ออกหน่วยบริการสุขภาพในพื้นที่',null,null);"""


            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qvil_com, multi=True):
            pass
        conn.commit()
            
        cursor.close()
        conn.close()
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)

# บังคับส่งออกแฟ้ม Labor
    def ser8():
        db_config = read_db_config()

        qcomp ="""UPDATE person_anc set  force_labor_complete_date = LAST_DAY(labor_date)
WHERE lmp  >= DATE_ADD(MAKEDATE(EXTRACT(YEAR FROM CURDATE()),1),INTERVAL -9 MONTH) and discharge ='N';
UPDATE person_anc set force_labor_complete_export ='Y' WHERE force_labor_complete_date IS NOT NULL and discharge ='N';
"""


            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qcomp, multi=True):
            pass
        conn.commit()
            
        cursor.close()
        conn.close()
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","เพิ่มข้อมูลแล้ว...",parent=window)
        

# ลบ LOG
    def ser9():
        db_config = read_db_config()

        qcomp ="""DELETE FROM vn_stat_log WHERE log_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM replicate_log WHERE event_time < DATE_ADD(NOW(), INTERVAL -365 DAY);

DELETE FROM ksklog WHERE logtime < DATE_ADD(NOW(), INTERVAL -1 YEAR) or modifytype ='fail' ;

DELETE FROM opitemrece_log WHERE event_date_time < DATE_ADD(NOW(), INTERVAL -2 YEAR) ;

DELETE FROM patient_log WHERE log_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR) ;

DELETE FROM lab_entry_log WHERE log_date_time < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM opitemrece_finance_log WHERE log_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM report_access_log WHERE access_date_time < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM patient_emr_log WHERE access_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM rx_operator_log WHERE log_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM pttype_log WHERE change_date_time < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM lab_access_log WHERE log_date_time < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM hosxp_chat_log WHERE chat_time < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM ipt_cancel_log WHERE cancel_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM ipt_chart_location_log WHERE log_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM system_backup_log WHERE backup_datetime < DATE_ADD(NOW(), INTERVAL -1 YEAR);

DELETE FROM ipt_diagnosis_log WHERE ipt_diagnosis_log_date < DATE_ADD(CURDATE(), INTERVAL -1 YEAR);

DELETE FROM opdcard_print_log WHERE print_date < DATE_ADD(CURDATE(), INTERVAL -1 YEAR);

"""


            # connect to the database server
        conn = MySQLConnection(**db_config)
           
            # execute the query multi
        cursor = conn.cursor()
        for result in cursor.execute(qcomp, multi=True):
            pass
        conn.commit()
            
        cursor.close()
        conn.close()
        time.sleep(2)
        messagebox.showinfo("การดำเนินการ","ลบแล้ว",parent=window)

# ฟังก์ชั่น
    def show_and_run(func, btn):
        # Save current button color and change it to green
        oldcolor = btn['bg']
        btn['bg'] = 'blue'

        # Call the function
        func()

        # Restore original button color
        btn['bg'] = oldcolor

    def run_function(func, btn):
        # Disable all buttons
        for b in buttons.values():
            b['state'] = 'disabled'

        processing_bar.start(interval=10)
        show_and_run(func, btn)
        processing_bar.stop()

        # Enable all buttons
        for b in buttons.values():
            b['state'] = 'normal'

    def clicked(func, btn):
        Thread(target=run_function, args=(func, btn)).start()

    #window = Tk()
    window = Toplevel()
    window.title('ตัวช่วยในการจัดการข้อมูล')
    
    window.iconbitmap('imake.ico')
    window.grab_set()
    style = ThemedStyle(window)
    style.set_theme("plastik")
    

    topFrame = Frame(window)

    # Tell the Frame to fill the whole window
    topFrame.pack(fill=BOTH, expand=1)

    # Make the Frame grid contents expand & contract with the window
    topFrame.columnconfigure(0, weight=1)
    for i in range(4):
        topFrame.rowconfigure(i, weight=1)

    button_data = (
        ('ปรับข้อมูลประชากร', ser1),
        ('ปรับสถานะคนเสียชีวิต', ser2),
        ('โอนรูปจากเวชระเบียนไปบัญชี 1', ser3),
        ('บังคับส่งออกแฟ้ม PRENATAL งาน ANC ', ser4),
        ('บังคับส่งออกแฟ้ม LABOR งาน ANC', ser8),
        ('ลบ LOG ย้อนหลัง 1 ปี', ser9),
        ('เพิ่มข้อมูลแฟ้ม pp_special กิจกรรมส่งเสริม/ป้องกัน ตามมาตรฐาน 43 แฟ้ม ปี 63', ser5),
        ('เพิ่มข้อมูลแฟ้ม community_service เยี่ยมบ้าน ตามมาตรฐาน 43 แฟ้ม ปี 63', ser6),
        ('เพิ่มข้อมูลแฟ้ม comactivity กิจกรรมในชุมชน ตามมาตรฐาน 43 แฟ้ม ปี 63', ser7),
        #('All', all_func),
    )

    # Make all the buttons and save them in a dict
    buttons = {}
    for row, (name, func) in enumerate(button_data):
        btn = Button(topFrame, text=name)
        btn.config(command=lambda f=func, b=btn: clicked(f, b))
        btn.grid(row=row, column=0, columnspan=1, sticky='EWNS')
        buttons[name] = btn
    row += 1

    processing_bar = ttk.Progressbar(topFrame, 
        orient='horizontal', mode='indeterminate')
    processing_bar.grid(row=row, column=0, columnspan=1, sticky='EWNS')

    window.mainloop()

#  ################ MENU SENT LINE ################

def sentline():

        with  open("linetoken.ini","r") as f1:
                                s1=f1.readlines()
                                s2 = [line.strip() for line in s1]
                                token_r = (s2[1])
                                s_token = token_r.split(' = ')[1]
                                f1.close()

        def token():
                    with  open("linetoken.ini","r") as f1:
                        s1=f1.readlines()
                        s2 = [line.strip() for line in s1]
                        token_r = (s2[1])
                        s_token = token_r.split(' = ')[1]
                        f1.close()
                        
                    def settoken():
                                
                            gettoken.get()
                            token=gettoken.get()

                            with open("linetoken.ini","w") as f:
                                            f.write('[line_token]\ntoken = %s\n'%(token))
                                            f.close()
                            messagebox.showinfo("การดำเนินการ","บักทึกเรียบร้อยแล้ว",parent=pop5)
                            pop5.destroy()
                                            
                                   
                    pop5 = Toplevel()
                    pop5.geometry('300x50')
                    pop5.iconbitmap('imake.ico')
                    pop5.grab_set()
                    
                    gettoken=StringVar()
                    gettoken.set(s_token)
                    
                    ent1=ttk.Entry(pop5,textvariable=gettoken,font=('Browallia New',12),width=80)
                    ent1.pack()
                    but1=ttk.Button(pop5,text='บันทึก',command=settoken)
                    but1.pack()
                    pop5.mainloop()

                    

        pop3 = Toplevel()
        pop3.geometry('466x400+100+100')
        pop3.iconbitmap('imake.ico')
        pop3.grab_set()
        #pop1.grab_release()

        def age1():
            
            getage1.get()
            ag1=getage1.get()
            getage2.get()
            ag2=getage2.get()
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage1 ="""SELECT concat("หมู่ ",v.village_moo," ",v.village_name," ",COUNT(*)," คน ") FROM person as p
            LEFT JOIN village as v on v.village_id=p.village_id
            WHERE p.death ='N'  and p.house_regist_type_id in ('1','3') and v.village_id <> '1'
            and timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
            GROUP BY v.village_moo
            UNION
            SELECT concat("Total = ",COUNT(*)) FROM person as p
            LEFT JOIN village as v on v.village_id=p.village_id
            WHERE p.death ='N' and p.house_regist_type_id in ('1','3') and v.village_id <> '1'
            and  timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
            """
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage1, (ag1,ag2,ag1,ag2,))
            record = cursor.fetchall()
            
            msg10 =(f'ประชากร type 1,3 \nช่วงอายุ {ag1} ปี ' +f'ถึง อายุ {ag2} ปี') 
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()              



        def age2():
            getage1.get()
            ag1=getage1.get()
            getage2.get()
            ag2=getage2.get()
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage2 ="""SELECT concat("หมู่ ",v.village_moo," ",v.village_name," ",COUNT(*)," คน ") FROM person as p
            LEFT JOIN village as v on v.village_id=p.village_id
            WHERE p.death ='N'  and p.house_regist_type_id in ('1','2','3') and v.village_id <> '1'
            and timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
            GROUP BY v.village_moo
            UNION
            SELECT concat("Total = ",COUNT(*)) FROM person as p
            LEFT JOIN village as v on v.village_id=p.village_id
            WHERE p.death ='N' and p.house_regist_type_id in ('1','2','3') and v.village_id <> '1'
            and  timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
            """
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage2, (ag1,ag2,ag1,ag2,))
            record = cursor.fetchall()
            
            msg10 =(f'ประชากร ทั้งหมด \nช่วงอายุ {ag1} ปี ' +f'ถึง อายุ {ag2} ปี')
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})

            #msg = (msg10,record)
            cursor.close()
            conn.close()              
            
        def age3():
            
            getage1.get()
            ag1=getage1.get()
            getage2.get()
            ag2=getage2.get()
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage3 ="""SELECT concat(s.name," ",COUNT(person_id)," คน") FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','3')
                and timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
                GROUP BY s.code
                UNION
                SELECT concat("Total = ",COUNT(person_id)) FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','3')
                and timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
            """
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage3, (ag1,ag2,ag1,ag2,))
            record = cursor.fetchall()
            
            msg10 =(f'ประชากร type 1,3 \nช่วงอายุ {ag1} ปี ' +f'ถึง อายุ {ag2} ปี')
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
                
            cursor.close()
            conn.close() 

            #msg = (msg10,record)
            cursor.close()
            conn.close()   

        def age4():
            
            getage1.get()
            ag1=getage1.get()
            getage2.get()
            ag2=getage2.get()
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT concat(s.name," ",COUNT(person_id)," คน") FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','2','3')
                and timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
                GROUP BY s.code
                UNION
                SELECT concat("Total = ",COUNT(person_id)) FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','2','3')
                and timestampdiff(year,p.birthdate,curdate())  BETWEEN %s and %s
            """
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4, (ag1,ag2,ag1,ag2,))
            record = cursor.fetchall()

            msg10 =(f'ประชากร ทั้งหมด \nช่วงอายุ {ag1} ปี ' +f'ถึง อายุ {ag2} ปี')
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
                
            cursor.close()
            conn.close() 

            #msg = (msg10,record)
            cursor.close()
            conn.close()              

        def d741():
          
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT concat("จำนวนผู้พิการ Type 1,3 ",s.name," ",COUNT(person_id)," คน") FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','3') and p.pttype in('74','D1','ND','VD')
                GROUP BY s.code
                UNION
                SELECT concat("Total = ",COUNT(person_id)) FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','3') and p.pttype in('74','D1','ND','VD')
            """
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4)
            record = cursor.fetchall()
            
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
                
            cursor.close()
            conn.close() 
            



        def d742():          
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT  concat("จำนวนผู้พิการ ทั้งหมด ",s.name," ",COUNT(person_id)," คน") FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','2','3') and p.pttype in('74','D1','ND','VD')
                GROUP BY s.code
                UNION
                SELECT concat("Total = ",COUNT(person_id)) FROM person as p
                LEFT JOIN sex as s on s.code=p.sex
                WHERE p.death ='N' and p.house_regist_type_id in ('1','2','3') and p.pttype in('74','D1','ND','VD')
            """
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4)
            record = cursor.fetchall()
            
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
                
            cursor.close()
            conn.close()              

            
            
        def house():          
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT concat(" หมู่ : ",v.village_moo," ",v.village_name," จำนวน ",COUNT(h.house_id),"  คาเรือน") FROM house as h
            LEFT JOIN village as v on v.village_id=h.village_id
            WHERE h.village_id <> '1'
            GROUP BY h.village_id
            UNION
            SELECT concat(" Total = ",COUNT(h.house_id)) FROM house as h
            LEFT JOIN village as v on v.village_id=h.village_id
            WHERE h.village_id <> '1'
            """
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4)
            record = cursor.fetchall()
            
            msg10 =('จำนวนหลังคาเรือน') 
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()              

# นัดวันนี้
        def oapp1():          
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT GROUP_CONCAT("นัดวันนี้ : ",CONCAT(p.pname,p.fname," ",p.lname),CONCAT(" ที่อยู่ ",p.addrpart," หมู่ ",p.tmbpart," ",t.full_name)," โทร. ",p.mobile_phone_number,
concat(" คลินิก ",c.name," นัด ",o.note))
FROM oapp AS o LEFT JOIN patient AS p ON o.hn = p.hn
LEFT JOIN clinic AS c ON o.clinic = c.clinic
LEFT JOIN thaiaddress AS t ON t.chwpart = p.chwpart AND t.amppart = p.amppart AND t.tmbpart = p.tmbpart
WHERE o.nextdate = CURRENT_DATE GROUP BY o.hn"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4)
            record = cursor.fetchall()
            
            #msg10 =('นัดวันนี้') 
            #r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()

# นัดพรุ่งนี้
        def oapp2():          
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT GROUP_CONCAT("นัดวันพรุ่งนี้ : ",CONCAT(p.pname,p.fname," ",p.lname),CONCAT(" ที่อยู่ ",p.addrpart," หมู่ ",p.tmbpart," ",t.full_name)," โทร. ",p.mobile_phone_number,
concat(" คลินิก ",c.name," นัด ",o.note))
FROM oapp AS o LEFT JOIN patient AS p ON o.hn = p.hn
LEFT JOIN clinic AS c ON o.clinic = c.clinic
LEFT JOIN thaiaddress AS t ON t.chwpart = p.chwpart AND t.amppart = p.amppart AND t.tmbpart = p.tmbpart
WHERE o.nextdate = DATE_ADD(CURRENT_DATE,INTERVAL 1 DAY)
GROUP BY o.hn"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4)
            record = cursor.fetchall()
            
            #msg10 =('นัดวันนี้') 
            #r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()
# จำนวนผู้ป่วยโรคเรื้อรัง
        def clinic():          
            
            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT concat(n.`name`," จำนวน ",COUNT(c.clinic)," คน") FROM clinicmember as c
LEFT JOIN clinic as n on n.clinic=c.clinic
WHERE c.discharge = 'N'
GROUP BY c.clinic"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4)
            record = cursor.fetchall()
            
            msg10 =('จำนวนผู้ป่วยโรคเรื้อรัง') 
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()
            
        def cal_oapp():
            #print(cal.get_date())
            #print(cal1.get_date())

            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT GROUP_CONCAT(DATE_FORMAT(DATE_ADD(o.vstdate,INTERVAL 543 YEAR),"%d/%m/%Y")," นัด : ",CONCAT(p.pname,p.fname," ",p.lname),CONCAT(" ที่อยู่ ",p.addrpart," หมู่ ",p.tmbpart," ",t.full_name)," โทร. ",p.mobile_phone_number,
concat(" คลินิก ",c.name," นัด ",o.note))
FROM oapp AS o LEFT JOIN patient AS p ON o.hn = p.hn
LEFT JOIN clinic AS c ON o.clinic = c.clinic
LEFT JOIN thaiaddress AS t ON t.chwpart = p.chwpart AND t.amppart = p.amppart AND t.tmbpart = p.tmbpart
WHERE o.nextdate between %s and %s
GROUP BY o.hn"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4,(cal.get_date(),cal1.get_date(),))
            record = cursor.fetchall()

            #msg10 =(f'ข้อมูลช่วงวันที่ \n {cal.get_date()}  ' +f'ถึง {cal1.get_date()}')
             
            #r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()


        def cal_icd10z():
            #print(cal.get_date())
            #print(cal1.get_date())

            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT CONCAT(nu.rank,'. ',nu.nn)
FROM
(SELECT @rownum := @rownum + 1 AS rank,id.* 
FROM (select CONCAT(v.pdx,' : ',i.tname,'(',i.`name`,') = ', count(*)) as nn
from vn_stat v
left join icd101 i on i.code=v.pdx
where v.vstdate between %s and %s
group by v.pdx 
order by count(*) desc
limit 10) as id,(SELECT @rownum := 0) r) as nu"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4,(cal.get_date(),cal1.get_date(),))
            record = cursor.fetchall()

            msg10 =(f'10 อันดับโรคไม่รวม icd10 Z\nข้อมูลช่วงวันที่ \n {cal.get_date()}  ' +f'ถึง {cal1.get_date()}')
             
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()

        def cal_icd10():
            #print(cal.get_date())
            #print(cal1.get_date())

            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT CONCAT(nu.rank,'. ',nu.nn)
FROM
(SELECT @rownum := @rownum + 1 AS rank,id.* 
FROM (select CONCAT(v.pdx,' : ',i.tname,'(',i.`name`,') = ', count(*)) as nn
from vn_stat v
left join icd101 i on i.code=v.pdx
where v.vstdate between %s and %s
and v.pdx not like 'Z%%'
group by v.pdx 
order by count(*) desc
limit 10) as id,(SELECT @rownum := 0) r) as nu"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4,(cal.get_date(),cal1.get_date(),))
            record = cursor.fetchall()

            msg10 =(f'10 อันดับโรครวม Z\nข้อมูลช่วงวันที่ \n {cal.get_date()}  ' +f'ถึง {cal1.get_date()}')
             
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()


        def cal_506():
            #print(cal.get_date())
            #print(cal1.get_date())

            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT CONCAT(nu.rank,'. ',nu.nn)
FROM
(SELECT @rownum := @rownum + 1 AS rank,id.*
FROM (select CONCAT(v.pdx,' : ',i.tname,'(',i.`name`,') = ', count(*)) as nn
from surveil_member v
left join icd101 i on i.code=v.pdx
where v.vstdate between %s and %s
group by v.pdx 
order by count(*) desc
limit 10) as id,(SELECT @rownum := 0) r) as nu"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4,(cal.get_date(),cal1.get_date(),))
            record = cursor.fetchall()

            msg10 =(f'10 อันดับโรค R506 \nข้อมูลช่วงวันที่ \n {cal.get_date()}  ' +f'ถึง {cal1.get_date()}')
             
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()


        def dspm():
            #print(cal.get_date())
            #print(cal1.get_date())

            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT concat(" hn : ",t.hn," ",t.pname,t.fname," ",t.lname," วันเกิด ",
DATE_FORMAT(DATE_ADD(p.birthdate,INTERVAL 543 YEAR),"%d/%m/%Y")," บ้านเลขที่  ",
t.addrpart," หมู่ ",t.moopart," อายุ ", timestampdiff(month,p.birthdate,%s)," เดือน ")
,p.mother_name,p.father_name
FROM person as p LEFT JOIN patient as t on t.cid=p.cid
WHERE timestampdiff(month,p.birthdate,%s) in ('9','18','30','42','60') 
AND p.death ='N' and p.house_regist_type_id in ('1','3') and p.person_id <> '0'
ORDER BY p.village_id"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4,(cal.get_date(),cal.get_date(),))
            record = cursor.fetchall()

            msg10 =(f'รายชื่อเด็ก DSPM \nข้อมูลช่วงวันที่ \n {cal.get_date()}  '+'คัดกรองได้ภายใน 30 วัน')
             
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()


        def cal_detail():
            #print(cal.get_date())
            #print(cal1.get_date())

            db_config = read_db_config()
            url = 'https://notify-api.line.me/api/notify'
            token = s_token
            headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

            qage4 ="""SELECT CONCAT(nu.rank,'. ',nu.detail) FROM
(SELECT @rownum := @rownum + 1 AS rank,
CONCAT('ผู้บันทึก : ',ck.name,' จำนวน ',ck.visit,' ครั้ง') as detail
FROM (SELECT o.staff,Count(o.staff) AS visit,u.name
FROM 	ovst o LEFT OUTER JOIN opduser u ON u.loginname = o.staff
WHERE 	o.staff <> ' ' AND o.staff IS NOT NULL
AND o.vstdate BETWEEN %s AND %s
GROUP BY 	o.staff ORDER BY 	visit DESC) as ck ,(SELECT @rownum := 0) r) as nu"""
            
            # connect to the database server
            conn = MySQLConnection(**db_config)
 
            # execute the query multi
            cursor = conn.cursor(buffered = True)
            cursor.execute(qage4,(cal.get_date(),cal1.get_date(),))
            record = cursor.fetchall()

            msg10 =(f'ตรวจสอบจำนวนการบันทึกข้อมูล ผู้ป่วย OPD \nข้อมูลช่วงวันที่ \n {cal.get_date()}  ' +f'ถึง {cal1.get_date()}')
             
            r = requests.post(url, headers=headers, data = {'message':msg10})
            for x in record:
                r = requests.post(url, headers=headers, data = {'message':x})
            #msg = (msg10,record)
            cursor.close()
            conn.close()


            
        #### SENT LINE
                
        getage1=StringVar()
        getage1.set(0)
        getage2=StringVar()
        getage2.set(100)

        
        bb1=ttk.Button(pop3,text='SET LINE TOKEN',command=token)
        bb1.pack(ipadx=500,ipady=5)

        frm1=Frame(pop3)
        frm1.place(x=120,y=45)

        frm11=Frame(pop3)
        frm11.place(x=25,y=75)

        fl1=ttk.Label(frm1,text='ประชากรกลุ่มอายุ  ',font=('Browallia New',14))
        fl1.pack(side = LEFT)
        
        fe1=ttk.Entry(frm1,textvariable=getage1,font=('Browallia New',12),width=4)
        fe1.pack(side = LEFT)

        fl2=ttk.Label(frm1,text=' ปี ถึง ',font=('Browallia New',14))
        fl2.pack(side = LEFT)
        
        fe2=ttk.Entry(frm1,textvariable=getage2,font=('Browallia New',12),width=4)
        fe2.pack(side = LEFT)

        fl2=ttk.Label(frm1,text=' ปี',font=('Browallia New',14))
        fl2.pack(side = LEFT)        

        fb2=ttk.Button(frm11,text='Type 1,3 รายหมู่บ้าน',command=age1)
        fb2.pack(side = LEFT)
        
        fb31=ttk.Button(frm11,text='ทั้งหมด รายหมู่บ้าน',command=age2)
        fb31.pack(side = LEFT)

        frm12=Frame(pop3)
        frm12.place(x=15,y=100)
        
        fb22=ttk.Button(frm11,text='Type 1,3 ชาย หญิง',command=age3)
        fb22.pack(side = LEFT)
        
        fb21=ttk.Button(frm11,text='ทั้งหมด ชาย หญิง',command=age4)
        fb21.pack(side = LEFT)

       

        frm2=Frame(pop3)
        frm2.place(y=125)
        
        frm21=Frame(pop3)
        frm21.place(x=150,y=175)

        frm22=Frame(pop3)
        frm22.place(x=190,y=220)

        frm221=Frame(pop3)
        frm221.place(x=140,y=240)


        
        #fl2=ttk.Label(frm2,text='-----------------------------------------------',font=('Browallia New',14))
        #fl2.pack()
        
        f2b=ttk.Button(frm2,text='จำนวนผู้พิการ type 1,3',command=d741)
        f2b.pack(side = LEFT)

        f2b2=ttk.Button(frm2,text='จำนวนผู้พิการ ทั้งหมด',command=d742)
        f2b2.pack(side = LEFT)

        f2b9=ttk.Button(frm2,text='จำนวนผู้ป่วยโรคเรื้อรัง',command=clinic)
        f2b9.pack(side = LEFT)

        
        f2b7=ttk.Button(frm2,text='จำนวนหลังคาเรือน',command=house)
        f2b7.pack(side = LEFT)

        
        f2b8=ttk.Button(frm21,text='รายชื่อ นัดวันนี้',command=oapp1)
        f2b8.pack(side = LEFT)

        f2b8=ttk.Button(frm21,text='รายชื่อ นัดวันพรุ่งนี้',command=oapp2)
        f2b8.pack(side = LEFT)



        fl6=ttk.Label(frm22,text=' กำหนดช่วงเวลา ',font=('Browallia New',14))
        fl6.pack()
        
        cal = DateEntry(frm221, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy' )
        cal.pack(side = LEFT)

        fl601=ttk.Label(frm221,text='ถึง',font=('Browallia New',14))
        fl601.pack(side = LEFT)

        cal1 = DateEntry(frm221, width=12, background='darkblue',
                    foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy')
        cal1.pack(side = LEFT)
        
        frm3=Frame(pop3)
        frm3.place(x=5,y=270)

        frm5=Frame(pop3)
        frm5.place(x=35,y=295)
       

        f3b10=ttk.Button(frm3,text='การนัดหมาย',command=cal_oapp)
        f3b10.pack(side = LEFT)

        f3b20=ttk.Button(frm3,text='10 อันดับโรครวม ICD10 Z',command=cal_icd10)
        f3b20.pack(side = LEFT)

       

        f4b10=ttk.Button(frm3,text='10 อันดับโรคไม่รวม ICD10 Z',command=cal_icd10z)
        f4b10.pack(side = LEFT)

        f4b20=ttk.Button(frm3,text='10 อันดับโรค R506',command=cal_506)
        f4b20.pack(side = LEFT)

        f5b10=ttk.Button(frm5,text='รายชื่อเด็กสำหรับคัดกรอง DSPM',command=dspm)
        f5b10.pack(side = LEFT)

        f5b20=ttk.Button(frm5,text='จำนวนการบันทึกข้อมูลผู้ป่วย OPD',command=cal_detail)
        f5b20.pack(side = LEFT)        


        frmline1=Frame(pop3)
        frmline1.place(y=100) 

        fl201=ttk.Label(frmline1,text='-----------------------------------------------------------------------------------------------------------------------------------------',font=('Browallia New',14))
        fl201.pack()

        frmline2=Frame(pop3)
        frmline2.place(y=150) 

        fl202=ttk.Label(frmline2,text='-----------------------------------------------------------------------------------------------------------------------------------------',font=('Browallia New',14))
        fl202.pack()

        frmline3=Frame(pop3)
        frmline3.place(y=200) 

        fl203=ttk.Label(frmline3,text='-----------------------------------------------------------------------------------------------------------------------------------------',font=('Browallia New',14))
        fl203.pack()

        pop3.mainloop()

#  ################ SETTHINGS ################    

def setsetting():
        with  open("config.ini","r") as f1:
                s1=f1.readlines()
                s2 = [line.strip() for line in s1]
                host_r = (s2[1])
                db_r = (s2[2])
                user_r = (s2[3])
                pass_r = (s2[4])
                s_host = host_r.split(' = ')[1]
                s_db = db_r.split(' = ')[1]
                s_user = user_r.split(' = ')[1]
                s_pass = pass_r.split(' = ')[1]
                f1.close()

        
        def setconnect():
                    
                getip.get()
                getdb.get()
                getuser.get()
                getpassword.get()
        

                host=getip.get()
                db=getdb.get()
                user=getuser.get()
                password=getpassword.get()

                with open("config.ini","w") as f:
                                f.write('[mysql]\nhost = %s\ndatabase = %s\nuser = %s\npassword = %s\n'%(host,db,user,password))
                                f.close()
                pop4.destroy()


        def testconnect():

                getip.get()
                getdb.get()
                getuser.get()
                getpassword.get()
        

                host=getip.get()
                db=getdb.get()
                user=getuser.get()
                password=getpassword.get()

                with open("config.ini","w") as f:
                                f.write('[mysql]\nhost = %s\ndatabase = %s\nuser = %s\npassword = %s\n'%(host,db,user,password))
                                f.close()

                
                """ Connect to MySQL database """
                db_config = read_db_config()
                conn = None
                try:
                        #print('Connecting to MySQL database...')
                        conn = MySQLConnection(**db_config)
                        if conn.is_connected():
                                messagebox.showinfo("การเชื่อมต่อฐานข้อมูล",'การเชื่อมต่อสำเร็จ',parent=pop4)
                        else:
                                messagebox.showinfo("การเชื่อมต่อฐานข้อมูล",'การเชื่อมต่อไม่สำเร็จ',parent=pop4)

                except Error as error:
                    messagebox.showinfo("การเชื่อมต่อฐานข้อมูลไม่สำเร็จ",error,parent=pop4)
             
 

        def aboutus():
                messagebox.showinfo("คำแนะนำ","""แนะนำในการใช้โปรแกรม\n1. คลิกขวาที่ ไอคอนโปรแกรม iMake\n2. Run as administrator
หรือคำหนดค่าโดย\nProperties --> Compatibility --> Privilege level = Run as administrator
3.ตั้งค่าให้เริ่มปรับปรุงข้อมูลตั้งวันที่ 1 เมษายน ของปีก่อน พ.ศ.ปัจจุบัน
4.โปรแกรมนี้เขียนขึ้นเพื่อช่วยงานไอทีโดยเฉพาะ""",parent=pop4)

        def aboutus2():
            
                messagebox.showinfo("ผู้เขียนโปรแกรม","""นายวิษณุ  เสนหอม  พนักงานธุรการ
โรงพยาบาลส่งเสริมสุขภาพตำบลบ้านหนองทุ่ม ตำบลหนองทุ่ม
อำเภอเซกา  จังหวัดบึงกาฬ 38150
โทร. 081-0509333
E-mail : wis.s@hotmail.com
Facebook : fb.com/nu1989nu
ID Line : nu1989nu""",parent=pop4)

      
          

        pop4=Toplevel()
        pop4.geometry('380x240')
        pop4.iconbitmap('imake.ico')
        pop4.grab_set()

        dl1=ttk.Label(pop4,text='ตั้งค่าการเชื่อมต่อ',font=('Browallia New',20))
        dl1.pack()

        frame1=Frame(pop4)
        frame1.place(x=30,y=60)
        
        dl1=ttk.Label(frame1,text='ไอพี เครื่องเซิฟเวอร์',font=('Browallia New',16))
        dl1.pack(anchor=E)


        dl2=ttk.Label(frame1,text='ชื่อฐานข้อมูล',font=('Browallia New',16))
        dl2.pack(anchor=E)

        dl3=ttk.Label(frame1,text='ชื่อผู้ใช้ฐานข้อมูล',font=('Browallia New',16))
        dl3.pack(anchor=E)

        dl4=ttk.Label(frame1,text='รหัสผ่านฐานข้อมูล',font=('Browallia New',16))
        dl4.pack(anchor=E)
        
        
        frame2=Frame(pop4)
        frame2.place(x=160,y=50)

        getip=StringVar()
        getip.set(s_host)
        
        getdb=StringVar()
        getdb.set(s_db)
        
        getuser=StringVar()
        getuser.set(s_user)
        
        getpassword=StringVar()
        getpassword.set(s_pass)
      
        
        de1=ttk.Entry(frame2,textvariable=getip,font=('Browallia New',15))
        de1.pack()


        de2=ttk.Entry(frame2,textvariable=getdb,font=('Browallia New',15))
        de2.pack()

        de3=ttk.Entry(frame2,textvariable=getuser,font=('Browallia New',15))
        de3.pack()
        
        de4=ttk.Entry(frame2,textvariable=getpassword,font=('Browallia New',15),show='*')
        de4.pack()

        frame3=Frame(pop4)
        frame3.place(x=50,y=190)

        
        db1=ttk.Button(frame3,text='บันทึก',command=setconnect)
        db1.pack(ipady=4,side=LEFT)

        db2=ttk.Button(frame3,text='ทดสอบ',command=testconnect)
        db2.pack(ipady=4,side=LEFT)

        db3=ttk.Button(frame3,text='คำแนะนำ',command=aboutus)
        db3.pack(ipady=4,side=LEFT)

        db4=ttk.Button(frame3,text='เกี่ยวกับฉัน',command=aboutus2)
        db4.pack(ipady=4,side=LEFT)
 
        
        pop4.mainloop()

#  ################ MIAN MENU ################

GUI = Tk()
GUI.title('iMAKE V. 0.2')
GUI.configure(bg='#00d2ff')
GUI.geometry('640x190+50+50')
GUI.iconbitmap('imake.ico')
style = ThemedStyle(GUI)
style.set_theme("plastik")


L1=Label(GUI,bg='#00d2ff')
L1.pack()

frame = Frame(GUI)
frame.pack()

bottomframe = Frame(GUI)
bottomframe.pack( side = LEFT )

greenbutton = Button(frame, text="บริการ", bg="#ffce00", width = 20, height = 9,command=menu1)
greenbutton.pack( side = LEFT )


redbutton = Button(frame, text="ตัวช่วย", bg="#c9ff00", width = 20, height = 9,command=menu2)
redbutton.pack( side = LEFT)

bluebutton = Button(frame, text="ส่งรายงานเข้าไลน์กลุ่ม", bg="#49ff00", width = 20, height = 9,command=sentline)
bluebutton.pack( side = LEFT )

pinkbutton = Button(frame, text="ตั้งค่า", bg="#00ffec", width = 20, height = 9,command=setsetting)
pinkbutton.pack( side = LEFT)


GUI.mainloop()



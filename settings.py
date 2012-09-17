#!/usr/bin/python
#encoding: utf-8
HOST = '220.181.83.18'
PORT = 8313
#PORT = 8315

LOGFILE = './log'
LOGFORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"
USERNAME = '虽大然'

UID = {
        'huatuo' : '41978',
        'xusu' : '44791',
        'yuanshao' : '44918',
        'zangfei' : '47845',
        'lvbu' : '49088',
        'sunsangxiang' : '46227',
        'guanping' : '41546',
        'caiyan' : '40991',
        'zaoyun' : '50107',
        'jiangwei' : '50497',
        'guanyu' : '50630',
        'zuge' : '51181',
        'mateng' : '51475',
        'jiayu' : '51934',
}

PEOPLE_ID = {
        'temp' : '63771615',
        'wangjiang': '65960391',
        'huicangai': '66342003',
        'siziniu' : '66487135',   
        'guoyunyu' : '63502523',   
        'daiqifei' : '64724243',   
        'jian' : '66894199', # jianjunsierhen   
        'menghuailei' : '67798563',
        'yipinruxi' : '65981963',
        'yanrubo' : '65470347',
        'jiange' : '64308127',
        'yingzi' : '65706331',
        'yanhuangdiguo' : '66574259',
        'zaozilong' : '66543199',
        # for tongsang
        'jianjianbiaoxie' : '64862103',
        'lolo' : '66290987',
        'wangdaiman' : '63771615',
        'daofeiwang' : '66284359',
        'nihongxiuse' : '65642323',
        'vmao' : '64726651',
}

ARMY_ID = {
        'menghuo' : '1240',    
        'wan' : '1320',
}

NPC_ID = {
        'huangjia80' : 1317,
        'xiangyuhuangjia' : 1427,
}

CITY_ID = {
        'xinye' : '309',
        'jiangxia' : '107',
        'wan' : '208',
        'wuling' : '311',
        'sangyong' : '308',
}

TRAINING_HOUR_TO_MODE = {
        2 : 2,
        8 : 3,
}

KEJI = {
        'yulin' : '101',
        'cangse' : '102',
        'fengsi' : '103',
        'yanyue' : '104',
        'cuxing' : '105',
        'bagua' : '106',
        'qixing' : '107',
        'yanxing' : '108',
        'bingfu' : '201',
        'lingqi' : '202',
        'pg' : '203',
        'pf' : '204',
        'zg' : '205',
        'zf' : '206',
        'fg' : '207',
        'ff' : '208',
        'jiwen' : '209',
        'hudun' : '211',
        'tousi' : '214',
}
KEJI_LIST = [
        ('jiwen', 2),
        ('pg', 1),
        ('pf', 1),
        ('zf', 1),
        ('hudun', 2),
        ('zg', 1),
        ('ff', 1),
        ('lingqi', 2),
        ('bingfu', 1),
        #('yanxing', 5),
        #('cuxing', 5),
        #('cangse', 5),
        #('yanyue', 5),
        #('yulin', 5),
        #('fengsi', 5),
]

JIANZHU = {
        'zuceng' : '100',
        'jiaocang' : '101',
        'jiaocang2' : '102',
        'junji' : '103',
        'sangdian' : '104',
        'yizan' : '107',
        'qianzuang' : '108',
        'zubicang' : '109',
        'zangfang' : '110',
        'yinku' : '112',  
        'minju1' : '114',  
        'minju2' : '115',  
        'minju3' : '116',  
        'minju4' : '117',  
        'minju5' : '118',  
        'minju6' : '119',  
        'minju7' : '120',  
        'minju8' : '121',  
        'minju9' : '122',  
        'minju10' : '123',  
}
JIANZHU_LIST = [
        'junji',
        'sangdian',
        'jiaocang',
        'jiaocang2',
        'zangfang',
        'zubicang',
        'minju1',
        'minju2',  
        'minju3',  
        'minju4',  
        'minju5',  
        'minju6',  
        'minju7',  
        'minju8',  
        'minju9',  
        'minju10',  
        'qianzuang',
        'yinku',
]

PLANTATION = {
        'xuzou' : '9',
        'yuzou' : '10',
}

LEVEL_EXP_MAP = {
        1 : 45,
        2 : 180,
        3 : 450,
        4 : 720,
        5 : 900,
        6 : 1800,
        7 : 2700,
        8 : 3600,
        9 : 4500,
        10 : 5400,
        11 : 6300,
        12 : 7200,
        13 : 8100,
        14 : 9000,
        15 : 10800,
        16 : 12600,
        17 : 14400,
        18 : 16200,
        19 : 18000,
        20 : 19800,
        21 : 21600,
        22 : 23400,
        23 : 25200,#?
        24 : 27000,
        25 : 28800,
        26 : 30600,
        27 : 32400,#
        28 : 34200,#
        29 : 36000,#
        30 : 37800,#
        31 : 39600,#
        32 : 41400,
        33 : 43200,
        34 : 45000,
        35 : 46800,#
        36 : 48600,#
        37 : 50400,#
        38 : 52200,#
        39 : 54000,#
        40 : 55800,#
        41 : 57600,#
        42 : 59400,#
        43 : 61200,
        44 : 63000,
        45 : 64800,
        46 : 66600,
        47 : 68400,
        48 : 70200,
        49 : 72000,#
        50 : 73800,#
        51 : 75600,#
        52 : 77400,
        53 : 79200,#
        54 : 81000,
        55 : 82800,
        56 : 84600,
        57 : 87300,
        58 : 90000,
        59 : 99000,
        60 : 108000,
        61 : 117000,
        62 : 126000,
        63 : 135000,
        64 : 144000,
        65 : 153000,
        66 : 162000,
        67 : 171000,
        68 : 180000,
        69 : 189000,
        70 : 198000,
        71 : 207000,
        72 : 216000,
        73 : 225000,
        74 : 234000,
        75 : 243000,
        76 : 252000,
        77 : 261000,
        78 : 270000,#
        79 : 297000,#
        80 : 324000,
        81 : 351000,#
        82 : 378000,#
        83 : 405000,#
        84 : 432000,#
        85 : 459000,
        86 : 486000,
        87 : 513000,
        88 : 540000,
        89 : 567000,
        90 : 594000,
        91 : 621000,
        92 : 648000,
        93 : 684000,
        94 : 720000,
        95 : 756000,
        96 : 792000,
        97 : 828000,
        98 : 864000,
        99 : 900000,
        100 : 936000,
        101 : 972000,
        102 : 1008000,
        103 : 1044000,#
}

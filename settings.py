#!/usr/bin/python
#encoding: utf-8
HOST = '220.181.83.18'
PORT = 8313
#PORT = 8315

LOGFILE = './log'
LOGFORMAT = "%(asctime)s %(filename)s [%(levelname)s] %(message)s"

DEFAULT_USER = 'flaresky'

USER_INFO = {
            'flaresky' : {
                        'USERNAME' : '虽大然',
                        'LOGIN_DATA' : '\x00\x53\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x36\x37\x32\x30\x31\x33\x30\x37\x00\x01\x30\x00\x00\x00\x3b\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x31\x39\x38\x33\x30\x38\x30\x39\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x66\x6c\x61\x72\x65\x73\x6b\x79\x40\x31\x36\x33\x2e\x63\x6f\x6d\x22\x7d',
                        },
            'flaresky1' : {
                        'USERNAME' : '隋大然',
                        'LOGIN_DATA' :     '\x00\x54\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x39\x39\x37\x39\x32\x39\x33\x31\x00\x01\x30\x00\x00\x00\x3c\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x31\x39\x38\x33\x30\x38\x30\x39\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x66\x6c\x61\x72\x65\x73\x6b\x79\x31\x40\x31\x36\x33\x2e\x63\x6f\x6d\x22\x7d',
                        },
            'flaresky2' : {
                        'USERNAME' : '随大然',
                        'LOGIN_DATA' : '\x00\x55\x00\x05\x00\x03\x6e\x69\x6c\x00\x09\x31\x30\x32\x34\x31\x36\x34\x38\x37\x00\x01\x30\x00\x00\x00\x3c\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x31\x39\x38\x33\x30\x38\x30\x39\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x66\x6c\x61\x72\x65\x73\x6b\x79\x32\x40\x31\x36\x33\x2e\x63\x6f\x6d\x22\x7d',
                        },
            'yansideyu' : {
                        'USERNAME' : '淹死的鱼',
                        'LOGIN_DATA' : '\x00\x51\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x36\x37\x34\x33\x35\x33\x31\x35\x00\x01\x30\x00\x00\x00\x39\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x32\x33\x35\x36\x38\x39\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x33\x36\x30\x32\x34\x36\x35\x37\x30\x40\x71\x71\x2e\x63\x6f\x6d\x22\x7d',
                        },
            'xiaotianya' : {
                        'USERNAME' : '萧天涯',
                        'LOGIN_DATA' :    '\x00\x4c\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x37\x31\x34\x39\x36\x30\x38\x33\x00\x01\x30\x00\x00\x00\x34\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x6a\x70\x6a\x70\x6a\x70\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x70\x70\x40\x73\x69\x6e\x61\x2e\x63\x6f\x6d\x22\x7d',
                        },
            'zilong2' : {
                        'USERNAME' : '紫龙2',
                        'LOGIN_DATA' :
                        '\x00\x4e\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x39\x39\x34\x30\x35\x36\x30\x33\x00\x01\x30\x00\x00\x00\x36\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x6a\x70\x6a\x70\x6a\x70\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x70\x70\x70\x70\x40\x73\x69\x6e\x61\x2e\x63\x6f\x6d\x22\x7d',
                        },
            'zilong3' : {
                        'USERNAME' : '紫龙3',
                        'LOGIN_DATA' :
                        '\x00\x4f\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x39\x39\x34\x30\x35\x39\x33\x31\x00\x01\x30\x00\x00\x00\x37\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x6a\x70\x6a\x70\x6a\x70\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x70\x70\x70\x70\x70\x40\x73\x69\x6e\x61\x2e\x63\x6f\x6d\x22\x7d',
                        },
            'senjianfeng' : {
                        'USERNAME' : '沈剑封uu',
                        'LOGIN_DATA' :
                        '\x00\x51\x00\x05\x00\x03\x6e\x69\x6c\x00\x08\x36\x36\x36\x32\x33\x32\x37\x35\x00\x01\x30\x00\x00\x00\x39\x7b\x22\x4b\x4c\x5f\x50\x41\x53\x53\x57\x4f\x52\x44\x22\x3a\x22\x31\x31\x31\x31\x31\x31\x22\x2c\x22\x4b\x4c\x5f\x50\x41\x53\x53\x50\x4f\x52\x54\x22\x3a\x22\x32\x36\x33\x37\x39\x32\x33\x37\x34\x40\x71\x71\x2e\x63\x6f\x6d\x22\x7d',
                        },
    }

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
        'liubang' : '52474',
        'hanxin' : '52491',
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
        'suidaran' : '67201307',
        'jianjianbiaoxie' : '64862103',
        'jbvcduj' : '66933947',
        'wangcencen' : '67115191',
        'lolo' : '66290987',
        'wangdaiman' : '63771615',
        'daofeiwang' : '66284359',
        'nihongxiuse' : '65642323',
        'vmao' : '64726651',
        'senniu' : '64401019',
        'bohe' : '69681303',
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
        'wu' : '101',
        'jianye' : '102',
        'jiangxia' : '107',
        'jiangling' : '108',
        'runan' : '109',
        'beiping' : '201',
        'nanpi' : '202',
        'wan' : '208',
        'xuzou' : '210',
        'zitong' : '305',
        'tiansui' : '306',
        'hanzong' : '307',
        'sangyong' : '308',
        'xinye' : '309',
        'xiangyang' : '310',
        'wuling' : '311',
        'test' : '209',
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
        'chengqiang' : '213',
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
        #'zuceng',
        'junji',
        'jiaocang',
        'jiaocang2',
        'sangdian',
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
        103 : 1044000,
        104 : 1080000,
        105 : 1116000,
        106 : 1152000,
        107 : 1188000,
        108 : 1224000,
        109 : 1260000,
        110 : 1296000,
}

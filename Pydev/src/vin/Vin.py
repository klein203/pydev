'''
Created on 2017年7月7日

@author: xusheng
'''

import re
from vin import Tree, TreePlotter

def splitLineCol(line):
    dataset = line.split(',')
    return dataset

def msg(code):
    msgDict = {
        0: 'success', 
        1000: 'vin length or character error', 
        1001: 'vin wmi error', 
        1002: 'vin checksum error', 
        1003: 'modelid is null'
    }
    return msgDict[code]

def checkValidWMI(wmi):
    wmiDict = {
        'AAV': 'Volkswagen South Africa', 
        'AC5': 'Hyundai South Africa', 
        'ADD': 'Hyundai South Africa', 
        'AFA': 'Ford South Africa', 
        'AHT': 'Toyota South Africa', 
        'JA3': 'Mitsubishi', 
        'JA4': 'Mitsubishi', 
        'JA': 'Isuzu', 
        'JD': 'Daihatsu', 
        'JF': 'Fuji Heavy Industries (Subaru)', 
        'JH': 'Honda', 
        'JK': 'Kawasaki (motorcycles)', 
        'JL5': 'Mitsubishi Fuso', 
        'JMB': 'Mitsubishi Motors', 
        'JMY': 'Mitsubishi Motors', 
        'JMZ': 'Mazda', 
        'JN': 'Nissan', 
        'JS': 'Suzuki', 
        'JT': 'Toyota', 
        'JY': 'Yamaha (motorcycles)', 
        'KL': 'Daewoo General Motors South Korea', 
        'KM': 'Hyundai', 
        'KMY': 'Daelim (motorcycles)', 
        'KM1': 'Hyosung (motorcycles)', 
        'KN': 'Kia', 
        'KNM': 'Renault Samsung', 
        'KPA': 'SsangYong', 
        'KPT': 'SsangYong', 
        'LAN': 'Changzhou Yamasaki Motorcycle', 
        'LBB': 'Zhejiang Qianjiang Motorcycle (Keeway/Generic)', 
        'LBE': 'Beijing Hyundai', 
        'LBM': 'Zongshen Piaggio', 
        'LBP': 'Chongqing Jainshe Yamaha (motorcycles)', 
        'LB2': 'Geely Motorcycles', 
        'LCE': 'Hangzhou Chunfeng Motorcycles (CFMOTO)', 
        'LDC': 'Dong Feng Peugeot Citroen (DPCA), China', 
        'LDD': 'Dandong Huanghai Automobile', 
        'LDN': 'SouEast Motor', 
        'LDY': 'Zhongtong Coach, China', 
        'LET': 'Jiangling-Isuzu Motors, China', 
        'LE4': 'Beijing Benz, China', 
        'LFB': 'FAW, China (busses)', 
        'LFG': 'Taizhou Chuanl Motorcycle Manufacturing', 
        'LFP': 'FAW, China (passenger vehicles)', 
        'LFT': 'FAW, China (trailers)', 
        'LFV': 'FAW-Volkswagen, China', 
        'LFW': 'FAW JieFang, China', 
        'LFY': 'Changshu Light Motorcycle Factory', 
        'LGB': 'Dong Feng (DFM), China', 
        'LGH': 'Qoros (formerly Dong Feng (DFM)), China', 
        'LGX': 'BYD Auto, China', 
        'LHB': 'Beijing Automotive Industry Holding', 
        'LH1': 'FAW-Haima, China', 
        'LJC': 'JAC, China', 
        'LJ1': 'JAC, China', 
        'LKL': 'Suzhou King Long, China', 
        'LL6': 'Hunan Changfeng Manufacture Joint-Stock', 
        'LL8': 'Linhai (ATV)', 
        'LMC': 'Suzuki Hong Kong (motorcycles)', 
        'LPR': 'Yamaha Hong Kong (motorcycles)', 
        'LSG': 'Shanghai General Motors, China', 
        'LSJ': 'MG Motor UK Limited - SAIC Motor, Shanghai, China', 
        'LSV': 'Shanghai Volkswagen, China', 
        'LSY': 'Brilliance Zhonghua', 
        'LTV': 'Toyota Tian Jin', 
        'LUC': 'Guangqi Honda, China', 
        'LVS': 'Ford Chang An', 
        'LVV': 'Chery, China', 
        'LVZ': 'Dong Feng Sokon Motor Company (DFSK)', 
        'LZM': 'MAN China', 
        'LZE': 'Isuzu Guangzhou, China', 
        'LZG': 'Shaanxi Automobile Group, China', 
        'LZP': 'Zhongshan Guochi Motorcycle (Baotian)', 
        'LZY': 'Yutong Zhengzhou, China', 
        'LZZ': 'Chongqing Shuangzing Mech & Elec (Howo)', 
        'L4B': 'Xingyue Group (motorcycles)', 
        'L5C': 'KangDi (ATV)', 
        'L5K': 'Zhejiang Yongkang Easy Vehicle', 
        'L5N': 'Zhejiang Taotao, China (ATV & motorcycles)', 
        'L5Y': 'Merato Motorcycle Taizhou Zhongneng', 
        'L85': 'Zhejiang Yongkang Huabao Electric Appliance', 
        'L8X': 'Zhejiang Summit Huawin Motorcycle', 
        'MAB': 'Mahindra & Mahindra', 
        'MAC': 'Mahindra & Mahindra', 
        'MAJ': 'Ford India', 
        'MAK': 'Honda Siel Cars India', 
        'MAL': 'Hyundai', 
        'MAT': 'Tata Motors', 
        'MA1': 'Mahindra & Mahindra', 
        'MA3': 'Suzuki India (Maruti)', 
        'MA6': 'GM India', 
        'MA7': 'Mitsubishi India (formerly Honda)', 
        'MBH': 'Suzuki India (Maruti)', 
        'MBJ': 'Toyota India', 
        'MBR': 'Mercedes-Benz India', 
        'MB1': 'Ashok Leyland', 
        'MCA': 'Fiat India', 
        'MCB': 'GM India', 
        'MC2': 'Volvo Eicher commercial vehicles limited.', 
        'MDH': 'Nissan India', 
        'MD2': 'Bajaj Auto', 
        'MEE': 'Renault India', 
        'MEX': 'Volkswagen India', 
        'MHF': 'Toyota Indonesia', 
        'MHR': 'Honda Indonesia', 
        'MLC': 'Suzuki Thailand', 
        'MLH': 'Honda Thailand', 
        'MMB': 'Mitsubishi Thailand', 
        'MMC': 'Mitsubishi Thailand', 
        'MMM': 'Chevrolet Thailand', 
        'MMT': 'Mitsubishi Thailand', 
        'MM8': 'Mazda Thailand', 
        'MNB': 'Ford Thailand', 
        'MNT': 'Nissan Thailand', 
        'MPA': 'Isuzu Thailand', 
        'MP1': 'Isuzu Thailand', 
        'MRH': 'Honda Thailand', 
        'MR0': 'Toyota Thailand', 
        'NLA': 'Honda Türkiye', 
        'NLE': 'Mercedes-Benz Türk Truck', 
        'NLH': 'Hyundai Assan', 
        'NLT': 'TEMSA', 
        'NMB': 'Mercedes-Benz Türk Buses', 
        'NMC': 'BMC', 
        'NM0': 'Ford Turkey', 
        'NM4': 'Tofaş Türk', 
        'NMT': 'Toyota Türkiye', 
        'NNA': 'Isuzu Turkey', 
        'PE1': 'Ford Phillipines', 
        'PE3': 'Mazda Phillipines', 
        'PL1': 'Proton, Malaysia', 
        'PNA': 'NAZA, Malaysia (Peugeot)', 
        'RFB': 'Kymco, Taiwan', 
        'RFG': 'Sanyang SYM, Taiwan', 
        'RFL': 'Adly, Taiwan', 
        'RFT': 'CPI, Taiwan', 
        'RF3': 'Aeon Motor, Taiwan', 
        'SAL': 'Land Rover', 
        'SAJ': 'Jaguar', 
        'SAR': 'Rover', 
        'SB1': 'Toyota UK', 
        'SBM': 'McLaren', 
        'SCA': 'Rolls Royce', 
        'SCB': 'Bentley', 
        'SCC': 'Lotus Cars', 
        'SCE': 'DeLorean Motor Cars N. Ireland (UK)', 
        'SCF': 'Aston', 
        'SDB': 'Peugeot UK (formerly Talbot)', 
        'SED': 'General Motors Luton Plant', 
        'SEY': 'LDV', 
        'SFA': 'Ford UK', 
        'SFD': 'Alexander Dennis UK', 
        'SHH': 'Honda UK', 
        'SHS': 'Honda UK', 
        'SJN': 'Nissan UK', 
        'SKF': 'Vauxhall', 
        'SLP': 'JCB Research UK', 
        'SMT': 'Triumph Motorcycles', 
        'SUF': 'Fiat Auto Poland', 
        'SUL': 'FSC (Poland)', 
        'SUP': 'FSO-Daewoo (Poland)', 
        'SUU': 'Solaris Bus & Coach (Poland)', 
        'TCC': 'Micro Compact Car AG (smart 1998-1999)', 
        'TDM': 'QUANTYA Swiss Electric Movement (Switzerland)', 
        'TK9': 'SOR buses (Czech Republic)', 
        'TMA': 'Hyundai Motor Manufacturing Czech', 
        'TMB': 'Škoda (Czech Republic)', 
        'TMK': 'Karosa (Czech Republic)', 
        'TMP': 'Škoda trolleybuses (Czech Republic)', 
        'TMT': 'Tatra (Czech Republic)', 
        'TM9': 'Škoda trolleybuses (Czech Republic)', 
        'TNE': 'TAZ', 
        'TN9': 'Karosa (Czech Republic)', 
        'TRA': 'Ikarus Bus', 
        'TRU': 'Audi Hungary', 
        'TSE': 'Ikarus Egyedi Autobuszgyar, (Hungary)', 
        'TSM': 'Suzuki Hungary', 
        'TW1': 'Toyota Caetano Portugal', 
        'TYA': 'Mitsubishi Trucks Portugal', 
        'TYB': 'Mitsubishi Trucks Portugal', 
        'UU1': 'Renault Dacia, (Romania)', 
        'UU3': 'ARO', 
        'UU6': 'Daewoo Romania', 
        'U5Y': 'Kia Motors Slovakia', 
        'U6Y': 'Kia Motors Slovakia', 
        'VAG': 'Magna Steyr Puch', 
        'VAN': 'MAN Austria', 
        'VBK': 'KTM (Motorcycles)', 
        'VF1': 'Renault', 
        'VF2': 'Renault', 
        'VF3': 'Peugeot', 
        'VF4': 'Talbot', 
        'VF6': 'Renault (Trucks & Buses)', 
        'VF7': 'Citroën', 
        'VF8': 'Matra', 
        'VF9': 'Bugatti', 
        '795': 'Bugatti', 
        'VG5': 'MBK (motorcycles)', 
        'VLU': 'Scania France', 
        'VN1': 'SOVAB (France)', 
        'VNE': 'Irisbus (France)', 
        'VNK': 'Toyota France', 
        'VNV': 'Renault-Nissan', 
        'VSA': 'Mercedes-Benz Spain', 
        'VSE': 'Suzuki Spain (Santana Motors)', 
        'VSK': 'Nissan Spain', 
        'VSS': 'SEAT', 
        'VSX': 'Opel Spain', 
        'VS6': 'Ford Spain', 
        'VS7': 'Citroën Spain', 
        'VS9': 'Carrocerias Ayats (Spain)', 
        'VTH': 'Derbi (motorcycles)', 
        'VTL': 'Yamaha Spain (motorcycles)', 
        'VTT': 'Suzuki Spain (motorcycles)', 
        'VV9': 'TAURO Spain', 
        'VWA': 'Nissan Spain', 
        'VWV': 'Volkswagen Spain', 
        'VX1': 'Zastava / Yugo Serbia', 
        'WAG': 'Neoplan', 
        'WAU': 'Audi', 
        'WA1': 'Audi SUV', 
        'WBA': 'BMW', 
        'WBS': 'BMW M', 
        'WDA': 'Daimler', 
        'WDB': 'Mercedes-Benz', 
        'WDC': 'DaimlerChrysler', 
        'WDD': 'Mercedes-Benz', 
        'WDF': 'Mercedes-Benz (commercial vehicles)', 
        'WEB': 'Evobus GmbH (Mercedes-Bus)', 
        'WJM': 'Iveco Magirus', 
        'WF0': 'Ford Germany', 
        'WKK': 'Kässbohrer/Setra', 
        'WMA': 'MAN Germany', 
        'WME': 'smart', 
        'WMW': 'MINI', 
        'WMX': 'Mercedes-AMG', 
        'WP0': 'Porsche', 
        'WP1': 'Porsche SUV', 
        'W0L': 'Opel', 
        'W0V': 'Opel', 
        'WUA': 'quattro GmbH', 
        'WVG': 'Volkswagen MPV/SUV', 
        'WVW': 'Volkswagen', 
        'WV1': 'Volkswagen Commercial Vehicles', 
        'WV2': 'Volkswagen Bus/Van', 
        'WV3': 'Volkswagen Trucks', 
        'XLB': 'Volvo (NedCar)', 
        'XLE': 'Scania Netherlands', 
        'XLR': 'DAF (trucks)', 
        'XL9': 'Spyker', 
        '363': 'Spyker', 
        'XMC': 'Mitsubishi (NedCar)', 
        'XTA': 'Lada/AvtoVAZ (Russia)', 
        'XTC': 'KAMAZ (Russia)', 
        'XTH': 'GAZ (Russia)', 
        'XTT': 'UAZ/Sollers (Russia)', 
        'XTY': 'LiAZ (Russia)', 
        'XUF': 'General Motors Russia', 
        'XUU': 'AvtoTor (Russia, General Motors SKD)', 
        'XW8': 'Volkswagen Group Russia', 
        'XWB': 'UZ-Daewoo (Uzbekistan)', 
        'XWE': 'AvtoTor (Russia, Hyundai-Kia SKD)', 
        'X1M': 'PAZ (Russia)', 
        'X4X': 'AvtoTor (Russia, BMW SKD)', 
        'X7L': 'Renault AvtoFramos (Russia)', 
        'X7M': 'Hyundai TagAZ (Russia)', 
        'YBW': 'Volkswagen Belgium', 
        'YB1': 'Volvo Trucks Belgium', 
        'YCM': 'Mazda Belgium', 
        'YE2': 'Van Hool (buses)', 
        'YH2': 'BRP Finland (Lynx snowmobiles)', 
        'YK1': 'Saab-Valmet Finland', 
        'YS2': 'Scania AB', 
        'YS3': 'Saab', 
        'YS4': 'Scania Bus', 
        'YTN': 'Saab NEVS', 
        'YT9': 'Koenigsegg', 
        '007': 'Koenigsegg', 
        'YU7': 'Husaberg (motorcycles)', 
        'YV1': 'Volvo Cars', 
        'YV4': 'Volvo Cars', 
        'YV2': 'Volvo Trucks', 
        'YV3': 'Volvo Buses', 
        'Y3M': 'MAZ (Belarus)', 
        'Y6D': 'Zaporozhets/AvtoZAZ (Ukraine)', 
        'ZAA': 'Autobianchi', 
        'ZAM': 'Maserati', 
        'ZAP': 'Piaggio/Vespa/Gilera', 
        'ZAR': 'Alfa Romeo', 
        'ZBN': 'Benelli', 
        'ZCG': 'Cagiva SpA / MV Agusta', 
        'ZCF': 'Iveco', 
        'ZDM': 'Ducati Motor Holdings SpA', 
        'ZDF': 'Ferrari Dino', 
        'ZD0': 'Yamaha Italy', 
        'ZD3': 'Beta Motor', 
        'ZD4': 'Aprilia', 
        'ZFA': 'Fiat', 
        'ZFC': 'Fiat V.I.', 
        'ZFF': 'Ferrari', 
        'ZGU': 'Moto Guzzi', 
        'ZHW': 'Lamborghini', 
        'ZJM': 'Malaguti', 
        'ZJN': 'Innocenti', 
        'ZKH': 'Husqvarna Motorcycles Italy', 
        'ZLA': 'Lancia', 
        'ZOM': 'OM', 
        'Z8M': 'Marussia (Russia)', 
        '1B3': 'Dodge', 
        '1C3': 'Chrysler', 
        '1C6': 'Chrysler', 
        '1D3': 'Dodge', 
        '1FA': 'Ford Motor Company', 
        '1FB': 'Ford Motor Company', 
        '1FC': 'Ford Motor Company', 
        '1FD': 'Ford Motor Company', 
        '1FM': 'Ford Motor Company', 
        '1FT': 'Ford Motor Company', 
        '1FU': 'Freightliner', 
        '1FV': 'Freightliner', 
        '1F9': 'FWD Corp.', 
        '1G': 'General Motors USA', 
        '1GC': 'Chevrolet Truck USA', 
        '1GT': 'GMC Truck USA', 
        '1G1': 'Chevrolet USA', 
        '1G2': 'Pontiac USA', 
        '1G3': 'Oldsmobile USA', 
        '1G4': 'Buick USA', 
        '1G6': 'Cadillac USA', 
        '1G8': 'Saturn USA', 
        '1GM': 'Pontiac USA', 
        '1GY': 'Cadillac USA', 
        '1H': 'Honda USA', 
        '1HD': 'Harley-Davidson', 
        '1J4': 'Jeep', 
        '1L': 'Lincoln USA', 
        '1ME': 'Mercury USA', 
        '1M1': 'Mack Truck USA', 
        '1M2': 'Mack Truck USA', 
        '1M3': 'Mack Truck USA', 
        '1M4': 'Mack Truck USA', 
        '1M9': 'Mynatt Truck & Equipment', 
        '1N': 'Nissan USA', 
        '1NX': 'NUMMI USA', 
        '1P3': 'Plymouth USA', 
        '1R9': 'Roadrunner Hay Squeeze USA', 
        '1VW': 'Volkswagen USA', 
        '1XK': 'Kenworth USA', 
        '1XP': 'Peterbilt USA', 
        '1YV': 'Mazda USA (AutoAlliance International)', 
        '1ZV': 'Ford (AutoAlliance International)', 
        '2A4': 'Chrysler Canada', 
        '2BP': 'Bombardier Recreational Products', 
        '2B3': 'Dodge Canada', 
        '2B7': 'Dodge Canada', 
        '2C3': 'Chrysler Canada', 
        '2CN': 'CAMI', 
        '2D3': 'Dodge Canada', 
        '2FA': 'Ford Motor Company Canada', 
        '2FB': 'Ford Motor Company Canada', 
        '2FC': 'Ford Motor Company Canada', 
        '2FM': 'Ford Motor Company Canada', 
        '2FT': 'Ford Motor Company Canada', 
        '2FU': 'Freightliner', 
        '2FV': 'Freightliner', 
        '2FZ': 'Sterling', 
        '2G': 'General Motors Canada', 
        '2G1': 'Chevrolet Canada', 
        '2G2': 'Pontiac Canada', 
        '2G3': 'Oldsmobile Canada', 
        '2G4': 'Buick Canada', 
        '2HG': 'Honda Canada', 
        '2HK': 'Honda Canada', 
        '2HJ': 'Honda Canada', 
        '2HM': 'Hyundai Canada', 
        '2M': 'Mercury', 
        '2NV': 'Nova Bus Canada', 
        '2P3': 'Plymouth Canada', 
        '2T': 'Toyota Canada', 
        '2V4': 'Volkswagen Canada', 
        '2V8': 'Volkswagen Canada', 
        '2WK': 'Western Star', 
        '2WL': 'Western Star', 
        '2WM': 'Western Star', 
        '3C4': 'Chrysler Mexico', 
        '3D3': 'Dodge Mexico', 
        '3FA': 'Ford Motor Company Mexico', 
        '3FE': 'Ford Motor Company Mexico', 
        '3G': 'General Motors Mexico', 
        '3H': 'Honda Mexico', 
        '3JB': 'BRP Mexico (all-terrain vehicles)', 
        '3MD': 'Mazda Mexico', 
        '3MZ': 'Mazda Mexico', 
        '3N': 'Nissan Mexico', 
        '3P3': 'Plymouth Mexico', 
        '3VW': 'Volkswagen Mexico', 
        '4F': 'Mazda USA', 
        '4JG': 'Mercedes-Benz USA', 
        '4M': 'Mercury', 
        '4RK': 'Nova Bus USA', 
        '4S': 'Subaru-Isuzu Automotive', 
        '4T': 'Toyota', 
        '4T9': 'Lumen Motors', 
        '4UF': 'Arctic Cat Inc.', 
        '4US': 'BMW USA', 
        '4UZ': 'Frt-Thomas Bus', 
        '4V1': 'Volvo', 
        '4V2': 'Volvo', 
        '4V3': 'Volvo', 
        '4V4': 'Volvo', 
        '4V5': 'Volvo', 
        '4V6': 'Volvo', 
        '4VL': 'Volvo', 
        '4VM': 'Volvo', 
        '4VZ': 'Volvo', 
        '538': 'Zero Motorcycles (USA)', 
        '5F': 'Honda USA-Alabama', 
        '5L': 'Lincoln', 
        '5N1': 'Nissan USA', 
        '5NP': 'Hyundai USA', 
        '5T': 'Toyota USA - trucks', 
        '5YJ': 'Tesla Motors', 
        '6AB': 'MAN Australia', 
        '6F4': 'Nissan Motor Company Australia', 
        '6F5': 'Kenworth Australia', 
        '6FP': 'Ford Motor Company Australia', 
        '6G1': 'General Motors-Holden (post Nov 2002)', 
        '6G2': 'Pontiac Australia (GTO & G8)', 
        '6H8': 'General Motors-Holden (splitLineCol Nov 2002)', 
        '6MM': 'Mitsubishi Motors Australia', 
        '6T1': 'Toyota Motor Corporation Australia', 
        '6U9': 'Privately Imported car in Australia', 
        '8AD': 'Peugeot Argentina', 
        '8AF': 'Ford Motor Company Argentina', 
        '8AG': 'Chevrolet Argentina', 
        '8AJ': 'Toyota Argentina', 
        '8AK': 'Suzuki Argentina', 
        '8AP': 'Fiat Argentina', 
        '8AW': 'Volkswagen Argentina', 
        '8A1': 'Renault Argentina', 
        '8GD': 'Peugeot Chile', 
        '8GG': 'Chevrolet Chile', 
        '935': 'Citroën Brazil', 
        '936': 'Peugeot Brazil', 
        '93H': 'Honda Brazil', 
        '93R': 'Toyota Brazil', 
        '93U': 'Audi Brazil', 
        '93V': 'Audi Brazil', 
        '93X': 'Mitsubishi Motors Brazil', 
        '93Y': 'Renault Brazil', 
        '94D': 'Nissan Brazil', 
        '9BD': 'Fiat Brazil', 
        '9BF': 'Ford Motor Company Brazil', 
        '9BG': 'Chevrolet Brazil', 
        '9BM': 'Mercedes-Benz Brazil', 
        '9BR': 'Toyota Brazil', 
        '9BS': 'Scania Brazil', 
        '9BW': 'Volkswagen Brazil', 
        '9FB': 'Renault Colombia', 
    }
    code = 0
    try:
        wmiDict[wmi]
    except KeyError:
        try:
            wmiDict[wmi[0:2]]
        except KeyError:
            code = 1001
    return code

def fullToHalf(s):
    ret = ''
    for uchar in s:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        ret += chr(inside_code)
    return ret

def vinMapping(ch):
    ret =  {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'J': 1, 'K': 2,
            'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9, 'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6,
            'X': 7, 'Y': 8, 'Z': 9}[ch]
    return ret

def calcVinWeight(vin):
    weight = [8, 7, 6, 5, 4, 3, 2, 10,  #skip 9
              9, 8, 7, 6, 5, 4, 3, 2]
    checksum = 0
    index = 0
    for i in vin:
#         print(weight[index])
        checksum = checksum + i * weight[index]
        index += 1
    mod = checksum % 11
    if mod == 0:
        ret = 'X'
    else:
        ret = str(mod)
    return ret

def checkValidCharacter(vin):
    code = 0
    regex = re.compile(r'^[\d|ABCDEFGHJKLMNPRSTUVWXYZ]{17}$')
    if regex.match(vin) == None:
        code = 1000
    return code 

def checkValidVin(vin):
    code = checkValidCharacter(vin)
    if code == 0:
        uppercase_vin = vin.upper()
        code = checkValidWMI(uppercase_vin[0:3])
        if code == 0:
            check_vin = uppercase_vin[0:8] + uppercase_vin[9:17]  #skip #9
            try:
                checksum = calcVinWeight(list(map(vinMapping, check_vin)))
            except BaseException as e:
                print('%s, %s' % (vin, e))
            if checksum != uppercase_vin[8]:
                code = 1002
            
    return code

def splitVinFeatures(s):
    vinFeatures = []
    vinFeatures.append(s[0:3])    # WMI
    vinFeatures.append(s[3:9])    # VDS
    vinFeatures.append(s[9])  # year
    vinFeatures.append(s[10]) # assembler
#     print(vinFeatures)
    return vinFeatures

def createDataSet():
    sourcefilename = 'd:/tmp/result_small.txt'
    dataSet = []
    with open(sourcefilename, 'r', encoding='utf-8') as fr:
        for line in fr.readlines():
            record = splitLineCol(line.strip())
            nFeatures = splitVinFeatures(record[3])
            nFeatures.append(record[1])
            dataSet.append(nFeatures)

#     col_labels = ['id', 'model_id', 'model_name', 'vin', 'del_flag', 'asset_id']
#     vin_labels = ['WMI', 'VDS', 'year', 'assembler']
    res_labels = ['WMI', 'VDS', 'year', 'assembler', 'model_id']
    return dataSet, res_labels

def dataPrepare():
    sourcefilename = 'd:/tmp/t_cust_vehicle.txt'
    resultfilename = 'd:/tmp/result.txt'
    errorfilename = 'd:/tmp/error.txt'
    total_line_cnt = 0
    valid_line_cnt = 0
    error_line_cnt = 0
    
    with open(resultfilename, 'w', encoding='utf-8') as fw:
        with open(errorfilename, 'w', encoding='utf-8') as ferw:
            with open(sourcefilename, 'r', encoding='utf-8') as fr:
                for line in fr.readlines():
                    record = splitLineCol(line.strip())
                    modelid = record[1] # mode_id
                    vin = fullToHalf(record[3].strip()) # vin
                    code = checkValidVin(vin)
                    if code == 0:
                        if modelid != '':
                            fw.write(line)
                            valid_line_cnt += 1
                        else:
                            code = 1003
                            ferw.write(msg(code) + ',' + line)
                            error_line_cnt += 1
                    else:
                        ferw.write(msg(code) + ',' + line)
                        error_line_cnt += 1
                    total_line_cnt += 1
                    if total_line_cnt % 10000 == 0:
                        print('total lines %d, valid lines %d, error %f%%' % (total_line_cnt, valid_line_cnt, 100.0*error_line_cnt/total_line_cnt))
    print('total lines %d, valid lines %d, error %.2f%%' % (total_line_cnt, valid_line_cnt, 100.0*error_line_cnt/total_line_cnt))
    print('done!')

def createTree(filename):
    dataSet, labels = createDataSet()
    print('dataset done!')

    tree = Tree.createTree(dataSet, labels)
    print('tree done!')
    
    Tree.storeTree(tree, filename)
    print('all done!')

def loadTree(filename):
    tree = Tree.grabTree(filename)
    print('tree done!')
    
    TreePlotter.createPlot(tree)
    print('plot done!')

if __name__ == '__main__':
    filename = 'd:/tmp/vintree.pickle' 
#     dataPrepare()
    loadTree(filename)
    
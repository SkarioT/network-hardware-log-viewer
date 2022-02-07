import os
import sys
import telnetlib
import time
import datetime
import socket

# универсальные или персональный креды.
USER='username\n'
PSWD='drowssap'

comand_index=""

commutator_list='S2995','Q3470','ZY3528','ZY3500','S2989','S2900','D5960','D5750','D4650','D4600','D3650','D3950','Z5250','Z5260','Z5900','Z5928','P2610','P2620','P2626','P2650','Z2900','D3000','D1210','A6224'
DCN_commutator_list='Q3470','D5960','D5750','D4650','D4600','D3650','D3950'


#функция разукрашивает результат выполнения, для большей наглядности
def colorator(output,td,port='23:34'):

    output=output.replace('gei-0/1/1/{}'.format(str(port)),'\033[32mgei-0/1/1/{}\033[0m'.format(str(port)))
    output=output.replace('Ethernet1/{}'.format(str(port)),'\033[32mEthernet1/{}\033[0m'.format(str(port)))
    output=output.replace('Ethernet0/0/{}'.format(str(port)),'\033[32mEthernet0/0/{}\033[0m'.format(str(port)))
    output=output.replace('Ethernet1/0/{}'.format(str(port)),'\033[32mEthernet1/0/{}\033[0m'.format(str(port)))
    output=output.replace('port {}'.format(str(port)),'\033[32mport {}\033[0m'.format(str(port)))

    output=output.replace("No limited group number on this port!","IGMP запросы для данного порта отсутствуют!")
    output=output.replace(" VCT can't perform on disabled port!","Нет возможности выполнить прозвон на отключенном порту!")

    output=output.replace("ip multicast destination-control access-group","\033[32mip multicast destination-control access-group : \033[0m")

    output=output.replace("enabled","\033[32menabled\033[0m")
    output=output.replace("6002","\033[32m6002\033[0m")
    output=output.replace("6004","\033[32m6004\033[0m")
    output=output.replace(" Up","\033[32m Up\033[0m")
    output=output.replace(" up","\033[32m up\033[0m")
    output=output.replace("/UP","\033[32m/UP\033[0m")
    output=output.replace(" UP","\033[32m UP\033[0m")
    output=output.replace("full ","\033[32mfull\033[0m")
    output=output.replace("100Mbps","\033[32m100Mbps\033[0m")
    output=output.replace("100M","\033[32m100M\033[0m")
    output=output.replace("linkup","\033[32mlinkup\033[0m")
    output=output.replace("Test Passed. No problem found.","\033[32mTest Passed. No problem found.\033[0m")

    output=output.replace("6000","\033[31m6000\033[0m")
    output=output.replace("Cable is open.","\033[31mCable is open.\033[0m")
    output=output.replace("violation rate.","\033[31m!!! VIOLATION RATE !!!\033[0m")
    output=output.replace(" Loop ","\033[31m Loop\033[0m")
    output=output.replace("abnormal","\033[31mabnormal\033[0m")
    output=output.replace("10Mbps","\033[31m10Mbps\033[0m")
    output=output.replace("10M","\033[31m10M\033[0m")
    output=output.replace(" Down","\033[31m Down\033[0m")
    output=output.replace(" DOWN","\033[31m DOWN\033[0m")
    output=output.replace("/DOWN","\033[31m/DOWN\033[0m")
    output=output.replace(" down","\033[31m down\033[0m")
    output=output.replace(" half","\033[31m half\033[0m")
    output=output.replace("CrcError","\033[31mCrcError\033[0m")
    output=output.replace("InMACRcvErr","\033[31mInMACRcvErr\033[0m")
    output=output.replace("linkdown","\033[31mlinkdown\033[0m")
    output=output.replace("blackhole","\033[31mblackhole\033[0m")
    output=output.replace("changed state to DOWN","\033[31mchanged state to DOWN\033[0m")
    output=output.replace("changed state to UP","\033[32mchanged state to UP\033[0m")
    output=output.replace("error","\033[31mERROR\033[0m")
    output=output.replace("ERROR","\033[31mERROR\033[0m")
    output=output.replace("CRC","\033[31mCRC\033[0m")
    output=output.replace("192.168.","\033[31m192.168.\033[0m")

    return str(output)+'\n'+'-'*80+"\n\033[31mВыполнено за : "+str(td)+' seconds !'+'\n\033[0m'


#функция для работы с оптическим оборудованинем( OLT <=> ONU)
def olt_onu_viewer(sn,olt_name_ip,command='0',card=0,port=0,vport=0):
    cdt=datetime.datetime.now()
    print('Connection to OLT {}'.format(olt_name_ip))
    print('-'*80)
    korch_olt = "10.227.128.35","MI-MIN269-OLT-2","MI-MIN269-OLT-1","10.227.128.34","10.227.128.130","fa-mi-uzbor2-olt-c610-1"
    if olt_name_ip in korch_olt :
        USER='логин для специфических железок'
        PSWD='пароль для специфических железок'
    else:
        USER="логин для типовых специфических железок"
        PSWD="пароль для типовых специфических железок"

    with telnetlib.Telnet(olt_name_ip,23,30) as t:
        t.write(USER.encode())
        t.write(b'\n')
        time.sleep(1)
        t.write(PSWD.encode()[::-1])
        t.write(b'\n')
        #блок команд
        SHOW_ONU="sh gpon onu state gpon-olt_1/{}/{}\n".format(card,port)
        SHOW_ONU_new="sh gpon onu state gpon_olt-1/{}/{}\n".format(card,port)
        SHOW_MAC="show mac gpon onu gpon-onu_1/{}/{}:{}\n".format(card,port,vport)
        SHOW_IP_MAC="show ip dhcp snooping dynamic port pon gpon-onu_1/{}/{}:{} vport 1\n".format(card,port,vport)
        SHOW_IP_MAC_new="show ip dhcp snooping dynamic port pon gpon_onu-1/{}/{}:{} vport 1\n".format(card,port,vport)
        SHOW_IPGM_LOG="show igmp log interface gpon-onu_1/{}/{}:{}\n".format(card,port,vport)
        SHOW_IPGM_LOG_new="show igmp log interface gpon_onu-1/{}/{}:{}\n".format(card,port,vport)
        ONU_UNCONFIG="show pon onu uncfg"
        ONU_FIND="sho gpon onu by sn {}\n".format(sn)
        SHOW_GPON_STAT="show gpon remote-onu interface pon gpon-onu_1/{}/{}:{}\n".format(card,port,vport)
        SHOW_GPON_STAT_new="show gpon remote-onu interface pon gpon_onu-1/{}/{}:{}\n".format(card,port,vport)
        SHOW_ETHER_STAT="show gpon remote-onu interface eth gpon-onu_1/{}/{}:{} eth_0/1\n".format(card,port,vport)
        SHOW_ETHER_STAT_new="show gpon remote-onu interface eth gpon_onu-1/{}/{}:{} eth_0/1\n".format(card,port,vport)
        onu_stat_info="""
        Описаниние состояний:
        Phase State - working - оптический порт на ONU работает
        Phase State - LOS - оптический линк не подключен
        Phase State - DyingGasp - ONU выключено (нет питания/выключено кнопкой).
        Phase State - Logging, syncMib - идет процесс установки связи между OLT и ONU"""
        info_gpon=" \n \033[32mRx optical level по стандарту (Class SFP B+) не должен быть меньше -28dBm\033[0m \n"
        #show pon onu information gpon-olt_1/2/4 || прост всех онух зареганых на конкретный кард/порт
        #show pon olt config || прост активных кардов
        #show gpon onu state || состояние всех ону
        #show gpon onu state gpon-olt_1/2/5 || просмотс состояние ону на кокретном карт/порт
        if command=='1':
            time.sleep(0.5)
            t.write(SHOW_ONU.encode())
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)

            res = t.read_very_eager().decode('ascii')
            if "Invalid input detected" in res:
                time.sleep(0.5)
                t.write(SHOW_ONU_new.encode())
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                res = t.read_very_eager().decode('ascii')
            
            res=res+'\n'+onu_stat_info
            res=res.replace("working","\033[32mworking\033[0m")
            res=res.replace("LOS","\033[31mLOS\033[0m")
            res=res.replace("OffLine","\033[31mOffLine\033[0m")
            res=res.replace("DyingGasp","\033[33mDyingGasp\033[0m")
            res=res.replace("Logging, syncMib","\u001b[35;1mLogging, syncMib\033[0m")
            
        if command=='2':
            time.sleep(0.5)
            t.write(SHOW_IP_MAC.encode())
            t.write(b'\n')
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)
            t.write(b' ')
            time.sleep(0.5)
            res = t.read_very_eager().decode('ascii')
            if "Invalid input detected" in res:
                time.sleep(0.5)
                t.write(SHOW_IP_MAC_new.encode())
                t.write(b'\n')
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                t.write(b' ')
                time.sleep(0.5)
                res = t.read_very_eager().decode('ascii')
            res=res+'\n'
        if command=='3':
            time.sleep(0.5)
            t.write(SHOW_IPGM_LOG.encode())
            t.write(b'\n')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            t.write(b' ')
            time.sleep(0.1)
            res = t.read_very_eager().decode('ascii')
            if "Invalid input detected" in res:
                time.sleep(0.5)
                t.write(SHOW_IPGM_LOG_new.encode())
                t.write(b'\n')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                t.write(b' ')
                time.sleep(0.1)
                res = t.read_very_eager().decode('ascii')
            res=res+'\n'
            len_int=len(res)
            if int(len_int) < 1150:
                res=res+"\n \033[31mIGMP запросы с момента последней перезагрузки ONU, по текущий момент - не найдены.\033[0m"
            
        if command=='4':
            time.sleep(0.5)
            t.write(ONU_UNCONFIG.encode())
            t.write(b'\n')
            time.sleep(0.5)
            if len(sn)!=0:
                res1 = t.read_very_eager().decode('ascii')
                t.write(ONU_FIND.encode())
                t.write(b'\n')
                time.sleep(0.5)
                strr="for {} ".format(sn)
                res2 = t.read_very_eager().decode('ascii')
                res2=res2.replace("Search result","Search result {}".format(strr)).replace("-",'')
                if "GPONSRV" not in res2:
                    res2=res2.replace(":",'\033[32m virtual_port:\033[0m')
                res2=res2.replace(sn,'\033[32m{}\033[0m'.format(sn))
                res=res1+res2
                res=res.replace("{}".format(sn),"\033[032m{}\033[0m".format(sn)).replace('No related information to show.','\033[031mNo related information to show for\033[0m \033[032m{}\033[0m'.format(sn))
            else:
                res = t.read_very_eager().decode('ascii')
                res=res.replace("ZTEGC","\033[031mZTEGC\033[0m")
                res=res.replace("GC","\033[031mGC\033[0m")
            res=res.replace("_1/","\033[032m card:\033[0m")
            res=res.replace("N/A","N\A")
            res=res.replace("/","\033[032m port:\033[0m")
        if command=='5':
            time.sleep(0.5)
            t.write(SHOW_GPON_STAT.encode())
            t.write(b'\n')
            time.sleep(0.5)
            res1 = t.read_very_eager().decode('ascii')
            if "Invalid input detected" in res1:
                time.sleep(0.5)
                t.write(SHOW_GPON_STAT_new.encode())
                t.write(b'\n')
                time.sleep(0.5)
                res1 = t.read_very_eager().decode('ascii')
            t.write(SHOW_ETHER_STAT.encode())
            t.write(b'\n')
            time.sleep(0.5)
            res2 = t.read_very_eager().decode('ascii')
            if "Invalid input detected" in res2:
                t.write(SHOW_ETHER_STAT_new.encode())
                t.write(b'\n')
                time.sleep(0.5)
                res2 = t.read_very_eager().decode('ascii')
            res=res1+info_gpon+res2+'\n'
        res=('-'*80+'\n'+res+'\n'+'-'*80)
        res=res.replace("No related information to show.","\033[31m No related information to show. \033[0m")
    res=res.replace(' F601V6.0 ',' ZTE-F601 ')
    res=res.replace("Rx optical level:","\033[32mRx optical level:\033[0m")
    if "Invalid input detected" in res:
        return "\033[31mНа интерфейсе {}/{}/{} ничего нет. Просмотр невозможен.\033[0m".format(card,port,vport)
    cdt_n=datetime.datetime.now()

    return res[0:]+'\n'+'\033[31mВыполнено за : '+str(cdt_n-cdt)+' seconds'+'\n\033[0m'#

#функция проверяет доступность OLT
def OLT_check():
    print("Введите 'q' для завершения работы программы")

    OLT_name=input("Введите \033[031m IP-адрес OLT \033[0m для диагностики: ")
    print('Вы ввели',OLT_name)
    if OLT_name=='q' or OLT_name=='Q' or OLT_name=='й' or OLT_name=='Й':
        return 0
    first_clear=OLT_name.replace(' ','',10)
    OLT_name=first_clear.replace('\t','')

    active=os.system('ping {} -c 2'.format(OLT_name))
    if active==0:
        print("\n\033[032m Всё ок, OLT доступен \033[0m")
        return OLT_name
    else:
        print("\n\033[031m OLT не доступен. \033[0m")
        time.sleep(3)
        return 0

#функция проверяет корректность ввода
def getNumberCard ():
    while True:
        getNumber = input('Введите номер КАРДа(целое положительное число): ')  # Ввод числа
        if getNumber.isdigit() : 
            return getNumber

#функция проверяет корректность ввода
def getNumberPort ():
    while True:
        getNumber = input('Введите номер ПОРТа(целое положительное число): ')  # Ввод числа
        if getNumber.isdigit() : 
            return getNumber

#функция проверяет корректность ввода
def getNumberVPort():
    while True:
        getNumber = input('Введите номер ВИРТУАЛЬНО ПОРТа(целое положительное число): ')  # Ввод числа
        if getNumber.isdigit() : 
            return getNumber


#функция для работы с сетевым оборудованием (Ethernet,access)
def commutator_show(commutator_name,port_name,menu_id):
    os.system('cls' if os.name=='nt' else 'clear')
    upd_com=commutator_name[0]
    commutator_name=commutator_name[1]
    first_clear=commutator_name.replace(' ','',10)
    commutator_name=first_clear.replace('\t','',10)

    #'D3950','Z5260','Z2900','Z5900','A6224','P2610','P2626'
    if ('Q3470' in upd_com) or ('S2995' in upd_com)or ('S2989' in upd_com) or ('D3950' in upd_com) or ('S2900' in upd_com) or ('D3650' in upd_com) or ('D5750' in upd_com) or ('D4650' in upd_com) or ('D4600' in upd_com) or ('D5960' in upd_com):
        print('Connection to DCN device {} / {}'.format(upd_com,commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:
                ss= t.read_until(b'login:')
                t.write(USER.encode())
                time.sleep(0.1)
                ss=t.read_until(b'Password:')
                time.sleep(0.1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                time.sleep(0.1)
                
                #блок команд
                SHOW_LOGG='sh logg b l w'
                SHOW_LOG='show log'

                SHOW_PORT='sh int ether 1/{}'.format(port_name)
                SHOW_PORT_CONF='sh run in e 1/{}'.format(port_name)

                SHOW_PORT48='sh int ether 0/0/{}'.format(port_name)
                SHOW_PORT48_CONF='sh run in e 0/0/{}'.format(port_name)

                SHOW_PORT_D57='sh int ether 1/0/{}'.format(port_name)
                SHOW_PORT_D57_CONF='sh run in e 1/0/{}'.format(port_name)

                VCT='virtual-cable-test interface ethernet 1/{}'.format(port_name)
                VCT48='virtual-cable-test interface ethernet 0/0/{}'.format(port_name)
                VCT_D57='virtual-cable-test interface ethernet 1/0/{}'.format(port_name)
                LOOP='show loopback-detection'
                IGMP='sh ip igmp snooping'
                DHCP='sh ip dhcp snooping binding all'
                MAC_PORT='sh mac-address-table int eth 1/{}'.format(port_name)
                MAC_PORT48='sh mac-address-table int eth 0/0/{}'.format(port_name)
                MAC_D57='sh mac-address-table int eth 1/0/{}'.format(port_name)
                SH_MAC='sh mac-address-table add {}'.format(port_name)
                ALL_PORT='sh interface ethernet status'
                #11) быстрая диагностика
                if menu_id=='11':
                    #состоянии порта
                    time.sleep(0.5)
                    t.write(SHOW_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(SHOW_PORT_CONF.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    output_state = t.read_very_eager().decode('ascii')
                    if 'error!' in output_state:
                        time.sleep(0.5)
                        t.write(SHOW_PORT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(0.3)
                        t.write(b' ')
                        time.sleep(0.3)
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(SHOW_PORT48_CONF.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(1)
                        output_state = t.read_very_eager().decode('ascii')
                        if 'error!' in output_state:
                            time.sleep(1)
                            t.write(SHOW_PORT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(0.3)
                            t.write(b' ')
                            time.sleep(0.3)
                            t.write(b' ')
                            time.sleep(0.3)
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(SHOW_PORT_D57_CONF.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            output_state = t.read_very_eager().decode('ascii')
                            print("Получены данные о состояни порта")
                    time.sleep(1)
                    t.write(VCT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output_vct = t.read_very_eager().decode('ascii')
                    if 'error!' in output_vct:
                        time.sleep(1)
                        t.write(VCT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(4)
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        output = t.read_very_eager().decode('ascii')
                        if 'error!' in output_vct:
                            time.sleep(1)
                            t.write(VCT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            output_vct = t.read_very_eager().decode('ascii')
                    output_vct = output_vct.replace("doesn't support VCT!","\033[31m doesn't support VCT! \033[0m").replace("well","\033[32mWELL\033[0m").replace("open","\033[31mOPEN\033[0m")
                    print("Получены данные о прозвоне порта")
                    #igmp
                    time.sleep(1)
                    t.write(IGMP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    readd = t.read_very_eager().decode('ascii')
                    split_list=readd.split()
                    len_split=len(split_list)-2
                    vlan=split_list[len_split]

                    igmp='sh ip igmp snoop vlan {}'.format(vlan)

                    time.sleep(1)
                    t.write(igmp.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    output_igmp = t.read_very_eager().decode('ascii')
                    print("Получены данные о IGMP запросах по всем портам")
                    #DHCP
                    t.write(b' ')
                    time.sleep(1)
                    t.write(DHCP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    output_dhcp = t.read_very_eager().decode('ascii')
                    output_dhcp = output_dhcp.replace("-",":")
                    print("Получены данные DHCP")
                    return output_state+"\n"+output_vct+"\n"+output_igmp+"\n"+output_dhcp
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    time.sleep(1)
                    t.write(SHOW_LOGG.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.3)
                    t.write(b' ')
                    time.sleep(0.5)
                    print("Блок команд выполнился")
                    output=t.read_very_eager().decode('ascii')
                    if 'Invalid input detected' in output:
                        time.sleep(1)
                        t.write(SHOW_LOG.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        t.write(b' ')
                        time.sleep(0.1)
                        output=t.read_very_eager().decode('ascii')
                    return output
                #2)просмотр порта
                if menu_id=='2':
                    time.sleep(0.5)
                    t.write(SHOW_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(SHOW_PORT_CONF.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    if 'error!' in output:
                        time.sleep(0.5)
                        t.write(SHOW_PORT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(b' ')
                        time.sleep(0.5)
                        t.write(SHOW_PORT48_CONF.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(2)
                        output = t.read_very_eager().decode('ascii')
                        if 'error!' in output:
                            time.sleep(1)
                            t.write(SHOW_PORT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(b' ')
                            time.sleep(0.5)
                            t.write(SHOW_PORT_D57_CONF.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            output = t.read_very_eager().decode('ascii')
                    return output
                #3)прозвон порта
                if menu_id=='3':
                    time.sleep(1)
                    t.write(VCT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    if 'error!' in output:
                        time.sleep(1)
                        t.write(VCT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        output = t.read_very_eager().decode('ascii')
                        if 'error!' in output:
                            time.sleep(1)
                            t.write(VCT_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            output = t.read_very_eager().decode('ascii')
                    return output.replace("doesn't support VCT!","\033[31m doesn't support VCT! \033[0m").replace("well","\033[32mWELL\033[0m").replace("open","\033[31mOPEN\033[0m")
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    time.sleep(1)
                    t.write(DHCP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    return output.replace("-",":")
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    time.sleep(1)
                    t.write(IGMP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    readd = t.read_very_eager().decode('ascii')
                    split_list=readd.split()
                    len_split=len(split_list)-2
                    vlan=split_list[len_split]

                    igmp='sh ip igmp snoop vlan {}'.format(vlan)

                    time.sleep(1)
                    t.write(igmp.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    out=t.read_very_eager().decode('ascii')
                    return out
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    time.sleep(1)
                    t.write(LOOP.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    return output
                #7)Просмотр мака на порту
                if menu_id=='7':
                    time.sleep(1)
                    t.write(MAC_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    if 'error!' in output:
                        time.sleep(1)
                        t.write(MAC_PORT48.encode())
                        t.write(b'\n')
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        t.write(b' ')
                        time.sleep(2)
                        output = t.read_very_eager().decode('ascii')
                        if 'error!' in output:
                            time.sleep(1)
                            t.write(MAC_D57.encode())
                            t.write(b'\n')
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            t.write(b' ')
                            time.sleep(2)
                            output = t.read_very_eager().decode('ascii')
                    return output.replace("No mac address found","\033[31m No mac address found =( \033[0m").replace("-",":")
                #8)
                if menu_id=='8':
                    time.sleep(1)
                    t.write(SH_MAC.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                    return output
                if menu_id=='9':
                    time.sleep(1)
                    t.write(ALL_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    output = t.read_very_eager().decode('ascii')
                    return output
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")

    if ('Z5250' in upd_com) or ('Z5260' in upd_com) or ('Z5900' in upd_com) or ('Z5928' in upd_com):
        print('Connection to ZTE 5-series  device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:

                ss= t.read_until(b'Username:')
                #input login
                t.write(USER.encode())
                t.read_until(b'Password:')
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                SHOW_LOGG='show logging alarm\n'
                SHOW_PORT='show interface gei-0/1/1/{}\n'.format(port_name)
                VCT='show vct interface gei-0/1/1/{}\n'.format(port_name)
                #LOOP='show loopback-detection\n'
                IGMP='show ip igmp snooping\n'
                DHCP='show ip dhcp snooping database\n'
                MAC_PORT='show mac table interface gei-0/1/1/{}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b'')
                    time.sleep(1)
                    output= t.read_very_eager().decode('ascii')
                    return output
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    return output
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    return output
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    output = t.read_very_eager().decode('ascii')
                    #new_module
                    j=1
                    index_index=0
                    index_mac=0
                    index_interface=0
                    index_vlan=0
                    index_ip=0
                    index_exp=0
                    index_op82=0
                    index_gw=0
                    all_port_str=""
                    temp_str=""
                    if len(output) < 100 :
                        res_str="IP ни кто не получил!!!"
                        return output+"\n"+res_str
                    split_output=output.split("\n")
                    count_target_line=split_output[2]
                    split_count_target_line=count_target_line.split(":")
                    count_iter=split_count_target_line[1]
                    
                    str_find_index_start=""
                    find_all_port=""
                    new_str=""
                    d_index = dict()
                    d_all_port=dict()

                    #полуаю индексы начал инфрмации по порту. набиваю словарь с началми индексов
                    while j < int(count_iter)+1:
                        find_index_start=output.find("Index   : {}".format(j))
                        d_index[j]=find_index_start
                        find_mac=output.find("MAC addr: ")
                        find_vlan=output.find("VLAN    :")
                        j+=1
                    j=1
                    #выбираю по индекс конкртные порты [ j(k) : j+1]. набиваю словарь фул инфой по порту
                    while j < int(count_iter)+1:
                        k=j
                        j+=1

                        if k==int(count_iter):
                                d_all_port[k]=output[ d_index[k]: ].replace("\n","").replace("\x08","").replace("\r","").replace("\t","").replace("--More--","")
                        elif j>int(count_iter):
                                pass
                        else:
                                d_all_port[k]=output[ d_index[k]:d_index[j] ].replace("\n","").replace("\x08","").replace("\r","").replace("\t","").replace("--More--","")

                    j=1
                    
                    #print("d_all_port : ",d_all_port)
                    while j < int(count_iter)+1:
                        # print("j = ",j)
                        all_port_str=d_all_port[j]
                        #полуаю индексы всех параметров, по каждому порту
                        index_index=all_port_str.find("Index   :")
                        index_mac=all_port_str.find("MAC addr:")
                        index_vlan=all_port_str.find("VLAN    :")
                        index_layer=all_port_str.find("Layer        : ")
                        index_interface =all_port_str.find("Interface    :")
                        index_op82=all_port_str.find(" Option82     :")
                        index_ip=all_port_str.find("IP addr      :")
                        index_exp=all_port_str.find("Expiration :")
                        index_gw=all_port_str.find(" Gateway IP :")
                        #получаю конечно значение параметра
                        index_=(all_port_str[index_index : index_mac ]).replace("Index   : ","")
                        # print("index:",index_)
                        mac_=(all_port_str[index_mac : index_vlan ]).replace("MAC addr: ","")
                        # print("mac:",mac_)
                        vlan_=(all_port_str[index_vlan : index_layer ]).replace("VLAN    : ","")
                        # print("vlan",vlan_)
                        interface_=(all_port_str[index_interface : index_op82]).replace("Interface    : ","").replace("\t","")
                        # print("interface_",interface_)
                        ip_=(all_port_str[index_ip : index_exp]).replace("IP addr      : ","")
                        # print("ip_",ip_)
                        expir_=(all_port_str[index_exp : index_gw]).replace("Expiration : ","")
                        # print("exp:",expir_)
                        temp_str= index_ +"\t"+ interface_ +"\t"+ mac_ +"\t"+ ip_ +"\t"+ expir_ +"\t"+ vlan_ 
                        # print("temp_str!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:",temp_str)
                        j+=1
                        new_str+=temp_str+"\n"
                        temp_str=""
                        # print(new_str)

                    res_str="Index\tInterface\tMAC\t\tIP\t\t\tExpiration\tVLAN\n"+new_str
                    
                    return output+"\n"+res_str
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    t.write(b' ')
                    time.sleep(0.1)
                    out=t.read_very_eager().decode('ascii')
                    return out.replace("--More--","")
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    output='на коммутатораз ZTE нет проверки на кольцо'
                    return output
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    return output
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")
    if ('P2650' in upd_com) or ('P2620' in upd_com) or ('P2610' in upd_com) or ('P2626' in upd_com):
        print('Connection to PROCURVE device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:
                t.write(b'\n')
                time.sleep(0.5)
                t.write(b' supportscript\n')
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                SHOW_LOGG='show log por -r'
                SHOW_PORT='show int {}\n'.format(port_name)
                SHOW_CONF='show config\n'
                #VCT='show vct interface gei-0/1/1/{}\n'.format(port_name)
                LOOP='show loop-protect\n'
                IGMP='show ip igmp\n'
                DHCP='show dhcp-snooping binding\n'
                MAC_PORT='show mac-address ethernet {}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    time.sleep(1)
                    print("Просмотр последних данных в  логе коммутатора")
                    t.write(SHOW_LOGG.encode())
                    time.sleep(0.5)
                    t.write(b'\n')
                    time.sleep(1.5)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    output= t.read_very_eager().decode('ascii')
                    t.close()
                    log_poz_start = output.find("Keys")
                    resault = output[log_poz_start:]
                    return resault
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    t.write(b'\n')
                    time.sleep(2)
                    output1 = t.read_very_eager().decode('ascii')
                    time.sleep(2)
                    t.write(b' ')
                    t.write(SHOW_CONF.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    output2 = t.read_very_eager().decode('ascii')
                    port_poz_start=output2.find("interface {}".format(port_name))
                    res_start=output2[port_poz_start:]
                    port_poz_fin_id=res_start.find("exit")
                    port_poz_fin=port_poz_start+port_poz_fin_id
                    output2=output2[port_poz_start:port_poz_fin]
                    output2=output2.replace("interface","port")
                    resault = output1+"\n"+output2
                    # return resault
                    os.system('clear')
                    try:
                        comand_index = resault.index("Status and Counters")
                        return resault[comand_index:]
                    except:
                        return resault
                    # print("index SHOW_PORT",comand_index)
                #3)прозвон порта
                if menu_id=='3':
                    output='Procurve - этим всё сказано.\nПрозвон не доступен'
                    return output
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    t.close()
                    return output
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(1.8)
                    t.write(b' ')
                    time.sleep(1.8)
                    t.write(b' ')
                    time.sleep(1.8)
                    t.write(b' ')
                    time.sleep(1.8)
                    resault =t.read_very_eager().decode('ascii')
                    # print("print resault:\n",resault)
                    t.close()
                    comand_index1 = resault.index("VLAN ID : 17")
                    resault = resault[comand_index1:]
                    # comand_index2 = resault.index("VLAN ID : 1")
                    # resault = resault[:comand_index2]
                    return resault
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    t.close()
                    return output
                #7)Просмотр мака на порту
                if menu_id=='7':
                    print("функция зашла в передачу команды")
                    t.write(MAC_PORT.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                    t.close()
                    return output
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")
    if ('Z2900' in upd_com):

        print('Connection to ZTE device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                SHOW_LOGG='show terminal log\n'
                SHOW_PORT='show port {}\n'.format(port_name)
                SHOW_PORT2='show port {} statistics\n'.format(port_name)
                SHOW_PORT_IGMP='show igmp snooping port {}\n'.format(port_name)
                #show iptv rule port 17 package
                VCT='show vct port {}\n'.format(port_name)
                LOOP='show loopdetect\n'
                IGMP='show igmp snooping\n'
                DHCP='show dhcp snooping binding\n'
                MAC_PORT='show fdb port {} detail\n'.format(port_name)
                port_name=str(port_name).replace(':','.')
                MAC_FIND='show fdb mac {}\n'.format(port_name)
                ALL_PORT='show port 1-20 brief\n'
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    output = t.read_very_eager().decode('ascii')
                    return output[150:]
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(SHOW_PORT2.encode())
                    t.write(b' ')
                    time.sleep(1)
                    t.write(SHOW_PORT_IGMP.encode())
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                    return output[140:]
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(10)
                    output = t.read_very_eager().decode('ascii')
                    return output[140:]
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    output = t.read_very_eager().decode('ascii')
                    return output[150:]
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(0.5)
                    out1=t.read_very_eager().decode('ascii')
                    out_1=out1[150:].split(' ')
                    ss=out_1[63].split(',')
                    vlan=ss[1]
                    time.sleep(0.5)
                    igmp_vlan='show igmp snooping vlan {}\n'.format(vlan)

                    t.write(igmp_vlan.encode())
                    time.sleep(0.5)
                    out2=t.read_very_eager().decode('ascii')
                    return str(out1)+'\n'+out2
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                # output='на коммутатораз ZTE нет проверки на кольцо'
                    return output
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    output = t.read_very_eager().decode('ascii')
                    return output[140:].replace(".",":")  
                if menu_id=='8':
                    print("мак для поиска:",port_name)
                    t.write(MAC_FIND.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    output = t.read_very_eager().decode('ascii')
                    return output[140:].replace(".",":")                
                if menu_id=='9':
                    t.write(ALL_PORT.encode())
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    t.write(b' ')
                    time.sleep(0.5)
                    output = t.read_very_eager().decode('ascii')
                    output = output.replace(".",':')
                    return output[140:]                
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")
    if ('D3000' in upd_com):

        print('Connection to D-link device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                SHOW_LOGG='show log\n'
                SHOW_PORT='show error ports {}\n'.format(port_name)
                VCT='cable_diag ports {}\n'.format(port_name)
                LOOP='show loopdetect ports 1-13\n'
                LOOP2='show loopdetect ports 14-28\n'
                IGMP='show igmp_snooping group\n'
                DHCP='show address_binding ip_mac all\n'
                DHCP2='show address_binding dhcp_snoop binding_entry\n'
                MAC_PORT='show fdb port {}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    #подставил DHCP2
                    t.write(DHCP2.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    output=res[380:]
                    return output
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    output=res[380:]
                    return output
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    out1=t.read_very_eager().decode('ascii')
                    time.sleep(1)
                    t.write(b'q')
                    t.write(LOOP2.encode())
                    time.sleep(1)
                    out2 = t.read_very_eager().decode('ascii')
                    res=out1+out2
                    output=out1[370:1480]+out2[200:]
                    return output
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")
    if ('D1210' in upd_com):

        print('Connection to D-link device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                SHOW_LOGG='show log\n'
                SHOW_PORT='show error ports {}\n'.format(port_name)
                VCT='cable diagnostic port {}\n'.format(port_name)
                LOOP='show loopdetect ports 1-13\n'
                LOOP2='show loopdetect ports 14-28\n'
                IGMP='show igmp_snooping group\n'
                DHCP='show address_binding ip_mac all\n'
                MAC_PORT='show fdb port {}\n'.format(port_name)
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(1.5)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:990]
                    return output
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
                #4)просмотр DHCP таблицы
                if menu_id=='4':
    
                    t.write(DHCP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b' ')
                    time.sleep(0.8)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:1105]
                    return output
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    out1=t.read_very_eager().decode('ascii')
                    time.sleep(1)
                    t.write(b'q')
                    t.write(LOOP2.encode())
                    time.sleep(1)
                    out2 = t.read_very_eager().decode('ascii')
                    res=out1+out2
                    output=out1[370:1480]+out2[165:1450]
                    return output
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    output=res[370:]
                    return output
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")
    if ('A6224' in upd_com):

        print('Connection to Alcatel device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                ####логи коммутатора. ГОТОВО.
                SHOW_LOGG='show logging\n'
                ####состояние порта. ГОТОВО.
                SHOW_PORT_2='show interfaces status ethernet e{}\n'.format(port_name)
                SHOW_PORT='show interfaces configuration ethernet e{}\n'.format(port_name)
                SHOW_PORT_3='show interfaces counters ethernet e{}\n'.format(port_name)
                SHOW_PORT_4='show interfaces access-lists ethernet e{}\n'.format(port_name)
                ####прозвон. ГОТОВО.
                VCT='test copper-port tdr e{}\n'.format(port_name)
                ####проверка на кольцо. ГОТОВО,но нужны тесты
                LOOP='show loopback-detection\n'
                #для получнеия информации по  IGMP, необxодимо знать влан. show vlan можно посмотреть все вланы, нас интерсует последний, тот, что начинается на 400-X
                getVLAN='show vlan\n' 
                #get all VLAN
                ####HCP. ГОТОВО
                DHCP='show ip dhcp snooping binding\n'
                #мак на порту ГОТОВО!!!
                MAC_PORT='show ip source-guard status ethernet e{}\n'.format(port_name)
                #поиск по маку
                SH_MAC=' show ip source-guard status mac-address {}'.format(port_name)
                ALL_PORT='show interfaces status'
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(1.5)
                    res1 = t.read_very_eager().decode('ascii')
                    t.write(SHOW_PORT_2.encode())
                    time.sleep(1.5)
                    res2 = t.read_very_eager().decode('ascii')
                    t.write(SHOW_PORT_3.encode())
                    time.sleep(1.5)
                    res3 = t.read_very_eager().decode('ascii')
                    t.write(SHOW_PORT_4.encode())
                    time.sleep(1.5)
                    res4 = t.read_very_eager().decode('ascii')
                    #'\033[31m'+ input_comman_ip_or_mac + '\033[0m'
                    res='\033[31m'+"Конфигурация порта:\n"+'\033[0m'+res1[112:]+'\033[31m'+"\nСостояние порта:\n"+'\033[0m'+res2[42:]+'\033[31m'+"\nТрафик в реальном времени+ошибки:\n"+'\033[0m'+res3[37:]+'\033[0m'+'\033[31m'+"\nIPTV параметры:\n"+'\033[0m'+res4[41:]
                    out=res.replace("a6224-r2-l6-s5-1#"," ")
                    return out.replace("Errors","\033[31m Errors \033[0m")
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(5)
                    res = t.read_very_eager().decode('ascii')
                    out=res[50:].replace("port e{}".format(port_name),"\033[031m port e{}\033[0m".format(port_name))
                    output=out.replace("good","\033[032m GOOD \033[0m").replace("open","\033[031m OPEN!!!\033[0m").replace("m","m\n").replace("{}".format(commutator_name)," ")
                    return output+'\n'
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(getVLAN.encode())
                    time.sleep(1.5)
                    res = t.read_very_eager().decode('ascii')
                    #из полученного результат всех вланов, нахожу тот который нужен.
                    split_list=res.split()
                    len_split=len(split_list)-5
                    vlan=split_list[len_split]
                    print("vlan:",vlan)
                    time.sleep(0.5)
                    igmp='show ip igmp snooping groups vlan {}'.format(vlan)
                    t.write(igmp.encode())
                    t.write(b'\n')
                    time.sleep(1.5)
                    t.write(b'q')
                    res = t.read_very_eager().decode('ascii')
                    return res
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    out1=t.read_very_eager().decode('ascii')
                    return out1[50:].replace("{}".format(commutator_name),"")
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(2)
                    t.write(b' ')
                    time.sleep(2)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:].replace("{}".format(commutator_name),"")
                if menu_id=='8':
                    print(port_name)
                    time.sleep(1)
                    t.write(SH_MAC.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                    return output[50:]
                if menu_id=='9':
                    time.sleep(1)
                    t.write(ALL_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                    return output[50:]
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")
    if ('ZY3500' in upd_com) or ('ZY3528' in upd_com):
    
        print('Connection to ZyXel device {}'.format(commutator_name))
        print('-'*80)
        try:
            with telnetlib.Telnet(commutator_name,23,30) as t:
                t.write(USER.encode())
                time.sleep(1)
                t.write(PSWD.encode()[::-1])
                t.write(b'\n')
                #блок команд
                time.sleep(1.5)
                #блок команд
                ####логи коммутатора. ГОТОВО.
                SHOW_LOGG='show logging\n'
                ####состояние порта. ГОТОВО.
                SHOW_PORT='show interfaces {}\n'.format(port_name)
                ####прозвон. ГОТОВО.
                VCT='cable-diagnostics {}\n'.format(port_name)
                ####проверка на кольцо. ГОТОВО,но нужны тесты
                LOOP='show loopguard\n'
                #igmp
                IGMP='show igmp-snooping group client all\n'
                IGMP28='show igmp-snooping group all\n'
                ####HCP. ГОТОВО
                DHCP='show dhcp snooping binding\n'
                #мак на порту ГОТОВО!!!
                MAC_PORT='show mac address-table port {}\n'.format(port_name)
                #поиск по маку
                SH_MAC='show mac address-table mac {}'.format(port_name)
                ALL_PORT='show interfaces status'
                #1)просмотр всего лога коммутатора
                if menu_id=='1':
                    t.write(SHOW_LOGG.encode())
                    time.sleep(0.7)
                    t.write(b' ')
                    time.sleep(0.7)
                    t.write(b' ')
                    time.sleep(0.7)
                    t.write(b' ')
                    time.sleep(0.7)
                    t.write(b' ')
                    time.sleep(0.7)
                    t.write(b' ')
                    time.sleep(0.7)
                    t.write(b' ')
                    time.sleep(0.7)
                    res = t.read_very_eager().decode('utf-8')
                    return res[50:].replace("link down","\033[031mlink down\033[0m").replace("link up","\033[032mlink up\033[0m")
                #2)просмотр порта
                if menu_id=='2':
                    t.write(SHOW_PORT.encode())
                    time.sleep(0.7)
                    t.write(b' ')
                    time.sleep(0.7)
                    res = t.read_very_eager().decode('utf-8')
                    #'\033[31m'+ input_comman_ip_or_mac + '\033[0m'
                    return res[50:].replace("Errors","\033[31mErrors \033[0m").replace("CRC","\033[31mCRC \033[0m").replace('10M','\033[031m10M\033[0m').replace('Down','\033[031mDown\033[0m').replace('/H','\033[031m/Half !!!\033[0m')
                #3)прозвон порта
                if menu_id=='3':
                    t.write(VCT.encode())
                    time.sleep(5)
                    res = t.read_very_eager().decode('ascii')
                    output=res[50:].replace("Ok","\033[032mOK\033[0m").replace("Open","\033[031mOPEN!!!\033[0m").replace("{}".format(commutator_name)," ")
                    return output
                #4)просмотр DHCP таблицы
                if menu_id=='4':
                    t.write(DHCP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[0:]
                #5)просмотр IGMP таблицы
                if menu_id=='5':
                    t.write(IGMP.encode())
                    t.write(b'\n')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    if 'Invalid' in res:
                        t.write(IGMP28.encode())
                        t.write(b'\n')
                        time.sleep(0.5)
                        t.write(b' ')
                        time.sleep(0.5)
                        res = t.read_very_eager().decode('ascii')
                    return res[50:]
                #6)Проверка на кольцо(Loopdetect)
                if menu_id=='6':
                    t.write(LOOP.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    out1=t.read_very_eager().decode('ascii')
                    return out1[50:].replace("Bad","\033[031mBad\033[0m")
                #7)Просмотр мака на порту
                if menu_id=='7':
                    t.write(MAC_PORT.encode())
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    res = t.read_very_eager().decode('ascii')
                    return res[50:]
                if menu_id=='8':
                    time.sleep(1)
                    t.write(SH_MAC.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                    return output[50:]
                if menu_id=='9':
                    time.sleep(1)
                    t.write(ALL_PORT.encode())
                    t.write(b'\n')
                    t.write(b' ')
                    time.sleep(1)
                    t.write(b' ')
                    time.sleep(1)
                    output = t.read_very_eager().decode('ascii')
                    return output[50:].replace('10M','\033[031m10M\033[0m').replace('Down','\033[031mDown\033[0m').replace('/H','\033[031m/Half !!!\033[0m')
        except BrokenPipeError or EOFError :
            print("\033[31mОшибка. Невозможно установить telnet подключение.\033[0m")
    else:
        return "\033[31m Не возможно выполнить данный запрос!\033[0m"

#функция проверят корректность ввода коммутатора (доменное имя или IP)
def commutator_check():
    res=1,2
    commutator_prefiks=''
    commutator_ip=0
    commutator_name=''
    print("Введите 'q' для завершения работы программы")
    
    def get_com_ip(commutator_name):
        
        time.sleep(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            print("Получаю IP из введённого имени")
            s.connect((f"{commutator_name}", 80))
            ip_commut = s.getpeername()[0]
            s.close()
        except:
            ip_commut = 0
            print(f"\n\nОшибка, не возможно получить IP коммутатора из данного имени: {commutator_name}\n\n")
        return str(ip_commut)

    while commutator_ip == 0:
        while len(commutator_name) <7 : 
            commutator_name=input("Введите имя коммутатора или IP-адрес коммутатор для диагностики.\nПример -  D3950-R1-L1-S1-0\nВы ввели: ")
        if commutator_name=='q' or commutator_name=='Q' or commutator_name=='й' or commutator_name=='Й':
            break

        #блок чисти для получения префикса и корректного имени
        first_clear_commutator_name=commutator_name.replace(' ','',10)
        second_clear_commutator_name=first_clear_commutator_name.replace('\t','',10)
        upd_commut_upper=second_clear_commutator_name.upper()
        upd_commut=upd_commut_upper.split('-')
        commutator_prefiks = upd_commut[0]
        while commutator_prefiks not in commutator_list:
            commutator_prefiks=input("Просмотр доступен только на коммутаторах {} \n: ".format(commutator_list))
            first_clear=commutator_prefiks.replace(' ','',10)
            second=first_clear.replace('\t','',10)
            upd_commut_upper=second.upper()
            upd_commut=upd_commut_upper.split('-')
            commutator_prefiks = upd_commut[0]
        #получаю через функцию ип( резол домена)
        commutator_ip = get_com_ip(second_clear_commutator_name)

        if len(commutator_ip)<7:
            commutator_ip = input("Введите IP коммутатор для диагностики.\nПример -  10.10.10.10 \nВы ввели: ")
        #если изначально введн только IP, получается что префикс не возмодно получить, и префиксом становится сам же ип. Сравниваем, если префикс == ип - запрашиваем отдельно префикс 
        while (commutator_prefiks == commutator_ip):
            print("\n\nВы ввели только IP адрес!")
            print(f"Возможные префиксы : {commutator_list}")
            commutator_prefiks = input("Введите префикс:")
            commutator_prefiks = commutator_prefiks.upper()
            while commutator_prefiks not in commutator_list:
                commutator_prefiks=input("Просмотр доступен только на коммутаторах {} \n: ".format(commutator_list))
    
    res = commutator_prefiks,commutator_ip
    os.system('cls' if os.name=='nt' else 'clear')
    print(res)
    return res

#при корректности ввода - возвращает префикс + (имя или ип адрес)

time.sleep(0.5)

#функция выполняет команту просмотра/поиска требуетмой инфы в логах и выводит её в рамках данного скрипта
def run(command,input_comman_ip_or_mac=0):
    print("-"*80)
    #выполняет команду и собирает полученные данные
    run=str(os.popen(command).read())
    lr=len(run)
    if lr==0:
        run="{} not found".format(input_comman_ip_or_mac)
    if input_comman_ip_or_mac in run:
        run=run.replace(input_comman_ip_or_mac,'\033[31m'+ input_comman_ip_or_mac + '\033[0m')
        run=run.replace("DHCPACK","\033[32mDHCPACK\033[0m")
        run=run.replace("no free leases","\033[31mno free leases\033[0m")
        run=run.replace("wrong network.","\033[31mwrong network.\033[0m")
        run=run.replace("192.168.","\033[31m192.168.\033[0m")

    print(run)

def menu():
    os.system('cls' if os.name=='nt' else 'clear')
    while True:
        print("Выберите пунк меню")
        print("1)просмотр DHCP логов\n2)Просмотр логов авторизации\n3)просмотр логов коммутатора\n4)Работа с OLT\nq)выход из программы")
        input_menu1=input("Ваш выбор : ")
        
        #блок меню 1 выполняет просмотр DHCP логов
        if input_menu1=='1':
            print("Выбран просмотр DHCP логов")
            print("Выберите регион для промотра.\n1)Регион1\n2)Регион2\n3)Регион3\n4)Возврат в предыдущее меню")
            input_menu_dhcp=input("Ваш выбор : ")
            if input_menu_dhcp=='1':
                print("Выбран просмотр для Регион1")
                print("Выполняется перенаправление ...")
                time.sleep(3)
                input_comman_ip_or_mac=input("Введи IP или MAC-addres или Логин или железка + порт в формате 'D3950-RXX-LXX-SX-X port XX'(без ковычек)  для поиска : ")
                run_comman='cat /var/log/remote/10.10.10.10.log | grep -i \''+input_comman_ip_or_mac+'\'| cut -f 1-4,7-100 -d \' \''
                run(run_comman,input_comman_ip_or_mac)
            if input_menu_dhcp=='2':
                print("Выбран просмотр для Регион2")
                input_comman_ip_or_mac=input("Введи IP или мак адрес для поиска : ")
                run_comman='cat /var/log/remote/radius* | grep -i \''+input_comman_ip_or_mac+' \'| cut -f 1-4,5,6-100 -d \' \''
                run(run_comman,input_comman_ip_or_mac)
            if input_menu_dhcp=='3':
                print("Выбран просмотр для Регион3")
                input_comman_ip_or_mac=input("Введи IP или мак адрес для поиска : ")
                run_comman='cat /var/log/remote/radius-region3* | grep -i \''+input_comman_ip_or_mac+' \'| cut -f 1-4,7-100 -d \' \''
                run(run_comman,input_comman_ip_or_mac)
            if input_menu_dhcp=='4':
                pass
        
        #блок меню 2 выполняет просмотр RADIUS логов
        if input_menu1=='2':
            print("Выбран просмотр RADIUS логов")
            print("Выберите регион для промотра.\n1)Регион1\n2)Регион2\n3)Регион3\n4)Возврат в предыдущее меню")
            input_menu_dhcp=input("Ваш выбор : ")
            if input_menu_dhcp=='1':
                #Добавить к GUI прилаге
                print("Выбран просмотр для Регион1 и Регион3")
                input_comman_ip_or_mac=input("Введи IP или MAC-addres или Логин или железка + порт в формате 'D3950-R12-L21-S4-1 port 15'(без ковычек)  для поиска : ")
                run_comman='cat /var/log/remote/10.10.10.10.log | grep -i \''+input_comman_ip_or_mac+'\'| cut -f 1-4,7-100 -d \' \''
                run(run_comman,input_comman_ip_or_mac)

            if input_menu_dhcp=='2':
                print("Выбран просмотр для Регион2")
                input_comman_ip_or_mac=input("Введи IP или мак адрес для поиска : ")
                run_comman='cat /var/log/remote/radius-region2* | grep -i \''+input_comman_ip_or_mac+'\] \'| cut -f 1-4,8-100 -d \' \''
                run(run_comman,input_comman_ip_or_mac)
            if input_menu_dhcp=='3':
                pass
        
        #блок меню 3 работа с сетевым оборудованием (Ethernet,access)
        if input_menu1=='3':
            commutator_name=commutator_check()
            
            while True: 
                if commutator_name[1]==0 :
                    while commutator_name[1]==0:
                        commutator_name=commutator_check()
                print("Выполняется диагностика для коммутатора {} / {}".format(commutator_name[0],commutator_name[1]))
                if commutator_name[0] in DCN_commutator_list:
                    print("\033[1m\n\n11)Быстрая диагностика для DCN\n\n\033[0m1)просмотр всего лога коммутатора\n2)просмотр порта(параметры/ошибки)\n3)прозвон порта \n4)просмотр DHCP таблицы\n5)просмотр IGMP таблицы\n6)Проверка на кольцо(Loopdetect)\n7)Просмотр мака на порту\n+Оптициально, работает не со всеми коммутаторами:\n8)Поиск по мак адресу\n9)Просмотр статуса ВСЕХ портов\n\nq)для возврата в предыдущее меню")
                else:
                    print("1)просмотр всего лога коммутатора\n2)просмотр порта(параметры/ошибки)\n3)прозвон порта \n4)просмотр DHCP таблицы\n5)просмотр IGMP таблицы\n6)Проверка на кольцо(Loopdetect)\n7)Просмотр мака на порту\n+Оптициально, работает не со всеми коммутаторами:\n8)Поиск по мак адресу\n9)Просмотр статуса ВСЕХ портов\n\nq)для возврата в предыдущее меню")

                input_menu=input("Ваш выбор: ")
                
                if input_menu=='11':
                    #буде смотреть лог коммутатор, состояние порта, IGMP запросы,прозвон
                    input_port=getNumberPort()
                    cdt=datetime.datetime.now()
                    res=commutator_show(commutator_name,input_port.replace(" ",""),input_menu)
                    cdt2=datetime.datetime.now()
                    td=cdt2-cdt
                    res=colorator(res,td,input_port)
                    print(res)

                if input_menu=='1':
                    print('Выбран просмотр всего лога коммутатора')
                    port_name=1
                    cdt=datetime.datetime.now()
                    res=commutator_show(commutator_name,port_name,input_menu)
                    cdt2=datetime.datetime.now()
                    td=cdt2-cdt
                    res=colorator(res,td)
                    print(res)

                if input_menu=='2':
                    print('Выбран просмотр порта')
                    input_port=getNumberPort()
                    cdt=datetime.datetime.now()
                    res=commutator_show(commutator_name,input_port.replace(" ",""),input_menu)
                    cdt2=datetime.datetime.now()
                    td=cdt2-cdt
                    res=colorator(res,td,input_port)
                    print(res)
                if input_menu=='3':
                    print('Выбран прозвон порта')
                    upd_commut=commutator_name[0]
                    if upd_commut=='P2626' or upd_commut=='P2610':
                        print('-'*80,"\nОшибка. Прозвон не доступен на коммутаторе {}".format(upd_commut))
                    else:
                        input_port=getNumberPort()
                        cdt=datetime.datetime.now()
                        res=commutator_show(commutator_name,input_port,input_menu)
                        cdt2=datetime.datetime.now()
                        td=cdt2-cdt
                        res=colorator(res,td,input_port)
                        print(res)
                if input_menu=='4':
                    upd_commut=commutator_name[0]
                    if upd_commut=='D3000' or upd_commut=='D1210':
                        print('Выбран просмотр DHCP таблицы')
                        print('-'*80,"\nВНИМАНИЕ!!! Просмотр DHCP таблицы не доступен на коммутаторе {}\n Альтернативным вариантом является просмотр всех маков на всех портах".format(upd_commut))
                        input_port='1'
                        cdt=datetime.datetime.now()
                        res=commutator_show(commutator_name,input_port,input_menu)
                        cdt2=datetime.datetime.now()
                        td=cdt2-cdt
                        res=colorator(res,td)
                        print(res)
                    else:
                        port_name='1'
                        print('Выбран просмотр DHCP таблицы')
                        cdt=datetime.datetime.now()
                        res=commutator_show(commutator_name,port_name,input_menu)
                        cdt2=datetime.datetime.now()
                        td=cdt2-cdt
                        res=colorator(res,td)
                        print(res)
                if input_menu=='5':
                    upd_commut=commutator_name[0]
                    if upd_commut=='D3000' or upd_commut=='D1210':
                        print('Выбран просмотр IGMP таблицы')
                        print('-'*80,"\nВНИМАНИЕ!!! Просмотр IGMP таблицы не доступен на коммутаторе {}\n Альтернативным вариантом является просмотр трафика на порту\nОбращаем внимание на Multicast".format(upd_commut))
                        input_port=input("Введите порт для просмотра: ")
                        cdt=datetime.datetime.now()
                        res=commutator_show(commutator_name,input_port,input_menu)
                        cdt2=datetime.datetime.now()
                        td=cdt2-cdt
                        res=colorator(res,td)
                        print(res)
                    else:
                        input_port='1'
                        print('Выбран просмотр IMGP таблицы')
                        cdt=datetime.datetime.now()
                        res=commutator_show(commutator_name,input_port,input_menu)
                        cdt2=datetime.datetime.now()
                        td=cdt2-cdt
                        res=colorator(res,td)
                        print(res)
                if input_menu=='6':
                    print('Выбрана проверка на кольцо')
                    input_port='1'
                    cdt=datetime.datetime.now()
                    res=commutator_show(commutator_name,input_port.replace(" ",""),input_menu)
                    cdt2=datetime.datetime.now()
                    td=cdt2-cdt
                    res=colorator(res,td)
                    print(res)
                if input_menu=='7':
                    print('Выбран просмотр мака на порту')
                    input_port=getNumberPort()
                    cdt=datetime.datetime.now()
                    res=commutator_show(commutator_name,input_port,input_menu)
                    cdt2=datetime.datetime.now()
                    td=cdt2-cdt
                    res=colorator(res,td,input_port)
                    print(res)
                if input_menu=='8':
                    print('Выбран поиск по маку\nДля поиска необxодимо вводить мак-адрес в следующем формате:\nD4:6E:0E:AC:6C:FB , т.е. через двоеточие')
                    input_port=input("Введите мак для поиска: ")
                    cdt=datetime.datetime.now()
                    res=commutator_show(commutator_name,input_port,input_menu)
                    cdt2=datetime.datetime.now()
                    td=cdt2-cdt
                    res=colorator(res,td,input_port)
                    print(res)
                if input_menu=='9':
                    print('Выбран просмотр ВСЕХ портов')
                    upd_commut=commutator_name[0]
                    input_port=0
                    if upd_commut=='ZY3528':
                        print("\033[031m zy3528 не поддерживают просмотр статуса всех портов. Просмотр доступен на zy3500 \033[0m")
                    else:
                        cdt=datetime.datetime.now()
                        res=commutator_show(commutator_name,input_port,input_menu)
                        cdt2=datetime.datetime.now()
                        td=cdt2-cdt
                        res=colorator(res,td)
                        print(res)

                if input_menu=='q' or input_menu=='й' or input_menu=='q' or input_menu=='Й' :
                    break
        #блок меню 4 для работы с оптическим оборудованинем( OLT <=> ONU)
        if input_menu1=='4':
            olt_name_ip=OLT_check()
            if olt_name_ip==0:
                print("Возврат в предыдущее меню")
                break
            while True:
                print("1)Просмотр состояния всех ONU на card/port \n2)Просмотр на порту IP|MAC и дата/время получения IP на конкретном порту \n3)Просмотр IGMP лога \n4)Поиск незареганых ONU\n5)Состояние ONU(+gpon\ether)\nq)Возврат в предыдущее меню")
                command=input("Ваш выбор: ")
                if command=='1':
                    sn='0'
                    card=getNumberCard()
                    port=getNumberPort()
                    res=olt_onu_viewer(sn,olt_name_ip,command,card,port)
                    print(res)
                if command=='2':
                    sn='0'
                    card=getNumberCard()
                    port=getNumberPort()
                    vport=getNumberVPort()
                    res=olt_onu_viewer(sn,olt_name_ip,command,card,port,vport)
                    print(res)
                if command=='3':
                    sn='0'
                    card=getNumberCard()
                    port=getNumberPort()
                    vport=getNumberVPort()
                    res=olt_onu_viewer(sn,olt_name_ip,command,card,port,vport)
                    print(res)
                if command=='4':
                    print("Выбран поиск незараганых ONU")
                    print("Для возвтрата в предыдущее меню введите 'q' или 'й' ")
                    sn=input("Введите SN ONU или нажмите ENTER: ")
                    if sn=='q' or sn=='й' or sn=='Q' or sn=='Й':
                        break
                    if (len(sn)<12 and len(sn)!=0) or len(sn)>12:
                        print("\033[031m Ошибка! Длина SN ONU должна быть 12 символом! \033[0m Вы ввели \033[032m {} \033[0m , длинна S/N : \033[031m {} \033[0m".format(sn,len(sn)))
                    else:
                        res=olt_onu_viewer(sn,olt_name_ip,command)
                        print(res)
                if command=='5':
                    sn='0'
                    card=getNumberCard()
                    port=getNumberPort()
                    vport=getNumberVPort()
                    res=olt_onu_viewer(sn,olt_name_ip,command,card,port,vport)
                    print(res)
                if command=='q' or command=='й' or command=='Q' or command=='Й':
                    break

        if input_menu1=='q' or input_menu1=='й' or input_menu1=='Q' or input_menu1=='Й' :
            sys.exit()
os.system('clear')


#основаная фукнция, вызывающая меню.
#меню, в зависимости от выбора - вызывает требуемую функцию.
while True:
    try:
        menu()
    except KeyboardInterrupt or BrokenPipeError:
        print("\n\nCansel")
        time.sleep(0.1)

from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI.HostGroup import KlAkHostGroup
from KlAkOAPI.Params import KlAkArray
from KlAkOAPI.SrvView import KlAkSrvView
from KlAkOAPI.ChunkAccessor import KlAkChunkAccessor


def Get_Server():
    server_url = 'https://test.ru:13299' # ksc server address
    username = 'APIUSER' # username with root admin rights
    password = 'password' # password from the selected user
    SSLVerifyCert = 'C:\\ProgramData\\KasperskyLab\\adminkit\\1093\\cert\\klserver.cer'
    server = KlAkAdmServer.Create(server_url, username, password, verify = SSLVerifyCert)
    return server

def Get_OWNER_ID(oSrvView, wstrIteratorId): 
    iRecordRange = oSrvView.GetRecordRange(wstrIteratorId, nStart=0, nEnd=100).OutPar('pRecords')
    for oObj in iRecordRange['KLCSP_ITERATOR_ARRAY']:
        KLHST_WKS_CUSTOM_OWNER_ID = oObj.GetValue('ul_binId')['value']
        return KLHST_WKS_CUSTOM_OWNER_ID

def Get_HOSTNAME_ID(oChunkAccessor, strAccessor):
    iItemsChunk = oChunkAccessor.GetItemsChunk(strAccessor, 0, 100).OutPar('pChunk')
    for oObj in iItemsChunk['KLCSP_ITERATOR_ARRAY']:
        KLHST_WKS_HOSTNAME = oObj['KLHST_WKS_HOSTNAME']
        return KLHST_WKS_HOSTNAME

if __name__ == "__main__":
    
    server = Get_Server()

    strUserName = "Surname Name Patronymic" # indicate a real user
    strHostName = "HostName" # indicate the real device

    oFields2Return = KlAkArray(['ul_nId', 'ul_binId', 'ul_wstrDisplayName'])
    oField2Order = KlAkArray([{"type":"params","value":{"Name":"ul_wstrDisplayName","Asc":True}}])
    pParams = KlAkArray({"bIncludeNativeEntraIdObjects":True})
    SrvWiew = KlAkSrvView(server)
    
    wstrIteratorId  = SrvWiew.ResetIterator('GlobalUsersListSrvViewName', f'ul_wstrDisplayName="{strUserName}"', oFields2Return, oField2Order, {"bIncludeNativeEntraIdObjects":True}, lifetimeSec = 1000).OutPar('wstrIteratorId')
    KLHST_WKS_CUSTOM_OWNER_ID = Get_OWNER_ID(SrvWiew, wstrIteratorId )

    oHostGroup = KlAkHostGroup(server)
    oChunkAccessor = KlAkChunkAccessor(server)
    strAccessor = oHostGroup.FindHosts(f"KLHST_WKS_DN = \"{strHostName}\"", ["KLHST_WKS_HOSTNAME"], [],{'KLGRP_FIND_FROM_CUR_VS_ONLY': True}, lMaxLifeTime=7200).OutPar('strAccessor')
    KLHST_WKS_HOSTNAME= Get_HOSTNAME_ID(oChunkAccessor, strAccessor)

    oHostGroup.UpdateHost(KLHST_WKS_HOSTNAME, pInfo={"KLHST_WKS_CUSTOM_OWNER_ID":{"type":"binary","value":f"{KLHST_WKS_CUSTOM_OWNER_ID}"}})

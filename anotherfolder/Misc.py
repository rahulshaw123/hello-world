







def FluxModes(ds, ReacSet, OutPath=False, OnlyDirection=True):

    numt=0
    n=0
    
    tot = 1e-10
    if OutPath != False:
        f = open(OutPath,"w")
        
    check_mode=[]
    ModesDic={}


    
    cn = ds.cnames
    ds.NewCol([0]*len(ds),'Done')

    while ds.GetCol('Done').count(0) != 0:
        flag = 0
        master_mode,numt = Cal(ds,ReacSet,numt)
        


        for row in ds:
            next_mode={}
            cnt = 0
            for i in master_mode.keys():
                next_mode[i] = row[cn.index(i)]
                if OnlyDirection:
                    if ((master_mode[i] > 0 and next_mode[i] > 0) or (master_mode[i] < 0 and next_mode[i] < 0) or
                    (master_mode[i] == 0 and next_mode[i] == 0)):
                        cnt = cnt + 1
                else:
                    if ((master_mode[i] > 0 and next_mode[i] > 0) or (master_mode[i] < 0 and next_mode[i] < 0) or 
                    (master_mode[i] == 0 and next_mode[i] == 0)) and abs(abs(master_mode[i]) - abs(next_mode[i])) < tot:
                        cnt = cnt + 1
                        
                    
            if cnt == len(master_mode.keys()):
                if flag == 0:
                    n=n+1
                    ModesDic["Mode_" + str(n)] = {}
                    for reac in next_mode.keys():
                        ModesDic["Mode_" + str(n)][reac]=master_mode[reac]
                        
                    flag = 1                        
                row[ds.cnames.index('Done')] = 1






    ds.DelCol('Done')           
    return ModesDic


def Cal(ds,ReacSet,numt):

    m_mode = {}
    for row in ds:
        if row[ds.cnames.index('Done')] == 0:
            numt = numt + 1
            for i in ReacSet:
                m_mode[i] = row[ds.cnames.index(i)]
            return m_mode,numt


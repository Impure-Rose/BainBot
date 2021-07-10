import urllib.request
url= 'http://fbi.overkillsoftware.com/'
badBuild=open("PD2Weapons.csv",'w')
req=urllib.request.build_opener()
req.addheaders=[('User-agent', 'Mozilla/5.0')]
primary=[]
secondary=[]
melee=[]
throw=[]
nextp=0
nexts=0
nextm=0
nextt=0
with req.open(url) as fnet:
    for line in fnet:
        if(nextp==1):
            primary.append(str(line))
            nextp=0
        elif(nexts==1):
            secondary.append(str(line))
            nexts=0
        elif(nextm==1):
            melee.append(str(line))
            nextm=0
        elif(nextt==1):
            throw.append(str(line))
            nextt=0
        if (b"fbifirearmsdbimgprimary") in line:
            nextp=1
        elif(b"fbifirearmsdbimgsecondary") in line:
            nexts=1
        elif(b"fbifirearmsdbimgmelee")in line:
            nextm=1
        elif(b"fbifirearmsdbimgthrown")in line:
            nextt=1
a=0
for i in range (0,len(throw)):
    badBuild.write(primary[a][6:][:-8]+','+secondary[a][6:][:-8]+','+melee[a][6:][:-8]+','+ throw[a][6:][:-8]+'\n')
    a+=1
for q in range (len(throw),len(secondary)-1):
    badBuild.write(primary[a][6:][:-8]+','+secondary[a][6:][:-8]+','+melee[a][6:][:-8]+ ','+'\n')
    
    a+=1
for w in range (len(secondary), len(melee)):
    badBuild.write(primary[a][6:][:-8]+', ,'+ melee[a][6:][:-8]+','+'\n')
    a+=1
for x in range(len(melee), len(primary)):
    badBuild.write(primary[a][6:][:-8]+', , ,'+'\n')
    a+=1

badBuild.close()
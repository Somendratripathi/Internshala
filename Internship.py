import re;

import pandas as pd;
Internship = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/Internship.csv')
def inter_profile(s):
    s = str(s)
    s = s.lower()
    s = re.sub(r"^.*((law)|(lega)|(account)|(audit)).*$", "LAW", s)
    s = re.sub(r"^.*((writ)|(conten)|(social)|(blog)|(editor)|(photo)|(camera)|(articl)|(journali)).*$", "WRT", s)
    s = re.sub(r"^.*((mark)|(sales)|(busin)|(mba)|(finance)|(manag)|(operat)|(advert)|(opera)|(human)).*$|^(hr).*$", "MKT", s)
    s = re.sub(r"^.*((design)|(adope)|(photoshop)).*$", "PHT", s)
    s = re.sub(r"^.*((soft)|(java)|(c\+\+)|(infor)|(progra)).*$|^i[\s]*\.*t[\s]*\.*$", "SFT", s)

    s = re.sub(r"^.*((andro)|(app)|(develop)|(comput)).*$", "AND", s)
    s = re.sub(r"^.*((intern)|(train)).*$", "TRN", s)
    s = re.sub(r"^.*((anal)|(data)|(consult)).*$", "ANA", s)
    s = re.sub(r"^.*((awar)).*$", "AWA", s)
    s = re.sub(r"^.*((teac)|(resea)|(journa)).*$", "TEA", s)
    s = re.sub(r"^.*((ambas)|(commi)|(memb)|(studen)).*$", "EXT", s)
    s = re.sub(
        r"^(?!((LAW)|(WRT)|(PHT)|(SFT)|(AND)|(MKT)|(TRN)|(ANA)|(AWA)|(TEA)|(EXT))).*$",
        "OTH", s)
    return s

Internship["Intern_Prof_clean"] = Internship['Internship_Profile'].apply(inter_profile)
Internship['Stipend1'] = Internship['Stipend1'].fillna(0)
Internship['Stipend2'] = Internship['Stipend2'].fillna(Internship['Stipend1'])

Internship['Skilled_IProfile'] = Internship['Skills_required'].fillna(' ')+Internship['Internship_Profile']

Mapping = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/map.csv')
Mapping['B'] = Mapping['B'].fillna('')
Map = dict(zip(Mapping['A'],Mapping['B']))


l = list()
l2= list()
for row in range(len(Internship)):
    s = ''
    t = ''
    for col in Internship.columns[-275:-2]:
        if Internship.loc[row,col] == 1:
            s = s + col
            t = t + Map[col]
    #t = t.split(",")
    l.append(s)
    l2.append(t)
    print row,col
df = pd.DataFrame(l,columns=['Skilldetail'])
df1 = pd.DataFrame(l2,columns=['StreamRequired'])

Internship = pd.concat([Internship,df],axis = 1)
Internship = pd.concat([Internship,df1],axis = 1)



'''run this'''
Internship = Internship.drop(Internship.columns[-277:-4],axis=1)
Internship.to_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/Internship_complete.csv')


# #########Post competition



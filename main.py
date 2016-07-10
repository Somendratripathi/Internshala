import numpy as np;
import re;

import pandas as pd;
from astropy.io.fits import column

train = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/train.csv')
test_x = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/test.csv')

print len(train), len(test_x),len(train_x),len(train_y)


train = pd.merge(train, student_complete, how='inner', on='Student_ID')
train = pd.merge(train, Internship, how='inner', on='Internship_ID')

train_y = train['Is_Shortlisted']
train_x = train.drop('Is_Shortlisted',axis=1)

test_x = pd.merge(test_x, student_complete, how='left', on='Student_ID')
test_x = pd.merge(test_x, Internship, how='inner', on='Internship_ID')
# all_x = pd.concat((train_x, test_x), axis=0, ignore_index=True)

train_x['Preferred_location'] = train_x['Preferred_location'].fillna('OTH')
test_x['Preferred_location'] = test_x['Preferred_location'].fillna('OTH')

train_x =  train_x.drop(['Degree','Stream','Performance_PG','PG_scale'	,'Performance_UG',	'UG_Scale'], axis =1)
test_x =  test_x.drop(['Degree','Stream','Performance_PG','PG_scale'	,'Performance_UG',	'UG_Scale'],axis = 1)

'''
def vector_days_2_start(x,y):
    z = datetime.datetime.strptime(x).date() - datetime.datetime.strptime(y).date()).days
    return z

train_x['Days_to_Start'] = 0
train_x['Days_str_in'] = 0
for i in range(len(train_x)):
    train_x['Days_to_Start'][i] = (datetime.datetime.strptime(train_x['Internship_deadline'][i],"%d-%m-%Y").date() - datetime.datetime.strptime(train_x['Earliest_Start_Date'][i],"%d-%m-%Y").date()).days
    train_x['Days_str_in'][i] = (datetime.datetime.strptime(train_x['Start_Date'][i],"%d-%m-%Y").date() - datetime.datetime.strptime(train_x['Earliest_Start_Date'][i],"%d-%m-%Y").date()).days
    print i

test_x['Days_to_Start'] = 0
test_x['Days_str_in'] = 0
for i in range(len(test_x)):
    test_x['Days_to_Start'][i] = (datetime.datetime.strptime(test_x['Internship_deadline'][i],"%d-%m-%Y").date() - datetime.datetime.strptime(test_x['Earliest_Start_Date'][i],"%d-%m-%Y").date()).days
    test_x['Days_str_in'][i] = (datetime.datetime.strptime(test_x['Start_Date'][i],"%d-%m-%Y").date() - datetime.datetime.strptime(test_x['Earliest_Start_Date'][i],"%d-%m-%Y").date()).days
    print i

'''
# train_x =  train_x.drop(['Internship_deadline','Start_Date','Earliest_Start_Date'], axis =1)
# test_x =  test_x.drop(['Internship_deadline','Start_Date','Earliest_Start_Date'],axis = 1)

#train_x = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/train_x.csv')
#test_x = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/test_x.csv')


####combing test and train

print len(train), len(test_x),len(train_x),len(train_y)
all_x = pd.concat((train_x, test_x), axis=0, ignore_index=True)

#Provided the format of dates has been stored as numbers in the csv file
all_x['Days_to_Start'] = all_x['Internship_deadline'] - all_x['Earliest_Start_Date']
all_x['Days_str_in'] = all_x['Start_Date'] - all_x['Earliest_Start_Date']

all_x = all_x.drop(['Internship_deadline','Start_Date','Earliest_Start_Date'],axis = 1)


def great_expect(x):
    if x == '2-5K':
        return 2000
    elif x == '5-10K':
        return 5000
    elif x == '10K+':
        return 10000
    elif x == 'No Expectations':
        return 0

all_x['expectation'] = all_x['Expected_Stipend'].apply(great_expect)
all_x['meet_expectation'] = ((all_x['Stipend2'] - all_x['expectation'])>0) * 1

#####fuzzy match for columns location and string

from fuzzywuzzy import fuzz;

#creating columns from fuzzy match
def fuz_columns(x,y):
    return fuzz.token_set_ratio(x,y)     #.apply(lambda x1,x2 : fuzzy )

#creating columns from fuzzy match
def fuz_columns_sort(x,y):

    return fuzz.token_sort_ratio(x,y)

#creating columns from fuzzy match
def fuz_columns_pr(x,y):
    return fuzz.partial_ratio(x,y)

all_x['loc_dummy1'] = all_x['Preferred_location']+" "+all_x['Locat']+ " "+all_x['Institute_location'] + " "+all_x['hometown']
all_x['loc_dummy2'] = all_x['Preferred_location']
all_x['loc_dummy3'] = all_x['hometown'] + " " +all_x["Institute_location"]

# all_x['Internship_Location']


all_x['IL_d1_token_sr_matchh'] = np.vectorize(fuz_columns)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy1']))
all_x['IL_d1_token_sort_ratio'] = np.vectorize(fuz_columns_sort)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy1']))
all_x['IL_d1_partial_ratio'] = np.vectorize(fuz_columns_pr)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy1']))

all_x['IL_d2_token_sr_matchh'] = np.vectorize(fuz_columns)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy2']))
all_x['IL_d2_token_sort_ratio'] = np.vectorize(fuz_columns_sort)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy2']))
all_x['IL_d2_partial_ratio'] = np.vectorize(fuz_columns_pr)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy2']))

all_x['IL_d3_token_sr_matchh'] = np.vectorize(fuz_columns)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy3']))
all_x['IL_d3_token_sort_ratio'] = np.vectorize(fuz_columns_sort)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy3']))
all_x['IL_d3_partial_ratio'] = np.vectorize(fuz_columns_pr)(np.array(all_x['Internship_Location']),np.array(all_x['loc_dummy3']))


all_x['Institute_Category'] = all_x['Institute_Category'].apply(lambda x: 1 if x=='Y' else 0)
all_x['Current_year'] = all_x['Current_year'].apply(lambda x: 8 if x=='already a graduate' else x*1)

all_x = all_x.drop(['Expected_Stipend','Preferred_location','Institute_location','hometown','Locat','Internship_Profile','Skills_required','Internship_Location','loc_dummy1','loc_dummy2',	'loc_dummy3','XP'],axis=1)

all_x['Internship_Type'] = all_x['Internship_Type'].apply(lambda x: 1 if x=='virtual' else 0)
all_x['Internship_category'] = all_x['Internship_category'].apply(lambda x: 1 if x=='Full Time' else 0)

def Stipend_Type_expect(x):
    if x == 'unpaid':
        return 0
    elif x == 'fixed':
        return 2
    elif x == 'variable':
        return 1
    elif x == 'performance':
        return 1.5

all_x['Stipend_Type'] = all_x['Stipend_Type'].apply(Stipend_Type_expect)


all_x['profile_skill_ip_token_sr_matchh'] = np.vectorize(fuz_columns)(np.array(all_x['Skilled_IProfile']),np.array(all_x['Prof']))
all_x['profile_skillip_token_sort_ratio'] = np.vectorize(fuz_columns_sort)(np.array(all_x['Skilled_IProfile']),np.array(all_x['Prof']))
all_x['profile_skillip_partial_ratio'] = np.vectorize(fuz_columns_pr)(np.array(all_x['Skilled_IProfile']),np.array(all_x['Prof']))

all_x['profile_skill_det_token_sr_matchh'] = np.vectorize(fuz_columns)(np.array(all_x['Skilldetail']),np.array(all_x['Prof']))
all_x['profile_skilldet_token_sort_ratio'] = np.vectorize(fuz_columns_sort)(np.array(all_x['Skilldetail']),np.array(all_x['Prof']))

all_x['Intern_match'] = (all_x['profile_build']==all_x['Intern_Prof_clean'])*1



def f(x):
    return len(re.findall(x['stream_clean'],x['StreamRequired']))


all_x['Streammatch'] = all_x.apply(f,axis=1)


# len(re.findall(all_x['StreamRequired'][0],all_x['stream_clean'][0]))


all_x_copy=all_x

all_x_copy =all_x_copy.drop(['Skilled_IProfile','Skilldetail','Prof'],axis=1)


df1 = pd.concat([pd.get_dummies(all_x_copy['profile_build']),pd.get_dummies(all_x_copy['degree_clean']),
                 pd.get_dummies(all_x_copy['degree_mas_bac']),pd.get_dummies(all_x_copy['stream_clean']),pd.get_dummies(all_x_copy['Intern_Prof_clean'])],axis=1)


all_xxx = pd.concat([all_x_copy,df1],axis=1)
all_xxx = all_xxx.drop(['degree_clean','degree_mas_bac','stream_clean','profile_build','Intern_Prof_clean'],axis =1)
all_xxx = all_xxx.drop(['StreamRequired'],axis=1)

train_xxx = all_xxx[:len(train_x)]
test_xxx = all_xxx[len(train_x):]

train_xxx.to_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/train_xxx.csv',Index=False)
test_xxx.to_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/test_xxx.csv',Index=False)
pd.DataFrame(train_y).to_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/train_y.csv',Index=False)

'''End of today'''



# all_x['Current_year'] = all_x['Current_year']*1




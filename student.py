import re;

import pandas as pd;


Student = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/Student.csv')

Student['Degree'] = Student['Degree'].fillna('Others')
Student['Stream'] = Student['Stream'].fillna('Others')



# Student.head()
'''
# ######Working on Student.csv

# All are unique except profile,location, start date end date
# 72621 students in total

1) Adding column for 7712500 to 78654321 switch ####Not using for now
2) Group degree into subgroups : Btech/Mtech
3) Checking if college loc and hometown same
4) Cleaning and adding the scaled ug and scores
5) Re for stream
6) Profile to columns

'''


# degree = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/degree.csv')
# degree['name'] = degree

# cleaning degree


def sub_str(s):
    s = str(s)
    s = s.lower()
    s = re.sub(r"^m[\s]*\.*[\s]*b[\s]*\.*[\s]*a[\s]*\.*$|^.*(manage).*$|^.*(mba).*$|^.*(admin).*$|^.*(busin).*$", "MBA",
               s)
    s = re.sub(r"^.*((and)|(dual)|(integ)).*$", "Dual", s)
    s = re.sub(r"^b[\s]*\.*[\s]*[t][\s]*.*$|^b[\s]*\.*[\s]*e[\s]*\.*.*$|b.*(tech).*$", "BT", s)
    s = re.sub(r"^b[\s]*\.*[\s]*(co)[\s]*.*$|^.*b[\s].*\.*(com).*$", "BCom", s)
    s = re.sub(r"^m[\s]*\.*[\s]*[t][\s]*.*$|^m[\s]*\.*e[\s]*\.*$", "MT", s)
    s = re.sub(r"^m[\s]*\.*[\s]*[c][\s]*.*a[\s]*.*$|^m[\s]*\.*[\s]*e[\s]*\.*[\s]*$", "MC", s)
    s = re.sub(r"^b[\s]*\.*[\s]*arch[\s]*\.*$", "BArch", s)
    s = re.sub(r"^b[\s]*\.*[\s]*a[\s]*\.*.*$", "BA", s)
    s = re.sub(r"^m[\s]*\.*[\s]*a[\s]*\.*.*$", "MA", s)
    s = re.sub(r"^b[\s]*\.*[\s]*(sc).*$", "BSC", s)
    s = re.sub(r"^m[\s]*\.*[\s]*(sc).*$", "MSC", s)
    s = re.sub(r"^.*(post).*$|^.*(pg).*|^.*(diploma).*$", "MPG", s)
    s = re.sub(r"^.*((grad)|(under)).*$|^.*(ug).*$", "BUG", s)
    s = re.sub(
        r"^.*((ing)|(none)|(nil)|(not)|(no)|(student)|(high)|(year)|(nan)|(na)|(college)|(school)|(twelt)|(first)|(inter)|(second)|(third)|(final)).*$|^.*((12)|(10)).*$",
        "NC", s)
    s = re.sub(r"^.*(mast).*$|^m[\s]*\.*[\s]*s[\s]*\.*.*$", "MAS", s)
    s = re.sub(r"^.*l[\s]*\.*[\s]*l[\s]*\.*[\s]*b[\s]*\.*[\s]*.*$", "LLB", s)
    s = re.sub(r"^.*m[\s]*\.*[\s]*b[\s]*\.*[\s]*b[\s]*\.*[\s]*s[\s]*\.*[\s]*.*$", "MBBS", s)
    s = re.sub(r"^m.*$", "M", s)
    s = re.sub(r"^b.*$", "B", s)
    s = re.sub(
        r"^(?!((M)|(B)|(MBBS)|(LLB)|(MAS)|(BUG)|(NC)|(MPG)|(MSC)|(BSC)|(MA)|(BA)|(BArch)|(MC)|(MT)|(BCom)|(BT)|(Dual)|(MBA))).*$",
        "OTH", s)
    return s

def mas_bachelor(s):
    s = str(s)
    s = s.lower()
    s = re.sub(r"^m.*$", "Mas", s)
    s = re.sub(r"^b.*$", "Bac", s)
    s = re.sub(r"^n.*$", "NC", s)
    s = re.sub(r"^d.*$", "Mas", s)
    s = re.sub(r"^l.*$", "LL", s)
    return s


def stream(s):
    s = str(s)
    s = s.lower()
    s = re.sub(r"^.*((media)|(journal)).*$", "JRN",s)
    s = re.sub(r"^.*((hr)|(accoun)|(human)|(psy)|(soci)|(polit)).*$", "HR",s)
    s = re.sub(r"^.*((econo)|(finan)).*$", "ECO",s)
    s = re.sub(r"^.*((comp)|(mca)).*$|^.*(cse).*$|^.*(soft).*$|^c[\s]*\.*[\s]*s[\s]*\.*$", "CSE",s)
    s = re.sub(r"^.*((math)|(stat)|(physi)).*$", "MAT",s)
    s = re.sub(r"^.*((elec)|(embed)|(instrum)).*$", "EEE",s)
    s = re.sub(r"^.*((mech)|(autom)).*$", "MEC",s)
        "OTH", s)
    return s

# degree['var2'] = degree['name'].apply(mas_bachelor)

# degree['var2'].to_clipboard()


Student['degree_clean'] = Student['Degree'].apply(sub_str)
Student['degree_mas_bac'] = Student['degree_clean'].apply(mas_bachelor)
Student['home_college_loc'] = 1 * np.array(Student['hometown'] == Student['Institute_location'])
Student['UG_performance'] = Student['Performance_UG'] / Student['UG_Scale']
Student['PG_performance'] = Student['Performance_PG'] / Student['PG_scale']
Student['stream_clean'] = Student['Stream'].apply(stream)

Student['Profile'] = Student['Profile'].fillna(' ')
Student['Location'] = Student['Location'].fillna(' ')
Student['Experience_Type'] = Student['Experience_Type'].fillna(' ')

# Profile,Location, Start Date,  End Date


degree = Student


'''
# Splitting profile to columns
def exp_group(x):
    exp = dict()
    exp[x] = exp.get(x,0)+1
'''

de = pd.DataFrame({'profile_strength' : Student.groupby([u'Student_ID', u'Institute_Category', u'Institute_location',
        u'hometown', u'Degree', u'Stream', u'Current_year',
        u'Year_of_graduation', u'Performance_PG', u'PG_scale',
        u'Performance_UG', u'UG_Scale', u'Performance_12th',
        u'Performance_10th',  u'degree_clean',
        u'degree_mas_bac', u'home_college_loc', u'stream_clean', u'UG_performance', u'PG_performance']).size()}).reset_index()

def function_df(Student,var,col_name):
    var_all = ['Profile','Location','Start Date','End Date','Experience_Type']
    var_all.remove(var)
    degree = Student
    degree = degree.drop(var_all, axis=1)
    deg_grp = degree.groupby([u'Student_ID', u'Institute_Category', u'Institute_location',
        u'hometown', u'Degree', u'Stream', u'Current_year',
        u'Year_of_graduation', u'Performance_PG', u'PG_scale',
        u'Performance_UG', u'UG_Scale', u'Performance_12th',
        u'Performance_10th',  u'degree_clean',
        u'degree_mas_bac', u'home_college_loc', u'stream_clean', u'UG_performance', u'PG_performance'])
    otp = deg_grp.apply(lambda x: x.sum())
    return pd.DataFrame({col_name : otp[var]}).reset_index()


job = function_df(Student,'Experience_Type','XP')
text = function_df(Student,'Profile','Prof')
location = function_df(Student,'Location','Locat')


job=job.drop([u'Institute_Category', u'Institute_location',
        u'hometown', u'Degree', u'Stream', u'Current_year',
        u'Year_of_graduation', u'Performance_PG', u'PG_scale',
        u'Performance_UG', u'UG_Scale', u'Performance_12th',
        u'Performance_10th',  u'degree_clean',
        u'degree_mas_bac', u'home_college_loc', u'stream_clean', u'UG_performance', u'PG_performance'],axis = 1)

text = text.drop([ u'Institute_Category', u'Institute_location',
        u'hometown', u'Degree', u'Stream', u'Current_year',
        u'Year_of_graduation', u'Performance_PG', u'PG_scale',
        u'Performance_UG', u'UG_Scale', u'Performance_12th',
        u'Performance_10th',  u'degree_clean',
        u'degree_mas_bac', u'home_college_loc', u'stream_clean', u'UG_performance', u'PG_performance'],axis = 1)

location = location.drop([u'Institute_Category', u'Institute_location',
        u'hometown', u'Degree', u'Stream', u'Current_year',
        u'Year_of_graduation', u'Performance_PG', u'PG_scale',
        u'Performance_UG', u'UG_Scale', u'Performance_12th',
        u'Performance_10th',  u'degree_clean',
        u'degree_mas_bac', u'home_college_loc', u'stream_clean', u'UG_performance', u'PG_performance'],axis = 1)



# merge all the three text df together
student_complete = pd.merge(de, job, how='inner', on='Student_ID')
student_complete = pd.merge(student_complete, text, how='inner', on='Student_ID')
student_complete = pd.merge(student_complete, location, how='inner', on='Student_ID')

# df_all = pd.merge(df_all, df_brand, how='left', on='product_uid')



def str_match(x,str_search):
    return len(re.findall(str_search,x))


student_complete['job_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(job)'))
student_complete['Intern_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(intern)'))
student_complete['academic_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(academic)'))
student_complete['award']= student_complete['XP'].apply(lambda x: str_match(x,r'(award)'))
student_complete['Intern_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(intern)'))
student_complete['other_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(other)'))
student_complete['por_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(por)'))
student_complete['part_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(participa)'))
student_complete['trai_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(train)'))
student_complete['wshop_regex']= student_complete['XP'].apply(lambda x: str_match(x,r'(works)'))

student_complete['worked_IIGB']= student_complete['Locat'].apply(lambda x: str_match(x,r'(IIGB)'))

#degree = pd.read_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/degree.csv')
#degree['name'] = degree


#degree['name'] = degree
def profile_build(s):
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




student_complete['profile_build'] = student_complete['Prof'].apply(profile_build)

# degree['name'] = degree['name'].apply(profile_build)
# degree['name'].to_clipboard()

# student_complete.to_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/student_complete.csv')
student_complete.to_csv('C:/Users/sotripathi/Desktop/Intershala/data/train/student_completev_2.csv',Index = False)

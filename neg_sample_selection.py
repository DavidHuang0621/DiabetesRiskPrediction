disease_periods = pd.read_csv('AP_posnegIDS.csv').drop(columns=['Unnamed: 0'])
PatientInfo = pd.read_csv('Patient.csv')
#PatientInfo.head()

pos_patients = disease_periods.iloc[0:1902].Patient_ID
pos_patients = pos_patients.loc[pos_patients.isin(Results.Patient_ID.unique())]

'''
bad = pos_patients.loc[~pos_patients.isin(Results.Patient_ID.unique())]
print(list(bad))
patient IDs of patients that develop AP but have no Lab results:
[1000100055369,
 1000100549315,
 1000100010363,
 9000900005309,
 11111093511977,
 11113000005142,
 11114000003410,
 4000000319656]
 '''

all_neg_patients = Results.loc[~Results.Patient_ID.isin(pos_patients)].Patient_ID.unique()
neg_patients = pd.Series([], dtype = 'int64')
size = len(pos_patients)
#takes 45 sec ish to run
for i in range(size):
    #print(i)
    refPatient_ID = pos_patients.iloc[i]
    refYOB = PatientInfo.loc[PatientInfo.Patient_ID == refPatient_ID].BirthYear.iloc[0]
    refSex = PatientInfo.loc[PatientInfo.Patient_ID == refPatient_ID].Sex.iloc[0]
    PossiblePatients = PatientInfo.loc[PatientInfo.Patient_ID.isin(all_neg_patients) 
                                       & (PatientInfo.Sex == refSex)]
    selectedPat = False
    yearGap = 0
    while not selectedPat:
        #print(len(PossiblePatients))
        possible = PossiblePatients.loc[(PossiblePatients.BirthYear >= refYOB - yearGap) 
                                        & (PossiblePatients.BirthYear <= refYOB + yearGap)].Patient_ID
        if len(possible > 0):
            selectedPat = possible.sample().iloc[0]
            neg_patients = neg_patients.append(pd.Series([selectedPat], dtype = 'int64'), ignore_index = True)
            all_neg_patients = all_neg_patients[all_neg_patients != selectedPat]
        yearGap += 1

neg_patients.head()
# Eda Ehler, molekulární informatika
# qsar analýza léků proti malárii 
# (predikce účinnosti látky - regrese vypočítaných prediktorů na IC50 (aktivitu))

############################################################
# !!!důležité - spouštím přes anacondu (nainstalovan rdkit)# 
# - mám udělané virt.env "molinf"                          #
# - spustit z příkazové řádky příkazem "activate molinf"   #
# -> "python malaria_regresion.py"                         #
############################################################

# IMPORTY - pandas, numpy, složky rdkitu a scikit-learnu
#--------
import pandas as pd
import numpy as np
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR # vypočet je moc pomalý, nepoužívám
from sklearn.cross_validation import KFold, cross_val_score, train_test_split, cross_val_predict
from sklearn.linear_model import LinearRegression, BayesianRidge, SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, explained_variance_score


# PROMĚNNÉ - input/output
#------------------------
bioactivity = pd.read_csv("bioactivity.txt", sep="\t")
malaria = pd.read_csv("malaria.txt", sep="\t")
out_file = "malaria_output.txt"


# FUNKCE
#-------
def convert_to_nM(radek):
    # pokud má molekula aktivitu v ug.mL-1, převede ji na nM
    if radek["ACTIVITY_UNITS"] == "ug.mL-1":
        act = int(radek["ACTIVITY"])
        molwt = AllChem.CalcExactMolWt(radek["MOL_OBJECT"])
        
        radek["ACTIVITY"] = (act/molwt)*1000000
        radek["ACTIVITY_UNITS"] = "nM"
                
        return radek
    
    else:
        return radek

# funkce na cross-validaci, upraveno dle Garreta, Moncecchi (2013) Learning scikit-learn. Chapter 2, p.29
def evaluate_cross_validation(clf, X, y, K):
    # create a k-fold cross-validation iterator
    cv = KFold(len(y), K, shuffle=False, random_state=0)
    # by default the score used is the one returned by score method of the estimator (accuracy)
    
    scores = []
    
    for train_index, test_index in cv:
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        
        scores.append(train_and_evaluate(clf, X_train, X_test, y_train, y_test))
        #print(scores)
    
    mean_abs_err = sum([x[0] for x in scores])/K
    mean_sqr_err = sum([x[1] for x in scores])/K
    avg_r2 = sum([x[2] for x in scores if (x[2] >= -1 and x[2] <= 1)])/K    # pouze od -1 do 1
    explained_var = sum([x[3] for x in scores if (x[3] >= -1 and x[3] <= 1)])/K # pouze od -1 do 1
    
    print("Mean abs error:", mean_abs_err)
    print("Mean sqr error:", mean_sqr_err)
    print("Coeficient of determination (r2):", avg_r2)
    print("Explained variance:", explained_var)
    
    return (mean_abs_err, mean_sqr_err, avg_r2, explained_var)

# funkce na trénování a evaluaci, upraveno dle Garreta, Moncecchi (2013) Learning scikit-learn. Chapter 2, p.29
def train_and_evaluate(clf, X_train, X_test, y_train, y_test):
    
    clf.fit(X_train, y_train)
    
    #print("Accuracy on training set:")
    #print(clf.score(X_train, y_train))
    #print("Accuracy on testing set:")
    #print(clf.score(X_test, y_test))
    
    y_predicted = clf.predict(X_test)
    
    vysledek = (mean_absolute_error(y_test, y_predicted),
                mean_squared_error(y_test, y_predicted),
                r2_score(y_test, y_predicted),
                explained_variance_score(y_test, y_predicted))
    
    #print("mean_absolute_error:")
    #print(vysledek[0])
    #print("mean_squared_error:")
    #print(vysledek[1])
    #print("r2_score:")
    #print(vysledek[2])
    #print("explained_variance_score:")
    #print(vysledek[3])
    
    return vysledek
        

# VÝPOČTY
#--------
# vyberu jen relevantní sloupce (jméno, smiles na vypočet fingerprintů, aktivitu, jednotky)
bioactivity = bioactivity[["CMPD_CHEMBLID", "CANONICAL_SMILES", "STANDARD_VALUE", "STANDARD_UNITS"]]
malaria = malaria[["CHEMBLID", "CANONICAL_SMILES", "A1_STANDARD_VALUE", "A1_STANDARD_UNITS"]]

# pro rychlé testy vezmu jen 30 prvních řádků##
#bioactivity = bioactivity[:30]               #
#malaria = malaria[:30]                       #
###############################################

# přejmenovat sloupce stejně
jmena_sloupcu = ["CHEMBLID", "SMILES", "ACTIVITY", "ACTIVITY_UNITS"]
bioactivity.columns = jmena_sloupcu
malaria.columns = jmena_sloupcu

# spojit bioactivity a malaria do jedné tabulky, a vyhodit stejná jména
bio_mal = pd.concat([bioactivity, malaria])
bio_mal = bio_mal.drop_duplicates(subset="CHEMBLID")

# dropne všechny řádky, kde je nějaký "NaN" (DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False))
bio_mal = bio_mal.dropna()

#print(bio_mal.head)

# add RDKit mol objects
bio_mal["MOL_OBJECT"] = bio_mal.SMILES.apply(AllChem.MolFromSmiles)
jmena_sloupcu.append("MOL_OBJECT")


# přehodí všechny řádky na stejné jednotky: ug/ml -> g/dm3 -> nM
bio_mal = bio_mal.apply(convert_to_nM, axis=1)


# vypočítá deskriptory z MOL_OBJECT proměnné a přidá je do tabulky
for jmeno, funkce in Descriptors.descList:  # slovnik nazev:funkce na vypocet deskriptoru z mol objektu
    bio_mal[jmeno] = bio_mal.MOL_OBJECT.apply(funkce)

#print(bio_mal.head) 

# dropne sloupce s malým standard deviation (uniformní nebo skoro uniformní deskriptory)
# http://stackoverflow.com/questions/31799187/drop-columns-with-low-standard-deviation-in-pandas-dataframe

threshold = 0.05

data_ready = bio_mal.drop(bio_mal.std()[bio_mal.std() < threshold].index.values, axis=1)

#print(data_ready.shape)

# pro další použití vezmu jen numpy matice prediktorů (variabilní deskriptory)
# a target qsar analýzy -> to je aktivita (de facto hodnota IC50)
prediktory = np.asarray(data_ready.drop(jmena_sloupcu, axis=1))
targety = np.asarray(data_ready.ACTIVITY)

# standardizace
prediktory = StandardScaler().fit_transform(prediktory)

"""
print(prediktory)
input("prediktory")
print(targety)
input("targety")
"""


# REGRESE
#--------
regressors_dict = {  "BayesianRidge": BayesianRidge(),
                    "LinearRegression": LinearRegression(n_jobs=-1),
                    "SGDRegressor": SGDRegressor(loss='squared_loss', penalty=None, random_state=42),
                    #"SVR_linear": SVR(kernel='linear'), # linear function
                    #"SVR_poly": SVR(kernel='poly'), # polynomial funtion
                    #"SVR_rbf": SVR(kernel='rbf')} #radial basis function
                    }


# výpočet a tisk výsledků
with open(out_file, mode="w", encoding="utf-8") as output:
    output.write("Regressor".ljust(20) + "\tmean_abs_err\tmean_sqr_err\tavg_r2\texplained_var\n")
    for name, regressor in regressors_dict.items():
        print(name)
        scores = evaluate_cross_validation(regressor, prediktory, targety, 5)
        
        output.write(name.ljust(20) + "\t")
        output.write(str(round(scores[0], 3)) + "\t")
        output.write(str(round(scores[1], 3)) + "\t")
        output.write(str(round(scores[2], 3)) + "\t")
        output.write(str(round(scores[3], 3)) + "\n")

        print("---")



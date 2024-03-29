# Installation des librairies
from scipy import misc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def update_annotation(ind):
    x,y = line.get_data()
    annotation.xy = (x[ind["ind"][0]], y[ind["ind"][0]])
    text = year_values[ind["ind"][0]]
    annotation.set_text(text)
    annotation.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annotation.get_visible()
    if event.inaxes == ax:
        cont, ind = line.contains(event)
        if cont:
            update_annotation(ind)
            annotation.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annotation.set_visible(False)
                fig.canvas.draw_idle()

def compareListValuesSimilarity(list1, list2):
    similarity = 0
    for i in range(0, len(list1)):
        similarity += abs(list1[i]-list2[i])
    return similarity

def compareListValuesSlidingStandardDeviation(list1, list2, radius):
    similarity = 0
    for i in range(radius, len(list1)-radius):
        similarity += abs(np.std(list1[i-radius:i+radius])-np.std(list2[i-radius:i+radius]))
    return similarity

# ------------ Traitement de la feuille SI ------------

data_climat = pd.read_excel('./data/Climat.xlsx', 'SI ', header=2, usecols="D:O").iloc[1:32]
df_climat_SI = pd.DataFrame(data_climat)

# Calcul des moyennes par mois
print(np.mean(df_climat_SI))

# Ecart-type par mois
print(np.std(df_climat_SI))

# Minimum par mois
print(df_climat_SI.min())

# Maximum par mois
print(df_climat_SI.max())

# Affichage des vues mensuelles
month_number = 0
for month in data_climat.head():
    plt.xlabel('Jours de '+month)
    plt.ylabel('Température (°C)')
    plt.plot(df_climat_SI.iloc[:,month_number])
    month_number = month_number+1
    plt.show()

# Affichage de la vue annuelle 
fig, ax = plt.subplots()

year_values = np.concatenate((df_climat_SI.iloc[:, 0], df_climat_SI.iloc[:, 1], df_climat_SI.iloc[:, 2], df_climat_SI.iloc[:, 3], df_climat_SI.iloc[:, 4], df_climat_SI.iloc[:, 5], df_climat_SI.iloc[:, 6], df_climat_SI.iloc[:, 7], df_climat_SI.iloc[:, 8], df_climat_SI.iloc[:, 9], df_climat_SI.iloc[:, 10], df_climat_SI.iloc[:, 11]))
year_values = [x for x in year_values if str(x) != 'nan']
line, = ax.plot(year_values)
ax.set(xlabel='Jour de l\'année', ylabel='Temperature (°C)', title='Evolution de la température sur l\'année')
annotation = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
plt.show(block=False)

# --------- Traitement de la feuille SI-erreur ---------

data_climat = pd.read_excel('./data/Climat.xlsx', 'SI -erreur', header=2, usecols="D:O").iloc[1:32]
df_climent_SI_erreur = pd.DataFrame(data_climat)

# Suppression des valeurs string en remplaçant pas la moyenne entre la valeur d'avant et celle d'après
for month in range(len(df_climent_SI_erreur.count())):
    for day in range(len(df_climent_SI_erreur.iloc[:, month])):
        if df_climent_SI_erreur.iloc[day, month] == "0xFFFF" or df_climent_SI_erreur.iloc[day, month] == "Sun":
            df_climent_SI_erreur.iloc[day, month] = (df_climent_SI_erreur.iloc[day+1, month] + df_climent_SI_erreur.iloc[day-1, month])/2

for month in range(len(df_climent_SI_erreur.count())):
    avg_month = np.mean(df_climent_SI_erreur.iloc[:, month])
    for day in range(len(df_climent_SI_erreur.iloc[:, month])):
        if np.abs(avg_month-df_climent_SI_erreur.iloc[day, month]) > 20:
            df_climent_SI_erreur.iloc[day, month] = (df_climent_SI_erreur.iloc[day+1, month] + df_climent_SI_erreur.iloc[day-1, month])/2

# Calcul des moyennes par mois
print(np.mean(df_climent_SI_erreur))

# Ecart-type par mois
print(np.std(df_climent_SI_erreur))

# Minimum par mois
print(df_climent_SI_erreur.min())

# Maximum par mois
print(df_climent_SI_erreur.max())

# Affichage des vues mensuelles
month_number = 0
for month in data_climat.head():
    plt.xlabel('Jours de '+month)
    plt.ylabel('Température (°C)')
    plt.plot(df_climent_SI_erreur.iloc[:,month_number])
    month_number = month_number+1
    plt.show()

# Affichage de la vue annuelle 
fig, ax = plt.subplots()

year_values = np.concatenate((df_climent_SI_erreur.iloc[:, 0], df_climent_SI_erreur.iloc[:, 1], df_climent_SI_erreur.iloc[:, 2], df_climent_SI_erreur.iloc[:, 3], df_climent_SI_erreur.iloc[:, 4], df_climent_SI_erreur.iloc[:, 5], df_climent_SI_erreur.iloc[:, 6], df_climent_SI_erreur.iloc[:, 7], df_climent_SI_erreur.iloc[:, 8], df_climent_SI_erreur.iloc[:, 9], df_climent_SI_erreur.iloc[:, 10], df_climent_SI_erreur.iloc[:, 11]))
year_values = [x for x in year_values if str(x) != 'nan']
line, = ax.plot(year_values)
ax.set(xlabel='Jour de l\'année', ylabel='Temperature (°C)', title='Evolution de la température sur l\'année')
annotation = ax.annotate("", xy=(0,0), xytext=(-20,20),textcoords="offset points", bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show(block=False)
plt.show()

# Liste des capitales d'Europe (https://worldpopulationreview.com/continents/capitals/europe)
capitals = ["Mariehamn" ,"Tirana" ,"Andorra la Vella" ,"Vienna" ,"Minsk" ,"Brussels" ,"Sarajevo" ,"Sofia" ,"Zagreb" ,"Nicosia" ,"Prague" ,"Copenhagen" ,"Tallinn" ,"Tórshavn" ,"Helsinki" ,"Paris" ,"Berlin" ,"Gibraltar" ,"Athens" ,"St. Peter Port" ,"Budapest" ,"Reykjavik" ,"Dublin" ,"Douglas" ,"Rome" ,"Saint Helier" ,"Pristina" ,"Riga" ,"Vaduz" ,"Vilnius" ,"Luxembourg" ,"Skopje" ,"Valletta" ,"Chișinău" ,"Monaco" ,"Podgorica" ,"Amsterdam" ,"Oslo" ,"Warsaw" ,"Lisbon" ,"Bucharest" ,"Moscow" ,"City of San Marino" ,"Belgrade" ,"Bratislava" ,"Ljubljana" ,"Madrid" ,"Longyearbyen" ,"Stockholm" ,"Bern" ,"Kiev" ,"London" ,"Vatican City"]

# Lecture d'un fichier récupéré sur Kaggle.com (https://www.kaggle.com/sudalairajkumar/daily-temperature-of-major-cities)
df_kaggle = pd.read_csv('./data/City_temperature_major_cities.csv')

# Filtre sur l'année 2018 et sur les villes d'Europe en retirant les colonnes inutiles à l'analyse
df_kaggle = df_kaggle[(df_kaggle.Year == 2018) & (df_kaggle.Region == 'Europe') & (df_kaggle.City.isin(capitals))].drop(['Country', 'Region', 'State', 'Year'], 1)

# Conversion Fahrenheit ou Celsius
df_kaggle['AvgTemperature'] = (df_kaggle['AvgTemperature']-32)/1.8

# Création du top des villes en fonction des méthodes de calcul
winnersTopAvg = dict()
winnersTopStd = dict()
winnersTopValues = dict()
winnersTopStdSlide = dict()

# Comparaison de la moyenne des températures par mois avec le fichier mystère
for city in list(df_kaggle.groupby("City").groups):
    current_temperatures = list(df_kaggle.groupby("City").get_group(city).groupby("Month")['AvgTemperature'].mean())
    currentScore = compareListValuesSimilarity(list(np.mean(df_climat_SI)), current_temperatures)
    winnersTopAvg[city] = currentScore
winnersTopAvg = dict(sorted(winnersTopAvg.items(), key=lambda item: item[1]))

# Comparaison de l'écart-type des températures par mois avec le fichier mystère
for city in list(df_kaggle.groupby("City").groups):
    current_temperatures = list(df_kaggle.groupby("City").get_group(city).groupby("Month")['AvgTemperature'].std())
    currentScore = compareListValuesSimilarity(list(np.std(df_climat_SI)), current_temperatures)
    winnersTopStd[city] = currentScore
winnersTopStd = dict(sorted(winnersTopStd.items(), key=lambda item: item[1]))

# Comparaison des valeurs des températures par jour avec le fichier mystère
for city in list(df_kaggle.groupby("City").groups):
    current_temperatures = list(df_kaggle.groupby("City").get_group(city)['AvgTemperature'])
    currentScore = compareListValuesSimilarity(year_values, current_temperatures)
    winnersTopValues[city] = currentScore
winnersTopValues = dict(sorted(winnersTopValues.items(), key=lambda item: item[1]))

# Comparaison de l'écart-type glissant par jour avec le fichier mystère
for city in list(df_kaggle.groupby("City").groups):
    current_temperatures = list(df_kaggle.groupby("City").get_group(city)['AvgTemperature'])
    currentScore = compareListValuesSlidingStandardDeviation(year_values, current_temperatures, 15)
    winnersTopStdSlide[city] = currentScore
winnersTopStdSlide = dict(sorted(winnersTopStdSlide.items(), key=lambda item: item[1]))

# Affichage de la ville gagnante en fonction de la méthode de calcul
print('Comparaison des moyennes mensuelles : '+ list(winnersTopAvg.keys())[0])
print('Comparaison des écart-types mensuels : '+ list(winnersTopStd.keys())[0])
print('Comparaison des moyennes quotidiennes : '+ list(winnersTopValues.keys())[0])
print('Comparaison des écart-types glissants : '+ list(winnersTopStdSlide.keys())[0])

# Affichage des villes gagnantes avec graphique
x, y = zip(*list(winnersTopAvg.items())[:5])
plt.xlabel('Villes')
plt.ylabel('Différence de température sur les moyennes mensuelles')
plt.title('Top des villes similaires')
plt.bar(x, y)
plt.show()

x, y = zip(*list(winnersTopStd.items())[:5])
plt.xlabel('Villes')
plt.ylabel('Différence de température sur les écart-types mensuels')
plt.title('Top des villes similaires')
plt.bar(x, y)
plt.show()

x, y = zip(*list(winnersTopValues.items())[:5])
plt.xlabel('Villes')
plt.ylabel('Différence de température cumulée sur les moyennes quotidiennes')
plt.title('Top des villes similaires')
plt.bar(x, y)
plt.show()

x, y = zip(*list(winnersTopStdSlide.items())[:5])
plt.xlabel('Villes')
plt.ylabel('Différence de température sur les écart-types glissants')
plt.title('Top des villes similaires')
plt.bar(x, y)
plt.show()
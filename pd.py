import pandas as pd
import numpy as np 
import requests
import matplotlib.pyplot as plt

def download (url,filename) : 
    response = requests.get (url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
file_path="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"
download(file_path, "usedcars.csv")
file_name="usedcars.csv"
headers = ["symboling","normalized-losses","make","fuel-type","aspiration", "num-of-doors","body-style",
         "drive-wheels","engine-location","wheel-base", "length","width","height","curb-weight","engine-type",
         "num-of-cylinders", "engine-size","fuel-system","bore","stroke","compression-ratio","horsepower",
         "peak-rpm","city-mpg","highway-mpg","price"]
df = pd.read_csv(file_name, names = headers)
df.replace('?',np.nan,inplace=True)
print(df.head(5))
missing_data=df.isnull()
missing_data.head(5)

for column in missing_data.columns.values.tolist() :
    print(column)
    print(missing_data[column].value_counts())
    print("")

avg_norm_loss = df['normalized-losses'].astype('float').mean(axis=0)
print("Average of normalized-losses:",avg_norm_loss)
df['normalized-losses'].replace(np.nan,avg_norm_loss,inplace=True)

avg_bore=df['bore'].astype('float').mean(axis=0)
print("Average of bore:", avg_bore)
df["bore"].replace(np.nan, avg_bore, inplace=True)

#Calculate the mean value for the "horsepower" column¶
avg_horsepower_loss = df ['horsepower'].astype('float').mean(axis=0)
print('Average of horsepower',avg_horsepower_loss)
df["horsepower"].replace(np.nan,avg_horsepower_loss, inplace=True) #Replace "NaN" with the mean value in the "horsepower" column

#Calculate the mean value for "peak-rpm" column
avg_peakrpm=df['peak-rpm'].astype('float').mean(axis=0)
print("Average peak rpm:", avg_peakrpm)
df['peak-rpm'].replace(np.nan, avg_peakrpm, inplace=True) #Replace "NaN" with the mean value in the "peak-rpm" column

#Calculate the mean vaule for "stroke" column
avg_stroke = df["stroke"].astype("float").mean(axis = 0)
print("Average of stroke:", avg_stroke)

# replace NaN by mean value in "stroke" column
df["stroke"].replace(np.nan, avg_stroke, inplace = True)

#To see which values are present in a particular column, we can use the ".value_counts()" method:
#df['num_of_doors'].value_counts()
#".idxmax()" method to calculate the most common type automatically:
df['num-of-doors'].value_counts().idxmax()
#replace the missing 'num-of-doors' values by the most frequent 
df["num-of-doors"].replace(np.nan, "four", inplace=True)

# simply drop whole row with NaN in "price" column
df.dropna(subset=["price"], axis=0, inplace=True)
# reset index, because we droped two rows
df.reset_index(drop=True, inplace=True)
df.head()
df.dtypes
#Convert data types to proper format
df[["bore", "stroke"]] = df[["bore", "stroke"]].astype("float")
df[["normalized-losses"]] = df[["normalized-losses"]].astype("int")
df[["price"]] = df[["price"]].astype("float")
df[["peak-rpm"]] = df[["peak-rpm"]].astype("float")
df.dtypes

# Convert mpg to L/100km by mathematical operation (235 divided by mpg)
df['city-L/100km'] = 235/df["city-mpg"]
df.head()
#transform mpg to L/100km in the column of "highway-mpg"
df['highway_L/100km'] = 235/df["highway-mpg"]
df.head()

#Normalization is the process of transforming values of several variables into a similar range. Typical normalizations include

#scaling the variable so the variable average is 0
#scaling the variable so the variance is 1
#scaling the variable so the variable values range from 0 to 1
# replace (original value) by (original value)/(maximum value)
df['length'] = df['length']/df['length'].max()
df['width'] = df['width']/df['width'].max()
df['height']=df['height']/df['height'].max()

df["horsepower"] = df["horsepower"].astype(int, copy=True)

# Plot histogram
plt.hist(df["horsepower"])
plt.xlabel("horsepower")
plt.ylabel("count")
plt.title("horsepower bins")
plt.show()

bins = np.linspace(min(df["horsepower"]), max(df["horsepower"]), 4)
bins
#Set group names:
group_names = ['Low','Meduim','Hight']
#Apply the function "cut" to determine what each value of `df['horsepower']` belongs to. 
df['horsepower-binned'] = pd.cut(df['horsepower'], bins, labels=group_names, include_lowest=True )
df[['horsepower','horsepower-binned']].head(20)
df["horsepower-binned"].value_counts()
plt.bar(group_names, df["horsepower-binned"].value_counts())

# set x/y labels and plot title
plt.xlabel("horsepower")
plt.ylabel("count")
plt.title("horsepower bins")
plt.show()

df.columns
dummy_variable_1= pd.get_dummies(df['fuel-type'])
dummy_variable_1.head()
#Change the column names for clarity
dummy_variable_1.rename(columns={'gas':'fuel-type-gas', 'diesel':'fuel-type-diesel'}, inplace=True)
dummy_variable_1.head()
df = pd.concat([df, dummy_variable_1],axis=1)
# drop original column "fuel-type" from "df"
df.drop("fuel-type", axis = 1, inplace=True)
df.head()
df.to_csv('cleaned_usedcars.csv', index=False)
import pandas as pd

#lead the current data base 
current_unis_df = pd.read_excel('Physics_departments_formatted_with_photo_counts.xlsx', na_values = 'None')
unis = current_unis_df['University'].sort_values

us_news_unis_df = pd.read_csv("US_new_top_schools.csv")
# us_news_unis = us_news_unis_df['name'].sort_values
unis = []
missing_unis = []

for index,row in current_unis_df.iterrows():
    unis.append(row['University'])

for index,row in us_news_unis_df.iterrows():
    if row['name'] not in unis and row['name']!= 'None':
        missing_unis.append([row['name']])
#write missing universities 
missing_unis_df = pd.DataFrame(missing_unis)
missing_unis_df.to_csv('missing_unis.csv', header=False, index=False)

df = pd.read_csv('missing_unis.csv')
test = []
for index,row in df.iterrows():
    name = row['University'].replace('_',' ')
    test.append([name + ' Physics department faculty'])

dg = pd.DataFrame(test)
dg.to_csv('missing_unis1.csv', header=False, index=False)

# df = pd.read_csv('missing_unis1.csv')
# test = []
# for index,row in df.iterrows():
#     name = row['University'].replace(' ','_')
#     name = name.replace('_Physics_department_faculty','')
#     print(name)
#     test.append([name])

# dg = pd.DataFrame(test)
# dg.to_csv('missing_unis2.csv', header=False, index=False)
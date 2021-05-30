import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

# Remove the columns not required
def remove_columns(dataset):
    dataset.drop(dataset.iloc[:, 38:100], inplace = True, axis=1)
    dataset.drop(dataset.iloc[:, 6:34], inplace = True, axis=1)
    dataset.drop(dataset.iloc[:, 6:7], inplace = True, axis=1)
    return dataset.drop(dataset.iloc[:, 7:8], inplace = True, axis=1)

# Rename the column headers to be short
def rename_column_headers(dataset):
    # Change the column names
    dataset.columns = ['Name','Applicants','Admissions','Enrolled','%_SAT','%_ACT','State','Region']
    return dataset

# transform data so it can be used in graphs and selections
def replace_region_data(dataset):
    # replace or strip the values in Region to only 10 characters
    dataset['Region'] = dataset['Region'].replace(['Southeast AL AR FL GA KY LA MS NC SC TN VA WV',
                               'Mid East DE DC MD NJ NY PA',
                               'Plains IA KS MN MO NE ND SD',
                               'Far West AK CA HI NV OR WA',
                               'Southwest AZ NM OK TX',
                               'Rocky Mountains CO ID MT UT WY',
                               'New England CT ME MA NH RI VT',
                               'Great Lakes IL IN MI OH WI',
                               'US Service schools'],
                              ['Southeast', 'Mid East', 'Plains', 'Far West', 'Southwest', 'Rocky Mountains', 'New England', 'Great Lakes', 'Service School'])
    return dataset

def data_visualization(df):
    chart_data = pd.DataFrame(
         df, columns=['Applicants', 'Admissions', 'Enrolled'])
    st.line_chart(chart_data)

    #########################  Number of Students Enrolled by Region  #####################

    st.write('Number of Students Enrolled by Region')

    basic_chart = alt.Chart(df.groupby(['Region', 'State']). \
                        agg({'Enrolled': 'sum'}).reset_index()).mark_bar().encode(
        x='Region',
        y='Enrolled',
        color='Region' )
    c = alt.layer(basic_chart)
    st.altair_chart(c, use_container_width=True)

    ############################## Students Enrolled by State  #####################
    st.write('Number of Students Enrolled by State')
    basic_chart1 = alt.Chart(df.groupby(['Region', 'State']). \
                        agg({'Enrolled': 'sum'}).reset_index()).mark_bar().encode(
        x='State',
        y='Enrolled',
        tooltip=['State','Enrolled'],
        color='State')
    c = alt.layer(basic_chart1)
    st.altair_chart(c, use_container_width=True)



############################## Top 5 States Students Enrolled  #####################
def condition(df):
    st.write('Top 5 States Students Enrolled')
    st.sidebar.write('*****Condition*****')
    st.sidebar.button('Top 5 States')

    if st.sidebar.button('Top 10 States'):
        top5 = df.groupby(['Region','State'])[['Applicants', 'Admissions', 'Enrolled']].sum().sort_values(by=['Enrolled'], ascending=[False]).head(10)

    else:
        top5 = df.groupby(['Region','State'])[['Applicants', 'Admissions', 'Enrolled']].sum().sort_values(by=['Enrolled'], ascending=[False]).head(5)
    st.dataframe(top5)

    st.write('')
    st.sidebar.write('**************')

############################# Students Enrolled by State  #####################
def sat_act(df):
    st.write('% SAT vs % ACT by State')
    basic_chart = alt.Chart(df.groupby(['Region', 'State']). \
                         agg({'%_SAT': 'mean'}).reset_index()).mark_line(color='red').encode(
        x='State',
        y='%_SAT',
        tooltip=['State','%_SAT'])
    basic_chart1 = alt.Chart(df.groupby(['Region', 'State']). \
                         agg({'%_ACT': 'mean'}).reset_index()).mark_line(color='blue').encode(
        x='State',
        y='%_ACT',
        tooltip=['State','%_ACT'])
    c = alt.layer(basic_chart , basic_chart1)
    st.altair_chart(c, use_container_width=True)
##########################################################################

###########################  University for Selected Region and State  #####################
def detail_data_display(df):
    st.write('University for Selected Region and State')
    region_name = st.sidebar.selectbox('Select a Region', options = df.Region.unique())
    df['% Applicants'] = ((df['Enrolled']/df['Applicants']) * 100).round(0)
    df['% Admissions'] = ((df['Enrolled']/df['Admissions']) * 100).round(0)
    st_name = st.sidebar.selectbox('Select a State', options = df["State"].loc[df["Region"] == region_name].unique())

    #   SAT vs ACT Scores

    scores = df.loc[df.State == st_name].groupby(['Name']). \
                            agg({'Applicants': 'sum',
                                 'Admissions': 'sum',
                                 'Enrolled': 'sum',
                                 '% Applicants': 'sum',
                                 '% Admissions': 'sum',
                                 '%_SAT': 'sum',
                                 '%_ACT': 'sum'
                                 })
    st.dataframe(data=scores,width=924, height=568)

#########################  Data Analysis of College Applications  #####################
# Main Program

    #Milestones for this project
    #Milestone 1: Upload the data
    #Milestone 2: Transform data
    #Milestone 3: Data Analysis by using charts
    #Milestone 4: Sort and apply conditions of data like top 5, top 10
    #Milestone 5: Leverage streamlit functionality and do drowndown features and show data

st.title('Data Analysis on College Data')
# Import the csv file
df = pd.read_csv('CollegeDataAnalysis.csv')

    # Transform data
    #Step 1: Remove columns not required for analysis
    #Step 2: Rename the column headers
    #Step 3: Replace the region data - Instead of a long name have a shorter name

remove_columns(df)
df = rename_column_headers(df)
df = replace_region_data(df)

# Data Visualization - charts
data_visualization(df)
# Conditions - Top 5 and Top 10 by state
condition(df)
sat_act(df)

# Drop down feature by Region and State
detail_data_display(df)












import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 10 charts will open up once you hit run, you will need python downloaded to view them

# Load the data
df_hh_income = pd.read_csv('Median_Household_Income_2015.csv', encoding="windows-1252")
df_pct_poverty = pd.read_csv('Pct_People_Below_Poverty_Level.csv', encoding="windows-1252")
df_pct_completed_hs = pd.read_csv('Pct_Over_25_Completed_High_School.csv', encoding="windows-1252")
df_share_race_city = pd.read_csv('Share_of_Race_By_City.csv', encoding="windows-1252")
df_fatalities = pd.read_csv('Deaths_by_Police_US.csv', encoding="windows-1252")

# Cleaning the data
df_hh_income.dropna(inplace=True)
df_hh_income.drop_duplicates(inplace=True)
df_fatalities.dropna(inplace=True)

# Manipulating data and grouping
df_pct_poverty["poverty_rate"] = df_pct_poverty["poverty_rate"].replace("-", 0)
df_pct_poverty["poverty_rate"] = pd.to_numeric(df_pct_poverty["poverty_rate"])
df_state_poverty = df_pct_poverty.groupby("Geographic Area", as_index=False).agg({"poverty_rate": pd.Series.mean})


# Bar chart of poverty levels per state
def poverty_per_state_bar():
    df_state_poverty_sorted = df_state_poverty.sort_values("poverty_rate")

    plt.figure(figsize=(20, 7), dpi=120)
    plt.title("Poverty Levels per State", fontsize=16)
    plt.ylabel("Poverty Percent", fontsize=12)
    plt.xlabel("State", fontsize=12)

    plt.bar(
        df_state_poverty_sorted["Geographic Area"],
        df_state_poverty_sorted["poverty_rate"],
        color="orange"
    )

    plt.grid(axis="y")

    plt.show()


poverty_per_state_bar()

# # Manipulating data and grouping
df_pct_completed_hs["percent_completed_hs"] = df_pct_completed_hs["percent_completed_hs"].replace("-", 0)
df_pct_completed_hs.percent_completed_hs = pd.to_numeric(df_pct_completed_hs.percent_completed_hs)
df_avg_hs_pct = df_pct_completed_hs.groupby("Geographic Area", as_index=False).agg(
    {"percent_completed_hs": pd.Series.mean})


# Line chart of highschool graduations and poverty levels
def highschool_poverty_line():
    plt.figure(figsize=(14, 7), dpi=120)
    plt.title("Highschool Graduation vs Poverty Percent", fontsize=16)
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    ax1.plot(
        df_avg_hs_pct["Geographic Area"],
        df_avg_hs_pct["percent_completed_hs"],
        linewidth=3,
        color="blue"
    )
    ax2.plot(
        df_state_poverty["Geographic Area"],
        df_state_poverty["poverty_rate"],
        "--r",
        linewidth=3,
    )
    ax1.set_xlabel("State", fontsize=14)
    ax1.set_ylabel("Percent High School Graduation", fontsize=14, color="blue")
    ax2.set_ylabel("Percent Poverty Levels", fontsize=14, color="red")

    plt.grid(linestyle='--', linewidth=0.5)
    plt.show()


highschool_poverty_line()


# Scatter plot of highschool graduations and poverty levels
def highschool_poverty_scatter():
    plt.figure(figsize=(14, 7), dpi=120)
    plt.title("Graduates vs Poverty Levels", fontsize=16)

    plt.scatter(
        df_avg_hs_pct["Geographic Area"],
        df_avg_hs_pct["percent_completed_hs"],
        linewidth=2,
        label="Highschool graduation",
        color="blue"
    )
    plt.scatter(
        df_state_poverty["Geographic Area"],
        df_state_poverty.poverty_rate,
        color="red",
        linewidth=2,
        label="Poverty Level"
    )

    plt.legend()
    plt.show()


highschool_poverty_scatter()


df_avg_hs_pct["poverty_rate"] = df_state_poverty["poverty_rate"]
df_poverty_vs_hs = df_avg_hs_pct.copy()
df_avg_hs_pct.drop("poverty_rate", axis=1, inplace=True)
df_poverty_vs_hs.sample(10)


def highschool_poverty_regression():
    plt.figure(figsize=(14, 7))
    plt.title("Graduates and Poverty Level Relationship", fontsize=12)
    with sns.axes_style("darkgrid"):
        ax = sns.regplot(
            data=df_poverty_vs_hs,
            x="poverty_rate",
            y="percent_completed_hs",
            color='#2f4b7c',
            scatter_kws={'alpha': 0.3},
            line_kws={'color': '#ff7c43'}
        )
        ax.set(
            ylabel='Graduation Levels',
            xlabel='Poverty Levels')
    plt.show()


highschool_poverty_regression()


def age_deaths_histoplot():
    with sns.axes_style("darkgrid"):
        ax = sns.histplot(
            data=df_fatalities,
            x="age",
            kde=True
        )
        ax.set(
            ylabel='Fatalities',
            xlabel='Age',
            title="Death by Age"
        )
    plt.show()


age_deaths_histoplot()


df_share_race_city = df_share_race_city.rename({"share_white":"White", "share_black":"Black", "share_native_american": "Native American", "share_asian": "Asian", "share_hispanic":"Hispanic"}, axis=1)

cols = ['White', 'Black', 'Native American', 'Asian', 'Hispanic']
df_share_race_city[cols] = df_share_race_city[cols].apply(pd.to_numeric, errors='coerce', axis=1)
df_state_races = df_share_race_city.groupby("Geographic area", as_index=False).agg({"White": pd.Series.mean, "Black": pd.Series.mean, "Native American": pd.Series.mean, "Asian": pd.Series.mean, "Hispanic": pd.Series.mean})


def racial_makeup_state_bar():
    race_bar = px.bar(
        df_state_races,
        x="Geographic area",
        y=['White', 'Black', 'Native American', 'Asian', 'Hispanic'],
        title="Average Racial Makeup per State",
        labels={"variable": "Race"}
    )
    race_bar.update_layout(xaxis_title="State", yaxis_title="Value")
    race_bar.show()


racial_makeup_state_bar()


def people_killed_pie():
    abc = df_fatalities.race.value_counts()
    pie = px.pie(
        abc,
        values=abc.values,
        names=abc.index,
        hole=0.5,
        title="People Killed by Race",
        labels={"index": "Race", "values": "Count"}
    )
    pie.update_traces(textposition='outside', textinfo='percent+label')
    pie.show()


people_killed_pie()


def men_vs_female_deaths_bar():
    male_vs_female = df_fatalities.gender.value_counts()
    sex_bar = px.bar(
        male_vs_female,
        x=male_vs_female.index,
        y=male_vs_female.values,
        labels={"index": "Sex", "y": "Count"},
        color=male_vs_female.index,
        title="Male vs Female Deaths"
    )
    sex_bar.update_layout()
    sex_bar.show()


men_vs_female_deaths_bar()


def rate_death_race_bar():
    city_list = ["Los Angeles", "Phoenix", "Houston", "Chicago", "Austin", "Las Vegas", "Columbus", "Miami",
                 "San Antonio", "Indianapolis"]
    df_top10 = df_fatalities[df_fatalities["city"].isin(city_list)]
    df = df_top10.groupby(["city", "race"], as_index=False).agg({"id": pd.Series.count})
    bar = px.bar(
        df,
        x="city",
        y="id",
        color="race",
        labels={"city": "City", "id": "Deaths", "race": "Race"},
        title="Rate of Death by Race"
    )
    bar.update_layout(xaxis={'categoryorder': 'total descending'})

    bar.show()


rate_death_race_bar()


def map_police_killings():
    df_state_fatalities = df_fatalities.groupby("state", as_index=False).agg({"id": pd.Series.count})
    fig = px.choropleth(
        locations=df_state_fatalities.state,
        locationmode="USA-states",
        color=df_state_fatalities.id,
        scope="usa",
        labels={"color": "Deaths", "locations": "State"},
        color_continuous_scale=px.colors.sequential.OrRd,
        title="Map of Police Killings by State"
    )
    fig.show()


map_police_killings()
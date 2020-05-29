import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator


def compare_across_years(column_and_value, df_1, df_2, df_3):
    """ 
    takes a tuple, column_and_value, that is compsed of the column name you want to check 
    and the value which you want to check for in that column. df_1, 2, and 3 are the dataframes which you want to compare.
    All three dataframes must use the same layout ie they should have all the same columns and values,
    just with different rows. 
    All dataframes MUST contain a 'weight' column for accurate calculations. (See pwgtp in the PUMS data dictionary)
    """
    variable = column_and_value[0]
    status = column_and_value[1]
    #takes the column name from the zeroth index of the tuple and takes the value from the first
    
    total_1 = df_1.weight.sum() 
    #sum the weights of the entire dataframe for your total population
    var_total_1 = df_1[df_1[variable] == status].weight.sum() 
    #take a subset of the dataframe that matches the variable and status criteria and sum the weights to get that population
    prct_1 = var_total_1/total_1
    #divide the subset population by the total population for a decimal representing the percent
    
    #repeat the process for the next 2 dataframes
    total_2 = df_2.weight.sum()
    var_total_2 = df_2[df_2[variable] == status].weight.sum()
    prct_2 = var_total_2/total_2
    
    total_3 = df_3.weight.sum()
    var_total_3 = df_3[df_3[variable] == status].weight.sum()
    prct_3 = var_total_3/total_3
    
    return (prct_1, prct_2, prct_3)


def get_oy(df):
    #takes our PUMS dataframe and gives us only the Opportunity Youth from that dataframe
    oy = df[(df['employment_status']=='Unemployed/not in labor force')&
                       (df['school']=='Has not attended in last 3 months')]
    return oy

def line_across_years(column_and_value, df_1, df_2, df_3):
    """ 
    takes a tuple, column_and_value, that is compsed of the column name you want to check 
    and the value which you want to check for in that column. df_1, 2, and 3 are the dataframes which you want to compare.
    All three dataframes must use the same layout ie they should have all the same columns and values,
    just with different rows. 
    All dataframes MUST contain a 'weight' column for accurate calculations. (See pwgtp in the PUMS data dictionary)
    
    Returns a line plot showing the changes in the rate of the column and value you entered in the general youth population
    and in the OY population
    """
    OY_df_1 = get_oy(df_1)
    OY_df_2 = get_oy(df_2)
    OY_df_3 = get_oy(df_3)
    
    x_var = [2014, 2017, 2018]
    
    y_var_oy = compare_across_years(column_and_value, OY_df_1, OY_df_2, OY_df_3)

    y_var_total = compare_across_years(column_and_value, df_1, df_2, df_3)
    
    
    fig, ax = plt.subplots(1,1, figsize=(10,5))

    ax.set_title(f'Rate of {column_and_value[0]}: {column_and_value[1]} in Opportunity Youth Compared to Total Youth')
    ax.set_ylabel('Percent of Sample')

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.plot(x_var, y_var_total, marker='o', color='g', label='Total Youth')
    ax.plot(x_var, y_var_oy, marker='o', color='b', label='Opportunity Youth')
    ax.legend()
#     fig.savefig(column_and_value[0]+'.png')

def compare(column_and_value, df_1, df_2):
    #takes a tuple, column_and_value, that is compsed of the variable column you want to check 
    #and the status which you want to compare. Also takes the data frame you want to look at.
    variable = column_and_value[0]
    status = column_and_value[1]
    
    total_1 = df_1.weight.sum()
    var_total_1 = df_1[df_1[variable] == status].weight.sum()
    prct_1 = var_total_1/total_1
    
    total_2 = df_2.weight.sum()
    var_total_2 = df_2[df_2[variable] == status].weight.sum()
    prct_2 = var_total_2/total_2
    
    return (prct_1, prct_2)

def create_graph(column_and_value, df_1, df_2, col_names=['1','2'], title='title'):
    prct_tuple = compare(column_and_value, df_1, df_2)

    height_values = prct_tuple

    fig, ax1 = plt.subplots(1,1, figsize=(8,8))
    ax1.set_title(title, fontsize=14)
    
    ax1.set_ylabel('Percent of Sample')
    sns.barplot(x=col_names, y=height_values, palette="deep", ax=ax1)
#     ax1.bar(x=col_names, height=height_values)
#    fig.savefig(column_and_value[0]+'.png')

def get_SKC_youth_2018(conn):
    query = """
                SELECT p.puma, rtrim(puma_name), agep,
                            CASE WHEN p.sex = '1' THEN 'male'
                     ELSE 'female'
                     END as gender,
                CASE WHEN p.racasn = '1' THEN 'asian'
                     WHEN p.racblk = '1' THEN 'black or African American'
                     WHEN p.racwht = '1' THEN 'white'
                     WHEN p.hisp <> '1' THEN 'hispanic'
                     END as race_or_ethnicity,
                CASE WHEN p.sch = '1' THEN 'Has not attended in last 3 months'
                     WHEN p.sch IN ('2','3') THEN 'public or private school or college and homeschool'
                     END as School,
                CASE WHEN p.schl in ('16','17') THEN 'HS diploma or GED'
                     WHEN p.schl in ('18','19','20','21','22','23','24') THEN 'post HS education'
                     ELSE 'No HS or GED'
                     END as Education_attainment,
                CASE WHEN p.esr in ('1','2') THEN 'employed'
                     WHEN p.esr in ('3','6') THEN 'Unemployed/not in labor force'
                     WHEN p.esr IN ('4','5') THEN 'Armed Forces'
                     END as Employment_status,
                CASE WHEN p.dis = '1' THEN 'reported disability'
                     ELSE 'no reported disability'
                     END as disability_status,
                CASE WHEN p.ddrs = '1' THEN 'Self-care difficulty'
                     WHEN p.dear = '1' THEN 'Hearing difficulty'
                     WHEN p.deye = '1' THEN 'Vision difficulty'
                     WHEN p.dphy = '1' THEN 'Ambulatory difficulty'
                     WHEN p.drem = '1' THEN 'Cognitive difficulty'
                     ELSE 'None reported'
                     END as disability_type,
                CASE WHEN p.cit IN ('1','2','3','4') THEN 'US Citizen'
                     WHEN p.cit = '5' THEN 'Not US Citizen'
                     END as Citizenship,
                CASE WHEN p.eng IN ('3','4') THEN 'Poor or No English language'
                     ELSE 'English Speaker'
                     END as English_language,
                CASE WHEN p.wkl = '1' THEN 'employed in the last year'
                     WHEN p.wkl in ('2','3') THEN 'not employed in the last year'
                     END AS last_employed,
                CASE WHEN p.esp in ('1','2','3','5','6','7','8') THEN 'One or both parents in labor force'
                     WHEN p.esp = '4' THEN 'Neither parent in labor force'
                     END as Parent_employment,
                CASE WHEN p.mar = '1' THEN 'married'
                     WHEN p.mar = '5' THEN 'never married'
                     ELSE 'divorced, widowed, or separated'
                     END as marital_status,
                CASE WHEN p.fer = '1' THEN 'yes'
                     END AS Child_born_las_year,
                CASE WHEN p.paoc in ('1','2','3') THEN 'own child(ren)'
                     ELSE 'no own children'
                     END as Presence_of_children,
                CASE WHEN p.mig = '1' THEN 'lived here last year'
                     ELSE 'moved here last year'
                     END AS Moved,
                CASE WHEN p.hicov = '1' THEN 'yes'
                     ELSE 'no'
                     END as Has_Health_Insurance,
                pap as Public_Assistance_Income_past_year,
                pwgtp as Weight
                FROM pums_2018 p
                JOIN puma_names_2010 n on p.puma = n.puma
                WHERE state_name = 'Washington'
                AND p.puma IN ('11610', '11611', '11612', '11613', '11614', '11615')
                AND agep BETWEEN 16 AND 24
                ORDER BY school, agep DESC"""

    return pd.read_sql(query, conn)


def get_SKC_youth_2017(conn):
    query = """
            SELECT p.puma, rtrim(puma_name), agep,
                        CASE WHEN p.sex = '1' THEN 'male'
                 ELSE 'female'
                 END as gender,
            CASE WHEN p.racasn = '1' THEN 'asian'
                 WHEN p.racblk = '1' THEN 'black or African American'
                 WHEN p.racwht = '1' THEN 'white'
                 WHEN p.hisp <> '1' THEN 'hispanic'
                 END as race_or_ethnicity,
            CASE WHEN p.sch = '1' THEN 'Has not attended in last 3 months'
                 WHEN p.sch IN ('2','3') THEN 'public or private school or college and homeschool'
                 END as School,
            CASE WHEN p.schl in ('16','17') THEN 'HS diploma or GED'
                 WHEN p.schl in ('18','19','20','21','22','23','24') THEN 'post HS education'
                 ELSE 'No HS or GED'
                 END as Education_attainment,
            CASE WHEN p.esr in ('1','2') THEN 'employed'
                 WHEN p.esr in ('3','6') THEN 'Unemployed/not in labor force'
                 WHEN p.esr IN ('4','5') THEN 'Armed Forces'
                 END as Employment_status,
            CASE WHEN p.dis = '1' THEN 'reported disability'
                 ELSE 'no reported disability'
                 END as disability_status,
            CASE WHEN p.ddrs = '1' THEN 'Self-care difficulty'
                 WHEN p.dear = '1' THEN 'Hearing difficulty'
                 WHEN p.deye = '1' THEN 'Vision difficulty'
                 WHEN p.dphy = '1' THEN 'Ambulatory difficulty'
                 WHEN p.drem = '1' THEN 'Cognitive difficulty'
                 ELSE 'None reported'
                 END as disability_type,
            CASE WHEN p.cit IN ('1','2','3','4') THEN 'US Citizen'
                 WHEN p.cit = '5' THEN 'Not US Citizen'
                 END as Citizenship,
            CASE WHEN p.eng IN ('3','4') THEN 'Poor or No English language'
                 ELSE 'English Speaker'
                 END as English_language,
            CASE WHEN p.wkl = '1' THEN 'employed in the last year'
                 WHEN p.wkl in ('2','3') THEN 'not employed in the last year'
                 END AS last_employed,
            CASE WHEN p.esp in ('1','2','3','5','6','7','8') THEN 'One or both parents in labor force'
                 WHEN p.esp = '4' THEN 'Neither parent in labor force'
                 END as Parent_employment,
            CASE WHEN p.mar = '1' THEN 'married'
                 WHEN p.mar = '5' THEN 'never married'
                 ELSE 'divorced, widowed, or separated'
                 END as marital_status,
            CASE WHEN p.fer = '1' THEN 'yes'
                 END AS Child_born_las_year,
            CASE WHEN p.paoc in ('1','2','3') THEN 'own child(ren)'
                 ELSE 'no own children'
                 END as Presence_of_children,
            CASE WHEN p.mig = '1' THEN 'lived here last year'
                 ELSE 'moved here last year'
                 END AS Moved,
            CASE WHEN p.hicov = '1' THEN 'yes'
                 ELSE 'no'
                 END as Has_Health_Insurance,
            pap as Public_Assistance_Income_past_year,
            pwgtp as Weight
            FROM pums_2017 p
            JOIN puma_names_2010 n on p.puma = n.puma
            WHERE state_name = 'Washington'
            AND p.puma IN ('11610', '11611', '11612', '11613', '11614', '11615')
            AND agep BETWEEN 16 AND 24
            ORDER BY school, agep DESC"""

    return pd.read_sql(query, conn)

def get_SKC_youth_2014(conn):
    query = """
            SELECT p.puma10, rtrim(puma_name), agep,
                        CASE WHEN p.sex = '1' THEN 'male'
                 ELSE 'female'
                 END as gender,
            CASE WHEN p.racasn = '1' THEN 'asian'
                 WHEN p.racblk = '1' THEN 'black or African American'
                 WHEN p.racwht = '1' THEN 'white'
                 WHEN p.hisp <> '1' THEN 'hispanic'
                 END as race_or_ethnicity,
            CASE WHEN p.sch = '1' THEN 'Has not attended in last 3 months'
                 WHEN p.sch IN ('2','3') THEN 'public or private school or college and homeschool'
                 END as School,
            CASE WHEN p.schl in ('16','17') THEN 'HS diploma or GED'
                 WHEN p.schl in ('18','19','20','21','22','23','24') THEN 'post HS education'
                 ELSE 'No HS or GED'
                 END as Education_attainment,
            CASE WHEN p.esr in ('1','2') THEN 'employed'
                 WHEN p.esr in ('3','6') THEN 'Unemployed/not in labor force'
                 WHEN p.esr IN ('4','5') THEN 'Armed Forces'
                 END as Employment_status,
            CASE WHEN p.dis = '1' THEN 'reported disability'
                 ELSE 'no reported disability'
                 END as disability_status,
            CASE WHEN p.ddrs = '1' THEN 'Self-care difficulty'
                 WHEN p.dear = '1' THEN 'Hearing difficulty'
                 WHEN p.deye = '1' THEN 'Vision difficulty'
                 WHEN p.dphy = '1' THEN 'Ambulatory difficulty'
                 WHEN p.drem = '1' THEN 'Cognitive difficulty'
                 ELSE 'None reported'
                 END as disability_type,
            CASE WHEN p.cit IN ('1','2','3','4') THEN 'US Citizen'
                 WHEN p.cit = '5' THEN 'Not US Citizen'
                 END as Citizenship,
            CASE WHEN p.eng IN ('3','4') THEN 'Poor or No English language'
                 ELSE 'English Speaker'
                 END as English_language,
            CASE WHEN p.wkl = '1' THEN 'employed in the last year'
                 WHEN p.wkl in ('2','3') THEN 'not employed in the last year'
                 END AS last_employed,
            CASE WHEN p.esp in ('1','2','3','5','6','7','8') THEN 'One or both parents in labor force'
                 WHEN p.esp = '4' THEN 'Neither parent in labor force'
                 END as Parent_employment,
            CASE WHEN p.mar = '1' THEN 'married'
                 WHEN p.mar = '5' THEN 'never married'
                 ELSE 'divorced, widowed, or separated'
                 END as marital_status,
            CASE WHEN p.fer = '1' THEN 'yes'
                 END AS Child_born_las_year,
            CASE WHEN p.paoc in ('1','2','3') THEN 'own child(ren)'
                 ELSE 'no own children'
                 END as Presence_of_children,
            CASE WHEN p.mig = '1' THEN 'lived here last year'
                 ELSE 'moved here last year'
                 END AS Moved,
            CASE WHEN p.hicov = '1' THEN 'yes'
                 ELSE 'no'
                 END as Has_Health_Insurance,
            pap as Public_Assistance_Income_past_year,
            pwgtp as Weight
            FROM pums_2014 p
            JOIN puma_names_2010 n on p.puma10 = n.puma
            WHERE state_name = 'Washington'
            AND p.puma10 IN ('11610', '11611', '11612', '11613', '11614', '11615')
            AND agep BETWEEN 16 AND 24
            ORDER BY school, agep DESC"""

    return pd.read_sql(query, conn)

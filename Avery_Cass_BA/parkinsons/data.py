"""
Author: Avery Soh
Date: 14/05/2019
Version: 2.1
Email: averysoh@outlook.com

"""

import numpy as np
import pandas as pd
from os.path import dirname, join


def process_data():

    # Import the Risk Dataset
    risk = pd.read_csv(join(dirname(__file__), 'data', 'IHME-GBD_2017_DATA-All-Risks.csv'))

    # cholesterol in YLDs
    chol = risk.loc[risk['rei_name'] == 'High LDL cholesterol']
    chol = chol.rename(columns={'val': 'cholesterol'})

    # Fasting Plasma Glucose in YLDs
    glucose = risk.loc[risk['rei_name'] == 'High fasting plasma glucose']
    glucose = glucose.rename(columns={'val': 'glucose'})

    # High body-mass index in YLDs
    bmi = risk.loc[risk['rei_name'] == 'High body-mass index']
    bmi = bmi.rename(columns={'val': 'bmi'})

    # Diet low in legumes in YLDs
    legumes = risk.loc[risk['rei_name'] == 'Diet low in legumes']
    legumes = legumes.rename(columns={'val': 'legumes'})

    # Diet low in fruits in YLDs
    fruits = risk.loc[risk['rei_name'] == 'Diet low in fruits']
    fruits = fruits.rename(columns={'val': 'fruits'})

    # Diet low in milk in YLDs
    milk = risk.loc[risk['rei_name'] == 'Diet low in milk']
    milk = milk.rename(columns={'val': 'milk'})

    # Diet low in whole grains in YLDs
    grains = risk.loc[risk['rei_name'] == 'Diet low in whole grains']
    grains = grains.rename(columns={'val': 'grains'})

    # Diet high in processed meat in YLDs
    meat = risk.loc[risk['rei_name'] == 'Diet high in processed meat']
    meat = meat.rename(columns={'val': 'processed_meat'})

    # Diet low in vegetables in YLDs
    veg = risk.loc[risk['rei_name'] == 'Diet low in vegetables']
    veg = veg.rename(columns={'val': 'veg'})

    # Diet high in sugar-sweetened beverages in YLDs
    sugar = risk.loc[risk['rei_name'] == 'Diet high in sugar-sweetened beverages']
    sugar = sugar.rename(columns={'val': 'sugar'})

    # Diet high in sodium in YLDs
    sodium = risk.loc[risk['rei_name'] == 'Diet high in sodium']
    sodium = sodium.rename(columns={'val': 'sodium'})

    # Merge risk dataset
    df_risk = pd.merge(chol[['location_name', 'sex_name', 'year', 'cholesterol']],
                       glucose[['location_name', 'sex_name', 'year', 'glucose']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       bmi[['location_name', 'sex_name', 'year', 'bmi']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       legumes[['location_name', 'sex_name', 'year', 'legumes']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       fruits[['location_name', 'sex_name', 'year', 'fruits']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       milk[['location_name', 'sex_name', 'year', 'milk']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       grains[['location_name', 'sex_name', 'year', 'grains']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       meat[['location_name', 'sex_name', 'year', 'processed_meat']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       veg[['location_name', 'sex_name', 'year', 'veg']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       sugar[['location_name', 'sex_name', 'year', 'sugar']],
                       on=['location_name', 'sex_name', 'year'])

    df_risk = pd.merge(df_risk,
                       sodium[['location_name', 'sex_name', 'year', 'sodium']],
                       on=['location_name', 'sex_name', 'year'])

    # Import the Direct Risk Dataset
    direct = pd.read_csv(join(dirname(__file__), 'data', 'IHME-GBD_2017_DATA-direct_cause_PD.csv'))

    # Smoking in YLDs
    smoking = direct.loc[direct['rei_name'] == 'Smoking']
    smoking = smoking.rename(columns={'val': 'smoking'})

    df_risk = pd.merge(df_risk,
                       smoking[['location_name', 'sex_name', 'year', 'smoking']],
                       on=['location_name', 'sex_name', 'year'])

    # Import the Parkinson's prevalence dataset
    cause = pd.read_csv(join(dirname(__file__), 'data', 'IHME-GBD_2017_DATA-PD_Incidence_prevalence.csv'))
    pv = cause.loc[cause["measure_id"] == 5]  # Prevalence of Parkinsons
    pv = pv.rename(columns={"val": "prevalence"})

    incidence = cause.loc[cause["measure_id"] == 6]  # Incidence of Parkinsons
    incidence = incidence.rename(columns={"val": "incidence"})

    df = pd.merge(df_risk,
                  pv[['location_name', 'sex_name', 'year', 'prevalence']],
                  on=['location_name', 'sex_name', 'year'])

    df = pd.merge(df,
                  incidence[['location_name', 'sex_name', 'year', 'incidence']],
                  on=['location_name', 'sex_name', 'year'])

    # Import the region dataset
    regions = pd.read_csv(join(dirname(__file__), 'data', 'region.csv'))
    regions.rename({'Country': 'location_name'}, axis='columns', inplace=True)
    regions.rename({'Group': 'regions'}, axis='columns', inplace=True)

    # Merge the data and create a single df
    df = pd.merge(df,
                  regions,
                  on="location_name")

    a = ['Smoking']
    a.extend(risk.rei_name.unique())
    risk_list = sorted(a)

    return df, risk_list

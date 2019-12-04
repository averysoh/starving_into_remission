"""
Author: Avery Soh
Date: 14/05/2019
Updated: 03/12/2019
Version: 2.2
Bokeh Version: 1.4.0
Email: averysoh@outlook.com

"""

import pandas as pd
import numpy as np
import math

from data import process_data
from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout, column
from bokeh.palettes import Blues8, PuRd6, RdPu9, PuBu9
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, SingleIntervalTicker,\
    Slider, Button, Label, CategoricalColorMapper, Legend, Circle, CheckboxButtonGroup, Select, NumeralTickFormatter

###############
# Import Data #
###############
# Import the Dataset from process_data
df, risk_list = process_data()

# Widgets to add, country list select, region select, x axis select, male female select

# Setting the size factor of each point
scale_factor = 1100
parkinsons_size = 10 * (scale_factor * (df["prevalence"]))
df.loc[:, "parkinsons_size"] = parkinsons_size


# Create the necessary years, region, country, risk names list
years = list(range(1990, 2018, 1))
regions_list = list(df.regions.unique())

a = df.location_name.unique()
country_list = ['None Selected']
country_list.extend(sorted(a))

risk_map = {
    'Diet high in processed meat': 'processed_meat',
    'Diet high in sodium': 'sodium',
    'Diet high in sugar-sweetened beverages': 'sugar',
    'Diet low in fruits': 'fruits',
    'Diet low in legumes': 'legumes',
    'Diet low in milk': 'milk',
    'Diet low in vegetables': 'veg',
    'Diet low in whole grains': 'grains',
    'High LDL cholesterol': 'cholesterol',
    'High body-mass index': 'bmi',
    'High fasting plasma glucose': 'glucose',
    'Smoking': 'smoking',
}

# Extract from the dataset the male and female categories followed by the necessary relevant data
df_both = df.copy()

############################
# Functions to filter Data #
############################


# Create a function to filter dataset by year
def country_data(year, country):
    '''
    Creates two dataframes based on a selected period and country
    For specific use in country selection from dropdown to plot course of single country
    :param year: year from years
    :param country: country from country_list
    :return: 2 Dataframes, 1 for men and 1 for women
    '''
    df_men = df_both.loc[df_both["sex_name"] == "Male"]
    data_men = df_men.loc[df_men['year'] == year]
    data_men = data_men.loc[data_men['location_name'] == country]

    df_women = df_both.loc[df_both["sex_name"] == "Female"]
    data_women = df_women.loc[df_women['year'] == year]
    data_women = data_women.loc[data_women['location_name'] == country]

    return data_men, data_women


def region_data(year, region):
    '''
    Creates two dataframes based on a selected period and region
    :param year: year from years
    :param region: region from region_list
    :return: 2 Dataframes, 1 for men and 1 for women
    '''
    df_men = df_both.loc[df_both["sex_name"] == "Male"]
    data_men = df_men.loc[df_men['year'] == year]
    data_men = data_men.loc[data_men['regions'] == region]

    df_women = df_both.loc[df_both["sex_name"] == "Female"]
    data_women = df_women.loc[df_women['year'] == year]
    data_women = data_women.loc[data_women['regions'] == region]

    return data_men, data_women


# Establishing the data source
m_america = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                       parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
w_america = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                       parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
m_eu_asia = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                       parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
w_eu_asia = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                       parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
m_sub_africa = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                          parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
w_sub_africa = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                          parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
m_mid_africa = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                          parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
w_mid_africa = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                          parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
m_pacific = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                       parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
w_pacific = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                       parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
m_sea = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                   parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
w_sea = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                   parkinsons_size=[], prevalence=[], sex_name=[], year=[]))

country_men_src = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                             parkinsons_size=[], prevalence=[], sex_name=[], year=[]))
country_women_src = ColumnDataSource(data=dict(x=[], y=[], location_name=[], regions=[],
                                               parkinsons_size=[], prevalence=[], sex_name=[], year=[]))

########
# Plot #
########
# Set the plot environment, x-axis = sugar, y-axis = Incidence of parkinsons
plot = figure(y_range=(0, max(df_both["incidence"]) * 1.1),
              title="Parkinson's Disease Prevalence",
              x_axis_type="log",
              tools="pan,tap,lasso_select,wheel_zoom,reset,save",
              toolbar_location="above",
              plot_height=450, plot_width=700,
              x_range=(0.15*(10**min(df['sugar']) - 1), 0.3*(10**max(df['sugar']) + 0.1))
              )
# To log and fix the x axis
#             x_range=(10 ** -5.5, 10 ** 0),
#             x_axis_type="log",

plot.title.text_font_size = "16px"
plot.xaxis.axis_label = "Diet high in sugar-sweetened beverages"
plot.yaxis.axis_label = "Incidence of Parkinson's Disease (percentage %)"
plot.yaxis.formatter = NumeralTickFormatter(format='0.000%')
bg_colour = '#fff9ed'
plot.background_fill_color = bg_colour
plot.border_fill_color = bg_colour

# Set the label on the top left corner to indicate the current year the data is presenting
label = Label(x=10**-5.2, y=9e-5, text=str(years[0]), text_font_size='60pt', text_color='#8a8a8a')
plot.add_layout(label)

# Alpha of glyph renderer for legend and plots
alpha_plot = 0.4
alpha = 0.75

# Plot points
# Plot Male Regions
Europe = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=m_eu_asia, fill_color="#084594", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
Middle = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=m_mid_africa, fill_color="#2171b5", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
East = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=m_pacific, fill_color="#4292c6", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
Sub = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=m_sub_africa, fill_color="#6baed6", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
America = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=m_america, fill_color="#9ecae1", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
South = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=m_sea, fill_color="#c6dbef", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)

# Plot Female Region
Europe_f = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=w_eu_asia, fill_color="#980043", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
Middle_f = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=w_mid_africa, fill_color="#dd1c77", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
East_f = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=w_pacific, fill_color="#df65b0", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
Sub_f = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=w_sub_africa, fill_color="#c994c7", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
America_f = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=w_america, fill_color="#d4b9da", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)
South_f = plot.circle(x='x', y='y', size='parkinsons_size',
                     source=w_sea, fill_color="#f1eef6", line_color='#7c7e71',
                     line_width=0.5, line_alpha=0.5, fill_alpha=alpha_plot)

# Plot selected country
country_m = plot.circle(
            x='x',
            y='y',
            size='parkinsons_size',
            source=country_men_src,
            fill_alpha=0.9,
            fill_color="#084594",
            line_color=None
        )
country_w = plot.circle(
            x='x',
            y='y',
            size='parkinsons_size',
            source=country_women_src,
            fill_alpha=0.9,
            fill_color="#980043",
            line_color=None
        )

# Add the tools
TOOLTIPS = [
    ('Country', "@location_name"),
    ('Region', "@regions"),
    ('Gender', '@sex_name'),
    ('Prevalence', "@prevalence{(0.0000 %)}"),
    ("(x,y)", "($x, $y)"),
]

plot.add_tools(HoverTool(tooltips=TOOLTIPS, show_arrow=False, point_policy='follow_mouse'))


# Legend configuration
legend = Legend(
    items=[("Europe & Central Asia", [Europe]),
           ("Middle East & North Africa", [Middle]),
           ("East Asia & Pacific", [East]),
           ("Sub-Saharan Africa", [Sub]),
           ("America", [America]),
           ("South Asia", [South]),
           ("Europe & Central Asia", [Europe_f]),
           ("Middle East & North Africa", [Middle_f]),
           ("East Asia & Pacific", [East_f]),
           ("Sub-Saharan Africa", [Sub_f]),
           ("America", [America_f]),
           ("South Asia", [South_f])
           ],
    location="top_center", orientation="vertical",
)

plot.add_layout(legend, "right")
plot.legend.background_fill_alpha = 0.0
plot.legend.click_policy = "hide"


# Creating the animation function
def animate_update():
    year = year_slider.value + 1
    if year > years[-1]:
        year = years[0]
    year_slider.value = year


# Updating the animation function
def update():
    year = year_slider.value
    country = country_choice.value
    label.text = str(year)

    x_name_ = risk_map[x_name.value]
    plot.xaxis.axis_label = x_name.value
    plot.x_range.start = 0.15*(10**min(df[x_name_]) - 1)
    plot.x_range.end = 0.3*(10**max(df[x_name_]) + 0.1)

    m_a, w_a = region_data(year, 'America')
    m_america.data = dict(
        x=m_a[x_name_],
        y=m_a['incidence'],
        location_name=m_a['location_name'],
        regions=m_a['regions'],
        parkinsons_size=m_a['parkinsons_size'],
        prevalence=m_a['prevalence'],
        sex_name=m_a['sex_name'],
        year=m_a['year']
    )
    w_america.data = dict(
        x=w_a[x_name_],
        y=w_a['incidence'],
        location_name=w_a['location_name'],
        regions=w_a['regions'],
        parkinsons_size=w_a['parkinsons_size'],
        prevalence=w_a['prevalence'],
        sex_name=w_a['sex_name'],
        year=w_a['year']
    )

    m_a, w_a = region_data(year, 'Europe & Central Asia')
    m_eu_asia.data = dict(
        x=m_a[x_name_],
        y=m_a['incidence'],
        location_name=m_a['location_name'],
        regions=m_a['regions'],
        parkinsons_size=m_a['parkinsons_size'],
        prevalence=m_a['prevalence'],
        sex_name=m_a['sex_name'],
        year=m_a['year']
    )
    w_eu_asia.data = dict(
        x=w_a[x_name_],
        y=w_a['incidence'],
        location_name=w_a['location_name'],
        regions=w_a['regions'],
        parkinsons_size=w_a['parkinsons_size'],
        prevalence=w_a['prevalence'],
        sex_name=w_a['sex_name'],
        year=w_a['year']
    )

    m_a, w_a = region_data(year, 'Sub-Saharan Africa')
    m_sub_africa.data = dict(
        x=m_a[x_name_],
        y=m_a['incidence'],
        location_name=m_a['location_name'],
        regions=m_a['regions'],
        parkinsons_size=m_a['parkinsons_size'],
        prevalence=m_a['prevalence'],
        sex_name=m_a['sex_name'],
        year=m_a['year']
    )
    w_sub_africa.data = dict(
        x=w_a[x_name_],
        y=w_a['incidence'],
        location_name=w_a['location_name'],
        regions=w_a['regions'],
        parkinsons_size=w_a['parkinsons_size'],
        prevalence=w_a['prevalence'],
        sex_name=w_a['sex_name'],
        year=w_a['year']
    )

    m_a, w_a = region_data(year, 'Middle East & North Africa')
    m_mid_africa.data = dict(
        x=m_a[x_name_],
        y=m_a['incidence'],
        location_name=m_a['location_name'],
        regions=m_a['regions'],
        parkinsons_size=m_a['parkinsons_size'],
        prevalence=m_a['prevalence'],
        sex_name=m_a['sex_name'],
        year=m_a['year']
    )
    w_mid_africa.data = dict(
        x=w_a[x_name_],
        y=w_a['incidence'],
        location_name=w_a['location_name'],
        regions=w_a['regions'],
        parkinsons_size=w_a['parkinsons_size'],
        prevalence=w_a['prevalence'],
        sex_name=w_a['sex_name'],
        year=w_a['year']
    )

    m_a, w_a = region_data(year, 'East Asia & Pacific')
    m_pacific.data = dict(
        x=m_a[x_name_],
        y=m_a['incidence'],
        location_name=m_a['location_name'],
        regions=m_a['regions'],
        parkinsons_size=m_a['parkinsons_size'],
        prevalence=m_a['prevalence'],
        sex_name=m_a['sex_name'],
        year=m_a['year']
    )
    w_pacific.data = dict(
        x=w_a[x_name_],
        y=w_a['incidence'],
        location_name=w_a['location_name'],
        regions=w_a['regions'],
        parkinsons_size=w_a['parkinsons_size'],
        prevalence=w_a['prevalence'],
        sex_name=w_a['sex_name'],
        year=w_a['year']
    )

    m_a, w_a = region_data(year, 'South Asia')
    m_sea.data = dict(
        x=m_a[x_name_],
        y=m_a['incidence'],
        location_name=m_a['location_name'],
        regions=m_a['regions'],
        parkinsons_size=m_a['parkinsons_size'],
        prevalence=m_a['prevalence'],
        sex_name=m_a['sex_name'],
        year=m_a['year']
    )
    w_sea.data = dict(
        x=w_a[x_name_],
        y=w_a['incidence'],
        location_name=w_a['location_name'],
        regions=w_a['regions'],
        parkinsons_size=w_a['parkinsons_size'],
        prevalence=w_a['prevalence'],
        sex_name=w_a['sex_name'],
        year=w_a['year']
    )

    plot.title.text = "Parkinson's Disease Prevalence in %s" % year

    if country != 'None Selected':
        country_men, country_women = country_data(year, country)
        country_men_src.data = dict(
            x=country_men[x_name_],
            y=country_men['incidence'],
            location_name=country_men['location_name'],
            regions=country_men['regions'],
            parkinsons_size=country_men['parkinsons_size'],
            prevalence=country_men['prevalence'],
            sex_name=country_men['sex_name'],
            year=country_men['year']
        )

        country_women_src.data = dict(
            x=country_women[x_name_],
            y=country_women['incidence'],
            location_name=country_women['location_name'],
            regions=country_women['regions'],
            parkinsons_size=country_women['parkinsons_size'],
            prevalence=country_women['prevalence'],
            sex_name=country_women['sex_name'],
            year=country_women['year']
        )

    else:
        country_men_src.data = dict(
            x=[], y=[], location_name=[], regions=[],
            parkinsons_size=[], prevalence=[], sex_name=[], year=[])

        country_women_src.data = dict(
            x=[], y=[], location_name=[], regions=[],
            parkinsons_size=[], prevalence=[], sex_name=[], year=[])


# Set the starting point of the animation
year_slider = Slider(start=years[0], end=years[-1], value=years[0], step=1, title="Year")
year_slider.on_change('value', lambda attr, old, new: update())

country_choice = Select(title='Country Choice', value='All', options=country_list)
country_choice.on_change('value', lambda attr, old, new: update())

x_name = Select(title='X-axis Choice', value='Diet high in sugar-sweetened beverages', options=risk_list)
x_name.on_change('value', lambda attr, old, new: update())


callback_id = None


# Set the speed for animation function here
def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 500)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)


button = Button(label='► Play', width=60)
button.on_click(animate)

# Initialise the process
update()

layout = layout([
    [plot],
    [year_slider, button],
    [country_choice, x_name]
], sizing_mode='scale_width', name='layout')

curdoc().add_root(layout)
curdoc().title = "Parkinsons Incidence Rate against various risks"

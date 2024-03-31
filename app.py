import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import pandas
from shiny import render, reactive
import seaborn as sns
import palmerpenguins  # This package provides the Palmer Penguins dataset


# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()
penguins_df_r = penguins_df.rename(columns={"bill_depth_mm": "Bill Depth (mm)", "bill_length_mm": "Bill Length (mm)", 
"flipper_length_mm": "Flipper Length (mm)", "body_mass_g": "Body Mass (g)", "species": "Species", "island": "Island", "sex": "Sex", "year": "Year"})



ui.page_opts(title="Teslim", fillable=True)

#Shiny UI sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    
    # Create a dropdown input to choose a column 
    ui.input_selectize("selected_attribute", "Body Measurement in Millimeters", choices=["Bill Length (mm)", "Bill Depth (mm)", "Flipper Length (mm)", "Body Mass (g)"]) 
    
    # Create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 10)
    
    # Create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 100, 50)

    # Create a checkbox group input to filter the species
    ui.input_checkbox_group("selected_species_list", "Selected Species of Penguins", 
                            ["Adelie", "Gentoo", "Chinstrap"], selected="Adelie", inline=False)

    # Add a horizontal rule to the sidebar
    ui.hr()

    # Add a hyperlink to the sidebar
    ui.a("GitHub",
        href="https://github.com/Tezzyray/cintel-02-data",
        target="_blank",)

# Show Data
with ui.card(full_screen=False):

    @render.data_frame
    def penguins_datatable():
        pen_dt = render.DataTable(filtered_data()) 
        return pen_dt

# Show Data
with ui.card(full_screen=True):#with ui.card(full_screen=True):
    @render.data_frame
    def penguins_grid():
        pen_grid = render.DataGrid(filtered_data())
        return pen_grid

# Plot Charts
with ui.card(full_screen=True):
    @render_plotly  
    def plot_plt():  
        plot_px = px.histogram(filtered_data(),
                            x=input.selected_attribute(),
                            nbins=input.plotly_bin_count(),
                            title="Plotly Penguin Body Measurements Histogram",
                            color="Species",
                            labels={"count": "Count"}
                           )
        plot_px.update_layout(yaxis_title="Count")
        return plot_px
        
    @render.plot  
    def plot_sns():  
        
        plot_snshist = sns.histplot(data=filtered_data(),
                            x=input.selected_attribute(),
                            bins=input.seaborn_bin_count(),
                            element="step",
                            hue="Species",
                            kde=False)
        plot_snshist.set_title("Seaborn Histogram of Body Measurements by Species")
        return plot_snshist




#Create Scatter plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
        return px.scatter(filtered_data(), x="Flipper Length (mm)", y="Bill Length (mm)", color="Species", 
                          facet_row="Species", facet_col="Sex", title="Penguin Scatterplot")


# Pie Chart plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Pie Chart: Body Mass")

    @render_plotly
    def plotly_pie():
        pie_chart = px.pie(filtered_data(), values="Body Mass (g)", names="Island", title="Body mass on Islands")
        return pie_chart

    @render_plotly
    def plotly_pie_s():
        pie_chart = px.pie(filtered_data(), values="Body Mass (g)", names="Species", title="Body mass from Species")
        return pie_chart

# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    return penguins_df_r[penguins_df_r["Species"].isin(input.selected_species_list())]

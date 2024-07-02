import altair as alt
import pandas as pd
import plotly.express as px
import seaborn as sns
import sys
import warnings


def plot_altair_multiline_highlight(data, x, y, **kwargs):
    """
    Diese Funktion erstellt ein interaktives Liniendiagramm in Altair. Doku dazu unter: https://altair-viz.github.io/gallery/ resp. https://altair-viz.github.io/gallery/multiline_highlight.html
    Aktuellste Version (2024-05-16). Im Vergleich zur vorherigen Version wurde der Umgang mit Parametern vereinfacht.
    Die genaue Reihenfolge der Parameter ist nicht mehr so wichtig wie zuvor. Die kwargs (keyword arguments) sind optional. Nutzung von kwargs.get für die optionalen Parameter, um Standardwerte festzulegen.

    Parameter (zwingend):
    - data (DataFrame): Die Daten, die für das Diagramm verwendet werden sollen.
    - x (str): Die Spalte für die X-Achse.
    - y (str): Die Spalte für die Y-Achse.

    Optionale Parameter:
    - myTitle (str): Der Titel des Diagramms.
    - x_beschriftung (str): Titel der X-Achse.
    - y_beschriftung (str): Titel der Y-Achse.
    - category (str): Die Spalte, die die Kategorien für die Farbcodierung darstellt. Default: '' (leerer String).
    - category_beschriftung (str): Legendentitel.
    - warning_status (str): Der Status der Warnmeldungen. 'always' oder 'ignore' 

    Rückgabe:
    - chart (alt.Chart): Das erstellte interaktive Diagramm.
    """
    try:
        #Defaultwerte der kwargs, falls nichts mitgegeben wird      
        myTitle = kwargs.get('myTitle', '')
        x_beschriftung = kwargs.get('x_beschriftung', '')
        y_beschriftung = kwargs.get('y_beschriftung', '')
        category = kwargs.get('category', '')
        category_beschriftung = kwargs.get('category_beschriftung', '')
        warning_status = kwargs.get('warning_status', 'ignore')

        highlight = alt.selection_point(on='pointerover', fields=[category], nearest=True)

        # Überprüfen, ob category_beschriftung definiert ist, bevor sie verwendet wird
        if category == '':
            base = alt.Chart(data, title=myTitle).encode(
                x=alt.X(x, axis=alt.Axis(title=x_beschriftung)),
                y=alt.Y(y, axis=alt.Axis(title=y_beschriftung)),
                tooltip=[x, y]
            )            

        else:
            base = alt.Chart(data, title=myTitle).encode(
                x=alt.X(x, axis=alt.Axis(title=x_beschriftung)),
                y=alt.Y(y, axis=alt.Axis(title=y_beschriftung)),
                color=alt.Color(category, legend=alt.Legend(title=category_beschriftung, orient="right")),
                tooltip=[x, category, y]
            )

        points = base.mark_circle().encode(
            opacity=alt.value(1.3)
        ).add_params(
            highlight
        ).properties(
            width=750, height=400
        )

        lines = base.mark_line().encode(
            size=alt.condition(~highlight, alt.value(1.2), alt.value(3))
        )

        warnings.filterwarnings(warning_status, category=FutureWarning)
        
        chart = points + lines

        return chart
   
    except Exception as e:
        print(f'Es ist ein Fehler aufgetreten: {str(e)}')
        print("Error: %s" % e, file=sys.stderr)
        print(file=sys.stderr)


def plot_sns_facetgrid(data, col, hue, col_wrap, height, x, y, **kwargs ):
    """
    Diese Funktion erstellt mit Seaborn eine faced grid lineplot.
    Doku dazu unter: 
    - https://seaborn.pydata.org/generated/seaborn.FacetGrid.html 
    - https://seaborn.pydata.org/examples/index.html

    Parameter (zwingend):
    - data (DataFrame): Die Daten, die für das Diagramm verwendet werden sollen.
    - col (str): Attribut für die Spalten des Grids.
    - hue(str): Kategorie für die Farbgebung.
    - col_wrap (num): Anzahl Grafiken pro Zeile.
    - x (str): Attribut der X-Achse
    - y (str):Attribut der Y-Achse

    Optionale Parameter:    
    - height (num): Höhe einer Grafik i.d.R 3-4
    - grafiktyp (str): Typen können sein: sns.lineplot, sns.scatterplot, sns.violinplot
    - xlabel (str): Beschriftung der X-Achse
    - ylabel (str): Beschriftung der Y-Achse
    - warning_status (str): Der Status der Warnmeldungen.'always' oder 'ignore' 
    - myTitle (str): Der Titel des Diagramms.


    Rückgabe:
    - chart (sns.FacetGrid): Das erstellte Seaborn Diagramm.

    """
    try:
        #Defaultwerte der kwargs, falls nichts mitgegeben wird      
        height = kwargs.get('height', 4)
        grafiktyp = kwargs.get('grafiktyp', 'sns.lineplot')
        xlabel = kwargs.get('xlabel', '')
        ylabel = kwargs.get('ylabel', '')
        warning_status = kwargs.get('warning_status', 'ignore')
        myTitle = kwargs.get('myTitle', '')


        fg = sns.FacetGrid(data, col=col, hue=hue, col_wrap=col_wrap, height=height) #palette könnte auch def werden: , palette="tab20c"
        fg.map(grafiktyp, x, y, alpha=.8)

        fg.set_axis_labels(xlabel,ylabel)
        fg.set_titles(col_template="{col_name}", row_template="{row_name}")
        fg.add_legend()

        fg.fig.subplots_adjust(top=0.95)
        fg.fig.suptitle(myTitle)

        warnings.filterwarnings(warning_status, category=FutureWarning)       

        return fg

    except Exception as e:
        print(f'Es ist ein Fehler aufgetreten: {str(e)}')
        print("Error: %s" % e, file=sys.stderr)
        print(file=sys.stderr)    


def plot_px_treemap(data, levels, values, color, **kwargs):
    """
    Diese Funktion erstellt mit Plotly Express eine interaktive Treemap.
    Doku dazu unter: 
    - https://plotly.com/python/treemaps/
    - https://plotly.com/python/builtin-colorscales/
#data, myHeaderTitle, levels, values, color, color_discrete_map, color_continuous_scale, height, width, hoover_label, warning_status
    Parameter (zwingend):
    - data (DataFrame): Die Daten, die für das Diagramm verwendet werden sollen.
    - levels (list): Auflistung der Attribute, die als Levels verwendet werden sollen. z.B. "var1, var2". Grösse von links nach rechts
    - values (num): Werte, welche die Kästchengrösse festlegen
    - color (str or num): Attribut, welcher die Farbe zugeordnet wird

    Optionale Parameter:
    - myHeaderTitle (str):
    - color_discrete_map: falls color vom Typ string ist (Kategorien)
    - color_continuous_scale: falls color vom Typ numerisch ist (Kennzahl)
    - height (num): Höhe der TreeMap
    - width (num): Breite der TreeMap
    - hoover_label (str): Text der beim hoovern angezeigt werden soll.
    - margin_val_top (str): Angaben zu leerem Space zu t, l, r, b (top, left, right, bottom)
    - margin_val_left (str): Angaben zu leerem Space zu t, l, r, b (top, left, right, bottom)
    - margin_val_right (str): Angaben zu leerem Space zu t, l, r, b (top, left, right, bottom)        
    - margin_val_bopttom (str): Angaben zu leerem Space zu t, l, r, b (top, left, right, bottom)    
    - warning_status (str): Der Status der Warnmeldungen.'always' oder 'ignore' 


    Rückgabe:
    - fig (px.treemap): Das erstellte interaktive Diagramm.

    """
    try:
        #Defaultwerte der kwargs, falls nichts mitgegeben wird      
        myHeaderTitle = kwargs.get('myHeaderTitle', '')
        color_discrete_map = kwargs.get('color_discrete_map', None)
        color_continuous_scale = kwargs.get('color_continuous_scale', None)
        height = kwargs.get('height', 700)
        width = kwargs.get('width', 1100)
        hoover_label = kwargs.get('hoover_label', 'Anzahl:')
        warning_status = kwargs.get('warning_status', 'ignore')
        margin_val_top = kwargs.get('margin_val_top', 25)
        margin_val_left = kwargs.get('margin_val_left', 25)
        margin_val_right = kwargs.get('margin_val_right', 25)
        margin_val_bottom = kwargs.get('margin_val_bottom', 25)

        #Bilde die Path-Variable
    
        path = [px.Constant(myHeaderTitle)] + levels
        print(f'path: {path}')
        print(f'Typ von path: {type(path)}')
        
        fig = px.treemap(data,
                     path=path,
                     values=values,  # Füge die entsprechenden Werte für values, color, etc. hinzu
                     color=color,
                     color_discrete_map=color_discrete_map,
                     color_continuous_scale=color_continuous_scale,
                     height=height,
                     width=width)

        fig.update_traces(root_color="grey")
        fig.update_layout(margin = dict(t=margin_val_top, l=margin_val_left, r=margin_val_right, b=margin_val_bottom))
        #Was soll beim hoovern angezeigt werden?
        fig.data[0].hovertemplate = f'%{{label}}<br><br>{hoover_label}<br>%{{value}}<extra></extra>'

        warnings.filterwarnings(warning_status, category=FutureWarning)  

        return fig.show()

    except Exception as e:
        print(f'Es ist ein Fehler aufgetreten: {str(e)}')
        print("Error: %s" % e, file=sys.stderr)
        print(file=sys.stderr)    


def plot_px_treemap_old(data, myHeaderTitle, levels, values, color, color_discrete_map, color_continuous_scale, height, width, hoover_label, warning_status):
    """
    Diese Funktion erstellt mit Plotly Express eine interaktive Treemap.
    Doku dazu unter: 
    - https://plotly.com/python/treemaps/
    - https://plotly.com/python/builtin-colorscales/

    Parameter:
    - data (DataFrame): Die Daten, die für das Diagramm verwendet werden sollen.
    - myHeaderTitle (str):
    - levels (list): Auflistung der Attribute, die als Levels verwendet werden sollen. z.B. "var1, var2". Grösse von links nach rechts
    - values (num): Werte, welche die Kästchengrösse festlegen
    - color (str or num): Attribut, welcher die Farbe zugeordnet wird
    - color_discrete_map: falls color vom Typ string ist (Kategorien)
    - color_continuous_scale: falls color vom Typ numerisch ist (Kennzahl)
    - height (num): Höhe der TreeMap
    - width (num): Breite der TreeMap
    - hoover_label (str): Text der beim hoovern angezeigt werden soll.
    - warning_status (str): Der Status der Warnmeldungen.'always' oder 'ignore' 


    Rückgabe:
    - fig (px.treemap): Das erstellte interaktive Diagramm.

    """
    try:

        path = [px.Constant(myHeaderTitle)] + levels 
        #print(path)
        
        fig = px.treemap(data,
                     path=path,
                     values=values,  # Füge die entsprechenden Werte für values, color, etc. hinzu
                     color=color,
                     color_discrete_map=color_discrete_map,
                     color_continuous_scale=color_continuous_scale,
                     height=height,
                     width=width)

        fig.update_traces(root_color="grey")
        fig.update_layout(margin = dict(t=25, l=25, r=25, b=25))
        #Was soll beim hoovern angezeigt werden?
        fig.data[0].hovertemplate = f'%{{label}}<br><br>{hoover_label}<br>%{{value}}<extra></extra>'

        warnings.filterwarnings(warning_status, category=FutureWarning)  

        return fig.show()

    except Exception as e:
        print(f'Es ist ein Fehler aufgetreten: {str(e)}')
        print("Error: %s" % e, file=sys.stderr)
        print(file=sys.stderr)    
        

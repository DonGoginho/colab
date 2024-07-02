import altair as alt
import plotly.express as px
import seaborn as sns
import sys
import warnings

def plot_altair_multiline_highlight(data, x, y, category, myTitle, x_beschriftung, y_beschriftung, category_beschriftung, warning_status):
    """
    Diese Funktion erstellt ein interaktives Liniendiagramm in Altair. Doku dazu unter: https://altair-viz.github.io/gallery/ resp. https://altair-viz.github.io/gallery/multiline_highlight.html

    Parameter:
    - data (DataFrame): Die Daten, die für das Diagramm verwendet werden sollen.
    - x (str): Die Spalte für die X-Achse.
    - x_beschriftung (str): Titel der X-Achse.
    - y (str): Die Spalte für die Y-Achse.
    - y_beschriftung (str): Titel der Y-Achse.
    - category (str): Die Spalte, die die Kategorien für die Farbcodierung darstellt.
    - category_beschriftung (str): Legendentitel.
    - title (str): Der Titel des Diagramms.
    - warning_status (str): Der Status der Warnmeldungen.'always' oder 'ignore' 

    Rückgabe:
    - chart (alt.Chart): Das erstellte interaktive Diagramm.

    """
    try:
        # Überprüfen, ob category_beschriftung definiert ist, bevor sie verwendet wird

        highlight = alt.selection_point(on='pointerover', fields=[category], nearest=True)

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

        return points + lines    
   
    except Exception as e:
        print(f'Es ist ein Fehler aufgetreten: {str(e)}')
        print("Error: %s" % e, file=sys.stderr)
        print(file=sys.stderr)



def plot_sns_facetgrid(data, col, hue, col_wrap, height, grafiktyp, x, xlabel, y, ylabel, warning_status):
    """
    Diese Funktion erstellt mit Seaborn eine faced grid lineplot.
    Doku dazu unter: 
    - https://seaborn.pydata.org/generated/seaborn.FacetGrid.html 
    - https://seaborn.pydata.org/examples/index.html

    Parameter:
    - data (DataFrame): Die Daten, die für das Diagramm verwendet werden sollen.
    - col (str): Attribut für die Spalten des Grids.
    - hue(str): Kategorie für die Farbgebung.
    - col_wrap (num): Anzahl Grafiken pro Zeile.
    - height (num): Höhe einer Grafik
    - grafiktyp (str): Typen können sein: sns.lineplot, sns.scatterplot, sns.violinplot
    - x (str): Attribut der X-Achse
    - xlabel (str): Beschriftung der X-Achse
    - y (str):Attribut der Y-Achse
    - ylabel (str): Beschriftung der Y-Achse
    - warning_status (str): Der Status der Warnmeldungen.'always' oder 'ignore' 


    Rückgabe:
    - chart (sns.FacetGrid): Das erstellte interaktive Diagramm.

    """
    try:
        fg = sns.FacetGrid(data, col=col, hue=hue, col_wrap=col_wrap, height=height) #palette könnte auch def werden: , palette="tab20c"
        fg.map(grafiktyp, x, y, alpha=.8)

        fg.set_axis_labels(xlabel,ylabel)
        fg.set_titles(col_template="{col_name}", row_template="{row_name}")
        fg.add_legend()

        warnings.filterwarnings(warning_status, category=FutureWarning)       

        return fg

    except Exception as e:
        print(f'Es ist ein Fehler aufgetreten: {str(e)}')
        print("Error: %s" % e, file=sys.stderr)
        print(file=sys.stderr)    


def plot_px_treemap(data, myHeaderTitle, levels, values, color, color_discrete_map, color_continuous_scale, height, width, hoover_label, warning_status):
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

        

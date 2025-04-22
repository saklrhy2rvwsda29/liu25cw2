
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats


df = pd.read_csv('Results_21MAR2022.csv')

print(df.columns.tolist())
print(df.info())


def create_scatter_matrix(df):
    """Create a scatter plot matrix for environmental indicators"""
    # Select environmental indicators to display
    env_indicators = ['mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut', 'mean_acid']
    
    # Create a new DataFrame containing only the required columns
    plot_df = df[env_indicators + ['diet_group']].copy()
    
    # Rename columns for better display
    column_names = {
        'mean_ghgs': 'GHG Emissions',
        'mean_land': 'Land Use',
        'mean_watscar': 'Water Scarcity',
        'mean_eut': 'Eutrophication',
        'mean_acid': 'Acidification'
    }
    plot_df = plot_df.rename(columns=column_names)
    
    # Define new color mapping - based on red theme
    colors = {
        'fish': '#AA3939',    # Main red
        'meat': '#D46A6A',    # Medium red
        'meat100': '#801515', # Dark red
        'meat50': '#FFAAAA',  # Light red
        'vegan': '#550000',   # Dark maroon
        'veggie': '#CC7777'   # Pink red
    }
    
    # Create scatter plot matrix
    fig = px.scatter_matrix(
        plot_df,
        dimensions=list(column_names.values()),
        color='diet_group',
        color_discrete_map=colors,
        title='Environmental Indicators Correlation Matrix by Diet Group',
        labels=column_names
    )
    
    # Update layout
    fig.update_layout(
        width=1000,
        height=1000,
        title={
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
        },
        # Add red theme background tint
        paper_bgcolor='rgba(255,240,240,0.5)',  # Slight red background
        plot_bgcolor='rgba(255,255,255,1)'      # White plot area
    )
    
    # Update traces
    fig.update_traces(
        diagonal_visible=False,  # Hide histograms on diagonal
        showupperhalf=False,    # Only show lower half
        marker=dict(size=4)     # Reduce point size
    )
    
    # Add trend lines
    for i in range(len(env_indicators)):
        for j in range(i+1, len(env_indicators)):
            # Calculate correlation coefficient
            corr = plot_df[list(column_names.values())[i]].corr(
                plot_df[list(column_names.values())[j]]
            )
            
            # Add correlation coefficient annotation to each scatter plot
            fig.add_annotation(
                x=list(column_names.values())[j],
                y=list(column_names.values())[i],
                text=f"r = {corr:.2f}",
                showarrow=False,
                font=dict(
                    size=10,
                    color='#801515'  # Use dark red for correlation coefficients
                )
            )
    
    return fig

# Call function and display chart
scatter_matrix_fig = create_scatter_matrix(df)
scatter_matrix_fig.show()


def plot_diet_environmental_impacts(df):
    """Comparison of multiple environmental impact indicators across diet groups"""
    # Create 3x2 subplots to accommodate all environmental indicators
    fig = make_subplots(
        rows=3, 
        cols=2,
        subplot_titles=(
            'GHG Emissions by Diet Group',
            'Land Use by Diet Group',
            'Water Scarcity by Diet Group', 
            'Eutrophication by Diet Group',
            'Acidification by Diet Group',
            'Water Use by Diet Group'
        )
    )
    
    # Define different shades of red for each indicator
    indicator_colors = {
        'mean_ghgs': '#8B0000',     # Dark red
        'mean_land': '#CD5C5C',     # Indian red
        'mean_watscar': '#DC143C',  # Crimson
        'mean_eut': '#B22222',      # Fire brick
        'mean_acid': '#FF0000',     # Pure red
        'mean_watuse': '#A52A2A'    # Brown red
    }
    
    # Create box plots for each indicator
    metrics = [
        ('mean_ghgs', 'GHG Emissions', 1, 1),
        ('mean_land', 'Land Use', 1, 2),
        ('mean_watscar', 'Water Scarcity', 2, 1),
        ('mean_eut', 'Eutrophication', 2, 2),
        ('mean_acid', 'Acidification', 3, 1),
        ('mean_watuse', 'Water Use', 3, 2)
    ]
    
    for metric, name, row, col in metrics:
        fig.add_trace(
            go.Box(
                x=df['diet_group'],
                y=df[metric],
                name=name,
                boxpoints='outliers',
                marker_color=indicator_colors[metric],  # Use corresponding color
                line_color=indicator_colors[metric],    # Use same color for border
            ),
            row=row, col=col
        )
    
    # Update layout
    fig.update_layout(
        height=1200,
        width=1200,
        title_text="Environmental Impacts by Diet Group",
        showlegend=True,
        boxmode='group',
        paper_bgcolor='#FFF5F5',  # Light pink background
        plot_bgcolor='#FFFAFA',   # Lighter pink background
        font=dict(
            family="Arial",
            size=12,
            color="#660000"
        ),
        title=dict(
            font=dict(
                size=24,
                color="#660000"
            )
        )
    )
    
    # Update all axis styles
    for i in range(1, 4):
        for j in range(1, 3):
            # Update x-axis
            fig.update_xaxes(
                title_text="Diet Group",
                row=i,
                col=j,
                gridcolor='#FFE6E6',
                tickfont=dict(color="#660000")
            )
            
            # Update y-axis
            fig.update_yaxes(
                title_text=metrics[(i-1)*2 + (j-1)][1],
                row=i,
                col=j,
                gridcolor='#FFE6E6',
                tickfont=dict(color="#660000")
            )
    
    return fig

# Display the plot
fig = plot_diet_environmental_impacts(df)
fig.show()


def plot_diet_group_comparison(df):
    """Comparison of environmental impacts across different diet groups"""
    fig = make_subplots(rows=2, cols=2,
                       subplot_titles=('GHG Emissions', 'Land Use', 
                                     'Water Scarcity', 'Eutrophication'))
    
    # GHG Emissions
    fig.add_trace(
        go.Box(x=df['diet_group'], y=df['mean_ghgs'], name='GHG'),
        row=1, col=1
    )
    
    # Land Use
    fig.add_trace(
        go.Box(x=df['diet_group'], y=df['mean_land'], name='Land'),
        row=1, col=2
    )
    
    # Water Scarcity
    fig.add_trace(
        go.Box(x=df['diet_group'], y=df['mean_watscar'], name='Water'),
        row=2, col=1
    )
    
    # Eutrophication
    fig.add_trace(
        go.Box(x=df['diet_group'], y=df['mean_eut'], name='Eut'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        width=1000,
        title_text="Environmental Impact by Diet Group",
        showlegend=False
    )
    return fig
fig4 = plot_diet_group_comparison(df)
fig4.show()


def create_parallel_coordinates(df):
    """Create parallel coordinates plot to show relationships between environmental impact indicators"""
    # Select environmental indicators
    env_indicators = ['mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut', 
                     'mean_bio', 'mean_watuse', 'mean_acid']
    
    # Create parallel coordinates plot
    fig = go.Figure(data=
        go.Parcoords(
            line = dict(color = df['mean_ghgs'],
                       colorscale = 'Viridis'),
            dimensions = list([
                dict(range = [df[col].min(), df[col].max()],
                     label = col,
                     values = df[col]) for col in env_indicators
            ])
        )
    )
    
    fig.update_layout(
        title='Environmental Impact Indicators Relationships',
        width=1000,
        height=600
    )
    
    return fig
create_parallel_coordinates(df)


def create_diet_radar_chart(df):
    """Create radar chart to compare environmental impacts across different diet groups"""
    # Ensure data is properly grouped and calculate means
    diet_means = df.groupby('diet_group').agg({
        'mean_ghgs': 'mean',
        'mean_land': 'mean',
        'mean_watscar': 'mean',
        'mean_eut': 'mean',
        'mean_acid': 'mean'
    }).reset_index()
    
    # Normalize each environmental indicator
    columns_to_normalize = ['mean_ghgs', 'mean_land', 'mean_watscar', 'mean_eut', 'mean_acid']
    for col in columns_to_normalize:
        max_val = diet_means[col].max()
        min_val = diet_means[col].min()
        diet_means[col] = (diet_means[col] - min_val) / (max_val - min_val)
    
    # Create radar chart
    fig = go.Figure()
    
    # Define dimensions
    dimensions = ['GHGs', 'Land Use', 'Water Scarcity', 'Eutrophication', 'Acidification']
    
    # Define color mapping
    colors = {
        'fish': '#6E4FD1',
        'meat': '#FF6B6B',
        'meat100': '#4CAF50',
        'meat50': '#FF9800',
        'vegan': '#E91E63',
        'veggie': '#00BCD4'
    }
    
    # Add a trace for each diet group
    for _, row in diet_means.iterrows():
        values = [
            float(row['mean_ghgs']),
            float(row['mean_land']),
            float(row['mean_watscar']),
            float(row['mean_eut']),
            float(row['mean_acid'])
        ]
        # Ensure the plot closes by connecting end to start
        values.append(values[0])
        dimensions_closed = dimensions + [dimensions[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=dimensions_closed,
            name=row['diet_group'],
            line=dict(color=colors.get(row['diet_group'], '#000000'), width=2),
            fill='toself',
            opacity=0.6
        ))
    
    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showline=True,
                showticklabels=True,
                tickformat='.2f',  # Show 2 decimal places
                range=[0, 1.1]  # Range set to 0-1.1 since data is normalized
            ),
            angularaxis=dict(
                direction="clockwise",
                period=6
            )
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        title={
            'text': 'Environmental Impact Comparison by Diet Group',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        width=800,
        height=600
    )
    
    return fig

# Call function and display chart
fig = create_diet_radar_chart(df)
fig.show()



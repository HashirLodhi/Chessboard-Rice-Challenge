import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def calculate_grains(square):
    """Calculate grains on a specific square"""
    return 2 ** (square - 1)

def calculate_total(up_to_square):
    """Calculate total grains up to a specific square"""
    return 2 ** up_to_square - 1

def format_number(num):
    """Format large numbers with suffixes"""
    if num < 1e6:
        return f"{num:,.0f}"
    elif num < 1e9:
        return f"{num/1e6:.2f}M"
    elif num < 1e12:
        return f"{num/1e9:.2f}B"
    elif num < 1e15:
        return f"{num/1e12:.2f}T"
    else:
        return f"{num/1e15:.2f}Q"

def create_chessboard_heatmap(current_square):
    """Create an interactive chessboard heatmap"""
    # Create 8x8 grid
    board = np.zeros((8, 8))
    annotations = []
    
    for i in range(8):
        for j in range(8):
            square_num = i * 8 + j + 1
            if square_num <= current_square:
                # Use log scale for better visualization
                board[i, j] = np.log10(calculate_grains(square_num) + 1)
            
            # Add square numbers as annotations
            annotations.append(
                dict(
                    x=j, y=i,
                    text=str(square_num),
                    showarrow=False,
                    font=dict(size=10, color='white' if board[i, j] > 5 else 'black')
                )
            )
    
    fig = go.Figure(data=go.Heatmap(
        z=board,
        colorscale='YlOrRd',
        showscale=True,
        colorbar=dict(title="Log₁₀(Grains)"),
        hovertemplate='Square %{text}<br>Grains: %{customdata:,.0f}<extra></extra>',
        customdata=np.array([[calculate_grains(i*8+j+1) if i*8+j+1 <= current_square else 0 
                             for j in range(8)] for i in range(8)])
    ))
    
    fig.update_layout(
        title=f"Chessboard - Up to Square {current_square}",
        xaxis=dict(showticklabels=False, showgrid=False, range=[-0.5, 7.5]),
        yaxis=dict(showticklabels=False, showgrid=False, range=[-0.5, 7.5]),
        annotations=annotations,
        width=600,
        height=600,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_exponential_growth_chart(current_square):
    """Create exponential growth visualization"""
    squares = list(range(1, min(current_square + 1, 65)))
    grains = [calculate_grains(s) for s in squares]
    
    # Create two subplots: linear and log scale
    fig = go.Figure()
    
    # Add the main trace with animation effect
    fig.add_trace(go.Scatter(
        x=squares,
        y=grains,
        mode='lines+markers',
        name='Grains per Square',
        line=dict(color='#f59e0b', width=3),
        marker=dict(size=8, color='#f59e0b'),
        hovertemplate='<b>Square %{x}</b><br>Grains: %{y:,.0f}<extra></extra>'
    ))
    
    # Highlight the current square
    if current_square > 1:
        fig.add_trace(go.Scatter(
            x=[current_square],
            y=[grains[-1]],
            mode='markers',
            marker=dict(size=15, color='#ef4444', symbol='star'),
            showlegend=False,
            hovertemplate='<b>Current Square</b><br>Grains: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Exponential Growth: Grains per Square",
        xaxis_title="Square Number",
        yaxis_title="Number of Grains",
        yaxis_type="log",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        font=dict(size=14),
        title_font_size=20,
        margin=dict(t=60, b=60, l=60, r=30)
    )
    
    return fig

def create_cumulative_chart(current_square):
    """Create cumulative grains chart"""
    squares = list(range(1, min(current_square + 1, 65)))
    cumulative = [calculate_total(s) for s in squares]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=squares,
        y=cumulative,
        mode='lines',
        fill='tozeroy',
        name='Cumulative Grains',
        line=dict(color='#8b5cf6', width=3),
        hovertemplate='<b>Up to Square %{x}</b><br>Total: %{y:,.0f}<extra></extra>'
    ))
    
    # Highlight the current point
    if current_square > 1:
        fig.add_trace(go.Scatter(
            x=[current_square],
            y=[cumulative[-1]],
            mode='markers',
            marker=dict(size=15, color='#ef4444', symbol='star'),
            showlegend=False,
            hovertemplate='<b>Current Total</b><br>Grains: %{y:,.0f}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Cumulative Total Grains",
        xaxis_title="Square Number",
        yaxis_title="Total Grains (Log Scale)",
        yaxis_type="log",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        font=dict(size=14),
        title_font_size=20,
        margin=dict(t=60, b=60, l=60, r=30)
    )
    
    return fig

def create_comparison_chart():
    """Create comparison with real-world quantities"""
    comparisons = {
        'World Population\n(8 billion)': 8e9,
        'Seconds in\n1 million years': 3.15e13,
        'Grains of sand\non Earth': 7.5e18,
        'Total Rice Grains\n(64 squares)': 1.844674407e19,
        'Stars in\nobservable universe': 1e24
    }
    
    df = pd.DataFrame({
        'Item': list(comparisons.keys()),
        'Value': list(comparisons.values())
    })
    
    # Create gradient colors
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    
    fig = go.Figure(go.Bar(
        x=df['Item'],
        y=df['Value'],
        marker_color=colors,
        text=[format_number(v) for v in df['Value']],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>%{y:,.0e}<extra></extra>',
        textfont=dict(size=14, color='white')
    ))
    
    fig.update_layout(
        title="Real-World Comparisons",
        yaxis_title="Quantity (Log Scale)",
        yaxis_type="log",
        height=500,
        template='plotly_white',
        font=dict(size=14),
        title_font_size=20,
        margin=dict(t=60, b=60, l=60, r=30)
    )
    
    return fig

def update_visualization(square_num):
    """Update all visualizations based on selected square"""
    current_grains = calculate_grains(square_num)
    total_grains = calculate_total(square_num)
    
    # Create statistics text with enhanced formatting
    stats = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
        <h2 style="margin-top: 0; text-align: center; font-weight: 700;">📊 Current Statistics</h2>
        
        <div style="display: flex; justify-content: space-around; margin: 20px 0;">
            <div style="text-align: center;">
                <div style="font-size: 1.2em; opacity: 0.9;">Square Number</div>
                <div style="font-size: 2.5em; font-weight: bold;">{square_num}<span style="font-size: 1.2em;">/64</span></div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2em; opacity: 0.9;">Grains on This Square</div>
                <div style="font-size: 2.5em; font-weight: bold; color: #fbbf24;">{format_number(current_grains)}</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2em; opacity: 0.9;">Total Grains So Far</div>
                <div style="font-size: 2.5em; font-weight: bold; color: #c084fc;">{format_number(total_grains)}</div>
            </div>
        </div>
        
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.3); margin: 20px 0;">
        
        <h3 style="text-align: center; margin-bottom: 15px;">🌾 Real-World Context</h3>
    """
    
    # Add context based on current square
    if square_num <= 10:
        stats += f"<p style='text-align: center; font-size: 1.1em;'>At square {square_num}, we have {format_number(current_grains)} grains - still manageable amounts!</p>"
    elif square_num <= 20:
        stats += f"<p style='text-align: center; font-size: 1.1em;'>At square {square_num}, we have {format_number(current_grains)} grains per square - this is getting significant!</p>"
    elif square_num <= 30:
        weight_kg = total_grains * 0.00002  # ~20mg per grain
        stats += f"<p style='text-align: center; font-size: 1.1em;'>Total weight so far: ~{format_number(weight_kg)} kg ({format_number(weight_kg / 1000)} metric tons!)</p>"
    else:
        stats += f"<p style='text-align: center; font-size: 1.1em;'>The numbers are now astronomically large! Current square alone: {format_number(current_grains)} grains</p>"
    
    if square_num == 64:
        stats += """
        <div style="background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; margin-top: 15px;">
            <h3 style="text-align: center; margin-top: 0; color: #fbbf24;">🏆 Complete Board!</h3>
            <p style="text-align: center; font-size: 1.2em;">
                <strong>Total: 18,446,744,073,709,551,615 grains</strong><br>
                Weight: ~461 billion metric tons<br>
                More than 1,000 years of global rice production!
            </p>
        </div>
        """
    
    stats += "</div>"
    
    # Create all charts
    chessboard = create_chessboard_heatmap(square_num)
    growth_chart = create_exponential_growth_chart(square_num)
    cumulative_chart = create_cumulative_chart(square_num)
    comparison_chart = create_comparison_chart()
    
    return stats, chessboard, growth_chart, cumulative_chart, comparison_chart

# Create the Gradio interface with enhanced UI
with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange", secondary_hue="purple"), 
               title="Chess & Rice Problem", 
               css="""
               .gradio-container { 
                   background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
                   color: white;
                   font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
               }
               .gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {
                   color: white;
                   text-align: center;
               }
               .gr-markdown p {
                   line-height: 1.6;
               }
               .gr-button {
                   border-radius: 8px;
                   font-weight: 600;
               }
               .gr-slider input[type="range"] {
                   height: 8px;
                   border-radius: 4px;
                   background: linear-gradient(to right, #f59e0b, #8b5cf6);
               }
               .gr-plot {
                   border-radius: 12px;
                   overflow: hidden;
                   box-shadow: 0 10px 30px rgba(0,0,0,0.3);
               }
               .gr-row {
                   margin-bottom: 20px;
               }
               .gr-column {
                   display: flex;
                   justify-content: center;
               }
               .footer {
                   text-align: center;
                   padding: 20px;
                   color: rgba(255,255,255,0.7);
                   font-size: 0.9em;
               }
               """) as app:
    
    gr.Markdown("""
    # 🎲 The Chess and Rice Grains Problem
    ## Exploring the Power of Exponential Growth
    
    ### 📖 The Legend
    According to legend, when the inventor of chess presented the game to an ancient king, the king was so pleased 
    that he offered the inventor any reward. The wise inventor made a seemingly humble request:
    
    - Place **1 grain of rice** on the first square of a chessboard
    - Place **2 grains** on the second square
    - Place **4 grains** on the third square
    - **Double the amount** on each subsequent square for all 64 squares
    
    The king agreed immediately, thinking it was a modest request. But was it?
    
    ### 🧮 The Mathematics
    This problem demonstrates **exponential growth** with base 2:
    - Grains on square n: **2<sup>(n-1)</sup>**
    - Total grains up to square n: **2<sup>n</sup> - 1**
    - Complete board (64 squares): **2<sup>64</sup> - 1 = 18,446,744,073,709,551,615**
    
    Use the slider below to explore how quickly the numbers grow!
    """)
    
    with gr.Row():
        square_slider = gr.Slider(
            minimum=1, 
            maximum=64, 
            value=1, 
            step=1, 
            label="Select Square Number",
            info="Move the slider to see how grains accumulate",
            interactive=True
        )
    
    with gr.Row():
        stats_output = gr.HTML()
    
    with gr.Row():
        chessboard_plot = gr.Plot(label="Interactive Chessboard", show_label=False)
    
    with gr.Row(equal_height=True):
        with gr.Column():
            growth_plot = gr.Plot(label="Exponential Growth", show_label=False)
        with gr.Column():
            cumulative_plot = gr.Plot(label="Cumulative Total", show_label=False)
    
    with gr.Row():
        comparison_plot = gr.Plot(label="Real-World Comparisons", show_label=False)
    
    gr.Markdown("""
    ---
    ### 🔬 Key Insights
    
    1. **Exponential Growth is Deceptive**: The first half of the board (32 squares) contains less than 0.00001% of the total grains!
    
    2. **The Power of Doubling**: Each square has more grains than all previous squares combined, plus one.
       - Mathematical proof: 2<sup>n</sup> = (2<sup>n</sup> - 1) + 1
    
    3. **Real-World Scale**: 
       - The total grains would weigh approximately **461 billion metric tons**
       - This exceeds **1,000 years** of current global rice production
       - If each grain is 6mm long, they would stretch over **116 trillion kilometers** (about 777 AU)
    
    4. **Computer Science**: This problem illustrates why 64-bit computing exists - 2<sup>64</sup> combinations!
    
    ### 🎯 Formula Summary
    
    | Concept | Formula | Example (Square 10) |
    |---------|---------|---------------------|
    | Grains on square n | 2<sup>(n-1)</sup> | 2<sup>9</sup> = 512 |
    | Total up to square n | 2<sup>n</sup> - 1 | 2<sup>10</sup> - 1 = 1,023 |
    | Doubling pattern | Each square = All previous + 1 | 512 = 511 + 1 |
    
    ### 💡 Applications
    - **Computing**: Understanding memory and storage (bytes, bits)
    - **Finance**: Compound interest and investment growth
    - **Biology**: Bacterial reproduction and population growth
    - **Virology**: Disease spread modeling
    - **Physics**: Radioactive decay (inverse exponential)
    """)
    
    # Set up interactivity with animation effect
    square_slider.change(
        fn=update_visualization,
        inputs=[square_slider],
        outputs=[stats_output, chessboard_plot, growth_plot, cumulative_plot, comparison_plot],
        show_progress="minimal"
    )
    
    # Initialize with square 1
    app.load(
        fn=update_visualization,
        inputs=[square_slider],
        outputs=[stats_output, chessboard_plot, growth_plot, cumulative_plot, comparison_plot]
    )

# Launch the app
if __name__ == "__main__":
    app.launch()
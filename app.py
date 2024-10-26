import gradio as gr
import pyfracgen as pf
from matplotlib import pyplot as plt
from matplotlib import colormaps
from PIL import Image
import io

def generate_fractal(x_min, x_max, y_min, y_max, width, height, dpi, maxiter):
    # Define x and y bounds based on user inputs
    x_min_b = 0.3602404434376143632361252444495 - (x_min * 10**-14)
    x_max_b = 0.3602404434376143632361252444495 + (x_max * 10**-14)
    y_min_b = -0.6413130610648031748603750151793 - (y_min * 10**-14)
    y_max_b = -0.6413130610648031748603750151793 + (y_max * 10**-14)

    xbound = (x_min_b, x_max_b)
    ybound = (y_min_b, y_max_b)
    
    # Generate the Mandelbrot fractal
    res = pf.mandelbrot(
        xbound, ybound, pf.funcs.power, width=width, height=height, dpi=dpi, maxiter=maxiter
    )
    stacked = pf.images.get_stacked_cmap(colormaps["gist_gray"], 50)
    
    # Plot the fractal image
    plt.figure(figsize=(width, height), dpi=dpi)
    pf.images.image(res, cmap=stacked, gamma=0.8)
    
    # Convert the plot to a Pillow image
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()  # Close the plot to free up memory
    return Image.open(buf)

# Gradio interface
with gr.Blocks() as frac_base:
    gr.Markdown("### Fractal Generator")

    output_image = gr.Image(type="pil", label="Fractal Image")
    
    with gr.Row():
        x_min = gr.Number(value=3, label="X Min")
        x_max = gr.Number(value=25, label="X Max")
        y_min = gr.Number(value=6, label="Y Min")
        y_max = gr.Number(value=13, label="Y Max")
    
    with gr.Row():
        width = gr.Number(value=4, label="Width")
        height = gr.Number(value=3, label="Height")
        dpi = gr.Number(value=300, label="DPI")
        maxiter = gr.Number(value=5000, label="Max Iterations")
    
    generate_button = gr.Button("Generate Fractal")
    
    
    # Connect inputs to the generation function
    generate_button.click(
        fn=generate_fractal,
        inputs=[x_min, x_max, y_min, y_max, width, height, dpi, maxiter],
        outputs=output_image
    )

def generate_lyapunov(base_string, x_lyapunov_min, x_lyapunov_max, y_lyapunov_min, y_lyapunov_max, width, height, dpi, ninit, niter):
    xbound = (x_lyapunov_min, x_lyapunov_max)
    ybound = (y_lyapunov_min, y_lyapunov_max)
    res = pf.lyapunov(
        base_string, xbound, ybound, width=width, height=height, dpi=dpi, ninit=ninit, niter=niter
    )
    pf.images.markus_lyapunov_image(
        res, colormaps["bone"], colormaps["bone_r"], gammas=(8, 1)
    )

    # Convert the plot to a Pillow image
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()  # Close the plot to free up memory
    return Image.open(buf)

with gr.Blocks() as lyapunov:
    gr.Markdown("### Fractal Generator")

    output_lyapunov = gr.Image(type="pil", label="Fractal Image")
    
    with gr.Row():
        base_string = gr.Textbox(value = "AAAAAABBBBBB", label="Base String")
        x_lyapunov_min = gr.Number(value=2.5, label="X Min")
        x_lyapunov_max = gr.Number(value=3.4, label="X Max")
        y_lyapunov_min = gr.Number(value=3.4, label="Y Min")
        y_lyapunov_max = gr.Number(value=4.0, label="Y Max")
    
    with gr.Row():
        width = gr.Number(value=4, label="Width")
        height = gr.Number(value=3, label="Height")
        dpi = gr.Number(value=300, label="DPI")
        ninit = gr.Number(value=2000, label="Number of Initial Points")
        niter = gr.Number(value=2000, label="Number of Iterations")
    
    generate_button = gr.Button("Generate Fractal")
    
    
    # Connect inputs to the generation function
    generate_button.click(
        fn=generate_lyapunov,
        inputs=[base_string, x_lyapunov_min, x_lyapunov_max, y_lyapunov_min, y_lyapunov_max, width, height, dpi, ninit, niter],
        outputs=output_lyapunov
    )

def nebula(x_min, x_max, y_min, y_max, ncvals, width, height, dpi, horizon):
    xbound = (x_min, x_max)
    ybound = (y_min, y_max)
    res = pf.buddhabrot(
        xbound,
        ybound,
        ncvals=ncvals,
        update_func=pf.funcs.power,
        horizon=horizon,
        maxiters=(100, 1000, 10000),
        width=width,
        height=height,
        dpi=dpi,
    )
    pf.images.nebula_image(tuple(res), gamma=0.4)

    # Convert the plot to a Pillow image
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()  # Close the plot to free up memory
    return Image.open(buf)

with gr.Blocks() as nebula_base:
    gr.Markdown("### Fractal Generator")

    output_nebula = gr.Image(type="pil", label="Fractal Image")

    with gr.Row():
        x_nebula_min = gr.Number(value=-1.75, label="X Min")
        x_nebula_max = gr.Number(value=0.85, label="X Max")
        y_nebula_min = gr.Number(value=-1.10, label="Y Min")
        y_nebula_max = gr.Number(value=1.10, label="Y Max")
        ncvals = gr.Number(value=10000000, label="Number of Iterations")

    with gr.Row():
        width = gr.Number(value=4, label="Width")
        height = gr.Number(value=3, label="Height")
        dpi = gr.Number(value=300, label="DPI")
        horizon = gr.Number(value=1.0e6, label="Horizon")

    generate_button = gr.Button("Generate Fractal")

    # Connect inputs to the generation function
    generate_button.click(
        fn=nebula,
        inputs=[x_nebula_min, x_nebula_max, y_nebula_min, y_nebula_max, ncvals, width, height, dpi, horizon],
        outputs=output_nebula
    )


demo = gr.TabbedInterface([frac_base, lyapunov, nebula_base], ["Mandelbrot Set", "Markus-Lyapunov Fractal", "Buddhabrot with Nebula Coloring"])


demo.launch()

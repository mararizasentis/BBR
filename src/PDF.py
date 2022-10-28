from reportlab.pdfgen import canvas
import rasterio as rio
import matplotlib.pyplot as plt
from matplotlib import pyplot


def TIF_to_PNG(CHM_input, CHM_output, NDVI_input, NDVI_output, ortho_input, ortho_output, heatmap_input, heatmap_output):
    # Convert the CHM, NDVI, heatmap and orthomosaic to PNG format
    CHM = rio.open(CHM_input)
    pyplot.imshow(CHM.read(1), cmap="nipy_spectral")
    plt.title("CHM", loc="center")
    plt.axis("off")
    pyplot.savefig(CHM_output)

    NDVI = rio.open(NDVI_input)
    pyplot.imshow(NDVI.read(1), cmap="nipy_spectral")
    plt.title("NDVI", loc="center")
    plt.axis("off")
    pyplot.savefig(NDVI_output)

    heatmap = rio.open(heatmap_input)
    pyplot.imshow(heatmap.read(1))
    plt.title("Botrytis risk heatmap", loc="center")
    plt.axis("off")
    pyplot.savefig(heatmap_output)

    ortho = rio.open(ortho_input)
    pyplot.imshow(ortho.read(1))
    plt.title("Orthomosaic", loc="center")
    plt.axis("off")
    pyplot.savefig(ortho_output)


def generate_PDF(report, orthomosaic, NDVI, CHM, heatmap):
    # Generate the PDF file with the desired inputs
    c = canvas.Canvas(report)
    c.drawString(180, 750, "BOTRYTIS RISK ASSESMENT REPORT")
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)

    c.drawString(30, 700, 'The field that has been analysed is shown in the following picture.')
    c.drawImage(orthomosaic, 100, 480, width=200, height=200, mask="auto")

    c.drawString(30, 450,
                 'Here are displayed some of the variables that were computed to analyse the Botrytis risk of the field.')
    c.drawImage(NDVI, 100, 330, width=100, height=100, mask="auto")
    c.drawImage(CHM, 300, 330, width=100, height=100, mask="auto")

    c.drawString(30, 300, 'Finally, the following image shows the normalized heatmap of the Botrytis risk.')
    c.drawImage(heatmap, 100, 80, width=200, height=200, mask="auto")

    c.drawString(30, 50, 'This report was automatically made thanks to the code of Wageningen University.')
    c.save()

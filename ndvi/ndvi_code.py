from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *

class NDVIPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        # Load the GUI from the .ui file
        self.dlg = YourDialogClass()

        # Populate the image combo box with loaded raster layers
        self.populate_image_combo_box()

        self.dlg.buttonBox.accepted.connect(self.process_ndvi)
        self.dlg.buttonBox.rejected.connect(self.close_dialog)
        self.dlg.show()

    def unload(self):
        pass

    def populate_image_combo_box(self):
        # Get a list of loaded raster layers and populate the combo box
        layers = QgsProject.instance().mapLayers().values()
        image_combo = self.dlg.imageComboBox
        image_combo.addItems([layer.name() for layer in layers if isinstance(layer, QgsRasterLayer)])

    def process_ndvi(self):
        # Get the selected bands and image layer
        band1 = self.dlg.band1ComboBox.currentText()
        band2 = self.dlg.band2ComboBox.currentText()
        image_layer_name = self.dlg.imageComboBox.currentText()

        image_layer = QgsProject.instance().mapLayer(image_layer_name)

        if band1 and band2 and image_layer:
            band1_idx = image_layer.dataProvider().fields().indexFromName(band1)
            band2_idx = image_layer.dataProvider().fields().indexFromName(band2)

            if band1_idx != -1 and band2_idx != -1:
                result_layer = self.calculate_ndvi(image_layer, band1_idx, band2_idx)
                QgsProject.instance().addMapLayer(result_layer)
            else:
                QMessageBox.critical(self.dlg, "Error", "Invalid band selections.")
        else:
            QMessageBox.critical(self.dlg, "Error", "Invalid input selections.")

    def calculate_ndvi(self, layer, band1_idx, band2_idx):
        # Replace this with your NDVI calculation code
        expression = f'({band1_idx} - {band2_idx}) / ({band1_idx} + {band2_idx})'
        output_uri = 'path_to_save_ndvi_output.tif'

        calc = QgsRasterCalculator(expression, output_uri, 'GTiff', layer.extent(), layer.width(), layer.height())
        calc.processCalculation()

        return QgsRasterLayer(output_uri, "NDVI")

    def close_dialog(self):
        self.dlg.reject()


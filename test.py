from qgis import processing
from qgis.processing import alg
from qgis.core import *
from qgis.PyQt.QtCore import QVariant

QgsApplication.setPrefixPath("/Applications/QGIS-LTR.app/", True)

# Create a reference to the QgsApplication.  Setting the
# second argument to False disables the GUI.
qgs = QgsApplication([], False)

# Load providers
qgs.initQgis()

@alg(name='test', label="test", group='examplescripts', group_label='Example scripts')
@alg.input(type=alg.SOURCE, name='INPUT',
           label='input')
@alg.output(type=alg.VECTOR_LAYER, name='OUTPUT',
           label='output')
def test(instance, parameters, context, feedback, inputs):
    """
    Description of the algorithm.
    (If there is no comment here, you will get an error)
    """
    vl = QgsVectorLayer(parameters["INPUT"], "ecu_bnd_adm2_ge", "ogr")
    context.temporaryLayerStore().addMapLayer(vl)    
    details = QgsProcessingContext.LayerDetails(QgsProcessingContext.LayerDetails('my_new_layer', context.project(), "OUTPUT"))
    context.addLayerToLoadOnCompletion(vl.id(), details)

    return {"OUTPUT": vl}

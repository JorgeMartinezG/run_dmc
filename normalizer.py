import numpy as np
from qgis import processing
from qgis.PyQt.QtCore import QVariant
from qgis.processing import alg
from qgis.core import *


@alg(name='normalizer', label="analysis", group='analysis', group_label='Risk analysis')
@alg.input(type=alg.SOURCE, name="INPUT", label="Input layer")
@alg.input(type=alg.SINK, name="OUTPUT", label="Output layer")
def normalize(instance, parameters, context, feedback, inputs):
    """
        Normalizer
    """

    attr_name = "norm_value"
    source = instance.parameterAsSource(parameters, "INPUT", context)
    source_fields = source.fields()
    source_fields.append(QgsField(attr_name, QVariant.Double))

    (sink, dest_id) = instance.parameterAsSink(parameters, "OUTPUT", context,
                                           source_fields, source.wkbType(), source.sourceCrs())

    features = [f for f in source.getFeatures(QgsFeatureRequest())]
    values = [float(f.attribute("mean_rwi")) for f in features]
    # np_values = np.array(values)

    Q1 = np.percentile(values, 25)
    Q3 = np.percentile(values, 75)
    IQR = Q3 - Q1

    upper = Q3 + 1.5 * IQR
    lower = Q1 + 1.5 * IQR

    for feat in features:
        out_feat = QgsFeature()
        out_feat.setFields(source_fields)
        out_feat.setGeometry(feat.geometry())
        attr = feat.attribute("mean_rwi")
        if attr > upper:
            norm_value = 1
        elif attr < lower:
            norm_value = 0.1
        else:
            norm_value = float((attr - lower) / (upper - lower))
            
        out_feat.setAttributes([*feat.attributes(), norm_value * 10])

        sink.addFeature(out_feat, QgsFeatureSink.FastInsert)

    return {"OUTPUT": dest_id}

import pandas as pd
import json
import requests
from datetime import timedelta, date
from qgis import processing
from qgis.PyQt.QtCore import QVariant
from qgis.processing import alg
from qgis.core import *
from functools import reduce


def flatten_row(row):
    name = row["region"]["name"]
    date = row["date"]

    flatten_metrics = [
        {f"{metric_key}_{key}".lower(): value for key, value in values.items()}
        for metric_key, values in row["metrics"].items()
    ]
    metrics = reduce(lambda acc, item: {**acc, **item}, flatten_metrics)

    return {"name": name, "date": date, **metrics}


@alg(
    name="download_hungermap",
    label="Download data from Hungermap",
    group="risk_analysis",
    group_label="Risk analysis",
)
@alg.input(type=alg.STRING, name="ISO3", label="Country ISO3", default="COL")
@alg.input(
    type=alg.DATETIME,
    name="START_DATE",
    label="start date",
    default=(date.today() - timedelta(days=90)).isoformat(),
)
@alg.input(
    type=alg.DATETIME,
    name="END_DATE",
    label="end date",
    default=date.today().isoformat(),
)
@alg.input(type=alg.SINK, name="OUTPUT", label="Output layer")
def download_hungermap(instance, parameters, context, feedback, inputs):
    """
    Download data from hunger map api.
    """
    iso3 = instance.parameterAsString(parameters, "ISO3", context)
    start_date_str = instance.parameterAsString(parameters, "START_DATE", context)
    end_date_str = instance.parameterAsString(parameters, "END_DATE", context)

    start_date = start_date_str.split("T")[0]
    end_date = end_date_str.split("T")[0]

    url = f"https://api.hungermapdata.org/v1/foodsecurity/country/{iso3}/region?date_start={start_date}&date_end={end_date}"
    resp = requests.get(url)
    resp.raise_for_status()

    rows = json.loads(resp.content.decode("utf-8"))
    data_dict = [flatten_row(r) for r in rows]

    fields = list(data_dict[0].keys())

    output_fields = QgsFields()
    [output_fields.append(QgsField(f, QVariant.String)) for f in fields]

    (sink, dest_id) = instance.parameterAsSink(
        parameters,
        "OUTPUT",
        context,
        output_fields,
    )

    for item in data_dict:
        feature = QgsFeature()
        feature.setFields(output_fields)

        feature.setAttributes(list(item.values()))

        sink.addFeature(feature, QgsFeatureSink.FastInsert)

    return {"OUTPUT": dest_id}

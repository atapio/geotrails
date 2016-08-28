import gpxpy
import gpxpy.gpx

import argparse

import pandas as pd
import numpy as np

import datashader as ds
import datashader.glyphs
import datashader.transfer_functions as tf

parser = argparse.ArgumentParser(description='Plot GPX tracks.')
parser.add_argument('gpx_files', metavar='track.gpx',  nargs='+', help='an integer for the accumulator')
args = parser.parse_args()


points = []

for gpx_file in args.gpx_files:
    print("Processing {0}".format(gpx_file))
    with open(gpx_file, 'r') as f:
        try:
            gpx = gpxpy.parse(f)

            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        points.append({ 'lat': point.latitude, 'lon': point.longitude, 'elev': point.elevation })

        except (UnicodeDecodeError, gpxpy.parser.mod_gpx.GPXXMLSyntaxException):
            print("Failed to process {0}".format(gpx_file))

print("Processed {0} points".format(len(points)))

df = pd.DataFrame(points)

glyph = ds.glyphs.Point('x', 'y')
canvas = ds.Canvas(plot_width=3000, plot_height=3000)
img = tf.shade(canvas.points(df,'lon','lat',agg=ds.reductions.count()))
ds.utils.export_image(img,"test")

# 3D exporter for use with libyaul

Exporter for Blender 3.x written to output s3d.c files to be used with [libyaul](https://github.com/ijacquez/libyaul-examples/tree/develop/vdp1-sega3d)

The exporter is still incomplete.

Current features : Geometry export. Requires that the polygons are quads before exporting.

What is missing :
	Polygon colors
	Polygon attibutes
	In case os triangles, to duplicate the last vertex according to SGL documentation
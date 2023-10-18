import bpy


# Exporter to be used with the examples on https://github.com/ijacquez/libyaul-examples/tree/develop/vdp1-sega3d
# It is a work im progress.
# 
#
#
# Author : Jaerder Sousa <jaerder@videmogroup.org>
#

def write_some_data(context, filepath, bApplyTranforms):
    output=open(filepath,"w")
    vertice_list = [] #lista de vertices
    vertices_indices = []
    vertice_list_len = 0

    if bApplyTranforms :
        obj = bpy.context.object
        matrix = obj.matrix_world.copy()
        for vert in obj.data.vertices:
            vert.co = matrix @ vert.co
        obj.matrix_world.identity()


    
    output.write("#include \"mesh.h\" \n \n")
    

    mesh = context.active_object.data
    objContext = context.object
    
    output.write("static const fix16_vec3_t point_%s[] = {\n" % mesh.name)
    for k,v in enumerate(mesh.vertices):
        output.write("FIX16_VEC3_INITIALIZER(%.2f,%.2f,%.2f) \t \t /* %d */" % (v.co[0], v.co[1], v.co[2], k))
        if(k+1 < len(mesh.vertices)):
            output.write(",\n")
    output.write("\n }; \n")

    output.write("static const fix16_vec3_t normals_%s[] = {\n" % mesh.name)
    for k,n in enumerate(mesh.vertex_normals):
        output.write("FIX16_VEC3_INITIALIZER(%.2f,%.2f,%.2f) \t \t /* %d */" % (n.vector[0], n.vector[1], n.vector[2], k))
        if(k+1 < len(mesh.vertices)):
            output.write(",\n")
    output.write("\n }; \n")


    output.write("static POLYGON polygon_%s[] = {\n" % mesh.name)    
    for i,fc in enumerate(mesh.polygons):
        output.write("NORMAL(%.2f,%.2f,%.2f) ," % (fc.normal[0], fc.normal[1], fc.normal[2]))
        output.write("VERTICES (")
        for j, vertex in enumerate(fc.vertices):
            output.write(" %d " %vertex)
            if (j+1 < len(fc.vertices)):
                output.write(",")
        output.write(") ")
        if (i+1 < len(mesh.polygons)):
            output.write(",\n")
    output.write("}; \n")        
    
    output.write("static ATTR attribute_%s[] = {\n" % mesh.name)
    for i , fc in enumerate(mesh.polygons):
            output.write("ATTRIBUTE(Dual_Plane, SORT_CEN, No_Texture, C_RGB( %d,  %d, %d), No_Gouraud, MESHoff, sprPolygon, No_Option),\n" %  (colorConv(objContext.material_slots[fc.material_index].material.diffuse_color[0]) , colorConv(objContext.material_slots[fc.material_index].material.diffuse_color[1]) , colorConv(objContext.material_slots[fc.material_index].material.diffuse_color[2])) )
    output.write("\n};\n")
    
    output.write("XPDATA XDATA_S3D[] = { \n")
    output.write("\t { \n")
    output.write("\t \t point_%s, \n" % mesh.name)
    output.write("\t \t sizeof(point_%s) / sizeof(POINT), \n" % mesh.name)
    output.write("\t \t polygon_%s, \n" % mesh.name)
    output.write("\t \t sizeof(polygon_%s) / sizeof(POLYGON), \n " % mesh.name)
    output.write("\t \t attribute_%s, \n"% mesh.name)
    output.write("\t \t NULL \n")
    output.write("\t } \n")
    output.write("}; ")
    output.write("\n uint32_t XPDATA_S3D_COUNT = 1;")

    output.close()
    
    vertice_indices_len = len(vertices_indices)


    
    return {'FINISHED'}

def colorConv(input):
    # max val : 31
    if(input > 1.0):
        return 1.0
    else:
        return (input*31)

# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSomeData(Operator, ExportHelper):
    """Experimental"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mixin class uses this
    filename_ext = ".s3d.c"

    filter_glob: StringProperty(
        default="*.s3d.c",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Apply Transforms",
        description="Apply transforms before model export",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="VI TIC80 3D mesh")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')

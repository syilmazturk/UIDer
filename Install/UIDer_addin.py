import arcpy
import pythonaddins
import time

class ButtonClass1(object):
    """Implementation for UIDer_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        list_contained_all_feature_classes = []
        list_contained_specified_field_name = []

        mxd = arcpy.mapping.MapDocument('CURRENT')
        layers = arcpy.mapping.ListLayers(mxd)

        for i in layers:
            list_contained_all_feature_classes.append(i.name)
            
        for j in list_contained_all_feature_classes:
            field_names = [f.name for f in arcpy.ListFields(j) if f.type != 'Geometry']
            if 'UID' in field_names:
                list_contained_specified_field_name.append(j)
                
        uid = str(int(time.time() * 1000))

        for feature_classes in list_contained_specified_field_name:
            if len(arcpy.Describe(feature_classes).FIDSet) > 0:
                with arcpy.da.UpdateCursor(feature_classes, ['UID']) as cursor:
                    for row in cursor:
                        row[0] = uid
                        cursor.updateRow(row)
                    del cursor
                    del row
            else:
                print 'there is no selection in ' + feature_classes
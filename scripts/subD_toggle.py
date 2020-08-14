import bpy

bl_info = {
	"name": "Subsurf Toggle",
	"author": "Quentin Steinke",
	"version": (1, 0),
	"blender": (2, 83, 4),
	"category": "Mesh",
	"location": "Operator Search",
	"description": "Maya-like subsurf toggling feature"
}

class OBJECT_OT_subd_toggling(bpy.types.Operator):
	"""Tool Tip"""
	bl_idname = 'object.subd_toggling'
	bl_label = 'SubT'


	del_subD: bpy.props.BoolProperty(
		name="x",
		description="Remove modifier",
		default=True,
	)
	subD_number: bpy.props.IntProperty(
		name="num",
		description="SubD amount",
		default=2,
		min=1, soft_max=4,
	)


	@classmethod
	def poll(cls, context):
		return context.area.type == 'VIEW_3D'

	def execute(self, context):

		has_subD = bpy.context.active_object.modifiers.find("Subdivision") + 1
		mesh = bpy.context.active_object.data
		mode = bpy.context.active_object.mode

		#perameters and buttons
		delete_modifier = self.del_subD
		sub_levels = self.subD_number

		def shade_flat():
			# shade flat
			if mode == 'OBJECT':
				bpy.ops.object.mode_set(mode='OBJECT')
				bpy.ops.object.shade_flat()

			if mode == 'EDIT':
				bpy.ops.object.mode_set(mode='OBJECT')
				bpy.ops.object.shade_flat()
				bpy.ops.object.mode_set(mode='EDIT')

		def shade_smooth():
			# shade smooth
			if mode == 'OBJECT':
				bpy.ops.object.mode_set(mode='OBJECT')
				bpy.ops.object.shade_smooth()

			if mode == 'EDIT':
				bpy.ops.object.mode_set(mode='OBJECT')
				bpy.ops.object.shade_smooth()
				bpy.ops.object.mode_set(mode='EDIT')

		# checking to see if object has subsurf modifier. if not, add one.
		if not has_subD:
			# adding subsurf with settings
			bpy.ops.object.modifier_add(type='SUBSURF')
			bpy.context.object.modifiers["Subdivision"].levels = sub_levels
			bpy.context.object.modifiers["Subdivision"].show_on_cage = True
			num_1 = 1

			shade_smooth()

		elif has_subD and delete_modifier and bpy.context.object.modifiers["Subdivision"].show_viewport:
			bpy.ops.object.modifier_remove(modifier="Subdivision")
			num_1 = 2

			shade_flat()

		elif has_subD and not delete_modifier and bpy.context.object.modifiers["Subdivision"].show_viewport:
			bpy.context.object.modifiers["Subdivision"].show_viewport = False
			num1 = 1

			shade_flat()

		else:
			bpy.context.object.modifiers["Subdivision"].show_viewport = True
			shade_smooth()

		return {'FINISHED'}

class VIEW3D_PT_subd_panel(bpy.types.Panel):
	bl_label = "SubDiv"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "SubD"

	def draw(self, context):
		col = self.layout.column()
		col.operator('object.subd_toggling',
			text='SubD',
			icon='META_BALL')
		props = col.operator('object.subd_toggling',
			text='Delete subD',
			icon='META_BALL')
		props.del_subD = False


blender_classes = [
	OBJECT_OT_subd_toggling,
	VIEW3D_PT_subd_panel
]

addon_keymaps = []

def register():
	for blender_class in blender_classes:
		bpy.utils.register_class(blender_class)

wm = bpy.context.window_manager
kc = wm.keyconfigs.addon
if kc:
	km = kc.keymaps.new(name='3D View', space_type= 'VIEW_3D')
	kmi = km.keymap_items.new("object.subd_toggling", type= 'FOUR', value= 'PRESS')
	addon_keymaps.append((km, kmi))

def unregister():
	for km,kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()

	for blender_class in blender_classes:
		bpy.utils.unregister_class(blender_class)
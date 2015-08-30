bl_info = {
	"name": "MegaRend",
	"category": "Render",
}

import bpy
import socket
import os
import sys

class MegaRendDraw(bpy.types.Panel):
	# bl_label shows up as a second set of text in the label for your entry in the Properties.
	bl_label = "MegaRend"

	# How to determine which of the 'EDITOR TYPES' your addon is going to be placed in.
	# You know when you click on a button to select the text editor, the python console, the 3D View, etc?
	# This is how we specify which Editor Type our functionality goes into.

	# Now does setting bl_space_type to other things besides 'PROPERTIES' in a class where bpy.types.Panel was passed in?  That I'm not sure yet.
	# We'll figure that out eventually.

	# But how do you find out what the names of these are?  It's a little convoluted, but here is the procedure:
	# 1.  Load up any window with Editor Type in question by left-click and selecting it.  Lets do the 3D View, since that's the normal default.
	# 2.  Right-click on the button that you would use to change the Editor Type, and say "Edit Source".
	# 3.  At top of Blender (the panel where you seeclt the Render Type (cycles, BI, game, etc), there will be a brief message saying 
	#     the name of the Text File, and to use the text editor to view it.  If you didn't catch the name, it's ok, we should still be able to find it.
	# 4.  Left-click the Editor Type button and select 'Text Editor'.
	# 5.  Now see the icon on the bottom of this panel where you can add/save/rename a file?  Click on the notepad icon, and you will see a list of current open 
	#     text files.  You might have to use a little detective work to figure out what blender save the file as, but in this case it's space_view3d.py
	# 6.  Now in space_view3d.py, look for "bl_space_type".  In this case it's set to 'VIEW_3D'.  So that's what we set bl_space_type below to to get into the
	#     the 3D Editor Type.

	# I went through all of the Default Editor Types and listed them here for reference:
	#bl_space_type = "CONSOLE"		# Python Console
	#bl_space_type = "FILE_BROWSER"		# File Browser
	#bl_space_type = "INFO"			# Info
	#bl_space_type = "USER_PREFERENCES"	# User Preferences
	#bl_space_type = "OUTLINER"		# Outliner (Default upper right hand tree view of the objects within a 3d view)
	#bl_space_type = "PROPERTIES"		# Where all of the Camera, Object, Materials etc values are modified.  
	#bl_space_type = "LOGIC_EDITOR"		# Logic Editor
	#bl_space_type = "NODE_EDITOR"		# Node Editor
	#bl_space_type = "TEXT_EDITOR"		# Text Editor
	#bl_space_type = "CLIP_EDITOR"		# Movie Clip Editor
	#bl_space_type = "SEQUENCE_EDITOR"	# Video Sequence Editor
	#bl_space_type = "IMAGE_EDITOR"		# UV/Image Editor
	#bl_space_type = "NLA_EDITOR"		# NLA Editor
	#bl_space_type = "DOPESHEET_EDITOR"	# Dope Sheet
	#bl_space_type = "GRAPH_EDITOR"		# Graph Editor
	#bl_space_type = "TIMELINE"		# Timeline
	#bl_space_type = "VIEW_3D"		# 3D View editor

	bl_space_type = "PROPERTIES"
	

	bl_region_type = "WINDOW"

	# How to determine Which button your addon appears in the 'Properties' Window/Editor type: 
	
	# In the 'Properties Editor Type', these are the button icons (the camera, the materials, the textures, the particle system, the physics button...etc).
	# bl_context will add us to one of those depending on what we set it to. 
	#bl_context = "world" 			
	bl_context = "render"			# This is the camera icon, for the render settings
	#bl_context = "render_layer"		# This is the Render Layer button, the icon with the 2 pictures stacked on top of each other, with the bottom being slightly offset.
	#bl_context = "scene"			# The scene icon, it has a sun and a couple objects.  
	#bl_context = "world"			# The world icon, a picture of Earth.  
	#bl_context = "object"			# The Object icon.  This is for the properties of an object.
	#bl_context = "constraint"		# The Object constraints icon.  
	#bl_context = "modifier"		# The Object Modifiers icon.  It's a wrench.
	#bl_context = "data"			# The Object Data icon.  Looks like an upside down triangle with the verticies enlarged.
	#bl_context = "material"		# The Material icon.  Looks like a sphere with red/pink colors.
	#bl_context = "texture"			# The Texture icon.  Looks like a red and white checkerboard. 
	#bl_context = "particle"		# The Particle System icon.  Looks like 4 shining stars.
	#bl_context = "physics"			# The Physics icon.  Looks like a ball bouncing with the checkmark path visible.	
		
	

	def draw_header(self, context):
		layout = self.layout
		#layout.label(text="MegaRend", icon="PHYSICS")
		#layout.label(text="MegaRend", icon="MOD_EXPLODE")

	def draw(self, context):
		layout = self.layout

		row = layout.row(align=True)
		#split = row.split(percentage=0.5)
		row.operator("my.server_button", text="Start Server")
		row.prop(context.scene, "server_port")

		row = layout.row(align=True)	
		row.prop(context.scene, "my_string_prop")


class MegaRend(bpy.types.Operator):
	"""Render on the Network using Shaunimation Studios MegaRend"""
	bl_idname = "object.megarend"		# Uniqe id name
	bl_label = "Render on the Network"
	bl_options = {'REGISTER', 'UNDO'}	# Enabled undo.  Figure it would work somehow.
	bl_description = "Render me on the network"

	def execute(self, context):
		self.report({'INFO'}, "This is where we would kick off renders.")	

		return {'FINISHED'}

#class OBJECT_OT_stop_server_button(bpy.types.Operator):
#	bl_idname = "my.server_stop_button"
#	bl_label = "This is how we stop the server"
#
#	def execute(self, context):
		

class OBJECT_OT_Button(bpy.types.Operator):
	bl_idname = "my.server_button"
	bl_label = "This is the Button Label"

	
	def execute (self, context):
		bpy.context.scene.my_string_prop = "Start Server clicked!"

		# Start the server!

		# Since we don't know exactly what is going on yet, the use of os.waitpid(pid,0) is in question.
		# Right now operationally it's going through without pausing now either way.
		# So in the spirit of keeping things as simple as possible, lets keep it commented out for now.

		def parent():
			try:
				pid = os.fork()

				print ("What is first PID: %d" % (pid))  
				
			except OSError as e:
				raise 

			if pid:
				print ("Parent procees here.")
				#os.waitpid(pid, 0)	
				
			else:
				print ("Child process here.")

				# This makes the child a session leader.
				#os.setsid()
				server_socket = socket.socket()				# Creating the socket object
				host = socket.gethostname()				# hostname of local machine
				port = int(bpy.context.scene.server_port)		# Get the port number specified in the GUI.

				try:
					server_socket.bind((host, port))			# Bind to the port
					server_socket.listen(5)
			
					while True:
						client, address = server_socket.accept()	# Establish connection with client
						print ('Got connection from', address)
						client.send('Thank you for connecting')		# Send client a note.
						client.close()					# Closing the connection
			
				except socket.error as msg:
					if server_socket:
						server_socket.close()

					print ("Socket in use.")

				os._exit(0)
		parent()

		return {'FINISHED'}


def register():
	bpy.utils.register_module(__name__)

	bpy.types.Scene.my_string_prop = bpy.props.StringProperty \
		(
			name = "My String",
			description = "My description",
			default = "default"
		)


	bpy.types.Scene.server_port = bpy.props.StringProperty \
		(
			name = "Port:",
			description = "Port for server to listen on",
			default = "1234"
		)

	#bpy.utils.register_class(MegaRend)
	#bpy.types.RENDER_PT_render.append(render_panel)

	#bpy.utils.unregister_class(MegaRend)

def unregister():
	bpy.utils.unregister_module(__name__)
	

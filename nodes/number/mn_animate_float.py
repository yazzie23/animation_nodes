import bpy
from bpy.types import Node
from mn_cache import getUniformRandom
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling
from mn_interpolation_utils import *

class mn_AnimateFloatNode(Node, AnimationNode):
	bl_idname = "mn_AnimateFloatNode"
	bl_label = "Animate Number"
	outputUseParameterName = "useOutput"
	
	def init(self, context):
		forbidCompiling()
		self.inputs.new("mn_FloatSocket", "Start")
		self.inputs.new("mn_FloatSocket", "End")
		self.inputs.new("mn_FloatSocket", "Time")
		self.inputs.new("mn_InterpolationSocket", "Interpolation")
		self.inputs.new("mn_FloatSocket", "Movement Time").number = 20.0
		self.inputs.new("mn_FloatSocket", "Stay Time").number = 0.0
		self.outputs.new("mn_FloatSocket", "Result")
		self.outputs.new("mn_FloatSocket", "New Time")
		self.outputs.new("mn_FloatSocket", "Difference")
		allowCompiling()
		
	def draw_buttons(self, context, layout):
		pass
		
	def getInputSocketNames(self):
		return {"Start" : "start", "End" : "end", "Time" : "time", "Interpolation" : "interpolation", "Movement Time" : "moveTime", "Stay Time" : "stayTime"}
	def getOutputSocketNames(self):
		return {"Result" : "result", "New Time" : "newTime", "Difference" : "difference"}
		
	def execute(self, useOutput, start, end, time, interpolation, moveTime, stayTime):
		influence = interpolation[0](max(min(time / moveTime, 1.0), 0.0), interpolation[1])
		result = start * (1 - influence) + end * influence
		velocity = 0
		if useOutput["Difference"]:
			influence = interpolation[0](max(min((time - 1)/ moveTime, 1.0), 0.0), interpolation[1])
			oldResult = start * (1 - influence) + end * influence
			difference = result - oldResult
		return result, time - moveTime - stayTime, difference
		
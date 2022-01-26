import zipfile

class InvalidUMvC3Stg(Exception):
	def __init__(self, message="umvc3stg must include a 0000.arc file"):
		super().__init__(message)

class UMvC3Stg(zipfile.ZipFile):
    def __init__(self, name, mode='r', compression=0, allowZip64=True, compresslevel=None):
    	super().__init__(name, mode, compression, allowZip64, compresslevel)

    	self.ARC = '0000.arc'
    	self.ANNOUNCER = 'announcer.xsew'
    	self.STG_TEXT = 'stage_select_text.tex'
    	self.STG_PREVIEW = 'stage_preview.tex'
    	self.STG_PREVIEW_SM = 'small_stage_preview.tex'
    	self.STG_TEXT_ARCADE = 'arcade_text.tex'

    	# file contents of possible files included in the .umvc3stg
    	self.stage_arc = b''             # 0000.arc
    	self.announcer = b''             # announcer.xsew
    	self.stage_select_text = b''     # stage_select_text.tex
    	self.stage_preview = b''         # stage_preview.tex
    	self.small_stage_preview = b''   # small_stage_preview.tex
    	self.arcade_text = b''           # arcade_text.tex

    	if mode == 'r':
    		namelist = set(self.namelist())

	    	# the arc file containing the stage
	    	if self.ARC not in namelist:
	    		raise InvalidUMvC3Stg
	    	else:
	    		with self.open(self.ARC, 'r') as f:
	    			self.stage_arc = f.read()

	    	# optional files
	    	if self.ANNOUNCER in namelist:
	    		with self.open(self.ANNOUNCER, 'r') as f:
	    			self.announcer = f.read()
	    	if self.STG_TEXT in namelist:
	    		with self.open(self.STG_TEXT, 'r') as f:
	    			self.stage_select_text = f.read()
	    	if self.STG_PREVIEW in namelist:
	    		with self.open(self.STG_PREVIEW, 'r') as f:
	    			self.stage_preview = f.read()
	    	if self.STG_PREVIEW_SM in namelist:
	    		with self.open(self.STG_PREVIEW_SM, 'r') as f:
	    			self.small_stage_preview = f.read()
	    	if self.STG_TEXT_ARCADE in namelist:
	    		with self.open(self.STG_TEXT_ARCADE, 'r') as f:
	    			self.arcade_text = f.read()

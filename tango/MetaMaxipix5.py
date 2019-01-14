############################################################################
# This file is part of LImA, a Library for Image Acquisition
#
# Copyright (C) : 2009-2019
# European Synchrotron Radiation Facility
# BP 220, Grenoble 38043
# FRANCE
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
############################################################################
#=============================================================================
#
# file :        MetaMaxipix5.py
#
# description : Python source for the MetaMaxipix5, a Lima Meta detector
#                for 5x1 or 3x2 maxipix meta assembly. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                Pilatus are implemented in this file.
#
# project :     TANGO Device Server
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#         (c) - Bliss - ESRF
#=============================================================================
#
import PyTango
import sys, types, os, time

from Lima import Core
from Lima import Maxipix as MaxipixModule
from Lima import Meta

# import some useful helpers to create direct mapping between tango attributes
# and Lima interfaces.
from Lima.Server import AttrHelper

class MetaMaxipix:
    Core.DEB_CLASS(Core.DebModApplication, 'MetaMaxipix')

    @Core.DEB_MEMBER_FUNCT
    def __init__(self, mpx):
        self.mpx = mpx
        self.priam=[]
        for p in range(5):
            self.priam.append(mpx[p].priamAcq())

                
    @Core.DEB_MEMBER_FUNCT
    def setFillMode(self, mode):
        for m in range(5):
            self.mpx[m].setFillMode(mode)
                
    @Core.DEB_MEMBER_FUNCT
    def getFillMode(self):
        if self.mpx[0].getFillMode() != self.mpx[1].getFillMode():
            return -1
        else:
            return self.mpx[0].getFillMode()

    
    @Core.DEB_MEMBER_FUNCT
    def setReadyMode(self, mode):
        for p in range(5):
            self.priam[p].setReadyMode(mode)
        
    @Core.DEB_MEMBER_FUNCT
    def getReadyMode(self):
        if self.priam[0].getReadyMode() != self.priam[1].getReadyMode():
            return -1
        else:
            return self.priam[0].getReadyMode()
        
    @Core.DEB_MEMBER_FUNCT
    def setGateMode(self, mode):
        for p in range(5):
            self.priam[p].setGateMode(mode)
        
    @Core.DEB_MEMBER_FUNCT
    def getGateMode(self):
        if self.priam[0].getGateMode() != self.priam[1].getGateMode():
            return -1
        else:
            return self.priam[0].getGateMode()
        
    @Core.DEB_MEMBER_FUNCT
    def setReadyLevel(self, level):
        for p in range(5):
            self.priam[p].setReadyLevel(level)
        
    @Core.DEB_MEMBER_FUNCT
    def getReadyLevel(self):
        if self.priam[p].getReadyLevel() != self.priam[p].getReadyLevel():
            return -1
        else:
            return self.priam[0].getReadyLevel()
        
    @Core.DEB_MEMBER_FUNCT
    def setGateLevel(self, level):
        for p in range(5):
            self.priam[p].setGateLevel(level)
        
    @Core.DEB_MEMBER_FUNCT
    def getGateLevel(self):
        if self.priam[0].getGateLevel() != self.priam[1].getGateLevel():
            return -1
        else:
            return self.priam[0].getGateLevel()

    @Core.DEB_MEMBER_FUNCT
    def setTriggerLevel(self, level):
        for p in range(5):
            self.priam[p].setTriggerLevel(level)

    @Core.DEB_MEMBER_FUNCT
    def getTriggerLevel(self):
        if self.priam[0].getTriggerLevel() != self.priam[1].getTriggerLevel():
            return -1
        else:
            return self.priam[0].getTriggerLevel()
    
    @Core.DEB_MEMBER_FUNCT
    def setShutterLevel(self, level):
	for p in range(5):
            self.priam[p].setShutterLevel(level)       
        
    @Core.DEB_MEMBER_FUNCT
    def getShutterLevel(self):
        if self.priam[0].getShutterLevel() != self.priam[1].getShutterLevel():
            return -1
        else:
            return self.priam[0].getTriggerLevel()
        
    @Core.DEB_MEMBER_FUNCT
    def setEnergy(self, energy):
	for m in range(5):
	    self.mpx[m].setEnergy(energy)
                
    @Core.DEB_MEMBER_FUNCT
    def getEnergy(self):
        energy = self.mpx[0].getEnergy()
        return energy
        
        
    @Core.DEB_MEMBER_FUNCT
    def getConfigName(self) :
        cfg_name = ''
        if self.config_name[0] and self.config_name[1]:
            cfg_name = 'm1:'+self.config_name[0] +'/m2:'+self.config_name[1]+ \
		'/m3:'+self.config_name[2] +'/m4:'+self.config_name[3]+ \
		'/m5:'+self.config_name[4]
        return cfg_name

    ## @brief read the config path
    #
    def getConfigPath(self,attr) :
       cfg_path = ''
       if self.config_path:
           cfg_path = self.config_path 
       return cfg_path

        

class MetaMaxipix5(PyTango.Device_4Impl):

    Core.DEB_CLASS(Core.DebModApplication, 'MetaMaxipix5')
    

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def __init__(self,*args) :
        PyTango.Device_4Impl.__init__(self,*args)
	
        self.__SignalLevel = {'LOW_FALL': MaxipixModule.PriamAcq.LOW_FALL,\
                              'HIGH_RISE': MaxipixModule.PriamAcq.HIGH_RISE}
        self.__ReadyLevel = self.__SignalLevel
        self.__GateLevel = self.__SignalLevel
        self.__TriggerLevel = self.__SignalLevel
        self.__ShutterLevel = self.__SignalLevel
        
        self.__ReadyMode =   {'EXPOSURE': MaxipixModule.PriamAcq.EXPOSURE,\
                              'EXPOSURE_READOUT': MaxipixModule.PriamAcq.EXPOSURE_READOUT}
        self.__GateMode =    {'INACTIVE': MaxipixModule.PriamAcq.INACTIVE,\
                              'ACTIVE': MaxipixModule.PriamAcq.ACTIVE}
        self.__FillMode =    {'RAW': MaxipixModule.MaxipixReconstruction.RAW,
                              'ZERO': MaxipixModule.MaxipixReconstruction.ZERO,
                              'DISPATCH': MaxipixModule.MaxipixReconstruction.DISPATCH,
                              'MEAN': MaxipixModule.MaxipixReconstruction.MEAN
                              }
        
        self.__Attribute2FunctionBase = {'signal_level': 'SignalLevel',
                                         'ready_level': 'ReadyLevel',
                                         'gate_level': 'GateLevel',
                                         'shutter_level': 'ShutterLevel',
                                         'trigger_level': 'TriggerLevel',
                                         'ready_mode': 'ReadyMode',
                                         'gate_mode': 'GateMode',
                                         'fill_mode': 'FillMode',
                                         'energy_threshold': 'Energy'
                                         }

        self.__MetaMpx = MetaMaxipix(_MaxipixInterface)
        
        self.init_device()

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        pass

#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def init_device(self):
        self.set_state(PyTango.DevState.ON)
        # Load the properties
        self.get_device_properties(self.get_device_class())

        # Apply property to the attributes

        for attr_name in ['fill_mode','ready_mode','ready_level','gate_mode','gate_level','shutter_level','trigger_level'] :       
            self.applyNewPropery(attr_name ,None)
                                         
	
#==================================================================
# 
# Some Utils
#
#==================================================================

    @Core.DEB_MEMBER_FUNCT
    def applyNewPropery(self, prop_name, extra=None):
        if extra is not None: name = self.__OtherAttribute2FunctionBase[prop_name]
        else: name = self.__Attribute2FunctionBase[prop_name]
        key = getattr(self, prop_name)
        if not key: return # property is not set
        
        dict = getattr(self, '_'+self.__class__.__name__+'__'+name)
        func = getattr(self.__MetaMpx, 'set'+name)
        deb.Always('Setting property '+prop_name) 

        val = AttrHelper._getDictValue(dict, key.upper())
        if  val is None:
            deb.Error('Wrong value for property %s :%s' % (prop_name, val))
        else:
            if extra is not None: func(extra,val)
            else: func(val)

        
#==================================================================
#
#    Maxipix read/write attribute methods
#
#==================================================================

            
    def __getattr__(self,name) :
        return AttrHelper.get_attr_4u(self, name, self.__MetaMpx)

        

#==================================================================
#
#    Maxipix command methods
#
#==================================================================
#------------------------------------------------------------------
#    getAttrStringValueList command:
#
#    Description: return a list of authorized values if any
#    argout: DevVarStringArray   
#------------------------------------------------------------------
    @Core.DEB_MEMBER_FUNCT
    def getAttrStringValueList(self, attr_name):
        return AttrHelper.get_attr_string_value_list(self, attr_name)

class MetaMaxipix5Class(PyTango.DeviceClass):

    class_property_list = {}

    device_property_list = {
        'espia_dev_nb':
        [PyTango.DevVarShortArray,
         "Espia board device number for detector module #1 to #5",[]],
        'config_path':
        [PyTango.DevString,
         "Configuration file path for modules",[]],
        'config_name':
        [PyTango.DevVarStringArray,
         "Configuration name for module #1",[]],
        'reconstruction_active':
        [PyTango.DevBoolean,
         "Set active or inactive the image reconstruction",[]],
        'meta_config':
        [PyTango.DevString,
         "Meta configuration: 5x1 or 2x3", ['2x3']],
        'fill_mode':
        [PyTango.DevString,
         "The default configuration loaded",[]],	 
       'ready_level':
        [PyTango.DevString,
         "The ready output signal level",[]],	  
       'gate_level':
        [PyTango.DevString,
         "The gate output signal level",[]],	  
       'shutter_level':
        [PyTango.DevString,
         "The shutter output signal level",[]],	  
       'trigger_level':
        [PyTango.DevString,
         "The trigger output signal level",[]],	  
       'ready_mode':
        [PyTango.DevString,
         "The ready output signal level",[]],	  
       'gate_mode':
        [PyTango.DevString,
         "The gate output signal level",[]],	  
        }

    cmd_list = {
        'getAttrStringValueList':
        [[PyTango.DevString, "Attribute name"],
         [PyTango.DevVarStringArray, "Authorized String value list"]],
        }

    attr_list = {
        'energy_threshold':
        [[PyTango.DevDouble,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"Energy thresholds",
             'unit':"keV",
             'format':"%5.2f",
             'description':"Threshold in energy (keV)",
         }],
        'config_name':
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ],
         {
             'label':"Configuration name",
             'unit':"N/A",
             'format':"",
             'description':"root name of the configuration files",
         }],
        'config_path':
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ],
         {
             'label':"Configuration directory path",
             'unit':"N/A",
             'format':"",
             'description':"Path of the configuration directory",
         }],
        'fill_mode':	  
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"Fill mode",
             'unit':"enum.",
             'format':"",
             'description':"Between chip filling mode",
         }],	  
        'ready_mode':	  
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"Ready output mode",
             'unit':"enum.",
             'format':"",
             'description':"Mode of the Ready output",
         }],	  
        'ready_level':	  
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"Ready output level",
             'unit':"enum.",
             'format':"",
             'description':"The level logic of the Ready output",
         }],	  
        'shutter_level':	  
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"Shutter output level",
             'unit':"enum.",
             'format':"",
             'description':"The level logic of the  Shutter output",
         }],	  
        'gate_mode':	  
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"The Gate input mode",
             'unit':"enum.",
             'format':"",
             'description':"",
         }],	  
        'gate_level':	  
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"",
             'unit':"",
             'format':"",
             'description':"",
         }],	  
        'trigger_level':	  
        [[PyTango.DevString,
          PyTango.SCALAR,
          PyTango.READ_WRITE],
         {
             'label':"",
             'unit':"",
             'format':"",
             'description':"",
         }],	  
        }


    def __init__(self,name) :
        PyTango.DeviceClass.__init__(self,name)
        self.set_type(name)


#----------------------------------------------------------------------------
#                              Plugins
#----------------------------------------------------------------------------
from Lima.Maxipix.MpxAcq import MpxAcq
import time

_MaxipixCamera = []
_MaxipixInterface = []
_MetaInterface = None

def get_control(espia_dev_nb = [],
                meta_config = '2x3',
                config_path='',
                config_name=[],
                reconstruction_active='true', **keys) :
    #properties are passed here as string

    if reconstruction_active.lower() == 'true': active = True
    else: active  = False
    if len(config_name) is not 5:
	print config_name
	raise Exception, "Invalid number of priam configuration, must be 5 !"
    else:
	for p in range(5):
            _MaxipixCamera.append(MaxipixModule.Camera(int(espia_dev_nb[p]), config_path, config_name[p], active))
            
            _MaxipixInterface.append(MaxipixModule[p].Interface(_MaxipixCamera[p]))
            time.sleep(3)

        global _MetaInterface            
        _MetaInterface = Meta.Interface()
        
        if meta_config == '2x3':
            _MetaInterface.addInterface(0,0, _MaxipixInterface[0])
            _MetaInterface.addInterface(0,1, _MaxipixInterface[1])
            _MetaInterface.addInterface(1,0, _MaxipixInterface[2])
            _MetaInterface.addInterface(1,1, _MaxipixInterface[3])
            _MetaInterface.addInterface(1,2, _MaxipixInterface[4])
            
        elif meta_config == '1x5':
            _MetaInterface.addInterface(0,0, _MaxipixInterface[0])
            _MetaInterface.addInterface(0,1, _MaxipixInterface[1])
            _MetaInterface.addInterface(0,2, _MaxipixInterface[2])
            _MetaInterface.addInterface(0,3, _MaxipixInterface[3])
            _MetaInterface.addInterface(0,4, _MaxipixInterface[4])
        else:
            raise Exception, "Invalid value for property meta_config: "+meta_config

    
    return Core.CtControl(_MetaInterface)
    
    
def get_tango_specific_class_n_device():
    return MetaMaxipix5Class,MetaMaxipix5

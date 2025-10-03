import nvapi
import sys
from ctypes import pointer, c_int
import logging

class NvAPI_Helper:
    """
    Base class for NvAPI Helper
    """
    def __init__(self):
        """
        Initializes NvAPI helper 
        """
        self.log = logging.getLogger()
        ret = nvapi.NvAPI_Initialize()
        if ret == nvapi.NvAPI_Status.NVAPI_OK:
            self.log.info("NvAPI_Initialize : Success,")
        else:
            self.log.error("NvAPI_Initialize : Failed,")
            
    def _get_driver_details(self):
        try:
            driverVersion = nvapi.NvU32()
            driverBranch = nvapi.NvAPI_ShortString()
            self.log.info("NvAPI_SYS_GetDriverAndBranchVersion :", nvapi.NvAPI_SYS_GetDriverAndBranchVersion(pointer(driverVersion), driverBranch))
            driverVersion = [int(driverVersion.value/100), driverVersion.value%100]
            self.log.info("    version :" , driverVersion)
            self.log.info("    branch :", str(driverBranch.value, "ascii"))
            return driverVersion,driverBranch
        except Exception as e:
            self.log.error(e)
            raise Exception ("Exception Found in fetch driver details ")
            
    def _get_gpu_driver_type(self):   
        try:
            gpuCount = nvapi.NvU32()
            gpuHandlesArr = (nvapi.NvPhysicalGpuHandle * nvapi.NVAPI_MAX_PHYSICAL_GPUS)()
            self.log.info("NvAPI_EnumPhysicalGPUs :", nvapi.NvAPI_EnumPhysicalGPUs(pointer(gpuHandlesArr), pointer(gpuCount)))
            self.log.info("    gpuCount : " + str(gpuCount.value))
            gpuBrandType = c_int()
            ret = nvapi.NvAPI_GPU_GetBrandType(gpuHandlesArr[0], pointer(gpuBrandType))
            if ret == nvapi.NvAPI_Status.NVAPI_OK:
                if gpuBrandType.value in {1,8}:
                    self.log.info("Driver Type is GeforceWeb")
                    return "GeforceWeb"
                elif gpuBrandType.value in {2,3,4,7,9}:
                    self.log.info("Driver Type is QuadroWeb")
                    return "QuadroWeb"
                else:
                    self.log.info("Driver Type is Others")
                    return "Others"
                    
            else:
                self.log.error("NvAPI_GPU_GetBrandType : Failed,")
                return None
        except Exception as e:
            self.log.error(e)
            raise Exception ("Exception Found in _get_gpu_driver_type")
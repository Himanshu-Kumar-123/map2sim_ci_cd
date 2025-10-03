import threading
import time
import logging
from omni_remote_ui_automator.driver.omnidriver import OmniDriver

class CoordinatesThread:
    """Coordinates threading class that fetches the coordinates of a prim
    """
    
    def __init__(self, omni_driver: OmniDriver):
        self.log = logging.getLogger()
        self.omni_driver = omni_driver
        self._coordinates = []
        self.collecting = False
        self.thread = None

    @property
    def get_coordinates(self):
        return self._coordinates

    def fetch_coordinates(self, prim_path: str):
        """Method to fetch coordinates

        Args:
            prim_path (str): Prim path to fetch coordinates
        """
        while self.collecting:
            try:
                self.log.info("Fetching coordinates")
                coordinates = self.omni_driver.get_prim_coordinates(prim_path=prim_path)
                self._coordinates.append(coordinates)
                time.sleep(1)
            except Exception as e:
                self.log.error(f"Error fetching coordinates: {str(e)}")
                break
            
    def start_fetching_coordinates(self, prim_path):
        """Method to start thread for fetching coordinates

        Args:
            prim_path (str): Prim path to fetch coordinates
        """
        self._coordinates = []
        if not self.collecting:
            self.collecting = True
            self.coordinates_thread = threading.Thread(target=self.fetch_coordinates, args=(prim_path,))
            self.coordinates_thread.start()
            
    def stop_fetching_coordinates(self):
        """Method to stop thread for fetching coordinates"""
        if self.collecting:
            self.collecting = False
            if self.thread is not None:
                self.thread.join()

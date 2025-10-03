import yaml

from typing import Dict, Literal, Optional
from pydantic import BaseModel
from pathlib import Path


class AutomatorKitServerConfig(BaseModel):
    host: str
    port: int


class NucleusServer(BaseModel):
    server_url: str
    token_name: str


class App(BaseModel):
    type: str = Literal["standalone", "cloud"]
    install_path: str


class AutomationServiceAccount(BaseModel):
    user01: Optional[str]
    user02: Optional[str]
    user04: Optional[str]
    ovqa_gmail: Optional[str]


class ExtensionPaths(BaseModel):
    zip_path: str
    name: str


class USDPaths(BaseModel):
    path: str
    file_name: str
    folder: Optional[str] = None


class Paths(BaseModel):
    extension_paths: Dict[str, ExtensionPaths]
    dsrs_app: Dict[str, str]
    framework: Dict[str, str]
    system: Dict[str, str]
    asset_paths: Dict[str, str]
    usd_paths: Dict[str, USDPaths]


class SwitftStackAppConfig(BaseModel):
    container: str
    base_path: str


class SwiftStackConfig(BaseModel):
    endpoint_url: str
    aws_access_key_id: str
    region_name: str
    golden_images: Dict[str, SwitftStackAppConfig]


class AutomationExtensionConfig(BaseModel):
    name: str
    version: str


class AutomationClientConfig(BaseModel):
    name: str
    version: str


class Wrapp(BaseModel):
    build_name: str
    batch_file: str
    install_path: str


class Config(BaseModel):
    automator_kit_server: Dict[str, AutomatorKitServerConfig]
    allure_server: Dict[str, str]
    nucleus_server: Dict[str, NucleusServer]
    app: App
    paths: Paths
    automation_service_account: AutomationServiceAccount
    swiftstack_config: SwiftStackConfig
    automation_extension: AutomationExtensionConfig
    automation_client_library: AutomationClientConfig
    wrapp: Wrapp
    bat_database: Dict[str, str]


def load_config_data() -> dict:
    """Load configuration data from a YAML file.

    Returns:
        dict: The configuration data as a dictionary.
    """
    with open(Path("config/configuration.yaml")) as f:
        config_data = yaml.safe_load(f)
    return config_data


def create_config_object(config_data: dict) -> Config:
    """Create a Config object from the configuration data.

    Args:
        config_data (dict): The configuration data as a dictionary.

    Returns:
        Config: The configuration object.
    """
    config = Config(**config_data)
    return config


def get_config() -> Config:
    """Get the configuration object.

    Returns:
        Config: The configuration object.
    """
    config_data = load_config_data()
    config = create_config_object(config_data)
    return config

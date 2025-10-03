from fwk.fwk_logger.fwk_logging import get_logger
from fwk.shared.variables_util import varc
from pathlib import Path
import logging


def get_test_logger(module_name: str, per_test_file: bool = False, test_logs_path: str = None) -> logging.Logger:
    logger = get_logger(module_name, varc.framework_logs_path)
    if per_test_file and test_logs_path:
        try:
            Path(test_logs_path).mkdir(parents=True, exist_ok=True)
            file_path = str(Path(test_logs_path) / f"{module_name.replace('.', '_')}.log")
            handler = logging.FileHandler(file_path, encoding='utf-8')
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('\n[DMF_TEST] : %(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        except Exception:
            # fallback silently
            pass
    return logger

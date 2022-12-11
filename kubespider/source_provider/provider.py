import os
import abc
import threading

import configparser

class SourceProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self) -> None:
        pass
    
    @abc.abstractmethod
    def get_provider_name(self):
        pass 

    @abc.abstractmethod
    def get_provider_type(self):
        pass

    @abc.abstractmethod
    def get_file_type(self):
        pass

    @abc.abstractmethod
    def get_download_path(self):
        pass

    @abc.abstractmethod
    def provider_enabled(self):
        pass

    @abc.abstractmethod
    def is_webhook_enable(self):
        pass

    @abc.abstractmethod
    def should_handle(self, dataSourceUrl):
        pass
    
    @abc.abstractmethod
    def get_links(self, dataSourceUrl):
        pass

    @abc.abstractmethod
    def update_config(self, reqPara):
        pass

    @abc.abstractmethod
    def load_config(self):
        pass

source_provider_file_lock = threading.Lock()

def load_source_provide_config(provider_name):
    source_provider_file_lock.acquire()
    cfg = configparser.ConfigParser()
    config_path = os.path.join(os.getenv('HOME'), '.kubespider/source_provider.cfg')
    cfg.read(config_path)
    if provider_name in cfg.sections():
        source_provider_file_lock.release()
        return cfg[provider_name]
    source_provider_file_lock.release()
    return {}

def save_source_provider_config(provider_name, section_cfg):
    source_provider_file_lock.acquire()
    cfg = configparser.ConfigParser()
    config_path = os.path.join(os.getenv('HOME'), '.kubespider/source_provider.cfg')
    cfg.read(config_path)
    cfg[provider_name] = section_cfg
    with open(config_path, 'w') as f:
        cfg.write(f)
        f.close()
    source_provider_file_lock.release()
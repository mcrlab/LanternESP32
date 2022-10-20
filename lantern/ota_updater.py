import socket
import os
import gc
from .logging import logger

try:
    from machine import reset
    import urequests as requests
except (ImportError, ModuleNotFoundError) as e:
    import requests
    from mocks import reset



class OTAUpdater:

    def __init__(self, github_repo, module='', main_dir='main', proxy=''):
        
        if proxy:
            self.github_repo = github_repo.rstrip('/').replace('https://github.com', proxy+'/repos')
        else:
            self.github_repo = github_repo.rstrip('/').replace('https://github.com', 'https://api.github.com/repos')
        self.main_dir = main_dir
        self.module = module.rstrip('/')
        self.proxy = proxy

    def check_for_update_to_install_during_next_reboot(self):
        current_version = self.get_version(self.modulepath(self.main_dir))
        latest_version = self.get_latest_version()

        logger.log('Checking version... ')
        logger.log('\tCurrent version: '+ current_version)
        logger.log('\tLatest version: '+ latest_version)
        if latest_version > current_version:
            logger.log('New version available, will download and install on next reboot')
            os.mkdir(self.modulepath('next'))
            with open(self.modulepath('next/.version_on_reboot'), 'w') as versionfile:
                versionfile.write(latest_version)
                versionfile.close()

    def download_and_install_update_if_available(self):
        if 'next' in os.listdir(self.module):
            if '.version_on_reboot' in os.listdir(self.modulepath('next')):
                latest_version = self.get_version(self.modulepath('next'), '.version_on_reboot')
                logger.log('New update found: '+ latest_version)
                self._download_and_install_update(latest_version)
        else:
            logger.log('No new updates found...')

    def _download_and_install_update(self, latest_version):
        self.download_all_files(self.github_repo + '/contents/' + self.main_dir, latest_version)
        self.rmtree(self.modulepath(self.main_dir))
        os.rename(self.modulepath('next/.version_on_reboot'), self.modulepath('next/.version'))
        os.rename(self.modulepath('next'), self.modulepath(self.main_dir))
        logger.log('Update installed ('+ latest_version+ '), will reboot now')
        reset()

    def apply_pending_updates_if_available(self):
        if 'next' in os.listdir(self.module):
            if '.version' in os.listdir(self.modulepath('next')):
                pending_update_version = self.get_version(self.modulepath('next'))
                logger.log('Pending update found: '+ pending_update_version)
                self.rmtree(self.modulepath(self.main_dir))
                os.rename(self.modulepath('next'), self.modulepath(self.main_dir))
                logger.log('Update applied ('+ pending_update_version+ '), ready to rock and roll')
            else:
                logger.log('Corrupt pending update found, discarding...')
                self.rmtree(self.modulepath('next'))
        else:
            logger.log('No pending update found')

    def download_updates_if_available(self):
        current_version = self.get_version(self.modulepath(self.main_dir))
        latest_version = self.get_latest_version()

        logger.log('Checking version... ')
        logger.log('Current version: '+ current_version)
        logger.log('Latest version: '+ latest_version)
        if latest_version > current_version:
            logger.log('Updating...')
            os.mkdir(self.modulepath('next'))
            self.download_all_files(self.github_repo + '/contents/' + self.main_dir, latest_version)
            with open(self.modulepath('next/.version'), 'w') as versionfile:
                versionfile.write(latest_version)
                versionfile.close()

            return True
        return False
    
    def rmtree(self, directory):
        logger.log("Removing tree: " + directory)

        try:
            for entry in os.ilistdir(directory):
                is_dir = entry[1] == 0x4000
                if is_dir:
                    self.rmtree(directory + '/' + entry[0])

                else:
                    os.remove(directory + '/' + entry[0])
            os.rmdir(directory)
        except AttributeError:
            for entry in os.listdir(directory):

                if os.path.isdir(entry):
                    self.rmtree(directory + '/' + entry)

                else:
                    os.remove(directory + '/' + entry)
            os.rmdir(directory)

    def get_version(self, directory, version_file_name='.version'):
        if version_file_name in os.listdir(directory):
            f = open(directory + '/' + version_file_name)
            version = f.read()
            f.close()
            return version
        return '0.0'

    def get_latest_version(self):
        logger.log("Fetching latest release")
        logger.log(self.github_repo + '/releases/latest')
        latest_release = requests.get(self.github_repo + '/releases/latest')
        version = latest_release.json()['tag_name']
        latest_release.close()
        return version

    def download_all_files(self, root_url, version):
        logger.log("Fetching all files")
        file_list = requests.get(root_url + '?ref=refs/tags/' + version)
        for file in file_list.json():
            if file['type'] == 'file':
                download_url = file['download_url']
                download_path = self.modulepath('next/' + file['path'].replace(self.main_dir + '/', ''))
                self.download_file(download_url.replace('refs/tags/', ''), download_path)
            elif file['type'] == 'dir':
                path = self.modulepath('next/' + file['path'].replace(self.main_dir + '/', ''))
                os.mkdir(path)
                self.download_all_files(root_url + '/' + file['name'], version)

        file_list.close()

    def download_file(self, url, path):
        if self.proxy:
            url = url.replace("https://raw.githubusercontent.com", self.proxy)

        logger.log('\tDownloading: '+ path)
        logger.log('\tURL: '+ url)
        with open(path, 'w') as outfile:
            try:
                response = requests.get(url)
                outfile.write(response.text)
            finally:
                response.close()
                outfile.close()
                gc.collect()

    def modulepath(self, path):
        return self.module + '/' + path if self.module else path

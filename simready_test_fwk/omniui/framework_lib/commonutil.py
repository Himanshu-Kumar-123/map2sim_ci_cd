# -*- coding: utf-8 -*-
# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

"""Common helper class

You can just add some common utility helpers.
Please notice that only cross-platform codes can be put here.

The following is a simple usage example:
None

The module contains the following public classes:
None

Reference:
None

"""
import re
import os
import sys
import time
import json
import shutil
import zipfile
import pkgutil
import inspect
import fnmatch
import hashlib
import argparse
import traceback
import importlib
import logging
import subprocess
from datetime import datetime
from distutils.version import LooseVersion
from threading import Thread
import requests

try:
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib import urlretrieve
    from urllib2 import urlopen


class MetaClassSingleton(type):
    """singleton helper in metaclass implementation"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaClassSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CommonUtilityClass:
    """
    Common helper class
    """

    log = logging.getLogger()

    @classmethod
    def is_url_available(cls, url_resource):
        """
        resource file
        """
        ret = False
        try:
            with urlopen(url_resource) as response:
                response.read()
            ret = True
        except:
            pass
        return ret

    @classmethod
    def get_url_response_code(cls, url):
        """
        returns response code of a given url
        """
        response = ""
        try:
            response = requests.get(url)
            return response.status_code
        except:
            return response.status_code

    @classmethod
    def log_verifier(cls, p_pat, n_pat, result_filename):
        """
        Reading log from text file then compared to given positive/negative log pattern
        Return true if all positive pattern matched; otherwise false
        Return true if all negative pattern non-matched; otherwise false
        """
        cls.log.info("Reading results from file: %s", result_filename)
        with open(result_filename, "r") as f_result:
            f_content = f_result.read()
        f_result.close()

        flag = True
        for positive in p_pat:
            if re.search(positive, f_content) is None:
                cls.log.info("[FAIL] Missing positive log pattern: %s", positive)
                flag = False
            else:
                cls.log.info("[PASS] Found positive log pattern")

        for negative in n_pat:
            if re.search(negative, f_content):
                cls.log.info("[FAIL] Found negative log pattern: %s", negative)
                flag = False
            else:
                cls.log.info("[PASS] Missing negative log pattern")

        return flag

    @classmethod
    def get_subdirs(cls, root_dir, exclude=None, dir_check=True, show_log=True):
        """Get the path of sub directories under the root dir"""
        subdirs = []
        dirs = os.listdir(root_dir)
        if exclude is None:
            exclude = []
        elif not isinstance(exclude, (list, tuple)):
            exclude = [exclude]
        exclusion_pattern = "|".join(exclude)
        exclusion_check = re.compile(exclusion_pattern)

        for direc in dirs:
            if dir_check and not os.path.isdir(os.path.join(root_dir, direc)):
                continue
            if exclusion_pattern:
                if exclusion_check.search(direc):
                    if show_log:
                        cls.log.info("-> Exclude folder:[%s]", os.path.join(root_dir, direc))
                    continue
            subdirs.append(os.path.join(root_dir, direc))
        return subdirs

    @classmethod
    def get_latest_subdir(cls, root_dir, exclude=None, dir_check=True, show_log=True):
        """
        Get latest modified sub directory under the root dir

        return Path of the latest modified dir
        """
        latest_time = 0
        latest_dir = None
        sub_dirs = cls.get_subdirs(root_dir, exclude=exclude, dir_check=dir_check, show_log=show_log)
        for dir_path in sub_dirs:
            temp_time = os.path.getmtime(dir_path)
            if latest_time < temp_time:
                latest_time = temp_time
                latest_dir = dir_path
        return latest_dir

    @classmethod
    def get_latest_versioned_subdir(cls, root_dir, exclude=None, dir_check=True, show_log=True):
        """Get latest sub directory under the root dir by version number

        return Path of latest versioned dir
        """
        lastest_version = "0.0"
        latest_versioned_dir = None
        sub_dirs = cls.get_subdirs(root_dir, exclude=exclude, dir_check=dir_check, show_log=show_log)
        for dir_path in sub_dirs:
            current_version = os.path.basename(dir_path)
            if LooseVersion(lastest_version) < LooseVersion(current_version):
                lastest_version = current_version
                latest_versioned_dir = dir_path
        return latest_versioned_dir

    @classmethod
    def cmp(cls, var_a, var_b):
        """
        cmp doesn't exist in Python 3.
        """
        return (var_a > var_b) - (var_a < var_b)

    @classmethod
    def version_comparison(cls, version1, version2):
        """
        Compare version number and return -1, 0, 1
        -1 : version1 < version2
        0  : version1 = version2
        1  : version1 > version2
        """

        def normalize(ver):
            """
            Remove the uninteresting part of the string (trailing zeroes and dots)
            """
            return [int(x) for x in re.sub(r"(\.0+)*$", "", ver).split(".")]

        return cls.cmp(normalize(version1), normalize(version2))

    @classmethod
    def md5_f(cls, fname):
        """
        get the md5 string by reading chunks of 4096 bytes sequentially and feed them to the Md5 function
        """
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:  # pylint: disable=invalid-name
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @classmethod
    def get_time_tuple_utc_now(cls):
        """get current utc time tuple"""
        dt_tuple = None
        try:
            dt_utc = datetime.strptime(str(datetime.utcnow()), "%Y-%m-%d %H:%M:%S.%f")
            dt_tuple = dt_utc.timetuple()
        except Exception as e:  # pylint: disable=broad-except,invalid-name
            cls.log.info("Failed to get current utc time: %s", str(e))
        return dt_tuple

    @classmethod
    def grab_rest_api_output_using_request(cls, url, account=(), retry=3):  # pylint: disable=invalid-name
        """
        grab rest api output using requests
        """
        from requests_ntlm import HttpNtlmAuth

        output = None
        for _ in range(retry):
            try:
                if account:
                    response = requests.get(url, auth=HttpNtlmAuth(account[0], account[1]))
                else:
                    response = requests.get(url)
                assert response.status_code == 200, "Fail to get rest api output from {0}".format(url)
                output = json.loads(response.text)
                break
            except Exception:  # pylint: disable=broad-except
                cls.log.info(traceback.format_exc())
        return output

    @classmethod
    def parse_datetime_from_string_date(cls, str_date):
        """
        parse date from string
        param str_date: support following string date input
            1. mm-dd-YYYY
            2. YYYY-mm-dd
            3. mm/dd/YYYY
            4. YYYY/mm/dd

        return datetime
        """
        date_time_format = None  # time format to parse time_filter
        time_filter_formats = []
        time_filter_formats.append({"pattern": r"^\d{2}-\d{2}-\d{4}$", "format": "%m-%d-%Y"})
        time_filter_formats.append({"pattern": r"^\d{4}-\d{2}-\d{2}$", "format": "%Y-%m-%d"})
        time_filter_formats.append({"pattern": r"^\d{2}/\d{2}/\d{4}$", "format": "%m/%d/%Y"})
        time_filter_formats.append({"pattern": r"^\d{4}/\d{2}/\d{2}$", "format": "%Y/%m/%d"})
        for filter_format in time_filter_formats:
            if re.search(filter_format["pattern"], str_date):
                date_time_format = filter_format["format"]
                break
        assert date_time_format is not None, "Find invalid str_date value:[{0}]".format(str_date)
        return datetime.strptime(str_date, date_time_format)

    @classmethod
    def is_isoformat_date_time_string(cls, str_datetime, assert_on_fail=False):
        """Check if input string is valid isoformat date time"""
        is_isoformat = False
        err_msg = (
            "Invalid Argument Format:[{0}],         expecting isoformat time string : YYYY-mm-ddTHH:MM:SS.fff".format(
                str_datetime
            )
        )
        if str_datetime is not None:
            m = re.search(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+$", str_datetime)  # pylint: disable=invalid-name
            is_isoformat = bool(m)
            if assert_on_fail:
                assert is_isoformat, err_msg

    @classmethod
    def find_files(cls, dir_path, filename_pattern):
        """find files recursively"""
        matches = []
        for root, _, filenames in os.walk(dir_path):
            for filename in fnmatch.filter(filenames, filename_pattern):
                matches.append(os.path.join(root, filename))
        return matches

    @classmethod
    def nested_update(cls, dict1, dict2):
        """Nested Dict Update
        Problem:
            > d = {}
            > d.update({'a': {'b': 1}})
            > d
            {'a': {'b': 1}}
            > d.update({'a': {'c': 2}})
            > d
            {'a': {'c': 2}}
        Solution:
            > d = {}
            > CommonUtilityClass.nested_update(d, {'a': {'b': 1}})
            {'a': {'b': 1}}
            > CommonUtilityClass.nested_update(d, {'a': {'c': 2}})
            {'a': {'c': 2, 'b': 1}}
        """
        for k, v in dict2.items():  # pylint: disable=invalid-name
            if isinstance(v, dict):
                dict1[k] = cls.nested_update(dict1.get(k, {}), v)
            else:
                dict1[k] = v
        return dict1

    @classmethod
    def find_subclass(cls, class_object, search_path):
        """search sub-class according to a given class_object in search_path which is
        a relative path to current working directory
        """
        namespace = search_path.replace("\\", ".").replace("/", ".")
        real_search_path = os.path.join(os.getcwd(), search_path)
        # cls.log.info("*** DEBUG:[{0}]".format(real_search_path))

        # https://docs.python.org/2/library/pkgutil.html#pkgutil.walk_packages
        # must import all packages (not all modules!) on the given path,
        # in order to access the __path__ attribute to find submodules.
        importlib.import_module(namespace)
        for _, module_name, _ in pkgutil.walk_packages([real_search_path], namespace + "."):
            # cls.log.info("*** DEBUG:[loader:{0}, module_name:{1}, is_package:{2}]".format(loader, module_name, _))
            try:
                for _, obj in inspect.getmembers(importlib.import_module(module_name)):
                    if inspect.isclass(obj) and class_object in inspect.getmro(obj) and obj != class_object:
                        # cls.log.info("*** DEBUG:[name:{0}, obj:{1}]".format(name, obj))
                        yield obj
            except Exception as ex:
                cls.log.info("Load Module Failed -> %s. (reason: %s)", module_name, str(ex))
                continue

    @classmethod
    def grab_infos_from_logfile(cls, log_file, from_line_number=0, re_flags=0, **patterns):
        """
        grab info from log file
        """
        result = argparse.Namespace()
        compiled_patterns = {}
        for _pattern_name in patterns:  # compile patterns
            compiled_patterns[_pattern_name] = re.compile(patterns[_pattern_name], re_flags)
            setattr(result, _pattern_name, [])
        file_obj = open(log_file)  # parse file
        lnum = 0
        for line in file_obj:
            lnum = lnum + 1
            if lnum < from_line_number:
                continue
            for pattern in compiled_patterns:
                gotten = compiled_patterns[pattern].findall(line)
                if gotten:
                    getattr(result, pattern).extend(list(gotten))
        dict_result = vars(result)
        for found in dict_result:
            cls.log.info("%s %s", str(found), str(dict_result[found]))
        return result

    @classmethod
    def unicode_to_ascii(cls, unicode_input, esc="ignore"):
        """transfer unicode to ascii and do escape handling"""
        try:
            if isinstance(unicode_input, bytes):
                unicode_input = unicode_input.decode("utf-8", esc)  # decode byte string as utf-8 first
            unicode_input = unicode_input.encode("ascii", esc).decode()
        except AttributeError:
            pass
        except (UnicodeEncodeError, UnicodeDecodeError):
            cls.log.info("UnicodeEncodeError occurred : input type %s.", str(type(unicode_input)))
            cls.log.info(traceback.format_exc())
        return unicode_input

    @classmethod
    def zip_files(cls, *to_zips, **kwargs):
        """
        zip files specified in args
        kwargs:
            out_zip_file - output zip file full path
        returns:
            output_zip - final output zip file full path
        """
        ts = datetime.fromtimestamp(time.time()).strftime("%Y%m%d%H%M%S")
        output_zip = kwargs.get("out_zip_file %s", str(ts))

        def zipdir(path, ziph):
            """zip directory recursively"""
            # ziph is zipfile handle
            for root, _, files in os.walk(path):
                for fn in files:
                    full_path = os.path.join(root, fn)
                    ziph.write(full_path, full_path.replace(path, ""))

        cls.log.info("[zip_files] Create zipfile %s.", str(output_zip))
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
            for to_zip in to_zips:
                if os.path.isdir(to_zip):
                    zipdir(to_zip, zipf)
                elif os.path.isfile(to_zip):
                    zipf.write(to_zip, os.path.basename(to_zip))
                else:
                    cls.log.info("[zip_files] unknown item, skip zip %s.", to_zip)
        return output_zip

    @classmethod
    def unzip(cls, src_file_path, dest_dir=None):
        """unzip file to destination dir"""
        # make sure dest_dir
        if not dest_dir:
            dest_dir = os.path.join(os.path.dirname(src_file_path), "extracted")
        if os.path.exists(dest_dir):
            cls.log.info("[DEBUG] Removing old extracted files")
            shutil.rmtree(dest_dir)
        cls.log.info("[DEBUG] Creating extracted folder: %s", dest_dir)
        os.makedirs(dest_dir)

        # extracting file
        zip_ref = zipfile.ZipFile(src_file_path)
        try:
            cls.log.info("unzip %s...", src_file_path)
            zip_ref.extractall(dest_dir)
        finally:
            zip_ref.close()

        # make sure file exist after extracting the zipped file
        if not os.listdir(dest_dir):
            cls.log.info("[DEBUG] No file is available after extracting the zipped source file")
        return dest_dir

    @classmethod
    def untgz(cls, src_file_path, dest_dir=None):
        """untgz file to destination dir
        This is Mac only
        """
        if sys.platform != "darwin":
            raise Exception("Please implement untgz() before using. Currently only support Mac")

        # make sure dest_dir
        if not dest_dir:
            dest_dir = os.path.join(os.path.dirname(src_file_path), "extracted")
        if os.path.exists(dest_dir):
            cls.log.info("[DEBUG] Removing old extracted files")
            shutil.rmtree(dest_dir)
        cls.log.info("[DEBUG] Creating extracted folder: %s", dest_dir)
        os.makedirs(dest_dir)

        # extracting file
        unzip_cmd = "tar -xvzf %s -C %s" % (src_file_path, dest_dir)
        cls.log.info(unzip_cmd)
        subprocess.check_output(unzip_cmd, cwd=os.getcwd(), shell=True)
        subprocess.check_output("chmod -R 777 %s" % dest_dir, cwd=os.getcwd(), shell=True)

        # make sure file exist after extracting
        if not os.listdir(dest_dir):
            cls.log.info("[DEBUG] No file is available after extracting the .tgz source file")
        return dest_dir

    # @classmethod
    # def download_file_from_url(
    #     cls, download_url=None, local_dir=None, force_download=True
    # ):  # pylint: disable=invalid-name
    #     """download dmg file from givn url(Ex, web released build url)

    #     Arg: download_url: url
    #     Arg: local_dir   : dir to save the downloaded file
    #     """
    #     cls.log.info("Download Url:[%s]", download_url)
    #     file_name = os.path.basename(download_url)
    #     if local_dir is None:
    #         from nvidia.atplib.platform_lib.common.system import (
    #             ATP_APPLICATION_DIR,
    #         )  # pylint:disable=import-outside-toplevel

    #         local_dir = os.path.join(ATP_APPLICATION_DIR, "DownloadTmp")
    #     cls.log.info("Download To :[%s]", local_dir)
    #     local_file_path = os.path.join(local_dir, file_name)  # full path of zip file
    #     start_time = time.time()
    #     if os.path.isfile(local_file_path) and not force_download:
    #         cls.log.info("%s is already downloaded, skip ...", file_name)
    #     else:
    #         # download time measurement start
    #         if os.path.exists(local_dir):
    #             cls.log.info("Removing old GPUWinPackage folder: %s", local_dir)
    #             shutil.rmtree(path=local_dir, ignore_errors=True)
    #         os.makedirs(local_dir)
    #         for _ in range(3):
    #             cls.log.info("start to download file: %s...", os.path.basename(download_url))
    #             try:
    #                 urlretrieve(download_url, local_file_path)
    #                 cls.log.info("-> Done.")
    #                 break
    #             except:  # pylint: disable=bare-except
    #                 cls.log.info("Fail to download file. Try again!")
    #                 if os.path.isfile(local_file_path):
    #                     cls.log.info("clean-up file %s.", local_file_path)
    #                     os.remove(local_file_path)

    #         assert os.path.isfile(local_file_path), "file download failed..."
    #         cls.log.info("download successfully to %s...", local_file_path)
    #     stop_time = time.time()
    #     cls.log.info("Total Package Download Time: %s seconds", str(round(stop_time - start_time, 3)))
    #     return local_file_path

    # pylint: disable=invalid-name,too-many-locals,too-many-branches,too-many-statements
    @classmethod
    def copy_zip_file_and_extract(cls, src_file_path=None, dest_dir=None, use_cache=True, assert_on_fail=False):
        """download and extracted zipped file from server

        :param src_file_path: full path of the zip file
        :param dest_dir: target folder to save extracted files
        :param use_cache: True to create a cache file to save download time.
        The cache file will be save at cached_src dir in os.path.dirname(dest_dir)

        return True if success else False
        """
        cls.log.info("-> copy_zip_file_and_extract(%s, %s)", src_file_path, dest_dir)
        assert src_file_path, "Error: src_file_path is not given"

        if dest_dir is None:
            # prevent from cycling import
            # pylint: disable=import-error, no-name-in-module
            from nvidia.atplib.platform_lib.common.system import (
                ATP_APPLICATION_DIR,
            )  # pylint:disable=import-outside-toplevel

            dest_dir = os.path.join(ATP_APPLICATION_DIR, "DownloadTmp", "Extracted")

        def is_file_available(f_path, retry_cnt=30):
            """check if file is available"""
            is_available = False
            for _ in range(retry_cnt):
                is_available = os.path.isfile(f_path)
                if is_available:
                    break
                time.sleep(1)
            return is_available

        try:
            # make sure file is available in server path
            err_msg = "Failed to find {0} in server path:{1}".format(
                os.path.basename(src_file_path), os.path.dirname(src_file_path)
            )
            assert is_file_available(src_file_path), err_msg

            # generate cached file name by source path
            hashstr = hashlib.md5(src_file_path.encode()).hexdigest()
            cached_src_map_file_name = "{0}_{1}".format(hashstr, os.path.basename(src_file_path))

            # extracted CovFiles path
            local_cache_dir = os.path.join(os.path.dirname(dest_dir), "local_cache")
            cached_src_file_path = os.path.join(local_cache_dir, cached_src_map_file_name)

            if os.path.exists(dest_dir):
                cls.log.info("[DEBUG] Removing old extracted files")
                shutil.rmtree(dest_dir)
            cls.log.info("[DEBUG] Creating extracted folder: %s", dest_dir)
            os.makedirs(dest_dir)

            if not use_cache and os.path.exists(local_cache_dir):
                cls.log.info("[DEBUG] Removing old cached file dir")
                shutil.rmtree(local_cache_dir)

            # Copy zipped source file if it's not yet copied to local
            if os.path.isfile(cached_src_file_path):
                cls.log.info("[DEBUG] Cached Source File:[%s] is existed, skip copying", cached_src_file_path)
            else:
                cls.log.info("[DEBUG] Downloading zipped source file from server")
                for _ in range(3):
                    try:
                        if os.path.exists(local_cache_dir):
                            cls.log.info("[DEBUG] Removing old cached file dir")
                            shutil.rmtree(local_cache_dir)
                        cls.log.info("[DEBUG] Creating cached file dir")
                        os.makedirs(local_cache_dir)
                        message_fmt = "[DEBUG] Copying Zipped Source File:[%s] to [%s]"
                        cls.log.info(message_fmt, src_file_path, cached_src_file_path)
                        shutil.copy(src_file_path, cached_src_file_path)
                        if os.path.isfile(cached_src_file_path):
                            break
                        assert False, "Failed to download file:{0}, Retry ...".format(cached_src_file_path)
                    except Exception as ex:  # pylint: disable=broad-except
                        cls.log.info(str(ex))
            assert os.path.isfile(cached_src_file_path), "Failed to download zipped source file from server"

            # extracting file
            zip_ref = zipfile.ZipFile(cached_src_file_path)
            try:
                cls.log.info("unzip %s...", cached_src_file_path)
                zip_ref.extractall(dest_dir)
            finally:
                zip_ref.close()

            # make sure file exist after extracting the zipped file
            assert os.listdir(dest_dir), "[DEBUG] No file is available after extracting the zipped source file"

        except AssertionError as aerr:
            if assert_on_fail:
                raise aerr
            dest_dir = None
            cls.log.info("[ERROR] %s", str(aerr))
        return dest_dir

    @classmethod
    def copyFile(cls, src, dst, replace=True):
        """
        Copy a file from source to destination. Create dst folder if it does not exist.
        :type src: str
        :type dst: str
        :return: True or False to signify success
        """
        return cls.copyObj(src, dst, True, replace=replace)

    @classmethod
    def copyDir(cls, src, dst, replace=True):
        """
        Copy a directory from source to destination. Create dst folder if it does not exist.
        :type src: str
        :type dst: str
        :return: True or False to signify success
        """
        return cls.copyObj(src, dst, False, replace=replace)

    @classmethod
    def copyObj(cls, src, dst, isFile, replace=True):
        """
        Copy a file/dir from source to destination. Create dst folder if it does not exist.
        :type src: str
        :type dst: str
        :return: True or False to signify success
        """
        new_file_format = lambda filename: "%s_%s%s" % (
            os.path.splitext(filename)[0],
            datetime.now().strftime("%Y_%m_%d_%H_%M_%S"),
            os.path.splitext(filename)[1],
        )
        assert isinstance(src, str), "Invalid source %s " % str(src)
        assert isinstance(dst, str), "Invalid destination %s " % str(dst)
        if isFile:
            if not os.path.isfile(src):
                cls.log.info("Source path is not a file %s", str(src))
                return False
            if os.path.splitext(dst)[1] == "":
                # it is a directory
                if not os.path.exists(dst):
                    # which does not exist
                    try:
                        os.makedirs(dst)
                    except:
                        cls.log.info(traceback.format_exc())
                        return False
                    else:
                        cls.log.info("Created the directory: %s", str(dst))
        else:
            if not os.path.isdir(src):
                cls.log.info("Source path is not a directory: %s", str(src))
                return False
        try:
            if isFile:
                try:
                    shutil.copy(src, dst if replace else new_file_format(os.path.join(dst, src.split(os.path.sep)[-1])))
                except Exception as e:
                    cls.log.info(e)
                    cls.log.info("Retry Copy file")
                    shutil.copy(src, dst if replace else new_file_format(os.path.join(dst, src.split(os.path.sep)[-1])))
            else:
                if replace:
                    shutil.rmtree(dst, ignore_errors=True)
                shutil.copytree(src, dst)
        except:
            cls.log.info(traceback.format_exc())
            return False
        else:
            cls.log.info("Completed copying %s", str(src))
        return True

    # @classmethod
    # def ensure_path(cls, path, retry_create=10):
    #     """
    #     Make sure the target path is there.
    #     Create if it is not there.
    #     """
    #     ret = False
    #     for i in range(retry_create):
    #         if os.path.exists(path):
    #             if i != 0:
    #                 cls.log.info("[CommonUtilityClass] Create directory: %s.", path)
    #             ret = True
    #             break
    #         try:
    #             os.makedirs(path)
    #         except:
    #             cls.log.info("[CommonUtilityClass] Fail to create directory: %s.", path)
    #         time.sleep(1)
    #     if ret and sys.platform in ('linux', 'linux2'):
    #         user_name = FrameworkService.get_user_name()
    #         cls.log.info("[CommonUtilityClass] Change path owner to {0} for directory: {1}.".format(user_name, path))
    #         shutil.chown(path, user=user_name, group=user_name)
    #     return ret

    @classmethod
    def get_public_ip(cls):
        """
        get public ip from www.ipify.org
        """
        ip_string = None
        url = "http://api.ipify.org"
        try:
            ip_string = urlopen(url).read()
        except:
            cls.log.info("[CommonUtilityClass] Fail to get public ip from %s.", url)
        return ip_string

    @classmethod
    def get_country(cls):
        """
        get country from webservice
        """
        country_string = None
        url = "http://ip2c.org/self"
        try:
            country_string = urlopen(url).read().decode()
        except:
            cls.log.info("[CommonUtilityClass] Fail to get public ip from %s.", url)
        return country_string

    @classmethod
    def retry(cls, func, *f_args, **f_kwargs):
        """do retry when exception occurred

        :param retry_times: retry count
        :param retry_delay: delay time in second for next run
        """
        default_retry_times = 3
        default_retry_delay = 3  # in seconds
        retry_times = f_kwargs.pop("retry_times") if "retry_times" in f_kwargs.keys() else default_retry_times
        delay_sec = f_kwargs.pop("retry_delay") if "retry_delay" in f_kwargs.keys() else default_retry_delay
        ret = None
        try:
            func_name = func.__name__
        except AttributeError:
            pass
        for i in range(retry_times + 1):
            try:
                if i != 0:
                    cls.log.info("[CommonUtilityClass] Retry %d-th %s().", i, func_name)
                ret = func(*f_args, **f_kwargs)
                if ret:
                    break
            except:  # pylint: disable=bare-except
                cls.log.info("[CommonUtilityClass] Error\n  %s", traceback.format_exc().replace("\n", "\n  "))
                if i == retry_times:
                    raise
            cls.log.info("[CommonUtilityClass] Sleep %s sec for next retry.", str(delay_sec))
            time.sleep(delay_sec)
        return ret

    @classmethod
    def try_parse_numeric(cls, str_num):
        """try to parse string numeric number from string to numeric"""
        try:
            str_num = int(str_num)
        except:  # pylint: disable=bare-except
            try:
                str_num = float(str_num)
            except:  # pylint: disable=bare-except
                pass
        return str_num

    @classmethod
    def clear_folder_content(self, folder: str):
        """Clears folder content

        Args:
        folder(str): Folder path
        """
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))

    @staticmethod
    def click(element):
        return element.click()

    @staticmethod
    def set_environment_variable(variable, value):
        """Sets env variable for windows/linux"""
        cmd = f"setx {variable} {value}"
        if sys.platform == "win32":
            subprocess.call(cmd, shell=True)
        else:
            os.environ[variable] = value


class ThreadWithReturnValue(Thread):
    """
    Run Thread With Return Value
    usage:
            def FindAll(a, b, c):
                return a(b, c)
            twrv = ThreadWithReturnValue(target=FindAll, args=(aeroot, scope, condition))
            twrv.start()
            elements = twrv.join(1)
    """

    log = logging.getLogger()

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

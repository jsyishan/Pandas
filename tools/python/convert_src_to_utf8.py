'''
此脚本用于将 src 目录中的源码文件都转换为 UTF-8-SIG 编码
'''

# -*- coding: utf-8 -*-

import codecs
import os
import platform

import chardet


class CharsetConverter():
    '''
    此操作类用于帮助对文本文件进行编码转换
    '''
    def __init__(self, options):
        self.__options__ = options

    def __detectCharset(self, filepath):
        '''
        给定一个文件路径, 获取该文本文件的编码
        '''
        with open(filepath, 'rb') as hfile:
            return chardet.detect(hfile.read())['encoding']

    def convertDirectory(self, directory, to_charset):
        '''
        给定一个目录和期望的目标文本编码
        将该目录中的所有文件都转换成指定的编码
        '''
        ignore_files = self.__options__['ignore_files']
        process_exts = self.__options__['process_exts']

        ignore_files = [x.lower() for x in ignore_files]
        process_exts = [x.lower() for x in process_exts]

        convert_cnt = 0

        for dirpath, _dirnames, filenames in os.walk(directory):
            for filename in filenames:
                _base_name, extension_name = os.path.splitext(filename.lower())

                if filename.lower() in ignore_files:
                    continue
                if extension_name not in process_exts:
                    continue

                fullpath = os.path.normpath('%s/%s' % (dirpath, filename))
                if self.convertFile(fullpath, to_charset, directory):
                    convert_cnt = convert_cnt + 1

        return convert_cnt

    def convertFile(self, filepath, to_charset, directory):
        '''
        给定一个文本文件, 将它转换成指定的编码并保存
        '''
        origin_charset = self.__detectCharset(filepath).upper()
        to_charset = to_charset.upper()

        if origin_charset == to_charset:
            return False

        try:
            absolutely_path = os.path.abspath(filepath)

            print('Convert {filename} ... From {origin_charset} to {to_charset}'.format(
                filename=os.path.relpath(absolutely_path, directory),
                origin_charset=origin_charset,
                to_charset=to_charset
            ))

            origin_file = codecs.open(filepath, 'r', origin_charset)
            content = origin_file.read()
            origin_file.close()

            target_file = codecs.open(filepath, 'w', to_charset)
            target_file.write(content)
            target_file.close()

            return True
        except IOError as err:
            print("I/O error: {0}".format(err))
            return False

def main():
    '''
    此脚本的主函数
    '''
    os.chdir(os.path.split(os.path.realpath(__file__))[0])

    print('=' * 70)
    print('Convert source code to UTF-8-SIG codepage.')
    print('=' * 70)

    print('')
    # ------------------------------------------------------------------
    count = CharsetConverter({
        'ignore_files' : ['Makefile', 'Makefile.in', 'CMakeLists.txt'],
        'process_exts' : ['.hpp', '.cpp']
    }).convertDirectory('../../src', 'UTF-8-SIG')

    if count <= 0:
        print('Great! All source code are using UTF-8-SIG.')
    # ------------------------------------------------------------------
    print('')

    print('=' * 70)

    if platform.system() == 'Windows':
        os.system('pause')

if __name__ == "__main__":
    main()


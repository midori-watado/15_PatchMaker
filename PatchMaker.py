# coding: utf-8
# python3.6

'''PatchMaker

パッチファイルを作成するツール。
想定してる流れとしては、
    1. gitで変更されたファイルを見る
    2. それを丸コピーして、下の targetpaths に貼る
    3. 実行する
    4. パッチファイルができる。

パッチフォルダはスクリプトと同階層に置かれます。
だからgit addとかするときパッチメイクの直後にやったりするとパッチフォルダも巻き込まれるから注意して。
型注釈を使っているからpython3.6未満では動かない気がする。

========================================
バージョン1.0(2017-04-04)
    完成。
'''

targetpaths = '''

project/html/html1.html
project/html/html2.html

'''
patchname_format = '{date}_patch'


import os
import sys
import pprint
import datetime
import shutil


class PatchMaker:
    def __init__(self):
        self.cd_()

    def cd_(self):
        '''カレントディレクトリを移す。'''
        if hasattr(sys, 'frozen'):
            os.chdir(os.path.dirname(sys.executable))
        else:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def run(self):
        '''トップレベルメソッド。'''
        pathlist = self.make_pathlist(targetpaths)
        no_exists_path = self.check_paths_exist(pathlist)
        if no_exists_path:
            self.output_error(1, no_exists_path)
            return
        self.output_result(self.create_patch(pathlist))

    def make_pathlist(self, targetpaths: str) -> list:
        '''冒頭でインプットした文字列を配列にする。'''
        pathlist = []
        for t in targetpaths.strip().split('\n'):
            if t:
                pathlist.append(t)
        return pathlist

    def check_paths_exist(self, pathlist: list) -> str:
        '''インプットしたパスが全部有効か確かめる。おかしいときはそのパスを返す。'''
        for path in pathlist:
            if not os.path.exists(path):
                return os.path.abspath(path)
        return ''

    def output_error(self, code: int, data: str) -> None:
        '''俺が定義したエラーの出力。'''
        if code in {1}:
            print(f'<ERROR{code}> No such file or directory: {data}')
        return

    def create_patch(self, pathlist: list) -> list:
        '''目的であるパッチの作成。'''
        patchfolder = patchname_format.replace(
            '{date}', datetime.datetime.today().strftime('%Y%m%d_%H%M%S'))
        os.mkdir(patchfolder)
        donelist = []
        for path in pathlist:
            if not os.path.exists(patchfolder + '/' + os.path.dirname(path)):
                os.makedirs(patchfolder + '/' + os.path.dirname(path))
            donelist.append(shutil.copy(path, patchfolder + '/' + path))
        return donelist

    def output_result(self, donelist):
        '''「終わったよー」の出力。'''
        print('<INFO>正常終了。')
        pprint.pprint(donelist)
        print('<INFO>以上 %s のパッチファイルを作成しました。' % (len(donelist),))


if __name__ == '__main__':
    pm = PatchMaker()
    pm.run()

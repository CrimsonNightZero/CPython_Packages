from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import os
import shutil


class Output:
    def __init__(self, py_path, pyx_path):
        self.note_statue = None
        self.py_path = py_path
        self.pyx_path = pyx_path

    def isnote(self, read):
        if '# -*- coding: utf-8 -*-' == read.strip('\n'):
            self.note_statue = "start"
        elif self.note_statue == "two":
            self.note_statue = None
        elif '"""' == read.strip('\n') and self.note_statue == "one":
            self.note_statue = "two"
        elif '"""' == read.strip('\n'):
            self.note_statue = "one"

        if self.note_statue is None:
            return False

        return True

    def split_file(self):
        istest = False
        pyx_text = ""
        test_text = ""
        note_text = ""
        pyx_import = dict()
        temp_import = 'from ' + self.pyx_path.split('.')[0] + ' import *\n'
        test_import = {temp_import: True}

        with open(self.pyx_path, 'r', encoding='utf8') as file:
            for read in file.readlines():
                if self.isnote(read):
                    note_text += read
                    continue

                if '__name__ == "__main__":' in read or "__name__ == '__main__':" in read:
                    istest = True
                    read = "\n\n" + read

                if istest:
                    test_text += read
                    test_import = self.check_import(read, test_import)
                elif "import" in read:
                    pyx_import[read] = False
                    test_import[read] = False

                else:
                    pyx_text += read
                    pyx_import = self.check_import(read, pyx_import)
        print(pyx_import)
        print(test_import)
        if istest:
            test_path = os.path.splitext(self.py_path)[0] + "_test.py"
            self.output_file(test_path, note_text, test_text, test_import)

        self.output_file(self.pyx_path, note_text, pyx_text, pyx_import)

    def check_import(self, read, file_import):
        for key, item in file_import.items():
            if not item:
                if 'as' in key:
                    if key.split('as')[1].strip('\n').strip('\s') in read:
                        file_import[key] = True
                else:
                    if key.split('import')[1].strip('\n').strip('\s') in read:
                        file_import[key] = True
        return file_import

    def output_file(self, path, note_text, file_text, file_import):
            with open(path, 'w', encoding='utf8') as file:
                file.write(note_text)
                file.write('\n')
                for key, item in file_import.items():
                    if item:
                        file.write(key)
                file.write(file_text)



if __name__ == '__main__':
    ext = list()
    for py_path in os.listdir():
        if "test" in py_path or "setup" in py_path:
            continue
        elif ".py" == os.path.splitext(py_path)[1]:
            pyx_path = py_path.replace("py", "pyx")
            shutil.copyfile(py_path, pyx_path)
            output = Output(py_path, pyx_path)
            output.split_file()
            ext.append(Extension(os.path.splitext(py_path)[0], [pyx_path]))

    # ext_modules = cythonize(ext, build_dir="build")

    setup(
        name='data_move',
        cmdclass={'build_ext': build_ext},
        ext_modules=cythonize(ext, build_dir="build")
    )

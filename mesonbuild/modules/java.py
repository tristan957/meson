# Copyright 2021 The Meson development team

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pathlib
import typing as T
from mesonbuild.build import CustomTarget
from mesonbuild.interpreterbase.decorators import FeatureNew, KwargInfo, typed_pos_args, typed_kwargs
from mesonbuild.interpreter.interpreterobjects import FileHolder
from . import ExtensionModule, ModuleReturnValue, ModuleState
from ..interpreter import Interpreter

class JavaModule(ExtensionModule):
    @FeatureNew('Java Module', '0.59.0')
    def __init__(self, interpreter: Interpreter):
        super().__init__(interpreter)
        self.methods.update({
            'generate_native_header': self.generate_native_header,
        })

    @typed_pos_args('generate_native_header', (str, FileHolder))
    @typed_kwargs('java.generate_native_header', KwargInfo('package', str, default=None))
    def generate_native_header(self, state: ModuleState, args: T.Tuple[T.Union[str, FileHolder]],
            kwargs: T.Dict[str, T.Optional[str]]) -> ModuleReturnValue:
        javac = state.find_program("javac")
        package = kwargs.get('package')

        file = self.interpreter.source_strings_to_files([a.held_object if isinstance(a, FileHolder) else a for a in args])[0]

        if package:
            header = f'{package.replace(".", "_")}_{pathlib.Path(file.fname).stem}.h'
        else:
            header = f'{pathlib.Path(file.fname).stem}.h'

        ct_kwargs = {
            'input': file,
            'output': header,
            'command': [
                *javac.get_command(),
                '-d',
                '@PRIVATE_DIR@',
                '-h',
                state.subdir,
                '@INPUT@',
            ]
        }

        target = CustomTarget(os.path.basename(header), state.subdir, state.subproject, backend=state.backend, kwargs=ct_kwargs)

        return ModuleReturnValue(target, [target])

def initialize(*args: T.Any, **kwargs: T.Any):
    return JavaModule(*args, **kwargs)

project('cmakeSubTest_advanced', ['c', 'cpp'])

dep_test = dependency('ZLIB', method: 'cmake', required: false)
if not dep_test.found()
  error('MESON_SKIP_TEST: zlib is not installed')
endif

cm = import('cmake')

# Test the "normal" subproject call
sub_pro = cm.subproject('cmMod')
sub_dep = sub_pro.dependency('cmModLib')
sub_sta = sub_pro.dependency('cmModLibStatic')

# Build some files
exe1 = executable('main1', ['main.cpp'], dependencies: [sub_dep])
exe2 = executable('main2', ['main.cpp'], dependencies: [sub_sta])
slib = shared_library('slib', ['slib.cpp'], dependencies: [sub_dep])
exe3 = executable('main3', ['main3.cpp'], link_with: slib)
test('test1', exe1)
test('test2', exe2)

# Test if we can also extract executables
assert(sub_pro.target_type('testEXE') == 'executable', 'The type must be executable for obvious reasons')
test('test3', sub_pro.target('testEXE'))

# Test that we can add a new target with the same name as the CMake subproject
exe4 = executable('testEXE', ['main.cpp'], dependencies: [sub_sta])
test('test4', exe4)

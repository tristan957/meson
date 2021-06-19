## Java Module

The Java module has been added to Meson. The Java module allows users to
generate native header files without needing to use a `custom_target()`.

```meson
jmod = import('java')
native_header = jmod.generate_native_header('File.java', package: 'com.mesonbuild')
```

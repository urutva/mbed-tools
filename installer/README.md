Spec build

System generates a file called mbed_tools.spec that can be reused by things like CI:

```pyinstaller <options> mbed_tools.spec```
    
This can then be made into a disk image using dmgbuild

## Creating an installer package
productbuild --component ~/HelloWorld.app /Applications/ ~/HelloWorld.pkg

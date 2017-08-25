# PSCalib
A set of pythonic methods for data processing with back-end implementation in C++ and cython interface.

## Documentation
- Sphinx generated documentation: https://lcls-psana.github.io/PSCalib/
<!--- - GitHub Pages: https://github.com/lcls-psana/PSCalib/wiki --->

## Quick start
### Create conda release
See for detail Psana Developer Documentation [3] 
```
cd <my-conda-release>
source conda_setup
```

### Clone package
**on pslogin:**
```
git clone https://github.com/lcls-psana/PSCalib.git
# or 
condarel --addpkg --name PSCalib --tag HEAD
```
### Build 
```
scons
```
Then run your application(s)

## References
- [1] https://lcls-psana.github.io/PSCalib/
- [2] https://github.com/lcls-psana/PSCalib/wiki
- [3] https://confluence.slac.stanford.edu/display/PSDMInternal/Psana+Developer+Documentation
- [4] https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
- [5] https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst
NPM Info
========

Sublime Text plugin for displaying information about modules included through require() in node.js files. Placing your cursor on a line that contains a require() will show a menu to quickly link to the package.json file, open the modules repo in a browser, or list properties and methods. It also displays version and module description in the status bar and menu panel.

How to use
========

Place your cursor on lines like this for 1.5 seconds (for this version, modules must exist in node_modules folder):
```javascript
var thingy = require("thingy");
```

For example:
![](https://raw.github.com/dsteinbach/npm-info/screenshots/thingy.jpg)


Also, version and description appears in status bar:
```
thingy@0.0.1 - Thingy does things better than no other npm does so well
```

**Note:** Version and description for native node.js modules won't display as they have no associated package.json file.

Installation
========
Installation via Package Control coming soon but for now you can download this repo zipped and unpack to:
```
OSX:
~/Library/Application Support/Sublime Text 2/Packages
```
```
Windows:
%APPDATA%\Sublime Text 2\Packages
```

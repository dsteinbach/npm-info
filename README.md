NPM Info
========

Sublime Text plugin for displaying information about modules included through require() in node.js files. Placing your cursor between the quotes of a require function will display a panel with a link to the package.json file, link to the module's repo in a browser, and a list properties and methods. It also displays version and module description in the status bar.

How to use
========

Place your cursor between the quotes of a require method and wait for 1.5 seconds (configurable):
```javascript
var thingy = require("thingy");
```

For example:
![](https://raw.github.com/dsteinbach/npm-info/screenshots/thingy.jpg)


Also, version and description appears in status bar:
```
lodash@2.4.1 - A utility library delivering consistency, customization, performance, & extras.
```

**Note:** Information for native node.js modules and non-modules requires won't display as they have no associated package.json file.

Installation
========
Installation via Package Control coming soon but for now you can download this repo zipped and unpack to:
```
OSX:
~/Library/Application Support/Sublime Text 2/Packages/NPMInfo
```
```
Windows:
%APPDATA%\Sublime Text 2\Packages\NPMInfo
```

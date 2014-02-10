NPM Info
========

Sublime Text plugin for displaying version and description of node.js NPMs in the status bar of opened javascript files.

How to use
========
```javascript
var thingy = require("thingy");
```
Place your cursor on any line containing a 'require' method (see above) in a node.js file and the version and description of the NPM will display in status bar of the Sublime Text window.

Open the Sublime Text console (Ctrl+`) to see the entire package.json file for the NPM logged.

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

/*
    Copyrights for code authored by Yahoo! Inc. is licensed under the following terms:
    MIT License
    Copyright (c) 2014 Yahoo! Inc. 
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

var fs = require('fs'),
    pkgLoc = process.argv[2],
    isWin = /^win/.test(process.platform),
    slash = isWin ? '\\' : '/',
    pkgFolder = getFolder(pkgLoc);

function getFolder(pkgLoc) {
    return pkgLoc.substr(0, pkgLoc.lastIndexOf(slash));
}

function getMethodsAndPropsStr(obj) {
    var i,
        res = '',
        type;

    for (i in obj) {
        if (obj.hasOwnProperty(i)) {
            type = typeof obj[i] === 'function' ? '()' : ''
            res += i + type + "\n";
        }
    }
    return res;
}

fs.readFile(pkgLoc, 'utf8', function (err, data) {
    var p,
        resp = {},
        n,
        npmFn = "index.js";

    if (err) {
        return;
    }

    try {
        p = JSON.parse(data);

        if (p && p.main) {
            npmFn = p.main;
        }
        n = require(pkgFolder + slash + npmFn);
    } catch (e) {
        n = null;
    }

    if (n) {
        console.log(getMethodsAndPropsStr(n));
    }

});

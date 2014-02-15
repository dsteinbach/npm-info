/*
 * Copyright (c) 2014, Yahoo! Inc. All rights reserved.
 * Copyrights licensed under the New BSD License.
 * See the accompanying LICENSE file for terms.
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

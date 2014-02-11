var fs = require('fs'),
    pkgLoc = process.argv[2],
    pkgFolder = getFolder(pkgLoc);

function getFolder(pkgLoc) {
    return pkgLoc.substr(0, pkgLoc.lastIndexOf('/'));
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
        n = require(pkgFolder + '/' + npmFn);
    } catch (e) {
        n = null;
    }

    if (n) {
        console.log(getMethodsAndPropsStr(n));
    }

});
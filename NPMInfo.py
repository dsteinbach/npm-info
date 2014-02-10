import sublime, sublime_plugin, re, json, os

class NPMInfoEvents(sublime_plugin.EventListener):

    def __init__(self):
        self.packagePaths = {}
        self.settings = sublime.load_settings('NPMInfo.sublime-settings')
        self.busy = False

    def on_load(self, view):
        fn = view.file_name()
        if fn in self.packagePaths:
            del self.packagePaths[fn]

    def on_selection_modified(self, view):

        if self.busy == True:
            return

        self.busy = True
        sublime.set_timeout(lambda: self.doCheck(view), 500)


    def doCheck(self, view):

        if view.is_scratch() or (view.file_name() and view.file_name().endswith('.js') == False):
            return

        view.set_status('NPMInfo', '')

        reg = view.sel()[0]
        if reg.empty():
            line = view.line(reg)
            line_contents = view.substr(line)
            matchObj = re.match(r'(.*)require\(([\"\']+)([a-zA-Z0-9\_\-]*)([\"\']+)\)(.*)', line_contents)
            if matchObj:
                npm = matchObj.group(3)
                o = self.getInfo(npm, view.file_name())

                if 'version' in o:
                    if 'description' in o:
                        desc = o['description']
                    else:
                        desc = "No description found"
                    view.set_status('NPMInfo', npm + "@" + o['version'] + " - " + desc)
                else:
                    view.set_status('NPMInfo', 'No package.json found for "' + npm + '"')

        self.busy = False

    def getJson(self, pkgPath):
        with open(pkgPath) as json_data:
            d = json.load(json_data)
            # print package info to console
            if self.settings.get('printPackageJson'):
                print json.dumps(d, indent=4, sort_keys=True)
            json_data.close()
            return d

    def getInfo(self, npm, dir):
        # cmd = ['/usr/local/bin/node', 'npm-info', npm, fileloc]
        # output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        # jsonOutput = json.loads(output)
        pkgPath = self.getPackagePath(npm, dir)

        if dir not in self.packagePaths:
            self.packagePaths[dir] = {}

        if pkgPath == False:
            return {}
        elif npm in self.packagePaths[dir]:
            return self.getJson(self.packagePaths[dir][npm])
        else:
            self.packagePaths[dir][npm] = pkgPath
            return self.getJson(pkgPath)

    def getPackagePath(self, npm, dir):
        dir = os.path.dirname(dir)

        if len(dir) <= 1:
            return False

        fn = dir + '/node_modules/' + npm + '/package.json'

        if os.path.exists(fn):
            # get info
            return fn
        else:
            # move up dir, and call again
            return self.getPackagePath(npm, dir)

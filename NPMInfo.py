import sublime, sublime_plugin, re, json, os, webbrowser, subprocess

class NPMInfoEvents(sublime_plugin.EventListener):

    def __init__(self):
        self.packagePaths = {}
        self.settings = sublime.load_settings('NPMInfo.sublime-settings')
        self.busy = False
        self.showQuickPanelDelay = self.settings.get('showQuickPanelDelay')
        if isinstance(self.showQuickPanelDelay, (int, long, float, complex)) == False:
            self.showQuickPanelDelay = 500

    def on_load(self, view):
        fn = view.file_name()
        if fn in self.packagePaths:
            del self.packagePaths[fn]

        self.view = view

    def on_selection_modified(self, view):
        if self.busy == True:
            return

        self.busy = True
        sublime.set_timeout(lambda: self.doCheck(view), self.showQuickPanelDelay)

    def doCheck(self, view):
        if view.is_scratch() or (view.file_name() and view.file_name().endswith('.js') == False):
            self.busy = False
            return

        view.set_status('NPMInfo', '')
        self.view = view

        reg = view.sel()[0]
        if reg.empty():
            line = view.line(reg)
            line_contents = view.substr(line)
            matchObj = re.match(r'.*require\(([\"\']+)([a-zA-Z0-9\_\-]*)([\"\']+)\).*', line_contents)
            if matchObj:
                npm = matchObj.group(2)
                qt = matchObj.group(1)
                npmStart = (line_contents.find("require(" + qt + npm + qt + ")") + 9)
                npmEnd = npmStart + len(npm) + 1
                col = view.rowcol(reg.b)[1]
                if col >= npmEnd or col < npmStart:
                    self.busy = False
                    return

                dir = view.file_name()
                pkgPath = self.getPackagePath(npm, dir)
                o = self.getInfo(npm, dir, pkgPath)
                self.pkgPath = pkgPath
                self.pkgJson = o
                self.npm = npm

                if 'version' in o:
                    if 'description' in o:
                        desc = o['description']
                    else:
                        desc = "No description found"
                    view.set_status('NPMInfo', npm + "@" + o['version'] + " - " + desc)

                    self.quickPanelOptions = [npm + " v" + o['version'], 'List properties and methods', 'Open package.json']
                    if 'repository' in o and 'url' in o['repository']:
                        self.quickPanelOptions += ['Open repo in browser']

                    if self.settings.get('showQuickPanel'):
                        view.window().show_quick_panel(self.quickPanelOptions, self.quickPanelSelect)

                else:
                    view.set_status('NPMInfo', 'No package.json found for "' + npm + '"')

        self.busy = False

    def quickPanelSelect(self, index):
        if index == 0:
            self.showPackageDesc()

        if index == 1:
            self.listPropsAndMethods()

        if index == 2:
            self.view.window().open_file(self.pkgPath)

        if index == 3 and len(self.quickPanelOptions) == 4:
            webbrowser.open(self.pkgJson['repository']['url'], new=2, autoraise=True)

    def showPackageDesc(self):
        if 'description' in self.pkgJson:
            sublime.message_dialog(self.pkgJson['description'])

    def listPropsAndMethods(self):
        res = []
        if sublime.platform() == 'windows':
            app = 'node'
            cmd = [app, 'npm-info', self.pkgPath]
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=startupinfo)
        else:
            pathToJS = sublime.packages_path() + '/NPMInfo/npm-info.js'
            cmd = ['/usr/local/bin/node', pathToJS, self.pkgPath]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in iter(p.stdout.readline, b''):
            lineStrip = line.rstrip()
            # ignore console logs outputted when requiring module
            if len(lineStrip) > 0 and ' ' not in lineStrip:
                res.append(lineStrip)

        self.view.window().show_quick_panel(res, self.onSelectPropAndMethod)

    def onSelectPropAndMethod(self, index):
        pass

    def getJson(self, pkgPath):
        with open(pkgPath) as json_data:
            d = json.load(json_data)
            json_data.close()
            return d

    def getInfo(self, npm, dir, pkgPath):
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

        if len(dir) <= 3:
            return False

        fn = dir + '/node_modules/' + npm + '/package.json'

        if os.path.exists(fn):
            # get info
            return fn
        else:
            # move up dir, and call again
            return self.getPackagePath(npm, dir)



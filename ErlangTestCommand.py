import sublime, sublime_plugin, subprocess, os

class ErlangTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if ".erl" not in self.view.file_name():
            print("No erl file skipping")
            return

        project_path=self.view.window().folders()[0]
        file_name=self.view.file_name()
        apps=self.get_app_name(file_name)
        module_name=self.get_module_name(file_name)
        (rebar, pwd)=self.get_rebar(file_name)
        tests=""
        for region in self.view.sel():
            if not region.empty():
                print(self.view.substr(region))
                tests=" tests=" + self.view.substr(region)

        print(self.view.window().project_file_name())
        # cmd = [rebar, "eunit", apps, module_name, tests, "-v", "skip_deps=true"]
        ## self.exec_cmd(cmd, pwd)
        cmd = "rebar.cmd eunit skip_deps=true -v {0} {1} {2}".format(apps, module_name, tests)
        print(cmd)
        self.view.window().run_command("exec", {
            "cmd": cmd,
            "shell": True,
            "encoding": "cp850",
            "working_dir": project_path,
            "file_regex": "([^ ]*\.erl):?(\d*)"
            })

    def get_app_name(self, file_name ):
        ret = file_name.split('apps\\')
        if len(ret) > 1:
            return "apps=" + ret[1].split('\\')[0]
        else:
            return ""

    def get_module_name(self, file_name):
        st=file_name.split('\\')
        st.reverse()
        return "suites=" + st[0].replace('.erl','')

    def get_rebar(self, file_name):
        filedir = os.path.dirname(file_name)
        path = filedir + "/../rebar.cmd"
        if os.path.isfile(path):
            return (path, os.path.dirname(path))

        path = filedir + "/../../../rebar.cmd"
        if os.path.isfile(path):
            return (path, os.path.dirname(path))        

    def exec_cmd(self, cmd, pwd):
        print(cmd)
        p = subprocess.Popen(cmd, cwd=pwd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        (out, stderr) = p.communicate()
        print(out, stderr)
        return out
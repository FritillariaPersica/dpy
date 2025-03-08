#!/usr/bin/env python3
# 2025 / 6 / 3

import os
import argparse

# Working directories
userunits = f"/home/{os.getlogin()}/.config/systemd/user/"
systemunits = "/etc/systemd/system/" # Going to be used in the future

try :
    os.listdir(userunits)
except FileNotFoundError : 
    os.makedirs(userunits, exist_ok=True)

# Main "Services" class
class Services:
    _instance = None # Used to know how many times we have instantiated this class 

    def __new__(cls, *args):
        if cls._instance is not None:
            raise Exception("This class can only be instantiated once")
        cls._instance = super().__new__(cls)
        return cls._instance
                      
    def __init__(self, name, Description="Test app", ExecStart='', root_level=False): # Root level services are to be added in the future
        if root_level :
            self.working_dir = systemunits
        else :
            self.working_dir = userunits
        self.Name = name
        self.variables = {"[Unit]" : {"Description=" : Description ,"StartLimitIntervalSec=": "0"}, "[Service]" : {"Restart=" : "on-failure" , "StandardOutput=" : "journal" , "StandardError=" : "journal" , "User=": os.getlogin() ,"ExecStart=": ExecStart} ,"[Install]" :{"WantedBy=" : "multi-user.target"}}

    def reset(self,*args):
        self.__init__(*args) # Re-calls init with new args

    def modify(self,branch, keyname, value):
        try:
            self.variables[f"[{branch}]"][f"{keyname}="] = value
            return True
        except:
            return False

    def apply(self):
        service = ""
        for i in self.variables.keys():
            service += f"{i}\n"
            for x in self.variables[i].keys():
                service += f"{x} {self.variables[i][x]}\n"
        try:
            with open(f"{self.working_dir}{self.Name}.service",'w') as f:
                f.write(service)
                f.close()
                return True
        except:
            return False

    def addup(self, branch, keyname, value):
        try:
            self.variables[f"[{branch}]"][f"{keyname}="] = value
            return True
        except:
            return False
    
    def run(self, Enable):
        if Enable :
            os.popen(f"systemctl --user start {self.Name}.service && systemctl --user enable {self.Name}.service")
        else:
            os.popen(f"systemctl --user stop {self.Name}.service")

    def stop(self, Disable=False):
        if Disable :
            os.popen(f"systemctl --user stop {self.Name}.service && systemctl --user disable {self.Name}.service")
        else:
            os.popen(f"systemctl --user stop {self.Name}.service")
        return True
    
    def check_if(self):
        if os.path.isfile(f"{self.working_dir}{self.Name}.service") or os.path.isfile(f"{systemunits}{self.Name}.service"):
            return True
        else:
            return False

    def remove(self,root_level=False):
        if root_level :
            os.remove(f"{systemunits}{self.Name}.service")
            return True
        else:
            os.remove(f"{userunits}{self.Name}.service")
            return True

    def in_use(self,thename): # Only use it to change the name of the currently used service
        self.Name = thename

    def get(self):
        return self.variables

    def __str__(self):
        service = ""
        for i in self.variables.keys():
            service += f"{i}\n"
            for x in self.variables[i].keys():
                service += f"{x} {self.variables[i][x]}\n"
        return service

    def __len__(self):
        return len(self.variables)


def main():
    Parser = argparse.ArgumentParser(description="dpy CLI")
    Parser.add_argument("--name", type=str, default="TestService", help="Your age")
    Parser.add_argument("--description", type=str, default="Test service", help="Description of the service")
    Parser.add_argument("--exec", type=str, default="", help="Command to execute")
    Parser.add_argument("--run", action="store_true", help="Will Start&Enable the service as well")
    args = Parser.parse_args()
    service = Services(args.name, args.description, args.exec)
    if service.apply() : print(f"<*> Made basic service configurations at /home/{os.getlogin()}/.config/systemd/user/")
    if args.run:
        service.run(Enable=True)
        print(r"<*> Service is started and enabled as well")


if __name__ == "__main__":
    main()

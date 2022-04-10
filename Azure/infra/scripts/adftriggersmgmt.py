import os
import subprocess
import sys
import json

def exec_cmd(cmd):
    try:
        resp = subprocess.check_output(cmd)
        if resp:
            ret_json = json.loads(resp)
            return ret_json
        else:
            return ''
    except subprocess.CalledProcessError as subprocerror:
        print("Error code",subprocerror.returncode,subprocerror.output)

def get_triggers_list(resource_group, factory_name):
    cmd_list = ['az','datafactory','trigger','list','--factory-name',factory_name, '--resource-group',resource_group,'--output=json']
    return exec_cmd(cmd_list)

def stop_triggers(resource_group, factory_name,trg_name):
    cmd_list = ['az','datafactory','trigger','stop','--factory-name',factory_name, '--resource-group',resource_group, '--name', trg_name, '--output=json']
    return exec_cmd(cmd_list)

def start_triggers(resource_group, factory_name,trg_name):
    cmd_list = ['az','datafactory','trigger','start','--factory-name',factory_name, '--resource-group',resource_group, '--name', trg_name, '--output=json']
    return exec_cmd(cmd_list)

def run():
    print("Run starts")
    resp = get_triggers_list(rg_name,adf_name)
    started_triggers = []
    started_triggers_from_file = []
    tmp_out_file_name = "tmp_latest_started_trgs_adf_"+adf_name+"_"+rg_name+".json"

    if trg_action == "stop":
        for ti in resp:
            if "Started" == (ti.get("properties").get("runtimeState")):
                print(ti.get("name"))
                started_triggers.append(ti.get("name"))
                print(ti.get("properties").get("runtimeState"))
                print("******************************************")
        print("Triggers in started state ",started_triggers)
        with open(tmp_out_file_name,"w") as trg_outfile:
            json.dump(started_triggers,trg_outfile)
        for trg in started_triggers:
            print("Stopping trigger: ", trg)
            try:
                stop_triggers(rg_name,adf_name,trg)
                print('Trigger stopped successfully: ',trg)
            except Exception as e:
                print('Error occurred at Trigger stop: ',trg)

    if trg_action == "start":
        with open(tmp_out_file_name,"r") as trg_infile:
            started_triggers_from_file = json.load(trg_infile)
            print("Triggers with prior started state from the file",started_triggers_from_file)
            for trg in started_triggers_from_file:
                try:
                    start_triggers(rg_name,adf_name,trg)
                    print('Trigger started successfully: ',trg)
                except Exception as e:
                    print('Error occurred at Trigger start: ',trg)



#Main Function..
if __name__ == '__main__':
    rg_name = sys.argv[1]
    adf_name = sys.argv[2]
    trg_action = sys.argv[3]

    #usr/bin/python3 /usr/local/share/workspace/ws_proj/proj_name/Devops/scripts/manage_adf_triggers.py RG_NAME ADF_NAME start/stop
    #QA: /usr/bin/python3 /usr/local/share/workspace/ws_proj/proj_name/Devops/scripts/manage_adf_triggers.py RG_NAME ADF_NAME stop
    #QA2: /usr/bin/python3 /usr/local/share/workspace/ws_proj/proj_name/Devops/scripts/manage_adf_triggers.py RG_NAME ADF_NAME stop
    assert trg_action in ["start","stop"], " Trigger action should be either start or stop only"
    print(f"""Given Input Params: Resource Group Name: {rg_name}, ADF Name: {adf_name}, Trigger Action: {trg_action} """)
    run()

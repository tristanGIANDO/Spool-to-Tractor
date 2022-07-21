import sys, os
import tractor.api.author as author
import tractor.api.query as tq
import maya.cmds as cmds

#Connect to Tractor
ids = {"user": "root",
                "password": ""}
tq.setEngineClientParam(user=ids["user"], password=ids["password"])


#QUERY SCENE NAME and remove extension to define job title
workspace,sceneName = os.path.split(cmds.file(query=True, sceneName=True))
workspace = os.path.join(workspace.split("maya")[0], "maya")

#ATTRIBUTES
job = author.Job()
job.title = str(sceneName)
job.priority = 100
job.service = "PixarRender"
#task = job.newTask(title="Render spool_RIB.ma", argv=["/usr/bin/prman", "//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/renderman/rib/spool_RIB/v001_t01/perspShape.0001.rib"])
#prman -Progress -t:0 -cwd %//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/renderman/rib/spool_RIB/v001_t01/perspShape.0001.rib)
#COMMANDS
#task.addCommand(command)
#command = task.newCommand(argv=["/usr/bin/prman", "//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/renderman/rib/spool_RIB/v001_t01/perspShape.0001.rib"], service="pixarRender")

job.newDirMap(src="Z:/", dst="//myserver/", zone="UNC")

task = job.newTask(title="Pre-Render TxMake Tasks")
task.serialsubtasks = 0

copyin = author.Command(argv=["scp", "remote://gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/renderman/rib/spool_RIB/v001_t01/perspShape.0001.rib", "//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/renderman/rib/spool_RIB/v001_t01/perspShape.0001.rib"])
task.addCommand(copyin)
render = author.Command(argv=["/usr/bin/prman", "/local/file.rib"])
task.addCommand(render)
copyout = author.Command(argv=["scp", "/local/file.tif", "remote:/path/file.tif"])
task.addCommand(copyout)
task = author.Task(title="multi-command task", service="PixarRender")
task.newCommand(argv=["scp", "remote:/path/file.rib", "/local/file.rib"])
task.newCommand(argv=["/usr/bin/prman", "/local/file.rib"])
task.newCommand(argv=["scp", "/local/file.tif", "remote:/path/file.tif"])

#SPOOL
job.spool(owner="k.reeves")

#deco tractor
tq.closeEngineClient()


print ("okay")

'''
Job -title {spool_RIB.ma} -projects {{instinct}} -priority {5.0} -service {PixarRender} -envkey {{rfm-24.3} {maya-2022}} -cleanup {
  RemoteCmd {{TractorBuiltIn} {File} {delete} {%D(//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN//scenes/_spool_RIB_pid18496_1658333933.alf)}}
} -dirmaps {
  {{/myserver/} {Z:/} UNC}
} -serialsubtasks 1 -subtasks {
  Task {Pre-Render TxMake Tasks} -serialsubtasks 0
  Task {Render spool_RIB.ma} -subtasks {
    Task {Render spool_RIB.ma Frame: 1 Layer: defaultRenderLayer Camera: perspShape} -serialsubtasks 1 -subtasks {
      Task {Render spool_RIB.ma Frame: 1 Layer: defaultRenderLayer Camera: perspShape (render)} -cmds {
        RemoteCmd {{prman} {-Progress} {-t:0} {-cwd} {%D(//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/)} {%D(//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/renderman/rib/spool_RIB/v001_t01/perspShape.0001.rib)}} -service {PixarRender}
      } -preview {{sho} {//gandalf/3d4_21_22/instinct/02_ressource/@TRISTAN/images/spool_RIB_v001_t01/spool_RIB__perspShape_beauty.0001.exr}}
    }
  }
}
'''





from roboflow import Roboflow
rf = Roboflow(api_key="HeBD4WDnlMGw1gNYeyM3")
project = rf.workspace("bismillah-4byr6").project("capstone-project-snjic")
version = project.version(1)
dataset = version.download("folder")

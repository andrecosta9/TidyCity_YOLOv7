from roboflow import Roboflow
#rf = Roboflow(api_key="ErF6qJjtrqfi7PykcPpj")
#project = rf.workspace("conedetection").project("tidycity-iorn6")
#dataset = project.version(1).download("yolov7")

rf = Roboflow(api_key="ErF6qJjtrqfi7PykcPpj")
project = rf.workspace("alpr-yrtzl").project("alpr_new")
dataset = project.version(1).download("yolov7")


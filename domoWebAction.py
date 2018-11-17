#=============================================================
#
#=============================================================
import domoWebModule

class domoWebAction(domoWebModule.domoWebModule) :
    nbDomoWebActions = 0
    def __init__(self, name=""):
        if (name == "") :
            name="domoWebAction-"+str(domoWebAction.nbDomoWebActions)
        domoWebModule.domoWebModule.__init__(self, name)
        
        self.addAttribute("object", None)
        self.addAttribute("attribute", None)
        self.addAttribute("value", None)
        domoWebAction.nbDomoWebActions = domoWebAction.nbDomoWebActions + 1
            
    def run(self) :
       print "Running action '"+self.name+"' ..."
       #print "  -> "+self.getAttribute("object").name+"."+self.getAttribute("attribute")+" <- "+self.getAttribute("value")
       obj = self.getAttribute("object")
       if (obj is None ):
           return
       obj.setAttribute(self.getAttribute("attribute"), self.getAttribute("value"))

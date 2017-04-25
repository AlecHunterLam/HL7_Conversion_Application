from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
# from .models import Home
from django.core.urlresolvers import reverse
from django.views import generic
import math


#CONVERSTION ALGORITHMS HL7 TO DICTIONARIES
import json
from hl7apy.parser import parse_message



def hl7_message_to_dict(m, use_long_name=True):
    """Convert an HL7 message to a dictionary
    :param m: The HL7 message as returned by :func:`hl7apy.parser.parse_message`
    :param use_long_name: Whether or not to user the long names
                          (e.g. "patient_name" instead of "pid_5")
    :returns: A dictionary representation of the HL7 message
    """
    if m.children:
        d = {}
        for c in m.children:
            name = c.name.lower()
            if use_long_name:
                name = c.long_name.lower() if c.long_name else name
            dictified = hl7_message_to_dict(c, use_long_name=use_long_name)
            if name in d:
                if not isinstance(d[name], list):
                    d[name] = [d[name]]
                d[name].append(dictified)
            else:
                d[name] = dictified
        return d
    else:
        return m.to_er7() 

def hl7_str_to_dict(s, use_long_name=True):
    """Convert an HL7 string to a dictionary
    :param s: The input HL7 string
    :param use_long_name: Whether or not to user the long names
                          (e.g. "patient_name" instead of "pid_5")
    :returns: A dictionary representation of the HL7 message
    """
    s = s.replace("\n", "\r")
    m = parse_message(s)
    return hl7_message_to_dict(m, use_long_name=use_long_name)


#Convert Dictionary to JSON#####################################################

################################################################################

# Create your views here.
class home(generic.View):
    def get(self,request):
        return render(request, 'HIT_Term_Project/home.html')
    def post(self,request):
        hl7_data = ""
        if "hl7_data" in request.POST:
            hl7_data = request.POST["hl7_data"]
            if hl7_data == "":
                return render(request,"HIT_Term_Project/home.html", {"message":"Empty Field"})
            # PARSE HL7 DATA
            hl7_data = str(hl7_data)
            dictionary_data = hl7_str_to_dict(hl7_data)
            json_data = json.dumps(dictionary_data)
            return render(request,"HIT_Term_Project/home.html", {"hl7_data":hl7_data})
        else:
            return render(request,"HIT_Term_Project/home.html", {"message":"Empty Field"})










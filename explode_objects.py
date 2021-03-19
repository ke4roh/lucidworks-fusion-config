#!/usr/bin/env python3
'''
Ths script takes an unzipped archive from Lucidworks application export
and splits the objects into separate folders one for each so that 
changes can be tracked between specific objects.

Run this from the export directory including objects.json.

It creates "index.json" which retains the structure of the objects
for reconstitution.
'''

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os
import sys
from urllib.parse import quote

def key_to_path(typ,key):
    uk=quote(str(key),safe='')
    return os.path.join("exploded_objects",typ,uk + ".json")

class FusionObject:
    def __init__(self,fusion_type):
        self.fusion_type=fusion_type

    def ids(self,elems):
        return list(self.items(elems).keys())
    def items(self,elems):
        return { elem["id"]: elem for elem in elems }
    def fusion_type(self):
        return self.fusion_type

    def explode(self,elems):
        items = self.items(elems)

        os.makedirs(os.path.join("exploded_objects",self.fusion_type), mode=0o775, exist_ok=True)

        for k,v in items.items():
            with open(key_to_path(self.fusion_type,k),"w") as f:
                json.dump(v,f,indent='  ')

    def type_structure(self):
        return list()

    def append(self,structure,idee,item):
        structure.append(item)

    def reconstitute(self,ids):
        typestructure=self.type_structure()
        for idee in ids:
            with open(key_to_path(self.fusion_type,idee),"r") as f:
                self.append(typestructure,idee,json.load(f))
        return typestructure

class NonstandardFusionObject(FusionObject):
    def __init__(self):
        super().__init__(self.__class__.__name__.lower())

class Features(NonstandardFusionObject):
    def items(self,elems):
        return dict(elems)
    def type_structure(self):
        return dict()
    def append(self,structure,idee,item):
        structure[idee]=item

class Links(NonstandardFusionObject):
    def ids(self,elems):
        return []
    def items(self,elems):
        return { "links":elems }

    def reconstitute(self,ids):
        with open(key_to_path(self.fusion_type,"links"),"r") as f:
            return json.load(f)

class Jobs(NonstandardFusionObject):
    def items(self,elems):
        return { elem["resource"]: elem for elem in elems }

objHandlers={ t.fusion_type:t for t in [ Features(), Links(), Jobs()] }

def explode():
    # track the original structure in "index"
    
    # read the file into "objects"
    with open("objects.json","r") as f:
        objects=json.load(f)
    
    # Objects consists of 2 keys, "objects" and "metadata"
    index = {"objects":dict(),"metadata":objects["metadata"]}

    for typ,elems in objects["objects"].items():
        handler = objHandlers.get(typ,None) or FusionObject(typ)
        handler.explode(elems)
        index["objects"][typ] = handler.ids(elems)
        
    with open("index.json","w") as f:
        json.dump(index,f,indent="  ")

def reconstitute():
    with open("index.json","r") as f:
        index = json.load(f)

    objects={"objects":dict(),"metadata":index["metadata"]}

    for typ,ids in index["objects"].items():
        handler = objHandlers.get(typ,None) or FusionObject(typ)
        objects["objects"][typ]=handler.reconstitute(ids)

    with open("objects.json","w") as f:
        json.dump(objects,f,indent="  ")

if "recon" in sys.argv[0]:
    reconstitute()
else: 
    explode()

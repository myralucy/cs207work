# your code here
import itertools, numbers
import os
from collections import defaultdict
import reprlib

def lc_reader(filename):
    listoflist_of_values = []
    with open(filename) as fp:
        n_line = 0
        for line in fp:
            if n_line == 0: 
                facet_names = line.strip("#").split() 
            elif n_line == 1:
                facet_values = line.strip("#").split()
            elif line.find('#')!=0:
                listoflist_of_values.append([float(f) for f in line.strip().split()])
            n_line += 1
    dict_of_facets = dict(zip(facet_names, facet_values))
    return listoflist_of_values, dict_of_facets

class LightCurve:
    
    def __init__(self, data, metadict):
        self._time = [x[0] for x in data]
        self._amplitude = [x[1] for x in data]
        self._error = [x[2] for x in data]
        self.metadata = metadict
        self.filename = None
        
        self.timeseries = zip(self._time, self._amplitude)
    
    @classmethod
    def from_file(cls, filename):
        lclist, metadict = lc_reader(filename)
        instance = cls(lclist, metadict)
        instance.filename = filename
        return instance
    
    def __repr__(self):
        class_name = type(self).__name__
        components = reprlib.repr(list(itertools.islice(self.timeseries,0,10)))
        components = components[components.find('['):]
        return '{}({})'.format(class_name, components)   
    
    def __len__(self):
        return len(self._time)
    
    def __getitem__(self, index):
        return (self._time[index], self._amplitude[index])
    
class LightCurveDB:
    
    def __init__(self):
        self._collection={}
        self._field_index=defaultdict(list)
        self._tile_index=defaultdict(list)
        self._color_index=defaultdict(list)
    
    def populate(self, folder):
        for root,dirs,files in os.walk(folder): # DEPTH 1 ONLY
            for file in files:
                if file.find('.mjd')!=-1:
                    the_path = root+"/"+file
                    self._collection[file] = LightCurve.from_file(the_path)
    
    def index(self):
        for f in self._collection:
            lc, tilestring, seq, color, _ = f.split('.')
            field = int(lc.split('_')[-1])
            tile = int(tilestring)
            self._field_index[field].append(self._collection[f])
            self._tile_index[tile].append(self._collection[f])
            self._color_index[color].append(self._collection[f])
     
    #your code here
    def retrieve(self, facet, value):
        if facet == 'field':
            return self._field_index[value]
        elif facet == 'tile':
            return self._tile_index[value]
        elif color == 'color':
            return self._color_index[value]
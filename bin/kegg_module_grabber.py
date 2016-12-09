#!/usr/bin/env python2
###############################################################################
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program. If not, see <http://www.gnu.org/licenses/>.        #
#                                                                             #
###############################################################################

__author__ = "Ben Woodcroft"
__copyright__ = "Copyright 2015-2016"
__credits__ = ["Ben Woodcroft"]
__license__ = "GPL3+"
__maintainer__ = "Ben Woodcroft"
__email__ = "b.woodcroft near uq.edu.au"
__status__ = "Development"

import os, re
import logging
import pickle

from module_description_parser import ModuleDescription
from build_enrichment_matrix import BuildEncrichmentMatrix

class KeggModuleGrabber:
    ANNOTATE = 'annotate'
    ENRICHMENT = 'enrichment'
    DATA_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             '..', 
                             'data')
        
    VERSION = open(os.path.join(DATA_PATH, 'VERSION')).readline().strip()
    PICKLE  = 'pickle'

    M2DEF = os.path.join(DATA_PATH, 'module_to_definition')
    M   = os.path.join(DATA_PATH, 'module_descriptions')
    
    def __init__(self):
        
        self.signature_modules = set(['M00611', 'M00612', 'M00613', 'M00614', 
         'M00617', 'M00618', 'M00615', 'M00616', 'M00363', 'M00542', 'M00574', 
         'M00575', 'M00564', 'M00660', 'M00664', 'M00625', 'M00627', 'M00745', 
         'M00651', 'M00652', 'M00704', 'M00725', 'M00726', 'M00730', 'M00744', 
         'M00718', 'M00639', 'M00641', 'M00642', 'M00643', 'M00769', 'M00649', 
         'M00696', 'M00697', 'M00698', 'M00700', 'M00702', 'M00714', 'M00705', 
         'M00746'])
        
        logging.info("Loading module definitions")
        self.m2def = pickle.load(open('.'.join([self.M2DEF, 
                                                 self.VERSION, self.PICKLE])))
        logging.info("Done!")
        logging.info("Loading module descriptions")
        self.m = pickle.load(open('.'.join([self.M, 
                                            self.VERSION, self.PICKLE])))
        logging.info("Done!")
            
    def main(self, args):
        
        if args.subparser_name == self.ANNOTATE:
            output_path = args.output_prefix + '_annotations.tsv'
    
            genome_to_ko_sets = {}
            ko_re = re.compile('^K\d+$')
            for line in open(args.genome_and_ko_file):
                sline = line.strip().split("\t")
                if len(sline) != 2: raise Exception("Input genomes/KO file error on %s" % line)
                
                genome, ko = sline
                
                if ko_re.match(ko):
                    if genome not in genome_to_ko_sets:
                        genome_to_ko_sets[genome] = set()
                    genome_to_ko_sets[genome].add(ko)
                else:
                    raise Exception("Malformed ko line: %i" % line)
            logging.info("Read in KOs for %i genomes" % len(genome_to_ko_sets))
        
            pathways2 = {}
            for name, pathway_string in self.m2def.items():
                if name not in self.signature_modules:   
                    path = ModuleDescription(pathway_string)
                    pathways2[name] = path
    
            logging.info('Writing results to file: %s' % output_path)
            with open(output_path, 'w') as output_path_io:
                header = ["Genome_name", "Module_id", "Module_name", "Steps_found",
                          "Steps_needed", "Percent_Steps_found"]
                output_path_io.write('\t'.join(header) + '\n')  
                for genome, kos in genome_to_ko_sets.items():
                    for name, path in pathways2.items():
                        num_covered  = path.num_covered_steps(kos)
                        num_all      = path.num_steps()
                        perc_covered = num_covered/float(num_all)
                        if perc_covered>=args.cutoff:
                            output_line =  "\t".join([genome,name,self.m[name],
                                                      str(num_covered),# 
                                                      str(num_all),
                                                      str(round(perc_covered*100, 2))]) 
                            output_path_io.write(output_line + '\n') 
            logging.info("Done!")
        elif args.subparser_name == self.ENRICHMENT:
            bem = BuildEncrichmentMatrix()
            bem.main(args.annotations, args.abundances, args.metadata, 
                     args.output_prefix)
            


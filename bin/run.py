#!/usr/bin/env python
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
 
__author__ = "Joel Boyd"
__copyright__ = "Copyright 2015"
__credits__ = ["Joel Boyd"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Joel Boyd"
__email__ = "joel.boyd near uq.net.au"
__status__ = "Development"

###############################################################################

import logging
import os
from kegg_module_grabber import KeggModuleGrabber
from preparer import Preparer
from network_analyzer import NetworkAnalyser
from metagenome_analyzer import MetagenomeAnalyzer

###############################################################################

class Run:
    
    MATRIX          = 'matrix'
    NETWORK         = 'network'
    EXPLORE         = 'explore'
    PATHWAY         = 'pathway'
    ANNOTATE        = 'annotate'
    ENRICHMENT      = 'enrichment'
    MODULE_AB       = 'module_ab'
    TRAVERSE        = 'traverse'

    def __init__(self):
        self.network_options    = [self.EXPLORE, 
                                   self.NETWORK, 
                                   self.PATHWAY,
                                   self.TRAVERSE]
                          
        self.annotation_options = [self.ANNOTATE, 
                                   self.ENRICHMENT]
    
        self.prepare_options    = [self.MATRIX]
    
        self.metagenome_annotation_options    = [self.MODULE_AB]
    
    def check_args(self, args):
    #    if args.subparser_name==NetworkAnalyser.MATRIX:
    #        if(args.blast_outputs or args.hmmsearch_outputs):
    #            if(args.blast_outputs and args.hmmsearch_outputs):
    #                raise Exception("Both blast and hmmsearch outputs were \
    #provided!")
    #        else:
    #            raise Exception("Neither blast or hmmsearch outputs were provided!")
        if args.subparser_name==KeggModuleGrabber.ANNOTATE:
            if(args.genome_and_ko_file or args.genome_and_ko_matrix):
                if(args.genome_and_ko_file and args.genome_and_ko_matrix):
                    raise Exception("A genome to KO matrix and list were provided. \
    Please run with one or the other!") 
            else:
                raise Exception("genome to KO matrix or list not provided!") 
        if args.subparser_name==KeggModuleGrabber.ENRICHMENT:
            if not(args.metadata or args.abundances):
                raise Exception("No metadata or abundance information provided to \
    enrichment.")
        if args.subparser_name==NetworkAnalyser.EXPLORE:
            if not(args.queries):
                if args.depth:
                    logging.warning("--depth argument ignored without --queries \
    flag")
    
        if(os.path.isfile(args.output_prefix + NetworkAnalyser.NETWORK_SUFFIX) or
           os.path.isfile(args.output_prefix + NetworkAnalyser.METADATA_SUFFIX)):
            if args.force:
                logging.warning("Removing existing file with name: %s" \
                                                            % args.output_prefix)
                if os.path.isfile(args.output_prefix + 
                                  NetworkAnalyser.NETWORK_SUFFIX):
                    os.remove(args.output_prefix + NetworkAnalyser.NETWORK_SUFFIX)
                if os.path.isfile(args.output_prefix + 
                                  NetworkAnalyser.METADATA_SUFFIX):
                    os.remove(args.output_prefix + NetworkAnalyser.METADATA_SUFFIX)
            else:
                raise Exception("File %s exists" % args.output_prefix)
    
    def main(self, args):
        self.check_args(args)
        
        if args.subparser_name in self.network_options:
            na=NetworkAnalyser(args.metadata)
            na.main(args)
        elif args.subparser_name in self.annotation_options:
            kmg = KeggModuleGrabber()
            kmg.main(args)
        elif args.subparser_name in self.prepare_options:
            p = Preparer()
            p.main(args)
        elif args.subparser_name in self.metagenome_annotation_options:
            ma = MetagenomeAnalyzer()
            ma.main(args)
#-------------------------------------------------------------------------------
#
#    Parameters Target Support for Xilinx Vivado SCons Tool
#
#    Author: Harry E. Zhurov
#
#-------------------------------------------------------------------------------

import os

from utils import *

#-------------------------------------------------------------------------------
#
#    Create Configuration Parameters header
#
def cfg_params_header(target, source, env):

    trg      = target[0]
    trg_path = str(trg)

    print_action('create cfg params header:  \'' + trg.name + '\'')
    params = {}
    for src in source:
        try:
            cfg_params = read_config(str(src))
            
        except SearchFileException as e:
            print_error('E: ' + e.msg)
            print_error('    while running "CreateCfgParamsHeader" builder')
            Exit(-1)
        
        cfg_params = prefix_suffix(str(src), cfg_params)
        params.update(cfg_params)

    max_len = max_str_len(params.keys()) + 2
    guard   = 'GUARD_' + os.path.splitext(trg.name)[0].upper() + '_SVH'
    text  = generate_title('This file is automatically generated. Do not edit the file!', '//')
    text += '`ifndef ' + guard + os.linesep
    text += '`define ' + guard + os.linesep*2

    text += '// synopsys translate_off' + os.linesep
    text += '`ifndef SIMULATOR'         + os.linesep
    text += '`define SIMULATOR'         + os.linesep
    text += '`endif // SIMULATOR'       + os.linesep
    text += '// synopsys translate_on'  + os.linesep*2

    for p in params:
        value = str(params[p])
        if value != '__NOT_DEFINE__':
            text += '`define ' + p + ' '*(max_len - len(p)) + value + os.linesep

    text += os.linesep + '`endif // ' + guard + os.linesep
    text += generate_footer('//')

    with open(trg_path, 'w') as ofile:
        ofile.write(text)

    return None

#-------------------------------------------------------------------------------
#
#    Create Configuration Parameters Tcl
#
def cfg_params_tcl(target, source, env):

    trg      = target[0]
    trg_path = str(trg)

    print_action('create cfg params tcl:     \'' + trg.name + '\'')
    params = {}
    for src in source:
        try:
            cfg_params = read_config(str(src))

        except SearchFileException as e:
            print_error('E: ' + e.msg)
            print_error('    while running "CreateCfgParamsTcl" builder')
            Exit(-1)
                
        cfg_params = prefix_suffix(str(src), cfg_params)
        params.update(cfg_params)

    max_len = max_str_len(params.keys()) + 2

    text  = generate_title('This file is automatically generated. Do not edit the file!', '#')
    for p in params:
        value = str(params[p])
        if not value:
            value = '""'
        text += 'set ' + p + ' '*(max_len - len(p)) + value + os.linesep

    text += generate_footer('#')

    with open(trg_path, 'w') as ofile:
        ofile.write(text)

    return None

#-------------------------------------------------------------------------------
def create_cfg_params_header(env, trg, src):

    if not SCons.Util.is_List(src):
        src = src.split()
    source = []
    for s in src:
        try:
            ss = os.path.abspath(search_file(s))
        except SearchFileException as e:
            print_error('E: ' + e.msg)
            print_error('    while running "CreateCfgParamsHeader" builder')
            Exit(-1)
            
        source.append(ss)

    env.CfgParamsHeader(trg, source)

    return trg

#-------------------------------------------------------------------------------
def create_cfg_params_tcl(env, trg, src):

    if not SCons.Util.is_List(src):
        src = src.split()
    source = []
    for s in src:
        try:
            ss = os.path.abspath(search_file(s))
        except SearchFileException as e:
            print_error('E: ' + e.msg)
            print_error('    while running "CreateCfgParamsTcl" builder')
            Exit(-1)
            
        source.append(ss)

    env.CfgParamsTcl(trg, source)

    return trg

#-------------------------------------------------------------------------------


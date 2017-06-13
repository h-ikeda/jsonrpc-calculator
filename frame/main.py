# coding: UTF-8
#
# The data structure of 'model' is below:
#
#     'nodes' : { id(hashable): { x:Real, y:Real, z:Real } }
#     'lines' : { id(hashable): { n1:id, n2:id, EA:Real } }
#     'boundaries' : { id(hashable): { node:id, x:Real or Bool, y:Real or Bool, z:Real or Bool, rx:Real or Bool, ry:Real or Bool, rz:Real or Bool } }
#     'nodeLoads' : { id(hashable): { node:id, x:Real, y:Real, z:Real, rx:Real, ry:Real, rz:Real } }
#

import numpy as np
from numpy import zeros
from scipy.sparse import dok_matrix
from scipy.sparse.linalg import spsolve
from scipy.linalg import solve
from frame import line, section
from frame.model import Model


coos = 'x', 'y', 'z', 'rx', 'ry', 'rz'


def items(seq):
    iters = seq.items() if isinstance(seq, dict) else enumerate(seq)
    for key, value in iters:
        if value is not None:
            yield key, value


def keys(seq):
    for key, _ in items(seq):
        yield key


def values(seq):
    iters = seq.values() if isinstance(seq, dict) else seq
    for value in iters:
        if value is not None:
            yield value


def fixed_coos_of_boundary(boundary_obj):
    for coo in coos:
        if boundary_obj[coo] and isinstance(boundary_obj[coo], bool):
            yield boundary_obj['node'], coo


def fixed_coos(boundary_objs):
    for boundary in boundary_objs:
        # yield from fixed_coos_of_boundary(boundary) # python 3.x
        for _ in fixed_coos_of_boundary(boundary):
            yield _


def unfixed_coos(node_ids, boundary_objs):
    fixed = set(fixed_coos(boundary_objs))
    for node_id in node_ids:
        for coo in coos:
            if (node_id, coo) not in fixed:
                yield node_id, coo


def index_dict(seq):
    return {d: i for i, d in enumerate(seq)}


def node_vector(node_obj):
    for coo in coos[:3]:
        yield node_obj[coo]


def line_vector(n1_obj, n2_obj):
    for c1, c2 in zip(node_vector(n1_obj), node_vector(n2_obj)):
        yield c2 - c1


def calculated_section(section_obj, arg_names):
    p = section.properties(**section_obj)
    return {
        arg_name: p[arg_name]
            for arg_name in arg_names
                if arg_name in p
    }


def calculated_sections(sections, arg_names):
    return {
        i: calculated_section(d, arg_names)
            for i, d in sections
    }


def calculated_material(material_obj, arg_names):
    m = material_obj # 必要ならここで演算してプロパティを作る。現在は丸投げ。
    return {
        arg_name: m[arg_name]
            for arg_name in arg_names
                if arg_name in m
    }


def calculated_materials(materials, arg_names):
    return {
        i: calculated_material(d, arg_names)
            for i, d in materials
    }


def get_indexes(node_id, coo_indexes):
    for i, coo in enumerate(coos):
        if (node_id, coo) in coo_indexes:
            yield i, coo_indexes[node_id, coo]


def line_node_ids(line_obj):
    for n in 'n1', 'n2':
        yield line_obj[n]


def stiffness_node_ids(line_obj):
    for n1 in line_node_ids(line_obj):
        for n2 in line_node_ids(line_obj):
            yield n1, n2


def line_nodes(line_obj, nodes):
    for i in line_node_ids(line_obj):
        yield nodes[i]


def calculate(model):
    boundaries = model['boundaries']
    nodes = model['nodes']
    unfixed = unfixed_coos(keys(nodes), values(boundaries))
    coo_indexes = index_dict(unfixed)
    section_keys = 'Ax', 'Iz', 'Iy', 'Ay', 'Az', 'theta', 'J'
    sections = calculated_sections(items(model['sections']), section_keys)
    material_keys = 'E', 'G'
    materials = calculated_materials(items(model['materials']), material_keys)
    a = dok_matrix((len(coo_indexes),) * 2)
    for ln in values(model['lines']):
        v = line_vector(*line_nodes(ln, nodes))
        p = dict(sections[ln['section']], **materials[ln['material']])
        for k, (n1, n2) in zip(line.stiffness_global(*v, **p), stiffness_node_ids(ln)):
            for i, row in get_indexes(n1, coo_indexes):
                for j, col in get_indexes(n2, coo_indexes):
                    a[row, col] += k[i][j]
    b = zeros(len(coo_indexes))
    for ld in values(model['nodeloads']):
        for i, row in get_indexes(ld['node'], coo_indexes):
            if ld[coos[i]]:
                b[row] += ld[coos[i]]
    dis_array = spsolve(a, b)
    dis = {}
    for (node_id, coo), i in coo_indexes.items():
        if node_id in dis:
            dis[node_id][coo] = dis_array[i]
        else:
            dis[node_id] = {coo: dis_array[i]}
    return {
        'displacements': dis
    }

directions = ('x', 'y', 'z', 'rx', 'ry', 'rz')


def effectiveCoodinates(nodes, boundaries):
        t = {b['node']: {d for d in directions if isinstance(b[d], bool) and b[d]} for b in boundaries}
        return tuple((n['recid'], d) for n in nodes for d in directions if n['recid'] not in t or d not in t[n['recid']])


def itemById(items, recid):
        for item in items:
            if item['recid'] == recid:
                return item

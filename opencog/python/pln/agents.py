__author__ = 'ramin'

from opencog.cogserver import MindAgent
from opencog.atomspace import types, AtomSpace
from utility.generic import DEFAULT_TRUTH_VALUE as def_tv
from logic import ForwardChainer
import random
import rules
import uuid


class SimpleForwardInferenceAgent(MindAgent):
    def run(self, atomspace=None):
        node = self.fetch(atomspace)
        if node is None:
            return None
        fc = ForwardChainer(atomspace)
        fc.add_rule(rules.DeductionRule(atomspace))
        return fc.run(node)

    def fetch(self, atomspace=None):
        links = list(atomspace.get_atoms_by_type(types.InheritanceLink))
        link = self._selectOne(links)
        if link is None:
            return None
        return link.out[0]

    def _selectOne(self, links):
        max = sum([link.getav().sti for link in links])
        pick = random.uniform(0, max)
        current = 0
        for link in links:
            current += link.getav().sti
            if current >= pick:
                return link


class AtomspacePopulatorAgent(MindAgent):
    def run(self, atomspace):
        pick = random.random()
        if pick > 0.65:
            atom = self._add_atom(atomspace)
            if atom is not None:
                a = atomspace.set_av(atom.h, random.uniform(0, 1), random.uniform(0, 1))
                pass
            return atom

    def _add_atom(self, atomspace):
        pick = random.random()
        if pick > 0.8:
            return self._add_node(atomspace)
        else:
            return self._add_link(atomspace)

    def _add_node(self, atomspace):
        name = str(uuid.uuid1())
        return atomspace.add_node(types.ConceptNode, name, def_tv)

    def _add_link(self, atomspace):
        nodes = atomspace.get_atoms_by_type(types.ConceptNode)
        if len(nodes) < 2:
            return None

        first_rand = random.randrange(0, len(nodes))
        second_rand = random.randrange(0, len(nodes))

        while first_rand == second_rand:
            second_rand = random.randrange(0, len(nodes))
        first_node = nodes[first_rand]
        second_node = nodes[second_rand]
        return atomspace.add_link(types.InheritanceLink, [first_node, second_node], def_tv)

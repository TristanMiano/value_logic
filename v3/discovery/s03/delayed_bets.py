"""One factor per sampled identity, with later positive-proof refinement.

Codex (GPT-6), 2026-10-11. DEVELOPMENT arithmetic; caller checks proof/source.
"""
from positive_bets import Group


class DelayedGroup(Group):
    def __post_init__(self):
        super().__post_init__()
        self.identities=[]
        self.position={}

    def add(self,index,proved):
        if type(index) is not int or not 0<=index<self.N or index in self.position:
            raise ValueError('distinct population identity required')
        super().observe(proved)
        self.position[index]=len(self.identities);self.identities.append(index)

    def accept(self,index):
        if type(index) is not int or index not in self.position:
            raise ValueError('sampled identity required')
        pos=self.position[index]
        if self.trace[pos][2]:return False
        zs=[z for _,_,z in self.trace];zs[pos]=1
        self.trace=[];self.positives=0;self.cache.clear()
        for z in zs:super().observe(z)
        return True

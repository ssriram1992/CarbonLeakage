import numpy as np
import gurobipy as gp
import matplotlib.pyplot as plt

class Stage1:
    def __init__(self, DemInt = 323.5, DemSl = 2.3814, invURcost = 15,
            costLrrBase = 10, CostLrr_l = 10, CostLrr_q = 0,
            costQrrBase = 0.1, upgradeLin = 20000, upgradeQuad = 30000,
            CTrrs = {'l':75, 'h':75}, borderTax = 100,
            costLur = 10, costQur = 0.1, CTur = 0):
        """
        Linear Cost of production will be: costLrrBase + (1-emission)*CostLrr_l
        Quadratic Cost of production will be: costQrrBase
        """
        self.DemInt = DemInt
        self.DemSl = DemSl
        self.costLrrBase = costLrrBase
        self.costLur = costLur
        self.costQrrBase = costQrrBase
        self.costQur = costQur
        self.CTur = CTur
        self.CTrrs = CTrrs
        self.borderTax = borderTax
        self.CostLrr_l = CostLrr_l
        self.CostLrr_q = CostLrr_q
        self.upgradeLin = upgradeLin
        self.upgradeQuad = upgradeQuad
        self.invURcost = invURcost
    def solve(self, SolFile = None):
        """
        Give a file Name for SolFile, then it will be written
        """
        M = gp.Model("Stage 1")
        # M.setParam('OutputFlag', False)
        M.setParam('LogToConsole', False)
        M.params.nonconvex = 2     # Nonconvex optimization
        # M.params.MIPGap = 0.01
        scenarios = list(self.CTrrs.keys()) #self.CTrrs.copy()
        # Variables
        emission = M.addVar(lb = 0, ub = 1, name = "emission")
        Qrrs = M.addVars(scenarios, ub=self.DemInt, name="Qrr")
        Qrrs_sq = M.addVars(scenarios, ub=self.DemInt*self.DemInt, name="Qrr_sq")
        M.addConstrs((Qrrs_sq[xi] == Qrrs[xi]*Qrrs[xi] for xi in scenarios), name="Qrr_sq_def")
        Qurs = M.addVars(scenarios, ub=self.DemInt, name="Qur")
        Qs = M.addVars(scenarios, ub=self.DemInt, name="Qs")
        invUR = M.addVar(name="invUR")
        M.addConstrs( Qurs[xi] <= invUR for xi in scenarios)
        M.addConstrs((Qs[xi] == Qrrs[xi] + Qurs[xi] for xi in scenarios))
        nScen = len(scenarios)
        costLrr = M.addVar(name="costLrr", lb = self.costLrrBase, ub = self.costLrrBase + self.CostLrr_l + self.CostLrr_q)
        M.addConstr(costLrr == self.costLrrBase + (1-emission)*self.CostLrr_l + (1-emission)*(1-emission)*self.CostLrr_q, name="linCost")
        objExpr = -invUR*self.invURcost - self.upgradeLin*(1-emission) - self.upgradeQuad*(1-emission)*(1-emission)
        M.update()
        for xi in scenarios:
            revenuexi = (self.DemInt - self.DemSl*Qs[xi])*Qs[xi]
            costRRxi = costLrr*Qrrs[xi] + 0.5*self.costQrrBase*Qrrs_sq[xi] #0.5*self.costQrrBase*Qrrs[xi]*Qrrs[xi]
            costURxi = self.costLur*Qurs[xi] + 0.5*self.costQur*Qurs[xi]*Qurs[xi]
            Taxesxi = self.borderTax*Qurs[xi] + self.CTrrs[xi]*Qrrs[xi]*emission
            objExpr += (revenuexi - costRRxi - costURxi - Taxesxi)/nScen
        M.setObjective(objExpr, gp.GRB.MAXIMIZE)
        #####################
        # Initial point
        #####################
        for xi in scenarios:
            Qurs[xi].start = 0
            Qrrs[xi].start = 0
            Qs[xi].start = 0
        emission.start = 1
        costLrr.start = self.costLrrBase + self.CostLrr_l + self.CostLrr_q
        #####################
        M.optimize()
        M.write("stage1.lp")
        if SolFile is not None:
            M.write(SolFile)
        self.expQrrval = sum(Qrrs[xi].X for xi in scenarios)/len(scenarios)
        self.expQurval = sum(Qurs[xi].X for xi in scenarios)/len(scenarios)
        self.expQsval = sum(Qs[xi].X for xi in scenarios)/len(scenarios)
        self.invURval = invUR.X
        CLtype = {xi:0 for xi in scenarios} # 0 - nowhere, 1 - only in RR, 2 - only in UR, 3 - in both; Order: scenarios
        lookup = {0: "N", 1:"R", 2:"U", 3:"B"}
        for xi in scenarios:
            tol = 1e-3
            val = 0
            if Qrrs[xi].X > tol:
                val += 1
            if Qurs[xi].X > tol:
                val += 2
            CLtype[xi] = lookup[val]
        tol = 0.01
        invType = ('I' if emission.X < 1-tol else 'B') if invUR.X < tol else ('M' if emission.X <1-tol else 'P')
        # B - Business as usual; I - Investment in sustainability;  M - investment inside, but also outside;   P is investment only outside
        # return self.expQrrval, self.expQurval, self.invURval, M.objVal, emission.X, CLtype, invType
        ans = {}
        ans['E-Qrr'] = self.expQrrval
        ans['E-Qur'] = self.expQurval
        ans['invUR'] = self.invURval
        ans['profit'] = M.objVal
        ans['emission'] = emission.X
        ans['CLtype'] = CLtype
        ans['invType'] = invType
        return ans

if __name__ == "__main__":
    stage1 = Stage1()
    ans = stage1.solve("stage1.sol")
    print(ans)

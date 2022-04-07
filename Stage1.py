import numpy as np
import gurobipy as gp
import matplotlib.pyplot as plt

class Stage1:
    def __init__(self, DemInt = 200, DemSl = 1, invURcost = 15,
            costLrrBase = 10, CostLrr_l = 100, CostLrr_q = 0,
            costQrrBase = 0.1,  CostQrr_l = 0.1, CostQrr_q = 0,
            CTrrs = [90, 910], borderTax = 100,
            costLur = 5, costQur = 0.1, CTur = 0):
        """
        Linear Cost of production will be: costLrrBase + (1-emission)*CostLrr_l + (1-emission)(1-emission)*CostLrr_q
        Quadratic Cost of production will be: costQrrBase + (1-emission)*CostQrr_l + (1-emission)(1-emission)*CostQrr_q
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
        self.CostQrr_l = CostQrr_l
        self.CostQrr_q = CostQrr_q
        self.invURcost = invURcost
    def solve(self, SolFile = None):
        """
        Give a file Name for SolFile, then it will be written
        """
        M = gp.Model("Stage 1")
        # M.setParam('OutputFlag', False)
        # M.setParam('LogToConsole', False)
        M.params.nonconvex = 2     # Nonconvex optimization
        scenarios = self.CTrrs.copy()
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
        costQrr = M.addVar(name="costQrr", lb = self.costQrrBase, ub = self.costQrrBase + self.CostQrr_l + self.CostQrr_q)
        M.addConstr(costLrr == self.costLrrBase + (1-emission)*self.CostLrr_l + (1-emission)*(1-emission)*self.CostLrr_q, name="linCost")
        M.addConstr(costQrr == self.costQrrBase + (1-emission)*self.CostQrr_l + (1-emission)*(1-emission)*self.CostQrr_q, name="quadCost")
        objExpr = -invUR*self.invURcost
        M.update()
        for xi in scenarios:
            revenuexi = (self.DemInt - self.DemSl*Qs[xi])*Qs[xi]
            costRRxi = costLrr*Qrrs[xi] + 0.5*costQrr*Qrrs_sq[xi] #0.5*self.costQrrBase*Qrrs[xi]*Qrrs[xi]                 
            costURxi = self.costLur*Qurs[xi] + 0.5*self.costQur*Qurs[xi]*Qurs[xi]
            Taxesxi = self.borderTax*Qurs[xi] + xi*Qrrs[xi]*emission
            objExpr += (revenuexi - costRRxi - costURxi - Taxesxi)/nScen
        M.setObjective(objExpr, gp.GRB.MAXIMIZE)
        #####################
        # Initial point
        #####################
        for xi in scenarios:
            Qurs[xi].start = 0
            Qrrs[xi].start = 0
            Qs[xi].start = 0
        emission.start = 0
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
        return self.expQrrval, self.expQurval, self.invURval, M.objVal

if __name__ == "__main__":
    stage1 = Stage1()
    ans = stage1.solve("stage1.sol")
    print(ans)
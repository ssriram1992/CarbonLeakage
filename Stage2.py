# %%:
import numpy as np
import gurobipy as gp
import matplotlib.pyplot as plt

class Stage2:
    def __init__(self, DemInt = 200, DemSl = 1, costLrr = 50, costQrr = 1, costLur = 40, costQur = 1, CTur = 0, capQur = 25, Emitrr = 0.5, Emitur = 1):
        self.DemInt = DemInt
        self.DemSl = DemSl
        self.costLrr = costLrr
        self.costLur = costLur
        self.costQrr = costQrr
        self.costQur = costQur
        self.CTur = CTur
        self.capQur = capQur
        self.Emitrr = Emitrr
        self.Emitur = Emitur
    def prds(self, CTrr, impRR):
        M = gp.Model()
        M.params.logtoconsole = 0
        Qrr = M.addVar(name="Qrr")
        Qur = M.addVar(name="Qur", ub=self.capQur)
        Qtot = M.addVar(name="Qtot")
        M.addConstr(Qrr + Qur == Qtot)
        # print("CTrr:{}, Emitrr:{}, impRR:{}".format(CTrr, self.Emitrr, impRR))
        M.setObjective( (self.DemInt - self.DemSl * Qtot)*Qtot - (self.costLrr*Qrr + 0.5*self.costQrr*Qrr*Qrr + self.costLur*Qur + 0.5*self.costQur*Qur*Qur+ CTrr * Qrr *self.Emitrr + self.CTur*Qur*self.Emitur +impRR*Qur ), gp.GRB.MAXIMIZE)
        M.optimize()
        return Qrr.X, Qur.X, M.objVal
    def getAllData(self):
        return {"DemInt":self.DemInt, "DemSl":self.DemSl, "costLrr":self.costLrr, "costLur":self.costLur, "costQrr":self.costQrr, "costQur":self.costQur, "CTur":self.CTur, "capQur":self.capQur, "Emitrr":self.Emitrr, "Emitur":self.Emitur}

# Test
mm = Stage2(DemInt = 200, DemSl = 1, 
            costLrr = 21,
            costQrr = 0.43,
            costLur = 5, costQur = 0.1, CTur = 0, capQur= 50.6814, Emitrr = 0)
Ans = mm.prds(499, 450)
print(Ans)

# %%: Sensitivity to taxes
if False:
    CL = Stage2(costQrr=2, costQur=2, capQur=250)
    n1 = 50
    n2 = 50
    impRRs, CTrrs = np.meshgrid(np.linspace(0,20,n1), np.linspace(0,40,n2))
    prdRRs = np.zeros_like(CTrrs)
    prdURs = np.zeros_like(CTrrs)
    profit = np.zeros_like(CTrrs)
    for i in range(n1):
        for j in range(n2):
            prdRRs[i,j], prdURs[i,j], profit[i,j] = CL.prds(CTrrs[i,j], impRRs[i,j])


    fig, ax = plt.subplots()
    plt.subplot(2,1,1)
    plt.contourf(CTrrs, impRRs, prdRRs, cmap='RdBu')
    plt.xlabel('CTrr')
    plt.ylabel('impRR')
    plt.title('Production of RR')
    plt.colorbar()


    plt.subplot(2,1,2)
    plt.contourf(CTrrs, impRRs, prdURs)
    plt.xlabel('CTrr')
    plt.ylabel('impRR')
    plt.title('Production of UR')
    plt.colorbar()
    plt.show()

    plt.contourf(CTrrs, impRRs, profit)
    plt.xlabel('CTrr')
    plt.ylabel('impRR')
    plt.title('Profit')
    plt.colorbar()
    plt.show()

# %%: Sensitivity to emissions
# Here, we assume that the linear and quadratic cost of production are functions of the emission factor. 
# We also assume that the border tax is a function of carbon tax.
# We plot production and profit as a function of the emission factor and carbon tax

if False:
    def Fun_prodcosts(emission):
        return 10*(1-emission) + 50, 0.1*(1-emission) + 2
    def Fun_borderTax(carbonTax):
        return 30 +0*carbonTax/0.75

    n1 = 50
    n2 = 50
    CarbTaxs = np.linspace(0,50,n1)
    Emitrrs = np.linspace(0,1,n2)
    CarbTaxgrid, EmitRRgrid = np.meshgrid(CarbTaxs, Emitrrs)
    prdRRs = np.zeros_like(CarbTaxgrid)
    prdURs = np.zeros_like(CarbTaxgrid)
    profit = np.zeros_like(CarbTaxgrid)
    for i in range(n1):
        for j in range(n2):
            t1, t2 = Fun_prodcosts(EmitRRgrid[i,j])
            t3 = Fun_borderTax(CarbTaxgrid[i,j])
            CL = Stage2(costLrr= t1, costQrr=t2, capQur=30, Emitrr=EmitRRgrid[i,j])
            prdRRs[i,j], prdURs[i,j], profit[i,j] = CL.prds(CarbTaxgrid[i,j], t3)

    fig, ax = plt.subplots()
    plt.subplot(2,1,1)
    plt.contourf(CarbTaxgrid, EmitRRgrid, prdRRs, cmap='RdBu', levels=25)
    plt.xlabel('CarbTax')
    plt.ylabel('Emitrr')
    plt.title('Production of RR')
    plt.colorbar()

    plt.subplot(2,1,2)
    plt.contourf(CarbTaxgrid, EmitRRgrid, prdURs, levels=25)
    plt.xlabel('CarbTax')
    plt.ylabel('Emitrr')
    plt.title('Production of UR')
    plt.colorbar()

    plt.show()

    plt.contourf(CarbTaxgrid, EmitRRgrid, profit, levels=25)
    plt.xlabel('CarbTax')
    plt.ylabel('Emitrr')
    plt.title('Profit')
    plt.colorbar()
    plt.show()

# %%: Sensitivity to investments in UR
# Here, we assume that the linear and quadratic cost of production are functions of the emission factor. 
# We also assume that the border tax is a function of carbon tax.
# We plot production and profit as a function of the emission factor and carbon tax

if False:
    def Fun_prodcosts(emission):
        return 10*(1-emission) + 50, 0.1*(1-emission) + 2

    n1 = 50
    n2 = 50
    capURs = np.linspace(0,50,n1)
    Emitrrs = np.linspace(0,1,n2)
    CapURgrid, EmitRRgrid = np.meshgrid(capURs, Emitrrs)
    prdRRs = np.zeros_like(CapURgrid)
    prdURs = np.zeros_like(CapURgrid)
    profit = np.zeros_like(CapURgrid)
    for i in range(n1):
        for j in range(n2):
            t1, t2 = Fun_prodcosts(EmitRRgrid[i,j])
            CL = Stage2(costLrr= t1, costQrr=t2, capQur=CapURgrid[i,j], Emitrr=EmitRRgrid[i,j])
            prdRRs[i,j], prdURs[i,j], profit[i,j] = CL.prds(50, 30)
            profit[i,j] -= CapURgrid[i,j]*20

    fig, ax = plt.subplots()
    plt.subplot(2,1,1)
    plt.contourf(CapURgrid, EmitRRgrid, prdRRs, cmap='RdBu', levels=25)
    plt.xlabel('Capacity in UR')
    plt.ylabel('Emitrr')
    plt.title('Production of RR')
    plt.colorbar()

    plt.subplot(2,1,2)
    plt.contourf(CapURgrid, EmitRRgrid, prdURs, levels=25)
    plt.xlabel('Capacity in UR')
    plt.ylabel('Emitrr')
    plt.title('Production of UR')
    plt.colorbar()

    plt.show()

    plt.contourf(CapURgrid, EmitRRgrid, profit, levels=25)
    plt.xlabel('Capacity in UR')
    plt.ylabel('Emitrr')
    plt.title('Profit')
    plt.colorbar()
    plt.show()

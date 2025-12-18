import numpy as np




class LinearRegression:
     def __init__(self):
          self.experience = [1,2,3,4]
          self.salary = [30,21,32]
          
     def Line(self):
          #formula y = m*x+b
          mean_experience = np.mean(self.experience)
          mean_salary = np.mean(self.salary)
          
          sum_experience = np.sum((self.experience - mean_experience))
          sum_salary = np.sum((self.salary - mean_salary))
          sum_mean_x = np.sum((self.experience - mean_experience)**2)  
            
          m = (sum_experience * sum_salary)/sum_mean_x
          print(m)
if __name__ == "__main__":
 p = LinearRegression.__new__(LinearRegression)
 LinearRegression.__init__(p)
 LinearRegression.Line(p)
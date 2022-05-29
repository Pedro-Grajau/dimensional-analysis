# Dimensional Analysis
Determine the dimensionless parameters for a given set of physical variables in accordance with the Buckingham $\Pi$ theorem.

## Requirements
* numpy
* pandas
* sympy
* streamlit

## Usage
Select the physical variables in the sidebar. Choose the symbols from a collection of available variables here: [tabela_de_variaveis.csv](tabela_de_variaveis.csv). The code determines the dimensional matrix and the number $d$ of independent dimensionless parameters that can be formed from these variables. Finally, if dimensionless parameters could be found, one specific set (of infinitely many possible solutions) is presented in a visually appealing way.

## Input
![image](https://user-images.githubusercontent.com/84031272/170895719-229e0e02-0d24-430d-abb8-7d47f5dd5cc7.png)

#### Result
$\Pi_1 = \frac{F_D \rho}{\eta^2} \Pi_2 = \frac{D \rho u}{\eta}$

In this example the symbols represent following physical variables
 
| Symbol  | Description                | SI unit |             
|---------|----------------------------|---------|            
| F_D     | Drag force                 |N        |            
| u       | Flow velocity              |m / s    |            
| eta     | Dynamic viscosity of fluid |Pa s     |            
| rho     | Density of fluid           |kg / m^3 |            
| D       | Diameter of sphere         |m        |

### Dimensional Matrix
The code looks up the dimensions of the entered symbols in the table above and builds the corresponding dimensional matrix. For the given example, the dimensional matrix is:

| Symbol | F_D | u  | eta | rho | D |
|--------|-----|----|-----|-----|---|
| L      | 1   | 1  | -1  | -3  | 1 |
| M      | 1   | 0  | 1   | 1   | 0 |
| T      | -2  | -1 | -1  | 0   | 0 |

From the rank of the dimensional matrix (here: $r=3$) and the number of variables/symbols (here: $n=5$) the number of dimensionless parameters is determined by $d = n - r$ (here: $d = 2$).

In most cases the rank of the dimensional matrix will be the number of involved base quantities (here: $L$, $M$, $T$) and therefore equal to the number of rows $m$ in the dimensional matrix. However, in some cases the rank is lower than the number of rows. In this case one or more rows must be deleted (without reducing the rank thereby), until the number of rows equals the rank ($m = r$)!

## License
This project is licensed under the terms of the MIT license, see [LICENSE.md](LICENSE.md).

## References
* [Simon, Volker; Weigand, Bernhard; Gomaa, Hassan (2017): Dimensional Analysis for Engineers. Cham: Springer International Publishing](https://doi.org/10.1007/978-3-319-52028-5)

* [Szirtes, Thomas; Rózsa, Pál (2007): Applied dimensional analysis and modeling. 2. ed. Amsterdam: Elsevier/Butterworth-Heinemann](https://doi.org/10.1016/B978-0-12-370620-1.X5000-X)


import streamlit as st
import numpy as np
import pandas as pd
import sympy as sp
from sympy import Matrix
import itertools

tabela = pd.read_csv('tabela_de_variaveis.csv')
tabela.index = tabela["Symbol"]

#Menu Lateral
st.sidebar.markdown("## Escolha as variáveis: ")
lista_nomes_variaveis = st.sidebar.multiselect("Filtro", tabela["Quantity"])

#variaveis = r'h u c_p \rho \eta k_th D'
#lista_variaveis = r'h u c_p \rho \eta k_th D'.split()

# Mostrar as variáveis selecionadas
df1 = tabela.set_index('Quantity')
tabela_variaveis = df1.loc[lista_nomes_variaveis, ['SI unit',
                                             'in SI base units',
                                             'Category',
                                             'Symbol']]

# Mostrar a base de expoente das variáveis selecionadas
lista_variaveis = tabela_variaveis["Symbol"]

tabela_dimensoes = tabela.loc[lista_variaveis, 'L':'J'].transpose()
tabela_dimensoes = tabela_dimensoes[(tabela_dimensoes.T != 0).any()]
indices_tabela = list(tabela_dimensoes.index)

#Aplicação Visual

st.markdown('#### Variáveis selecionadas: ')
st.table(tabela_variaveis)

st.markdown('#### Dimensões: ')
st.table(tabela_dimensoes)

st.sidebar.markdown('#### Variáveis: \n')
for indice, variavel in enumerate(tabela_variaveis.index):
    latex = fr'$${tabela_variaveis.iloc[indice, -1]}$$ = {variavel}'
    st.sidebar.write(latex)

variaveis = (" ").join(lista_variaveis)

############## Lógica de resolução ##############
matriz_inicial = Matrix(tabela_dimensoes.values)

n_linhas, n_colunas = matriz_inicial.shape

n_variables = n_colunas
rank_matriz = matriz_inicial.rank()
n_dimensioes = n_variables - rank_matriz

def verificar_sistema(flag=True):
    #Pegando a submatriz responsável pelo sistema
    submatriz = Matrix(tabela_dimensoes[lista_variaveis[-rank_matriz:]].values)
    
    # Check if the rank of submatrix C_temp differs from rank_A
    if submatriz.rank() != matriz_inicial:
        st.write(f'Não são linearmente independente')
        st.write(f'Por favor organize as entradas das variáveis')
        st.write(f'Possíveis combinações para {rank_matriz} são:')
        
        # Get all possible combinations of a number of rank_A variables
        combinacoes = itertools.combinations(lista_variaveis, rank_matriz)
        
        # Check for each of the combinations if the rank of submatrix C_temp is equal to rank_A
        for combinacao in combinacoes:
            submatriz = Matrix(tabela_dimensoes[list(combinacao)].values)
            st.write(combinacao)
            if submatriz.rank() == matriz_inicial:
                st.write('... ' + ' '.join(list(combinacao)))
        flag = False

    return flag

def calcular_resultados():  
    # Partition matrix A into submatrix B...
    submatriz_b = matriz_inicial[:,0:n_dimensioes]
    # ...and submatrix C
    submatriz_c = matriz_inicial[:,n_dimensioes:]
    # Invert matrix C 
    submatriz_inversa_c = submatriz_c.inv()                         
    # Calculate matrix D 
    submatriz_d = - submatriz_inversa_c * submatriz_b
    # Concatenate identity matrix with transpose of matrix D
    matriz_final = sp.eye(n_dimensioes).row_join(submatriz_d.T)          
    # Create list of dimensionless parameter names
    pi_list = []
    for j in range(n_dimensioes):
        pi_list.append('Pi_' + str(j+1))
    # Create data frame from K_mat values
    expoentes_df = pd.DataFrame(np.array(matriz_final), index=pi_list, columns=lista_variaveis)
    return pi_list, matriz_final

def resolver(pi_list, matriz_final):
    # Define Sympy symbols
    var_symb = sp.symbols(variaveis)
    Pi_symb = sp.symbols(pi_list)
    # Create list with Sympy equations
    expressions = []
    for i in range(n_dimensioes):
        product = 1
        for j in range(n_colunas):
            product *= var_symb[j]**matriz_final[i,j]
        expression = sp.Eq(Pi_symb[i],product)
        expressions.append(expression)
        st.write(fr"$${sp.latex(expression)}$$")

#################################################

if st.button("Resolver"):
    pi_list, matriz_final = calcular_resultados()
    st.markdown("##### Resultado: ")
    resolver(pi_list, matriz_final)
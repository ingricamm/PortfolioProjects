"""
a)	Excluir las autorizaciones anuladas.
"""

# Import libreries
import pandas as pd
# file path
BaseAutorizaciones = 'BaseAutorizaciones.txt'
BaseSalario = 'BaseSalario.txt'

# Read files in DataFrames of Pandas
df1 = pd.read_csv(BaseAutorizaciones, sep='\t')  
df2 = pd.read_csv(BaseSalario, sep=',')

# Print first five rows of the dataframe
print(df1.head())
print(df2.head())

# rename column 'Afiliado' as 'Afiliado_Id' 
df2.rename(columns={'Afiliado': 'Afiliado_Id'}, inplace=True)  
print(df2.head())

# Inner DataFrames regarding 'Afiliado_Id'
df_unido = pd.merge(df1, df2, on='Afiliado_Id', how='inner') 

# DataFrame (df_anulada) where estado is "ANULADA"
df_anulada = df_unido[df_unido['Estado_Autorizacion'].str.contains('ANULADA', case=False, na=False)] 
print("\n rows TO REMOVE where estado is 'anulada':")
print(df_anulada )  # 

#DataFrame (df_filtered) removing rows where estado is "anulada"
df_filtered = df_unido[~df_unido['Estado_Autorizacion'].str.contains('ANULADA', case=False, na=False)] 
print("\n rows after removing row where estado is 'ANULADA':")
print(df_filtered )  

"""
b)	Por mes, obtener el top 5 de prestaciones por valor pagado.
"""

print(df_filtered ['Fecha'] )
df_filtered['Fecha'] = pd.to_datetime(df_filtered['Fecha'], format='%Y-%d-%m')

print(type(df_filtered['Fecha'] ))
#Extract the month and year to create a 'Mes' column for grouping
df_filtered['Mes'] = df_filtered['Fecha'].dt.to_period('M')  # This will give 'YYYY-MM' format
print(df_filtered ['Mes'] )

# Sort first, then group and apply head(5)
df_top5 = df_filtered.sort_values(['Mes', 'Valor_Prestacion'], ascending=[True, False]).groupby('Mes').head(5)

# result
print("Top 5 prestaciones por valor pagado por mes:")
print(df_top5)

"""
c)	Por mes, obtener el promedio de numero de prestaciones por autorización.
"""

# Count the number of prestaciones per authorization within each month
prestaciones_por_auto = df_filtered.groupby(['Mes', 'Estado_Autorizacion']).size().reset_index(name='Num_Prestaciones')
# Calculate the average number of prestaciones per authorization per month
avg_prestaciones_per_month = prestaciones_por_auto.groupby(['Mes'])['Num_Prestaciones'].mean().reset_index(name='Avg_Prestaciones_por_Autorizacion')

# result
print("Promedio de numero de prestaciones por autorizacion por mes:")
print(prestaciones_por_auto)
print("Promedio de numero de prestaciones por mes:")
print(avg_prestaciones_per_month)

"""
d)	Identificar si existen afiliados con más de una autorización.
"""

# Count the number of unique authorizations for each affiliate
afiliados_count = df_filtered.groupby('Afiliado_Id')['Autorizacion_id'].nunique().reset_index(name='Num_Autorizaciones')

# Identify affiliates with more than one authorization
afiliados_multiple_auto = afiliados_count[afiliados_count['Num_Autorizaciones'] > 1]
# Sort the result in descending order by the number of authorizations
afiliados_multiple_auto_sort =afiliados_multiple_auto.sort_values(by='Num_Autorizaciones', ascending=False)


print("Afiliados con mas de una autorización:")
print(afiliados_multiple_auto)

# result
print("Afiliados con mas de una autorización ordenados de forma descendente:")
print(afiliados_multiple_auto_sort)

"""
e)	Cada afiliado cotiza el 12.5% de su salario mensual, identificar para cada afiliado,
a cuanto porcentaje de su cotización corresponde el costo total incurrido en las autorizaciones
"""

# Calculate total contributions per affiliate (12.5% of their monthly salary)
df_filtered['Cotizacion'] = df_filtered['salario'] * 0.125

# Calculate the total cost incurred for authorizations per affiliate
total_costs = df_filtered.groupby('Afiliado_Id')['Valor_Prestacion'].sum().reset_index()
print("costo por afiliado:")
print(total_costs)

# Merge the contributions with the total costs
merged_data = pd.merge(total_costs, df_filtered[['Afiliado_Id', 'Cotizacion']], on='Afiliado_Id', how='left')
print("margen por afiliado:")
print(merged_data)
#Calculate the percentage of the total cost incurred relative to the contributions
merged_data['Porcentaje_Costo'] = (merged_data['Valor_Prestacion'] / merged_data['Valor_Prestacion']) * 100

merged_data = merged_data.groupby(['Afiliado_Id','Cotizacion'])['Porcentaje_Costo'].mean().reset_index(name='Avg_Porcentaje_Costo')

#  result
print("Porcentaje del costo total incurrido en las autorizaciones respecto a la cotización de cada afiliado:")
print(merged_data)

"""
f)	Calcular cuánto ingreso se espera recibir por concepto de cotizaciones durante el año 2024, suponiendo que se conservan
todos los afiliados y que se aplica un incremento salarial de 11% para los afiliados que devengan $2.000.000 o menos, 
9% para los que devengan entre $2.000.001 y $2.500.000 y 6% para los que devengan más de $2.500.000
"""

# Step 1: Apply salary increments
def calculate_new_salary(salary):
    if salary <= 2000000:
        return salary * 1.11  # 11% increase
    elif 2000001 <= salary <= 2500000:
        return salary * 1.09  # 9% increase
    else:
        return salary * 1.06  # 6% increase

df_filtered['Nuevo_Salario'] = df_filtered['salario'].apply(calculate_new_salary)

# Step 2: Calculate new contributions (12.5% of the new salary)
df_filtered['Cotizacion'] = df_filtered['Nuevo_Salario'] * 0.125

# Step 3: Calculate annual contributions
df_filtered['Cotizacion_Anual'] = df_filtered['Cotizacion'] * 12

# Step 4: Calculate total expected income from contributions
total_expected_income = df_filtered['Cotizacion_Anual'].sum()

# result
print("Ingreso total esperado por concepto de cotizaciones durante el año 2024:")
print(f"${total_expected_income:,.2f}")
from dazer_methods import Dazer
from uncertainties import unumpy
from collections import OrderedDict
from pylatex import Package, NoEscape
from numpy import isnan
from pandas import isnull
import pandas as pd
import numpy as np
import uncertainties as un
from uncertainties.umath import pow as umath_pow, log10 as umath_log10, exp as umath_exp, isnan as un_isnan

dz = Dazer()

#Load observational data
bayes_catalogue_df_address = '/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_BayesianResults.txt'
bayes_catalogue_df = pd.read_csv(bayes_catalogue_df_address, delim_whitespace=True, header=0, index_col=0)

#Define data to load
ext_data = ''
pdf_address = '/home/vital/Dropbox/Astrophysics/Thesis/tables/bayes_AbundancesTable'

#Headers
headers_dic = OrderedDict()
headers_dic['HeI_HI']   = r'$\nicefrac{He}{H}$'
headers_dic['Ymass_O']  = r'$Y_{\left(\nicefrac{O}{H}\right)}$'
headers_dic['Ymass_S']  = r'$Y_{\left(\nicefrac{S}{H}\right)}$'
headers_dic['OI_HI']    = r'$12 + log\left(\nicefrac{O}{H}\right)$'
headers_dic['NI_HI']    = r'$12 + log\left(\nicefrac{N}{H}\right)$'
headers_dic['SI_HI']    = r'$12 + log\left(\nicefrac{S}{H}\right)$'

properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
headers_format = ['HII Galaxy'] + headers_dic.values()

#Create a new list for the different entries
metals_list = properties_list[:]

del metals_list[metals_list.index('HeI_HI' + ext_data)]
del metals_list[metals_list.index('Ymass_O' + ext_data)]
del metals_list[metals_list.index('Ymass_S' + ext_data)]

#Generate pdf
# dz.create_pdfDoc(pdf_address, pdf_type='table')
# dz.pdfDoc.packages.append(Package('nicefrac'))
# dz.pdfDoc.packages.append(Package('pifont'))
# dz.pdfDoc.append(NoEscape(r'\newcommand{\cmark}{\ding{51}}')) 
# dz.pdfDoc.append(NoEscape(r'\newcommand{\xmark}{\ding{55}}'))

# ['OI_HI_emis2nd', 'NI_HI_emis2nd', 'SI_HI_emis2nd']
# catalogue_df[metal_x].notnull()

#Set the pdf format
dz.pdf_insert_table(headers_format)

print properties_list

for objName in bayes_catalogue_df.index:

    entry_name   = '{}'.format(bayes_catalogue_df.loc[objName].quick_index)

    if entry_name not in ['SHOC588', 'SHOC592', 'SHOC036', 'SHOC575', 'SHOC579', 'SHOC220']:

        objData = bayes_catalogue_df.loc[objName]
        row = [entry_name]

        for param in properties_list:
            param_value = objData[param]
            param_err   = objData[param + '_err']
            param_un    = un.ufloat(param_value, param_err)

            if param not in ['HeI_HI', 'Ymass_O', 'Ymass_S']:
                param_un = 12 + umath_log10(param_un)

            if np.isnan(param_un.nominal_value):
                param_un = np.nan

            row.append(param_un)

    dz.addTableRow(row, last_row = False if bayes_catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)


    # regressions_employed = []
    # for element in ['O', 'N', 'S']:
    #     validity_entry = catalogue_df.loc[objName, element + '_valid']
    #     element_abundance_key = '{}I_HI_emis2nd'.format(element)
    #     element_abundance_check = isnull(catalogue_df.loc[objName, element_abundance_key])
    #     print objName, element, element_abundance_check
    #     if element_abundance_check is False:
    #         if (validity_entry not in ['ignored', 'NO_excess', 'Wide Component']):
    #             regressions_employed.append(element)
    #     else:
    #         print 'Fallo', objName, element
    # name_superscript = r'\textsuperscript{{{regrens}}}'.format(regrens = ', '.join(regressions_employed))
    #
    # entry_name = r'{text}{expo}'.format(text=catalogue_df.loc[objName].quick_index, expo=name_superscript)
    #
    # objData         = catalogue_df.loc[objName]
    # abundValues     = objData[metals_list].values
    # objData[metals_list] = 12.0 + unumpy.log10(abundValues)
    #
    # HeI_HI_entry    = dz.format_for_table(catalogue_df.loc[objName, 'HeII_HII_from_O' + ext_data], rounddig=3, rounddig_er=2)
    # Ymass_O_entry   = dz.format_for_table(catalogue_df.loc[objName, 'Ymass_O' + ext_data], rounddig=3, rounddig_er=2)
    # Ymass_S_entry   = dz.format_for_table(catalogue_df.loc[objName, 'Ymass_S' + ext_data], rounddig=3, rounddig_er=2)
    #
    # print objName, objData[['OI_HI' + ext_data]].values, objData[['OI_HI' + ext_data]].isnull().values.any(), regressions_employed
    #
    # row             = [entry_name] + [HeI_HI_entry, Ymass_O_entry, Ymass_S_entry]
    # row             += list(objData[['OI_HI' + ext_data, 'NI_HI' + ext_data, 'SI_HI' + ext_data]].values)
    #
    # dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)

# dz.generate_pdf()   
dz.generate_pdf(output_address=pdf_address)



# from dazer_methods import Dazer
# from uncertainties import unumpy
# from collections import OrderedDict
# from pylatex import Package, NoEscape
# 
# #Import library object
# dz = Dazer()
# 
# #Load observational data
# catalogue_df = dz.load_excel_DF('/home/vital/Dropbox/Astrophysics/Data/WHT_observations/WHT_Galaxies_properties.xlsx')
# dz.quick_indexing(catalogue_df)
# 
# #Define data to load
# ext_data        = '_emis2nd'
# pdf_address     = '/home/vital/Dropbox/Astrophysics/Papers/Yp_AlternativeMethods/tables/AbundancesTable'
# 
# #Headers
# headers_dic = OrderedDict()
# headers_dic['HeI_HI']   = r'$\nicefrac{He}{H}$'
# headers_dic['Ymass_O']  = r'$Y_{\left(\nicefrac{O}{H}\right)}$'
# headers_dic['Ymass_S']  = r'$Y_{\left(\nicefrac{S}{H}\right)}$'
# headers_dic['OI_HI']    = r'$12 + log\left(\nicefrac{O}{H}\right)$'
# headers_dic['NI_HI']    = r'$12 + log\left(\nicefrac{N}{H}\right)$'
# headers_dic['SI_HI']    = r'$12 + log\left(\nicefrac{S}{H}\right)$'
# headers_dic['He-O']   = r'$He-O$'
# headers_dic['He-N']   = r'$He-N$'
# headers_dic['He-S']   = r'$He-S$'
# 
# properties_list = map(( lambda x: x + ext_data), headers_dic.keys())
# headers_format  = ['HII Galaxy'] + headers_dic.values()
# 
# #Create a new list for the different entries
# metals_list   = properties_list[:]
# 
# del metals_list[metals_list.index('HeI_HI' + ext_data)]
# del metals_list[metals_list.index('Ymass_O' + ext_data)]
# del metals_list[metals_list.index('Ymass_S' + ext_data)]
# del metals_list[metals_list.index('He-O' + ext_data)]
# del metals_list[metals_list.index('He-N' + ext_data)]
# del metals_list[metals_list.index('He-S' + ext_data)]
# 
# #Generate pdf
# # dz.create_pdfDoc(pdf_address, pdf_type='table')
# # dz.pdfDoc.packages.append(Package('nicefrac'))
# # dz.pdfDoc.packages.append(Package('pifont'))
# # dz.pdfDoc.append(NoEscape(r'\newcommand{\cmark}{\ding{51}}')) 
# # dz.pdfDoc.append(NoEscape(r'\newcommand{\xmark}{\ding{55}}')) 
# 
# #Set the pdf format
# dz.pdf_insert_table(headers_format)
# 
# for objName in catalogue_df.loc[dz.idx_include].index:
#     
#     entry_name      = '{slash}href{{{url}}}{{{text}}}'.format(slash='\\',url=catalogue_df.loc[objName].SDSS_Web,text=catalogue_df.loc[objName].quick_index).replace('&','\&')
#     
#     objData         = catalogue_df.loc[objName]
#     abundValues     = objData[metals_list].values
#     objData[metals_list] = 12.0 + unumpy.log10(abundValues)
#     
#     HeI_HI_entry    = dz.format_for_table(catalogue_df.loc[objName, 'HeII_HII_from_O' + ext_data], rounddig=3, rounddig_er=2)
#     Ymass_O_entry   = dz.format_for_table(catalogue_df.loc[objName, 'Ymass_O' + ext_data], rounddig=3, rounddig_er=2)
#     Ymass_S_entry   = dz.format_for_table(catalogue_df.loc[objName, 'Ymass_S' + ext_data], rounddig=3, rounddig_er=2)
#     
#     row             = [entry_name] + [HeI_HI_entry, Ymass_O_entry, Ymass_S_entry]
#     row             += list(objData[['OI_HI' + ext_data, 'NI_HI' + ext_data, 'SI_HI' + ext_data]].values)
#     
#     for element in ['O', 'N', 'S']:
#         validity_entry = catalogue_df.loc[objName, element + '_valid']
#         if validity_entry not in ['ignored', 'NO_excess', 'Wide Component']:
#             entry = '\ding{51}'
#         else:
#             entry = '\ding{55}'
#         row += [entry]
#             
#     dz.addTableRow(row, last_row = False if catalogue_df.index[-1] != objName else True, rounddig=3, rounddig_er=1)
# 
# # dz.generate_pdf()   
# dz.generate_pdf(output_address=pdf_address)

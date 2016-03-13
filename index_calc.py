# a function to calculate indices 

#uses avgflux
# filename is the .txt file of indices with name,startw numerator,endw numerator, startw dem, endw dem as
#defined in allers 2013 

import pylab
import pandas as pd
import BDdb
import avgflux
import math


#dfspec again is a dataframe of all the bdnyc spectra 

def index_2inputs(dfspec,i, filename):

	dfindices = pd.read_csv(filename,names =['index_name','startw_num','endw_num','startw_dem','endw_dem'])
	dfspec_indexcalc = pd.DataFrame(dfindices['index_name'],columns=['index_name'])
	dfspec_indexcalc['dfspec_iloc'] = None
	dfspec_indexcalc['index_value'] = None
	dfspec_indexcalc['index_value_err'] = None
	dfspec_indexcalc['avgflux_top'] = None
	dfspec_indexcalc['avgflux_bottom'] = None
	dfspec_indexcalc['avgflux_top_err'] = None
	dfspec_indexcalc['avgflux_bottom_err'] = None
	
	
	#right now only for NIR	

	if dfspec['regime'][i] == 'NIR':
		for j in dfindices.index:
			avgflux_top    = avgflux.avgflux(dfindices['startw_num'][j],dfindices['endw_num'][j],dfspec,i)
			avgflux_bottom = avgflux.avgflux(dfindices['startw_dem'][j],dfindices['endw_dem'][j],dfspec,i)
					
			if avgflux_top != -444:
				dfspec_indexcalc['dfspec_iloc'][j] = i
				dfspec_indexcalc['avgflux_top'][j] = avgflux_top[0]
				dfspec_indexcalc['avgflux_bottom'][j] = avgflux_bottom[0]
				dfspec_indexcalc['avgflux_top_err'][j] = avgflux_top[1]
				dfspec_indexcalc['avgflux_bottom_err'][j] = avgflux_bottom[1]
				dfspec_indexcalc['index_value'][j]     = avgflux_top[0] / avgflux_bottom[0]
				dfspec_indexcalc['index_value_err'][j] = dfspec_indexcalc['index_value'][j] * math.sqrt(((avgflux_top[1]/avgflux_top[0])**2)+ ((avgflux_bottom[1]/avgflux_bottom[0])**2))	
	
	return dfspec_indexcalc
	
	
	
def index_3inputs(dfspec,i, filename):
	
	#read in file
	dfindices = pd.read_csv(filename,names =['index_name','w_line','w_cont1','w_cont2','bandwidth'])
	
	dfspec_indexcalc = pd.DataFrame(dfindices['index_name'],columns=['index_name'])
	dfspec_indexcalc['dfspec_iloc'] = None
	dfspec_indexcalc['index_value'] = None
	dfspec_indexcalc['index_value_err'] = None
	dfspec_indexcalc['F_cont1'] = None
	dfspec_indexcalc['F_cont1_err'] = None
	dfspec_indexcalc['F_cont2'] = None
	dfspec_indexcalc['F_cont2_err'] = None
	dfspec_indexcalc['F_line'] = None
	dfspec_indexcalc['F_line_err'] = None

	
	#right now only for NIR	

	if dfspec['regime'][i] == 'NIR':
		
		for j in dfindices.index:
			
			F_cont1    = avgflux.avgflux(dfindices['w_cont1'][j] - dfindices['bandwidth'][j] ,dfindices['w_cont1'][j] + dfindices['bandwidth'][j],dfspec,i)

			F_cont2    = avgflux.avgflux(dfindices['w_cont2'][j] - dfindices['bandwidth'][j] ,dfindices['w_cont2'][j] + dfindices['bandwidth'][j],dfspec,i)

			F_line    = avgflux.avgflux(dfindices['w_line'][j],dfindices['w_line'][j] + dfindices['bandwidth'][j],dfspec,i)
					
			if F_cont1 != -444:
				dfspec_indexcalc['dfspec_iloc'][j] = i
				dfspec_indexcalc['F_cont1'][j] = F_cont1[0]
				dfspec_indexcalc['F_cont2'][j] = F_cont2[0]
				dfspec_indexcalc['F_line'][j] = F_line[0]
				dfspec_indexcalc['F_cont1_err'][j] = F_cont1[1]
				dfspec_indexcalc['F_cont2_err'][j] = F_cont2[1]
				dfspec_indexcalc['F_line_err'][j] = F_line[1]
				
				
				#A and B as definied as the const. terms in front of flux continuums in allers 2013 eqn (1)
				 
				A = (dfindices['w_line'][j] - dfindices['w_cont1'][j])/(dfindices['w_cont2'][j] - dfindices['w_cont1'][j])
				
				B = (dfindices['w_cont2'][j] - dfindices['w_line'][j])/(dfindices['w_cont2'][j] - dfindices['w_cont1'][j])
				
				dfspec_indexcalc['index_value'][j] = ( (A * F_cont2[0]) + ( B * F_cont1[0])) / F_line[0]   
				
				#error calculated by propagation of errors 
				#num_err is the error of the numerator term in allers 2013 eqn (1)
				num_err = math.sqrt((A**2)*(F_cont2[1]**2) + (B**2)*(F_cont1[1]**2)) 
				
				dfspec_indexcalc['index_value_err'][j] = dfspec_indexcalc['index_value'][j] * math.sqrt(((F_cont2[1]**2)/(F_cont2[0]**2)) + ((F_cont1[1]**2)/(F_cont1[0]**2)))	
	
	return dfspec_indexcalc
	
	
	
	
	
		

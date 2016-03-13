#!/usr/bin/python

import pylab
import pandas as pd
import matplotlib.pyplot as pl
from matplotlib.pyplot import *
import BDdb
import avgflux
import numpy.polynomial.polynomial as poly
import index_calc
#db call
db = BDdb.get_db('/home/erini/BDNYC/BDNYCdb/BDNYC.db')

#lets call all of our spec into a pandas dataframe, dfspec in essence is all of the spectra table in the bdnyc database

dfspec=pd.DataFrame(data=db.query.execute("SELECT * FROM spectra").fetchall(), columns=['id','source_id','wavelength','wavelength_units','flux','flux_units','unc','snr','wavelength_ord','regime', 'publication_id','obs_date','instrument_id','telescope_id','mode_id','airmass','filename', 'comment', 'header'])


#add a few more columns

dfindex = pd.DataFrame(columns=['dfspec_iloc','index_name','index_value','index_value_err','avgflux_top','avgflux_top_err','avgflux_bottom','avgflux_bottom_err'])





dfspec['H20_index'] = None
dfspec['H20_index_err'] = None
dfspec['H20D_index'] = None
dfspec['H20D_index_err'] = None
dfspec['H20-1_index'] = None
dfspec['H20-1_index_err'] = None
dfspec['H20-2_index'] = None
dfspec['H20-2_index_err'] = None

dfspec['H20_avgflux_top'] = None
dfspec['H20_avgflux_top_err'] = None
dfspec['H20_avgflux_bot'] = None
dfspec['H20_avgflux_bot_err'] = None
dfspec['H20D_avgflux_top'] = None
dfspec['H20D_avgflux_top_err'] = None
dfspec['H20D_avgflux_bot'] = None
dfspec['H20D_avgflux_bot_err'] = None



dfspec['spectral_type']= 0.


dfspec_new =dfspec

#lets do a quick plot
pl.plot(dfspec['wavelength'][0],dfspec['flux'][0],'b')
#let's say you want a quick plot of some source_id you know, e.g.
sourceid = 12
pl.plot(dfspec['wavelength'][sourceid],dfspec['flux'][sourceid],'b')

#pandas allows you to sort or search by any index or condition you can imagine seamless and importantly, fast!




#function call


#for now lets pick a random source id, you can use an sql query to get a more specified list of source ids 
source_id = 0

#here is where you call the indicesto be calculated file, note the format 
filename='grav_sensitive_indices.txt'

#reading it into another df
dfindices = pd.read_csv(filename,names =['index_name','w_line','w_cont1','w_cont2','bandwidth'])

#function call, index_calc, uses avfflux
a = index_calc.index_3inputs(dfspec,source_id,filename)







#overplot all the index values

for j in dfindices.index: 
	xtop=(dfindices['startw_num'][j],dfindices['endw_num'][j])
	ytop = (a['avgflux_top'][j],a['avgflux_top'][j])
	
	pl.plot(xtop,ytop,'b',color='black')
	pl.fill_between(xbottom,ybottom[0]-a['avgflux_top_err'][j],ybottom[0]+a['avgflux_top_err'][j],color='red')
	pl.annotate(str(dfindices['index_name'][j]),(xtop[0]+.1e-14,ytop[0]+.1e-14))	
		
	xbottom=(dfindices['startw_dem'][j],dfindices['endw_dem'][j])
	ybottom = (a['avgflux_bottom'][j],a['avgflux_bottom'][j])
	pl.plot(xbottom,ybottom,'b',color='black')
	pl.fill_between(xbottom,ybottom[0]-a['avgflux_bottom_err'][j],ybottom[0]+a['avgflux_bottom_err'][j],color='red')
	pl.annotate(str(dfindices['index_name'][j]),(xbottom[0]+.1e-14,ybottom[0]+.1e-14))



pl.title('Avg flux for grav sensitive indices for a random BDNYCdb spec')

pl.show()


#lotta extra stuff going on down below





['index_name','w_line','w_cont1','w_cont2','bandwidth']

pl.plot(dfspec['wavelength'][source_id],dfspec['flux'][source_id],'b')

color = ['red','green','blue','orange','purple']

for j in dfindices.index: 
	wavelength=(dfindices['w_cont1'][j],dfindices['w_cont2'][j],dfindices['w_line'][j])
	flux = (a['F_cont1'][j],a['F_cont2'][j],a['F_line'][j])
	pl.scatter(wavelength[0],flux[0],color=color[j])
	pl.scatter(wavelength[1],flux[1],color=color[j])
	pl.scatter(wavelength[2],flux[2],color=color[j])

	
pl.show()	
	
pl.fill_between(wavelength[0],flux[0]-a['F_cont1_err'][j],flux[0]+a['F_cont1_err'][j])
pl.fill_between(wavelength[1],flux[1]-a['F_cont2_err'][j],flux[1]+a['F_cont2_err'][j])
pl.fill_between(wavelength[2],flux[2]-a['F_line_err'][j],flux[2]+a['F_line_err'][j])
	
	
	
	
	pl.annotate(str(dfindices['index_name'][j]),(xtop[0]+.1e-14,ytop[0]+.1e-14))	
		
	xbottom=(dfindices['startw_dem'][j],dfindices['endw_dem'][j])
	ybottom = (a['avgflux_bottom'][j],a['avgflux_bottom'][j])
	pl.plot(xbottom,ybottom,'b',color='black')
	pl.fill_between(xbottom,ybottom[0]-a['avgflux_bottom_err'][j],ybottom[0]+a['avgflux_bottom_err'][j],color='red')
	pl.annotate(str(dfindices['index_name'][j]),(xbottom[0]+.1e-14,ybottom[0]+.1e-14))



pl.title('Avg flux for H20 index for a random BDNYCdb spec')

pl.show()

















['dfspec_iloc','index_name','index_value','index_value_err','avgflux_top','avgflux_top_err','avgflux_bottom','avgflux_bottom_err'] 

for i in dfspec.index:
	
	#df of index c
	a = index_calc.index_oplot(dfspec,i,'H20_indices.txt')
	 
	print i
	












#lets hard code some allers mentioned indices

#H2O

H2O_num = [1.550,1.560]
H2O_den = [1.492, 1.502]

#H20D

H2OD_num = [1.951,1.977]
H2OD_den = [2.062,2.088]

#H20-1

H2O-1_num = [1.335,1.345]
H2O-1_den = [1.295,1.305]

#H20-2

H2O-1_num = [2.035,2.045]
H2O-1_den = [2.145,2.155]

#ok lets do a test, for all the spectra in the db, that are NIR and have units of microns get the H20 index and plot it vs. the spec type in the db


#H20 index
for i in dfspec.index:
	
	if dfspec['source_id'][i]:
		
		if dfspec['regime'][i] == 'NIR':
			spectral_type = db.query.execute("SELECT spectral_type FROM spectral_types WHERE source_id={}".format(dfspec['source_id'][i])).fetchone()
		
			#H20 index
			num1 = avgflux.avgflux(H2O_num[0],H2O_num[1] , dfspec,i)
			if num1 == -444:
				dfspec['spectral_type'][i] = -444
				dfspec['H20_index'][i]     = -444
			else:
				num2 = avgflux.avgflux(H2O_den[0],H2O_den[1] , dfspec,i)	
				H20_index = num1[0]/num2[0]	
				H20_index_err = H20_index*math.sqrt(((num1[1]/num1[0])**2)+ ((num2[1]/num2[0])**2))
				dfspec['H20_index'][i] = H20_index
				dfspec['H20_index_err'][i] = H20_index_err
				if not spectral_type:
					dfspec['spectral_type'][i] = -444
				else:
					spectral_type=list(spectral_type)
					spectral_type=spectral_type[0]
					dfspec['spectral_type'][i] = spectral_type
		else:
			dfspec['spectral_type'][i] = -444
			dfspec['H20_index'][i]     = -444
		
			
	print "Index: ", i	

#H20D index
for i in dfspec.index:
	
	if dfspec['source_id'][i]:
		
		if dfspec['regime'][i] == 'NIR':
			spectral_type = db.query.execute("SELECT spectral_type FROM spectral_types WHERE source_id={}".format(dfspec['source_id'][i])).fetchone()
		
			#H20 index
			num1 = avgflux.avgflux(H2OD_num[0],H2OD_num[1] , dfspec,i)
			if num1 == -444:
				dfspec['spectral_type'][i] = -444
				dfspec['H20D_index'][i]     = -444
			else:
				num2 = avgflux.avgflux(H2OD_den[0],H2OD_den[1] , dfspec,i)	
				H20_index = num1[0]/num2[0]	
				H20_index_err = H20_index*math.sqrt(((num1[1]/num1[0])**2)+ ((num2[1]/num2[0])**2))
				dfspec['H20D_index'][i] = H20_index
				dfspec['H20D_index_err'][i] = H20_index_err
				if not spectral_type:
					dfspec['spectral_type'][i] = -444
				else:
					spectral_type=list(spectral_type)
					spectral_type=spectral_type[0]
					dfspec['spectral_type'][i] = spectral_type
		else:
			dfspec['spectral_type'][i] = -444
			dfspec['H20_index'][i]     = -444
		
			
	print "Index: ", i	
		


#doing a polyfit of the scatter plot of type vs. index

#getting rid of annoying abnormalities or gravity index
dfspec['spectral_type'][dfspec['spectral_type'] == 'XX'] = None 
dfspec['spectral_type'][dfspec['spectral_type'] == '12.0J'] = 12.0 
dfspec['spectral_type'][dfspec['spectral_type'] == '10.0J'] = 10.0 



h20index = dfspec['H20_index'][dfspec['spectral_type'] > 0.].values.astype('float')
spectype = dfspec['spectral_type'][dfspec['spectral_type'] > 0.].values.astype('float')
h20_index_err = dfspec['H20_index_err'][dfspec['spectral_type'] > 0.].values.astype('float')

#get rid of nans
g =  np.isfinite(h20index) & np.isfinite(spectype) 
x = spectype[g]
y = h20index[g]
yerr = h20_index_err[g]

#get rid of thing i need to debug
f = [y != 1]
x = x[f]
y = y[f]
yerr = yerr[f]

#get rid of bad data
h = [y > 0]
x = x[h]
y = y[h]
yerr = yerr[h]

#poly fit
coefs = poly.polyfit(x, y, 10)
ffit = poly.Polynomial(coefs)
x_new = np.linspace(min(x), max(x), num=len(x)*10)

#get rid of yerr nans and crazines
s = [(yerr != None) and (yerr < 1e10)]
x=x[s]
y=y[s]
yerr=yerr[s]


#plot call
pl.plot(x_new, ffit(x_new))
pl.plot(x,y,'.')
pl.errorbar(x,y,yerr=yerr,linestyle='None')


pl.title('H20 Index vs Spectral Type of BDNYC db - Allers Range ')
pl.show()

#allers range

k = [(x >= 4.0) & (x <= 19.0)]
x=x[k]
y=y[k]
yerr=yerr[k]

coefs = poly.polyfit(x, y, 10)
ffit = poly.Polynomial(coefs)
x_new = np.linspace(6., 19., num=len(x)*10)

pl.plot(x_new, ffit(x_new))
pl.plot(x,y,'.')
pl.errorbar(x,y,yerr=yerr,linestyle='None')

if x > 2.:
	pl.plot(x,y,'.')


pl.title('H20 Index vs Spectral Type of BDNYC db - Allers Range ')
pl.show()








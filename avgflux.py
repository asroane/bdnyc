#!/usr/bin/python

#erini's pythonian version of kelle's avgflux.pro

#to be used in conjuction with indices_oplot.py or anyother spec dataframes
import pylab
import numpy as np
import pandas as pd
import math
import BDdb


'''
Inputs to functions:

startw:
	type: float
	Beginning wavelength of index to calculate avg flux for

endw:
	type: float
	End wavelength of index to calculate avg flux for

dfspec:
	type: dataframe
	Data frame of all bdnyc spectra gathered in an sql query call (see indices_oplot.py)

'''



def avgflux(startw, endw, dfspec,i):
	avgflux   = -444
	sigflux   = -444
	numpixels = -444
	#lets replace zeroes with NaNs, to not mess up min and max conditions
	dfspec['wavelength'][i][dfspec['wavelength'][i] == 0.0] = None	
	if max(dfspec['wavelength'][i]) > startw and min(dfspec['wavelength'][i]) < endw: 
	
		b = dfspec['wavelength'][i][dfspec['wavelength'][i] >= startw]
		pix_scale=b[0+1]-b[0]
		a = dfspec['wavelength'][i][(dfspec['wavelength'][i]+pix_scale/2 >= startw) & (dfspec['wavelength'][i]-pix_scale/2 <= endw)]
		wavelength = a
		flux= dfspec['flux'][i][(dfspec['wavelength'][i]+pix_scale/2 >= startw) & (dfspec['wavelength'][i]-pix_scale/2 <= endw)]
		
		if dfspec['unc'][i] == None: 
			print "No sigma spec"
			dfspec['unc'][i] = np.zeros(len(wavelength))
			sigma= dfspec['unc'][i]
		elif dfspec['unc'][i][0] != 0.:
			sigma= dfspec['unc'][i][(dfspec['wavelength'][i]+pix_scale/2 >= startw) & (dfspec['wavelength'][i]-pix_scale/2 <= endw)]
		else:
			print "No sigma spec"
			dfspec['unc'][i] = np.zeros(len(wavelength))
			sigma= dfspec['unc'][i]
			
		num_pixels = len(wavelength)
		first = 0
		last = num_pixels - 1
		if num_pixels > 1:
			#determine the fractional pixel value for the pixels on the edge of the region
			frac1 = (wavelength[first] + pix_scale/2 - startw) / pix_scale
			frac2 = (endw - (wavelength[last] - pix_scale/2)) / pix_scale
			#sum flux
			sumflux = 0.
			sumsigma2 = 0.
			
			for k in range(last+1):
				if k == first: 
					pixflux = frac1*flux[k] 
				elif k == last: 
					pixflux = frac2*flux[k]
				else:
					pixflux = flux[k]
								
				sumflux = sumflux + pixflux
				#print sumflux
				sigflux2 = sigma[k]**2
				sumsigma2 = sumsigma2 + sigflux2
				#print, sumsigma2
			
				#print, sumflux, pixflux
			
			#print "sumflux: ", sumflux
			realpix = num_pixels - 2 + frac1 + frac2 
			avgflux = sumflux/realpix
			#print "avgflux: ", avgflux
				#use the sample variance if the sigma
			#spectrum is not present to estimate uncertainty
			if len(sigma) > 1:
				sigflux=math.sqrt(sumsigma2)/realpix 
			else:
				sigflux= math.sqrt((((flux[first:last] - mean(flux[first:last])).sum())**2)/(num_pixels-1))/math.sqrt(num_pixels)
			#end npixels > 1
		if num_pixels == 1:
			frac = (endw-startw)/pix_scale
			avgflux=frac*flux[0]
			sigflux = frac*.1*flux[0]
		
		#MEDIAN DOENST WORK WELL for LOW RES
		# see p.33 of Ahra's notebook
	else:
		avgflux = -444
		sigflux = -444
		num_pixels = -444
		
	#print "avgflux: ",avgflux,"sigflux: ",sigflux,"num_pixels: ",num_pixels
	return[avgflux,sigflux,num_pixels]

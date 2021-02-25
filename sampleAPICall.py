#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:37:11 2020

@author: lukas
"""

import requests

#%%

data = { 'query': """Using satellite data on deforestation and weather in Malawi and
        linking those datasets with household survey datasets, we estimate the causal
        effect of deforestation on access to clean drinking water. In the existing
        literature on forest science and hydrology, the consensus is that
        deforestation increases water yield. In this study, we directly examine the
        causal effect of deforestation on households’ access to clean drinking water.
        Results of the two-stage least-squares (2SLS) with cluster and time fixed-effect
        estimations illustrate strong empirical evidence that deforestation decreases
        access to clean drinking water. Falsification tests show that the possibility of
        our instrumental variable picking up an unobserved time trend is very unlikely.
        We find that a 1.0-percentage-point increase in deforestation decreases access
        to clean drinking water by 0.93 percentage points. With this estimated impact,
        deforestation in the last decade in Malawi (14%) has had the same magnitude of
        effect on access to clean drinking water as that of a 9% decrease in rainfall.
        """ }


#%%
response = requests.post('http://localhost:5000/', data=data)

result = response.text

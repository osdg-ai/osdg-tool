<img src="/assets/OSDG_new.png" alt="OSDG_Logo" width="200"/>

OSDG is an open-source tool that assigns labels to scientific content based on Sustainable Development Goals (SDGs). 

A version of the OSDG tool is available at [OSDG website](https://www.osdg.ai). There user can classify publications by inputting:
1) a single DOI,
2) multiple DOIs in one CSV file,
3) a text fragment.

**Check out our paper on ArXiv [OSDG -- Open-Source Approach to Classify Text Data by UN Sustainable Development Goals (SDGs)](https://arxiv.org/abs/2005.14569)**

A smaller version of the tool to classify text fragments is available at [Technote Docker Hub](https://hub.docker.com/r/technoteai/osdg) repository.

## Usage
The tool is uploaded to the Docker Hub repository. If you do not have docker installed on your system, please visit [Docker page](https://docs.docker.com/get-docker/) and follow the instructions to install docker on your OS.

To check docker installation run the following command on the terminal on your machine:
```bash
docker --version
```

To download the docker image :

```bash
docker pull osdg-ai/osdg-tool:latest
```

Then run the downloaded docker image

 ```bash
 docker run --name osdg-tool -p 5000:5000 --detach osdg-ai/osdg-tool:latest
 ```

Once container is started, it will be running on port 5000.
To verify that the container has started and works, visit [http://localhost:5000/](http://localhost:5000/)

or try the following Python query

```python
import requests

data = {'text': r"""Developing nations are faced with a two‐edged sword in the field of energy.
                   On the one hand the rising price of oil has reduced the potential for fossil fuel energy and eroded foreign exchange reserves in oil‐importing countries. 
                   At the same time deforestation may be causing increased prices or shortages of fuels such as fuelwood and charcoal. 
                   This paper reviews the most recent and sometimes controversial estimates of deforestation in developing countries and analyzes the relationship 
                   between deforestation and its probable causes. Three recent estimates of the rate of deforestation in developing countries 
                   between 1968 and 1978 are compared using rank order correlation. 
                   Two of the estimates, of closed forest and moist tropical forest, are in significant agreement but differ from a third estimate that includes 
                   open woodland and regenerating forest. Agreement is strong among all three sources for a restricted group of countries. 
                   A cross‐national analysis confirms the most frequently cited causes of deforestation. 
                   Deforestation from 1968–78 in 39 countries in Africa, Latin America, and Asia is significantly related to the rate of population growth 
                   over the period and to wood fuels production and wood exports in 1968; it is indirectly related to agricultural expansion and 
                   not related to the growth of per capita GNP. Results indicate that in the short term, deforestation is due to population growth and agricultural expansion, 
                   aggravated over the long term by wood harvesting for fuel and export.""",
        'detailed': False}

response = requests.post('http://localhost:5000/tag', json=data)

result = response.json()
print(result)
```

For multiple texts it is recommended to use `/tag_many` endpoint

```python
from .loaders import load_texts
import requests

my_list_of_texts = load_texts()

data = {'texts': my_list_of_texts,
        'detailed': False}

response = requests.post('http://localhost:5000/tag_many', json=data)

results = response.json()
```


If you are having trouble with any of the following steps, please contact our team at [info@osdg.ai](mailto:info@osdg.ai).

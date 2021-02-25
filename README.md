<img src="/img/OSDG_new.png" alt="OSDG_Logo" width="200"/>

OSDG is an open-source tool that assigns labels to scientific content based on Sustainable Development Goals (SDGs). 

A version of the OSDG tool is available at [OSDG website](https://www.osdg.ai). There user can classify publications by inputting:
1) a single DOI,
2) multiple DOIs in one CSV file,
3) a text fragment.

**Check out our paper on ArXiv [OSDG -- Open-Source Approach to Classify Text Data by UN Sustainable Development Goals (SDGs)](https://arxiv.org/abs/2005.14569)**

A smaller version of the tool to classify text fragments is available at [Technote Docker Hub](https://hub.docker.com/r/technoteai/osdg) repository.

## Usage

**NB! We recommend to run OSDG on a machine with at least 30 GB RAM. The tool may not start properly on a smaller machine.**
*This problem will be addressed in the upcoming release.*

The tool is uploaded to the Docker Hub repository. If you do not have docker installed on your system, please visit [Docker page](https://docs.docker.com/get-docker/) and follow the instructions to install docker on your OS.

To check docker installation run the following command on the terminal on your machine:
```bash
docker --version
```

To download the docker image :

```bash
docker pull technoteai/osdg
```

Then run the downloaded docker image

 ```bash
 docker run --name my-osdg -p 5000:5000 --detach technoteai/osdg:latest
 ```

The container takes about 2 minutes to fully start.Once it does, it will be running on port 5000.
To verify that the container has started and works, enter the following :

```bash
docker ps
```
If the container runs OK, please go to :

[http://localhost:5000/](http://localhost:5000/)

or try the following Python query

```python
import requests

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

response = requests.post('http://localhost:5000/search', data=data)

print( response.json() )
```

If you are having trouble with any of the following steps, please contact our team at [info@osdg.ai](mailto:info@osdg.ai).

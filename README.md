<img src="/img/OSDGlogo.png" alt="OSDG_Logo" width="300"/>


**OSDG** is an open-source tool that maps and connects activities to the UN Sustainable Development Goals (SDGs) by identifying SDG-relevant content in any text.
The OSDG tool is available free of charge at [OSDG.ai](https://www.osdg.ai/).

The tool supports the following types of input:

1. **Text fragments**
2. **PDF files**.


The system uses state-of-the-art neural **machine translation** models to translate the input into English. OSDG currently supports **15 languages**: English, Arabic, Danish, Dutch, Finnish, French, German, Italian, Korean, Polish, Portuguese, Russian, Spanish, Swedish, and Turkish.

For each query, we return a detailed breakdown of all SDGs found in the text, entitled the **OSDG Wheel**. You can learn more about it [here](https://osdg.ai/news/OSDG-launches-the-OSDG-Wheel-with-detailed-SDG-data-breakdowns).

## Methodology

OSDG 2.0 works in two stages. The first stage uses machine learning (ML) models, trained on the data collected via the OSDG Community Platform (CP). You can access this data through the [osdg-data](https://github.com/osdg-ai/osdg-data) repository. These models carry out the initial screening of texts and suggest the preliminary SDG labels. In the second stage, OSDG uses its ontology/keyword map to verify the initial labels. To assign a specific SDG label, **both the ML and ontology approaches must be in agreement**.

For a more detailed description of the methodology, please refer to **our paper on ArXiv**:

📘 [OSDG 2.0: a multilingual tool for classifying text data by UN Sustainable Development Goals (SDGs)](https://arxiv.org/abs/2211.11252)

## OSDG API

Are you conducting research on the SDGs, and aim to publish it in a scholarly journal, present at a conference, etc.?

Our API is **free** **for research purposes**. For access, please [contact us](https://osdg.ai/contact) with a short outline of your research and anticipated scope of content.

## ⚠️ Repository files

**OSDG 2.0** is not available on the repository due to the use of ML and ontology approaches and machine translation. To access the latest version of the tool, visit the [OSDG website](https://osdg.ai).

OSDG API is available free of charge for research teams, please [contact us](https://osdg.ai/contact) for more information.

🔴 **Please note:** At the moment, the files in this repository refer to a **legacy version of the tool, OSDG 1.0**.
You can use them to set up a legacy OSDG application via Docker. However, the results obtained may not correspond to the most recent version of the tool, OSDG 2.0.
For the highest quality results, please refer to the [online version of the tool](https://www.osdg.ai/), or consult us for API access.

## About the team

OSDG is a partnership between [PPMI](https://www.ppmi.lt/), [UNDP SDG AI Lab](https://sdgailab.org/), and a growing community of researchers led by [Dr. Nuria Bautista Puig](https://orcid.org/0000-0003-2404-0683).

import torch
import json
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config

model = T5ForConditionalGeneration.from_pretrained('t5-large')
tokenizer = T5Tokenizer.from_pretrained('t5-large')
device = torch.device('cpu')

text=""" President Trump signed an executive order that enables federal agencies to waive environmental review for infrastructure projects such as highways and pipelines to speed the economic recovery. It weakens the National Environmental Policy Act (NEPA) that requires government agencies to conduct a review of potential environmental and public health impacts before a project is approved and enables local communities to weigh in. The executive order gives NEPA “flexibility” in emergency situations, and allows agencies to put aside normal environmental reviews and make alternative plans.

The EPA has announced that it will temporarily “exercise enforcement discretion” with regard to violations of environmental laws as a result of COVID-19. New guidelines enable companies to monitor themselves to determine if they are violating air and water quality regulations. In other words, entities unable to comply with regulations due to social distancing or shortage of workers will not be penalized. States and environmental groups are suing the EPA for abdicating its duty. Gina McCarthy, head of the EPA under the Obama administration, now president of the Natural Resources Defense Council, called it “an open license to pollute.”

One result of the EPA’s action is that manufacturing or energy production facilities, coal mines, industrial waste landfills and others can delay reporting of their greenhouse gas emissions. This emissions data is necessary to help the EPA assess its existing greenhouse gas regulations and determine if additional ones are necessary.

Using the pandemic as cover, President Trump is continuing his efforts to weaken environmental regulations. The EPA has proposed a new rule that would alter the cost-benefit formulas used in Clean Air Act regulations. “Co-benefits” such as improvements in public health from reducing pollution, will no longer be given as much weight in justifying regulations.

In addition, Trump signed another executive order opening up a marine conservation area off New England to commercial fishing. The Northeast Canyons and Seamounts Marine National Monument established by President Obama is a haven for endangered right whales and other vulnerable marine creatures.

The Pipeline and Hazardous Materials Safety Administration declared that it would exercise discretion in enforcing natural gas pipeline safety regulations during the pandemic. This could result in more methane (a greenhouse gas with 80 times more global warming potential than CO2 over a 20-year span) being emitted from leaking pipelines. The EPA estimates that the natural gas pipeline system was responsible for almost 13 percent of national methane emissions in 2018.
"""

def abstractive_summarizer(raw_text):

    print("hello")
    preprocess_text = raw_text.strip().replace("\n", "")
    t5_prepared_Text = "summarize:"+ preprocess_text
    # print ("original text preprocessed: \n", preprocess_text)

    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt", max_length=1024, truncation=True)

    # summmarize
    output = model.generate(tokenized_text,
                            num_beams=4,
                            length_penalty=80.0,
                            min_length=80,
                            max_length=600,
                            early_stopping=True)

    summary = tokenizer.decode(output[0])
    # print(summary)
    return summary;

    # Summarized output from above ::::::::::
    # the us has over 637,000 confirmed Covid-19 cases and over 30,826 deaths.
    # president Donald Trump predicts some states will reopen the country in april, he said.
    # "we'll be the comeback kids, all of us," the president says.
#print(abstractive_summarizer(text))
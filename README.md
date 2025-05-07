# tidbits

<img src="pics/Create Card.png" width=30%/><img src="pics/Review Card Hidden.png" width=30%/><img src="pics/Review Card Open.png" width=30%/>

Tidbits is a spaced repetition program that uses large language models to generate the questions.

## Why Use LLMs

Unlike traditional uses of spaced repetition systems the goal of tidbits is not perfect rote memorization. Instead the goal here is simply to remember the gist of something long term. Using an LLM to create the recall prompts means adding something to remember is as simple as CTRL-C, CTRL-V. 

Tidbits uses the FSRS algorithm to minimize the time spent reviewing information that is easily remembered and spend more time improving recall on information where recall is difficult.

## Question Prompt

Each piece of information used to create a flashcard is passed to the LLM with a system prompt provided in `prompts/question_prompt.txt`. Longer and more detailed prompts may provide better review questions at the expense of speed and or token usage. **Experimentation with new and different prompts is definitely recommended!**

## Setup

**Python >= 3.13 is required.**

1. Clone the repository
```
git clone https://github.com/holtmenzies/tidbits
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Install Ollama: 
    - Install directly to host machine:
    ```
    # install from https://ollama.ai
    ollama run gemma3:4b-it-qat
    ```
    - -OR- Install with Docker:
    ```
    docker exec -it ollama ollama run gemma3:4b-it-qat
    ```
    - **In either case** verify that ollama server is available at `http://localhost:11434`
    - *Here gemma3:4b-it-qat is used due to GPU constraints. Definitely consider using a larger model if you want / have the GPU resources*
4. Run the program!
```
python main.py
```
To exit simply close the GUI window.

## Using Different APIs

Currently tidbits is set up to work with an LLM server using Ollama. If you need a different model client in `model.py`: 
- implement a new class with `ModelClient` as a parent class
- Add that as an option in the constructor for the Model class
- Enter the appropriate parameters in model params in config.yaml.

## TODOs
- Implement async interface with LLM server
- Implement function to pause / delete cards
- Implement ability to update / change questions created by LLM
- Implement Tag generation
- Implement Title generation
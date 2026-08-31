#  Lycaon - Local Voice Assistant

A voice assistant that runs entirely on your machine, no cloud, no API keys. Uses a local LLM (Qwen, via Ollama) to understand commands and talk back.

Started this to learn about speech recognition, local LLMs, and tool-calling agents with LangChain. Hit a bunch of real problems along the way (models that don't support tool calling, slow responses, the model just making stuff up) and learned a lot fixing them.

## What it does

- Listens for a wake word ("Lycaon") and enters conversation mode
- Understands voice commands in Spanish
- Runs on a local LLM, no internet needed
- Can call tools, like checking the time in different cities
- Talks back instead of just printing text

## Note on language

Built for Spanish (speech recognition, wake word, responses). Code and comments are also in Spanish for now. To adapt it to another language, mainly change the `language='es-ES'` param in speech recognition and tweak the system prompt. PRs welcome.

## How it works

1. Mic listens in standby until it hears the wake word
2. Once triggered, records your next command
3. Command gets transcribed to text (Google Speech Recognition)
4. Text goes to the local Ollama model
5. If the command needs a tool (like time lookup), the model calls it
6. Response gets converted back to speech with pyttsx3

## Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running
- A model pulled in Ollama
- A working mic

## Install

\`\`\`bash
git clone https://github.com/your-username/lycaon.git
cd lycaon

python -m venv assistant-env
# Windows:
assistant-env\Scripts\activate
# Mac/Linux:
source assistant-env/bin/activate

pip install -r requirements.txt
cp .env.example .env
ollama pull qwen2:1.5b
\`\`\`

## Run

\`\`\`bash
python main.py
\`\`\`

Say "Lycaon", wait for the confirmation, then give your command.

## Lessons learned

**Not every model supports tools.** Some small Ollama models throw a `does not support tools` error. Either switch to a model that does (e.g. `llama3.2:3b`) or skip the LangChain agent and handle commands manually.

**The model will make things up.** Asked it about today's financial markets once and it confidently gave me a made-up date and fake numbers. Local models have no internet access and no real sense of the current date — if you don't tell them to admit what they don't know, they'll fill the gap with something that sounds real but isn't. Fixed by adding the real date and explicit "admit when you don't know" instructions to the system prompt.

**Knowledge has a cutoff.** Qwen2, like any LLM, only knows what it was trained on. No way to get current info without hooking it up to external tools (web search, APIs), which this project doesn't do yet.

**Speech recognition can mishear the wake word.** Google Speech Recognition sometimes transcribed "Lycaon" as similar-sounding words. If that happens, add those variants to the accepted list or pick an easier wake word.

## Project structure

\`\`\`
lycaon/
├── main.py
├── ai_agent.py
├── voice_recognition.py
├── text_to_speech.py
├── tools/
│   └── time_tool.py
├── .env.example
└── requirements.txt
\`\`\`

## Ideas for later

- Internet access for real-time info (weather, news)
- Multi-language support
- GUI instead of console only
- More tools (reminders, calculations, device control)

## License

MIT
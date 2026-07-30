#AIAgent
agent_project/
│
├── agent/
│   ├── __init__.py
│   ├── agent.py          # main agent loop
│   ├── planner.py        # prompt + decision logic
│   ├── memory.py         # context assembly
│   └── state.py          # state object
│
├── tools/
│   ├── __init__.py
│   ├── base.py           # tool interface
│   ├── filesystem.py    # example tool
│   └── network.py       # example tool
│
├── prompts/
│   └── system.txt       # agent identity + rules
│
├── config/
│   └── settings.py
│
├── main.py               # entry point
└── README.md

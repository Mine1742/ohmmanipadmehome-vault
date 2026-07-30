
- **Product thinking** defines the scope and shapes agent behavior. This involves:
    - Writing prompts that drive agent behavior (often hundreds or thousands of lines). Good communication and writing skills are key here.
    - Deeply understanding the "job to be done" that the agent replicates
    - Defining evaluations that test whether the agent performs as intended by the “job to be done”
- **Engineering** builds the infrastructure that makes agents production-ready. This involves:
    - Writing tools for agents to use
    - Developing UI/UX for agent interactions (with streaming, interrupt handling, etc.)
    - Creating robust runtimes that handle durable execution, human-in-the-loop pauses, and memory management.
- **Data science** measures and improves agent performance over time. This involves:
    - Building systems (evals, A/B testing, monitoring etc.) to measure agent performance and reliability
    - Analyzing usage patterns and error analysis (since agents have a broader scope of how users use them than traditional software)


Here’s where the practice typically shows up:

- **Software engineers and ML engineers** writing prompts and building tools for agents to use, tracing why an agent made specific tool calls, and refining the underlying models
- **Platform engineers** building agent infrastructure that handles durable execution and human-in-the-loop workflows
- **Product managers** writing prompts, defining agent scope, and ensuring the agent solves the right problem
- **Data scientists** measuring agent reliability and identifying opportunities for improvement

things that make agents useful also make them behave differently than traditional software. This usually means that:

- **Every input is an edge case.** There's no such thing as a "normal" input when users can ask anything in natural language. When you type in “make it pop” or “do what you did last time but differently”, the agent (just like a human) can interpret the prompts in different ways.
- **You can’t debug the old way.** Because so much logic lives inside the model, you have to inspect each decision and tool call. Small prompt or config tweaks can create huge shifts in behavior.
- **“Working” isn’t binary.** An agent can have 99.99% uptime while still being off the rails and broken. There aren’t always simple yes/no answers to the questions that matter, like: is the agent making the right calls? Using tools the right way? Following the intent behind your instructions?

cadence for agent development that looks something like this:

- **Build your agent’s foundation.** Start with designing your agent's foundation, whether it's a simple LLM call with tools or a complex multi-agent system. Your architecture depends on how much workflow (deterministic step-by-step processes) versus agency (LLM-driven decisions) you need.
- **Test based on scenario you can imagine**. Test your agent against example scenarios to catch obvious issues with prompts, tool definitions, and workflows. Unlike traditional software where you can map out user flows, you can't anticipate every way users will interact with natural language input. Shift your mindset from "test exhaustively, then ship" to "test reasonably, ship to learn what actually matters.”
- **Ship to see real-world behavior.** Once you ship, you’ll immediately start seeing inputs you hadn’t considered and every production trace shows what your agent actually needs to handle.
- **Observe.** Trace every every interaction to see the full conversation, every tool called, and the exact context that informed each decision the agent made. Run evals over your production data to measure agent quality, whether you care about accuracy, latency, user satisfaction, or other criteria.
- **Refine**. Once you’ve identified patterns in what's failing, refine by editing prompts and modifying tool definitions. It’s all continuous, as you can add problematic cases back to your set of example scenarios for regression testing.
- **Repeat**. Ship your improvements and watch what’s changing in production. Each cycle teaches you something new about how users are interacting with your agent and what reliability actually means in your context.
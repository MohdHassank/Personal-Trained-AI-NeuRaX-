
# 🧠 NeuRaX : Personal AI Desktop Assistant



A voice-powered AI desktop assistant that understands natural language, reasons over user requests, and performs real actions on the computer.

NeuRaX is a Python-based personal AI assistant designed to bridge the gap between conversational AI and real-world desktop automation.

Instead of only generating text responses, NeuRaX can understand spoken commands, classify user intent, interact with AI models, perform desktop actions, search for real-time information, open applications, execute multiple tasks, and respond through both a graphical interface and voice.


## What Makes this diffrent?
Most AI chatbots stop at:

User → Question → AI → Answer

NeuRaX extends this workflow:


<img src="./assets/workflow.png" alt="Neurax Workflow" width="600">

## Features

### 🎙️ Natural Voice Interaction

- Speak naturally instead of typing commands.
- NeuRaX converts speech into text and processes it through its AI intent pipeline.

**Example:**

> "Open Chrome and search Google Careers."

NeuRaX can interpret the request and execute the corresponding actions.

---

### 🧠 AI-Powered Intent Detection

NeuRaX doesn't directly send every command to the same model.

A dedicated intent layer analyzes each request and categorizes it into different execution paths:

- `general`
- `realtime`
- `open`
- `close`
- `play`
- `system`
- `content`
- `google search`
- `youtube search`

This allows the system to distinguish between different types of requests:

- **General question:**  
  > "What is artificial intelligence?"

- **Application command:**  
  > "Open Chrome."

- **Search command:**  
  > "Search Google Careers."

---

### 🤖 Conversational AI

For general questions and conversations, NeuRaX uses an LLM-powered chatbot pipeline.

**Example:**

**User:**
> "What is machine learning?"

**NeuRaX:**
> Provides an AI-generated explanation.

The conversational layer is separated from the automation layer so that normal conversations don't unnecessarily trigger system actions.

---

### 🖥️ Desktop Automation

NeuRaX can interact with the user's desktop environment.

Current automation capabilities include:

- Opening applications
- Closing applications
- Opening Google Chrome
- Opening WhatsApp
- Searching Google
- Searching YouTube
- Playing requested content
- Executing system-level actions
- Running multiple detected actions from a single request

**Example:**

> "Open Chrome and search Google Careers."

NeuRaX can interpret this as multiple actions:

1. Open Chrome
2. Perform Google search

---

### 🔎 Real-Time Search

For queries requiring current information, NeuRaX can route the request through its real-time search pipeline instead of relying only on the LLM's static knowledge.

**Example:**

> "What is the latest information about AI?"

The system can route the query through its real-time search workflow before generating the final response.

---

### 🗣️ Text-to-Speech

NeuRaX doesn't only display responses. The generated response can also be converted back into speech.

```text
User Voice
    ↓
Speech → Text
    ↓
AI Processing
    ↓
Text Response
    ↓
Text → Speech
    ↓
🔊 NeuRaX speaks

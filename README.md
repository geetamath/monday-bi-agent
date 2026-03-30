#  Monday.com Business Intelligence Agent

> AI agent that answers natural language business questions about Monday.com data in seconds.

**[Live Demo](https://insight-engine--gsmvjp.replit.app/)** | 📖 **[Decision Log](DECISION_LOG.md)**

---

##  The Problem

Executives need quick answers across multiple Monday.com boards. Current process:
- Manually export data → Clean inconsistent formats → Run custom analysis → Deal with missing data

**This agent provides instant AI-powered insights through natural language queries.**

---

##  What It Does

-  Ask questions in plain English
-  Analyzes Work Orders & Deals data live from Monday.com
-  Handles messy real-world data (missing values, inconsistent formats)
-  Provides business insights, not just raw numbers
-  Real-time data — no hardcoded CSVs
-  Stores analysis history for reference

### Example Questions:
- "Which deals are most likely to close this quarter?"
- "What are the top 3 risks in current work orders?"
- "Show me high priority work orders needing immediate attention"
- "Which sectors are performing best?"
- "Give me a 5-line executive summary of our business health"

---

##  Screenshots

### Main Interface
![Dashboard](OUTPUT-UI/BI%20Agent-Output%20Screenshot.JPG)

### AI Analysis Output
![AI Insights](OUTPUT-UI/BI%20Agent-Analysis%20Output.JPG)

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React |
| Backend | Node.js + Express |
| AI Model | Groq API — Llama 3.3 70B |
| Data Source | Monday.com GraphQL API |
| Database | PostgreSQL (analysis history) |
| Hosting | Replit (always-on deployment) |

---

##  Architecture

```
User Question
     ↓
React Frontend
     ↓
Node.js API Gateway
     ↓
Monday.com GraphQL API (fetch live data)
     ↓
Smart Filter (limit to 15 relevant records)
     ↓
Groq AI — Llama 3.3 70B (analyze)
     ↓
Structured Business Insight → User
```

---

##  Quick Start

```bash
# Clone
git clone https://github.com/geetamath/monday-bi-agent.git
cd monday-bi-agent

# Install
npm install

# Configure .env
MONDAY_API_KEY=your_key
GROQ_API_KEY=your_key
WORK_ORDERS_BOARD_ID=your_id
DEALS_BOARD_ID=your_id

# Run
npm start
```

**Setup Details:**
1. Import CSVs to Monday.com as separate boards
2. Get API key: Monday.com → Developers
3. Get free Groq API key: console.groq.com
4. Copy board IDs from Monday.com board URLs

---

##  Key Engineering Decisions

**Why Groq?**
Free tier, fast inference (~1s response), no credit card needed. Llama 3.3 70B gives GPT-4 quality for BI queries.

**Why GraphQL?**
Flexible data fetching — only request the fields needed, reducing payload size significantly.

**Token Limit Challenge & Solution**
Monday.com boards had 500+ records (~60,000 tokens). Groq's limit is 12,000 tokens.

Solution: Implemented a smart pre-filter that scores each record by keyword relevance to the user's question, keeps only the top 15 matching records, strips empty fields, and truncates long text — reducing token usage from 60,000 to under 5,000 per request.

**Why direct API over MCP?**
Simpler debugging, better documentation, faster development for a time-constrained build.

See **[DECISION_LOG.md](DECISION_LOG.md)** for full technical decisions.

---

##  What I Learned

- AI prompt engineering for business intelligence use cases
- Handling real-world messy data (missing values, inconsistent formats)
- GraphQL API optimization and dynamic query building
- Token budget management for LLM API calls
- Building and deploying a full-stack AI product in 4–6 hours

---

##  Future Improvements

**Short-term:**
- Data visualisation (charts and trend graphs)
- Caching layer for repeated queries
- PDF export for leadership reports

**Long-term:**
- Predictive analytics (revenue forecasting)
- Natural language actions ("Create a work order for...")
- Fine-tuned model on company-specific terminology

---

##  Project Context

Built as a technical assignment demonstrating:
- AI agent development with real LLM integration
- Live API data fetching (no hardcoded data)
- Production-quality engineering under time pressure
- Full-stack deployment

**Assignment Requirements:**
- Dynamic Monday.com integration (no hardcoded data) 
- Handles messy data gracefully 
- Natural language understanding 
- Business intelligence insights 
- Leadership update preparation 

---

##  Contact

**Geeta Math**
📧 gsmvjp@gmail.com | 💼 [LinkedIn](https://www.linkedin.com/in/geeta-math-128874353/) | 🌐 [Portfolio](https://geetamath.github.io/portfolio/)

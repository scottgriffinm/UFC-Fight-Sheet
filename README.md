# UFC Fight Sheet Generator

A Python agent that automatically generates comprehensive fight sheets for UFC events scheduled for today. The agent uses web tools (Tavily search + webpage reader) to collect fighter information, statistics, and video links, then generates and saves a beautifully formatted markdown document.

## Features

- **Agent-Driven Workflow**: A tool-using agent autonomously plans, searches, extracts, compiles and saves the fight sheet
- **Event Detection**: Checks if there's a UFC event scheduled for today
- **Comprehensive Fighter Data**: Collects for each fighter:
  - Basic info (height, weight, age, reach, stance)
  - Betting odds
  - Striking stats (sig. strikes per minute, accuracy, etc.)
  - Grappling stats (takedown average, accuracy, submission average)
  - Fight records (overall, KO/TKO, submissions)
  - Last 5 fight results
- **Video Links**: Finds YouTube links to each fighter's recent fights with quality filtering (1000+ likes, no analysis/recap videos, must be freely viewable)
- **Web Search Integration**: Uses Tavily for search plus an HTML reader tool for extraction
- **Beautiful Output**: Generates a well-formatted markdown file with:
  - Event information and date
  - Fight-by-fight breakdowns
  - Side-by-side fighter comparisons
  - Organized statistics tables
  - Direct links to fight videos

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd UFC Fight Sheet
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with your API keys:
   ```env
   # OpenAI / xAI / Google Vertex AI / Anthropic as configured in `ufc_agent/models.yaml`
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   XAI_API_KEY=your_xai_api_key
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json

   # Tavily (for internet_search tool)
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Configure models** (optional):
   - Edit `ufc_agent/models.yaml` to customize which AI models are used by the agent.

## Usage

Run the agent application:
```bash
python ufc_fight_sheet.py
```

### Command Line Options

- `--last-n-fights N`: Hint to the agent to limit the number of fights to process to the last N fights in the event
  ```bash
  # Process only the last 5 fights (main event, co-main, and 3 prelims)
  python ufc_fight_sheet.py --last-n-fights 5

  # Process only the main event and co-main event
  python ufc_fight_sheet.py --last-n-fights 2
  ```

The agent will:
1. Determine today's date
2. Check for UFC events today
3. Collect detailed fight information (for all fights or limited subset)
4. Find video links for each fighter
5. Generate a markdown file named `ufc_fight_sheet_YYYYMMDD.md`

## Architecture

This project uses a LangChain tool-calling agent with the following key tools:
- `internet_search` (Tavily)
- `read_webpage` (direct + Jina Reader fallback)
- `get_today_date`
- `write_text_file`

The UFC-specific agent is built with a tailored system prompt to autonomously determine when the sheet is complete and to save the output to disk.

## Requirements

- Python 3.8+
- API keys for at least one supported AI provider (see `ufc_agent/models.yaml`)
- `TAVILY_API_KEY` for search
- Internet connection for data collection

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
# UFC Fight Sheet Generator

A Python application that automatically generates comprehensive fight sheets for UFC events scheduled for today. The application uses AI agents to collect detailed fighter information, statistics, and video links, then generates a beautifully formatted markdown document.

## Features

- **Event Detection**: Automatically checks if there's a UFC event scheduled for today using web search
- **Comprehensive Fighter Data**: Collects detailed information for each fighter including:
  - Basic info (height, weight, age, reach, stance)
  - Betting odds
  - Striking statistics (significant strikes per minute, accuracy, etc.)
  - Grappling statistics (takedown average, accuracy, submission average)
  - Fight records (overall, KO/TKO, submissions)
  - Last 5 fight results
- **Video Links**: Finds YouTube links to each fighter's 3 most recent fights with quality filtering (1000+ likes, no analysis/recap videos, must be freely viewable)
- **Web Search Integration**: Uses AI models with built-in web search capabilities for real-time information
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
   cd UFC-Fight-Sheet
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with your API keys:
   ```env
   # Google Vertex AI (for Gemini models)
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
   
   # OpenAI (for GPT models)
   OPENAI_API_KEY=your_openai_api_key
   
   # Anthropic (for Claude models)
   ANTHROPIC_API_KEY=your_anthropic_api_key
   
   # xAI (for Grok models)
   XAI_API_KEY=your_xai_api_key
   ```

4. **Configure models** (optional):
   Edit `llm/models.yaml` to customize which AI models are used for different tasks.

## Usage

Run the application:
```bash
python ufc_fight_sheet.py
```

### Command Line Options

- `--last-n-fights N`: Limit the number of fights to process to the last N fights in the event
  ```bash
  # Process only the last 5 fights (main event, co-main, and 3 prelims)
  python ufc_fight_sheet.py --last-n-fights 5
  
  # Process only the main event and co-main event
  python ufc_fight_sheet.py --last-n-fights 2
  ```

The application will:
1. Check for UFC events today
2. Collect detailed fight information (for all fights or limited subset)
3. Find video links for each fighter
4. Generate a markdown file named `ufc_fight_sheet_YYYYMMDD.md`

## Output Example

The generated markdown file will include:

```markdown
# UFC Fight Sheet - December 15, 2024

## Event: UFC Fight Night: Edwards vs. Covington

**Date:** December 15, 2024
**Total Fights:** 12

# Or when using --last-n-fights 5:
# UFC Fight Sheet - December 15, 2024

## Event: UFC Fight Night: Edwards vs. Covington

**Date:** December 15, 2024
**Fights Included:** Last 5 fights (limited from full event)

---

### 🏆 MAIN EVENT - Fight #12

**Weight Class:** Welterweight

| Stat | Fighter 1 | Fighter 2 |
|------|-----------|-----------|
| **Name** | Leon Edwards | Colby Covington |
| **Record** | 22-3-0 | 17-4-0 |
| **Age** | 32 | 35 |
| **Height** | 5'11" | 5'11" |
| **Reach** | 74" | 72" |
| **Stance** | Orthodox | Orthodox |
| **Betting Odds** | +150 | -170 |

#### Striking Stats
| Stat | Fighter 1 | Fighter 2 |
|------|-----------|-----------|
| **Sig Str LPM** | 3.12 | 4.54 |
| **Sig Str %** | 49% | 42% |
| **Sig Str ACC** | 58% | 45% |

#### Grappling Stats
| Stat | Fighter 1 | Fighter 2 |
|------|-----------|-----------|
| **TD AVG** | 1.23 | 3.45 |
| **TD ACC** | 35% | 45% |
| **SUB AVG** | 0.2 | 0.1 |

#### Records
| Record Type | Fighter 1 | Fighter 2 |
|-------------|-----------|-----------|
| **(T)KO** | 7-0-0 | 4-0-0 |
| **Submissions** | 3-0-0 | 4-0-0 |

#### Last 5 Fights
**Leon Edwards:**
1. W - Kamaru Usman (KO/TKO)
2. W - Kamaru Usman (Decision)
3. W - Nate Diaz (Decision)
4. W - Belal Muhammad (No Contest)
5. W - Rafael dos Anjos (Decision)

**Colby Covington:**
1. L - Kamaru Usman (Decision)
2. W - Tyron Woodley (TKO)
3. L - Kamaru Usman (TKO)
4. W - Robbie Lawler (Decision)
5. W - Demian Maia (Decision)

#### Recent Fight Videos
**Leon Edwards:**
1. [Fight Video 1](https://youtube.com/watch?v=...)
2. [Fight Video 2](https://youtube.com/watch?v=...)
3. [Fight Video 3](https://youtube.com/watch?v=...)
4. [Fight Video 4](https://youtube.com/watch?v=...)
5. [Fight Video 5](https://youtube.com/watch?v=...)

**Colby Covington:**
1. [Fight Video 1](https://youtube.com/watch?v=...)
2. [Fight Video 2](https://youtube.com/watch?v=...)
3. [Fight Video 3](https://youtube.com/watch?v=...)
4. [Fight Video 4](https://youtube.com/watch?v=...)
5. [Fight Video 5](https://youtube.com/watch?v=...)

---
```

## Architecture

The application uses a modular architecture with three main AI agents:

1. **Event Search Agent** (`event-search`): Checks for UFC events today
2. **Fight Info Agent** (`info-search`): Collects detailed fighter information
3. **Video Search Agent** (`video-search`): Finds high-quality YouTube video links for individual fighters

Each agent uses structured output parsing to ensure consistent and accurate data transfer between components.

## Configuration

### Model Configuration (`llm/models.yaml`)

You can customize which AI models are used for different tasks:

```yaml
# Available models and their providers
available_models:
  gemini-2.5-flash:
    provider: google_vertexai
    temperature: 0.0
  gpt-4o:
    provider: openai
    temperature: 0.0

# Task-to-model mapping
event-search:
  model_name: gemini-2.5-flash
info-search:
  model_name: grok-3-mini
video-search:
  model_name: gemini-2.5-pro
```

## Requirements

- Python 3.8+
- API keys for at least one of the supported AI providers
- Internet connection for data collection

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
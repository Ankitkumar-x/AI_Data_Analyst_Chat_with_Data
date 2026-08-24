# AI Data Analyst — LLM-Powered Conversational Analytics

An LLM-powered conversational analytics platform that allows users to upload structured datasets and interact with them using natural-language questions. The system combines agentic tool calling, Pandas analytics, and LLM-driven insights to enable seamless data exploration and visualization.

## Live Demo

**Frontend:**  
https://ai-chat-with-data.vercel.app

**Backend API:**  
https://ai-data-analyst-chat-with-data.onrender.com/docs

## Features

- Natural-language data analysis
- Agentic multi-step tool calling
- Dataset profiling and schema detection
- Automatic KPI detection
- Statistical analysis
- Filtering and conditional analysis
- Top-N and group comparison analysis
- Percentage contribution analysis
- Correlation and relationship analysis
- Automatic categorical analysis
- Automatic chart generation
- Bar, line, pie, scatter, and metric visualizations
- Multi-turn conversational context
- CSV and Excel upload support
- Production deployment with Vercel and Render

## System Architecture

```text
                         User
                           |
                           v
                    React + Vite
                   Vercel Frontend
                           |
                           | HTTPS / REST API
                           v
                    FastAPI Backend
                        Render
                           |
                +------------+------------+
                |            |            |
                v            v            v
             Pandas       Agent       Groq API
            Analytics      Tools         LLM
                |
                v
          Dataset Processing
```

## Technology Stack

### Frontend
- React
- Vite
- JavaScript
- CSS
- Plotly

### Backend
- Python
- FastAPI
- Pandas
- NumPy
- Pydantic
- Uvicorn

### AI & Analytics
- Groq API
- GPT-OSS-120B
- Prompt Engineering
- Function / Tool Calling
- Statistical Analysis
- Agentic Reasoning

### Deployment
- Vercel
- Render
- GitHub

## Analytical Capabilities

The platform supports operations including:

- Sum
- Average
- Minimum
- Maximum
- Count
- Top-N analysis
- Group comparison
- Conditional filtering
- Percentage share
- Correlation analysis
- Comparative analysis
- Time-series analysis
- Statistical summaries
- Business-oriented insight generation

## Workflow

```
Upload Dataset
      ↓
Dataset Profiling
      ↓
Natural-Language Query
      ↓
Intent Detection
      ↓
Tool Selection
      ↓
Pandas / Statistical Computation
      ↓
Multi-Step Analysis
      ↓
Visualization Generation
      ↓
LLM Insight Generation
      ↓
Final Response
```

## Testing

The project includes automated tests covering:

- Analysis tools
- Dataset profiler
- Dashboard APIs
- Upload API
- Chat API
- Integration workflow

## Engineering Highlights

- Agentic multi-step analytical workflow
- Dynamic function/tool calling
- Context-aware multi-turn reasoning
- Dataset-aware computation
- Automated visualization selection
- Production API integration
- Automated regression testing
- Environment-based configuration
- CORS and upload validation
- Error handling and temporary-file cleanup

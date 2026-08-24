# AI Data Analyst — LLM-Powered Conversational Analytics

An LLM-powered conversational analytics platform that allows users to upload structured datasets and interact with them using natural-language questions. The system combines agentic tool calling, Pandas-based analysis, automated visualizations, statistical analysis, and context-aware conversational reasoning.

## Live Demo

Frontend:
https://ai-chat-with-data.vercel.app

Backend API:
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
          +-----------+-----------+
          |           |           |
          v           v           v
       Pandas      Agent       Groq API
      Analytics    Tools        LLM
          |
          v
      Dataset
     Processing

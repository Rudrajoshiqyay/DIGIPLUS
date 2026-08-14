# Rules

This document outlines the coding standards, workflows, and operational rules for the Digiplus project.

## General Rules
1. **Maintain documentation integrity.** Preserve docstrings and comments.
2. **Follow specified architecture.** Ensure components align with the flowchart in `architecture.md`.
3. **Clean Code & Modularity.** Code must be clean, modular, and organized into logical directories (e.g., `src/`, `data/`). Avoid monolithic scripts.
4. **Git Readiness.** The repository must always be ready for a clean `git push`. Maintain a strict `.gitignore` to prevent committing virtual environments, raw data files, `.env` files, or cache files.
5. **Clean Data Principle.** All data must be validated and cleaned (handling nulls, standardizing types) before being ingested into the core pipelines.

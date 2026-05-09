# Chronostatistics

A longitudinal observational study of stochastic human arrival-time behavior under varying environmental and academic conditions.

## Overview

This repository contains:
- manually acquired event timing data,
- preprocessing scripts,
- statistical analyses,
- visualization tools,
- and a final report.

The project investigates temporal residuals between scheduled and observed arrival times across multiple event categories.

## Research Questions

Main questions include:
- What is the underlying distribution of arrival-time residuals?
- Are there measurable correlations with environmental variables?
- Do certain event classes induce stronger temporal deviations?
- Can punctuality be modeled perturbatively?

## Dataset

Recorded observables currently include:
- scheduled event time,
- observed arrival time,
- delay residual,
- event category,
- weather conditions,
- temperature,
- weekday,
- attendance state.

Additional observables may be introduced as statistics improve.

## Planned Analysis

- Distribution fitting
- Correlation analysis
- Time-series evolution
- Bayesian arrival prediction
- Perturbative reminder corrections
- Late-time asymptotics
- Rare-event punctuality detection

## Repository Structure

```text
data/           raw and processed datasets
plots/          generated figures
analysis/       notebooks and scripts
report/         LaTeX source for final paper
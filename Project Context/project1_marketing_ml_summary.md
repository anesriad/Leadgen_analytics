# Project 1 — Lead Acquisition Profitability System

## Goal of the project

Build an end-to-end machine learning and analytics project that answers real commercial and marketing questions, not just model questions.

The project should help a business understand:

- which traffic sources or campaigns bring the best customers
- which leads or users are most likely to convert
- which leads or users are most likely to bring strong revenue or commission
- where budget should be increased or reduced
- how to test whether model-based decisions improve business results

This project should feel close to a real lead generation or paid acquisition setup.

---

## Main project idea

Use a realistic acquisition dataset setup made of:

1. **Core lead or user outcome data**
   - either your interview lead dataset
   - or the public `theLook eCommerce` dataset from BigQuery

2. **A realistic marketing spend table**
   - channel / source / campaign / date / spend / clicks / impressions

3. **Optional event or behavior data**
   - sessions, events, page views, product interactions, etc.

Then combine them into one commercial analytics layer that lets you answer:

- revenue by source
- conversion rate by segment
- CAC by channel
- ROAS by campaign
- profit by segment
- predicted lead value or user value

---

## Recommended project framing

### Project title

**Lead Acquisition Profitability System**

### One-line positioning

An end-to-end ML system that predicts conversion and customer value, connects acquisition spend to downstream revenue, and helps optimize budget allocation.

### Why this project is strong

- It matches your background in analytics and commercial data.
- It gives you real business questions, not toy ML.
- It naturally includes EDA, testing, modeling, serving, deployment, and monitoring.
- It is strong for data scientist and ML engineer roles.
- It can become a solid YouTube project because it has both business meaning and technical depth.

---

## Best data options

## Option A — Best overall option

### Public base dataset

Use **Google BigQuery public dataset: `bigquery-public-data.thelook_ecommerce`**.

Main useful tables:

- `users`
- `events`
- `orders`
- `order_items`
- `products`

### Why this dataset is useful

- multi-table structure
- realistic joins
- user-level and order-level data
- traffic source information
- enough complexity for SQL and pipelines
- good fit for marketing and profitability analysis

### Important note

This dataset gives you user, order, and event data, but not full ad spend. That is why you add a spend table yourself.

---

## Option B — Strong if you want to stay close to the interview case

Use your **interview lead dataset** as the core base.

Then add:

- synthetic spend table
- campaign table
- optional enrichment table

### Why this is useful

- closest to the kind of analysis you already did
- likely better for lead scoring and commission prediction
- stronger commercial story for lead-gen companies

### Safe publishing approach

If you use the interview dataset, do not publish it raw. Instead:

- rename some columns if needed
- remove anything that could look internal
- slightly modify values if needed
- publish a cleaned or simulated version inspired by the original

---

## Recommended final choice

For the full project, the best balance is:

- use your **interview-style lead data** or a similar lead-style table for lead outcomes
- use **theLook** to understand how to structure realistic user / order / event logic
- create one **realistic spend table** that joins to your core table

If you want to keep it simple, start with one main dataset only:

### Simplest practical version

- core table = your lead dataset
- add spend table
- build end-to-end pipeline from there

---

## Business questions the project should answer

The project should be framed around business and marketing questions first.

### Commercial questions

- Which traffic sources bring the highest-quality users or leads?
- Which campaigns produce the highest commission or revenue?
- Which segments convert well but are not profitable?
- Which channels have poor CAC or weak ROAS?
- Which user or lead segments should get more budget?
- Which segments should be deprioritized?

### Product and ML questions

- Can we predict whether a user or lead will convert?
- Can we predict expected revenue or commission?
- Can we identify high-value leads early?
- Can we rank users or leads by expected value?
- Can we choose thresholds that improve profit, not just accuracy?

### Experimentation questions

- If the business uses model scores, how should it run an A/B test?
- What should the main success metric be?
- What guardrails should be watched?
- How would we test whether model-based budget allocation improves outcomes?

---

## Suggested success metrics

Your project should define three types of metrics.

## 1. ML metrics

Use depending on task:

- ROC AUC
- PR AUC
- F1 score
- precision at top K
- recall
- MAE / RMSE for revenue prediction

## 2. Business metrics

These matter most:

- conversion rate
- average commission or revenue
- CAC
- ROAS
- gross profit
- profit per lead
- percentage of high-value customers found in top model-ranked group

## 3. System metrics

These matter for ML engineering:

- inference latency
- API response time
- failed requests
- schema errors
- model drift indicators
- deployment cost estimate

---

## What data tables you need

## A. Core lead or user table

Examples of columns:

- `lead_id` or `user_id`
- `created_at`
- `traffic_source`
- `campaign`
- `device`
- `age_band`
- `region`
- `segment`
- `verified`
- `premium`
- `lead_status`
- `commission`
- `converted_flag`

## B. Spend table

You will likely create this yourself.

Suggested columns:

- `date`
- `traffic_source`
- `campaign`
- `ad_group` (optional)
- `spend`
- `clicks`
- `impressions`
- `ctr` (optional, can be calculated)
- `cpc` (optional, can be calculated)

## C. Optional event table

If using theLook or event-style logic:

- `user_id`
- `event_type`
- `event_timestamp`
- `session_id`
- `page_type`
- `product_category`

## D. Revenue or order table

If using order-style data:

- `order_id`
- `user_id`
- `order_timestamp`
- `revenue`
- `status`
- `product_category`

---

## How the spend table should connect to the core data

Keep the join logic simple and believable.

### Best join keys

Join on:

- `date`
- `traffic_source`
- `campaign`

Example logic:

- core dataset has user or lead created date
- core dataset has source and campaign
- spend dataset has daily spend by source and campaign

Then you aggregate your outcomes by the same level.

### Example final analytics grain

A final analytics table could look like this:

| date | traffic_source | campaign | spend | clicks | impressions | leads | conversions | revenue | commission | profit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|

This becomes your marketing performance layer.

### Why this makes sense

In real companies, spend usually comes from ad platforms, while conversions and revenue come from CRM or product systems. The data is rarely stored in one perfect source. Joining separate systems is realistic.

---

## Approach to the data

## Step 1 — Understand the grain

Before coding too much, answer:

- Is each row a lead, a user, an event, or an order?
- What is the time unit?
- What columns describe acquisition?
- What columns describe outcomes?
- What columns describe commercial value?

## Step 2 — Create a data map

Write down:

- table name
- row grain
- primary key
- join keys
- useful columns
- target columns

## Step 3 — Build a clean staging layer

Create three layers:

- `raw`
- `staging`
- `mart` or `analytics`

### raw
Original extracted files or query outputs

### staging
Basic cleaning and type fixing

### mart / analytics
Joined tables used for EDA, business metrics, and ML

## Step 4 — Decide the prediction target early

Choose one main target first.

Good options:

- `converted_flag`
- `high_value_flag`
- `expected_commission`
- `expected_revenue`

Do not start with too many targets at once.

### Best first target

Start with:

**Will this lead or user convert?**

Then later add:

**Will this lead or user be high value?**

---

## Data quality checks you should include

These checks are very important because they make the project feel real.

### Schema checks

- required columns exist
- data types are correct

### Null checks

- missing values in key columns
- missing target values
- missing acquisition source

### Duplicate checks

- duplicate lead IDs
- duplicate order IDs
- duplicate user IDs where not expected

### Range checks

- negative revenue
- negative commission
- impossible ages
- future timestamps

### Category checks

- unexpected traffic sources
- campaign naming inconsistencies
- strange status values

### Join coverage checks

- percentage of leads or users that fail to join to spend
- percentage of orders with no matching user

### Leakage checks

- do not use post-conversion fields when predicting conversion
- do not use future data in features

---

## EDA plan

Your notebook should first answer business questions before modeling.

### Basic EDA

- row counts
- date coverage
- null summary
- unique values for main categories
- target balance

### Business EDA

- revenue by source
- conversion rate by source
- commission by segment
- performance by device
- performance by region
- performance over time
- spend vs revenue by campaign
- CAC and ROAS by source

### Behavioral EDA if event data is used

- sessions before conversion
- time from first visit to conversion
- event patterns of high-value users

### Segment deep dives

- age band x source
- device x source
- region x campaign
- verified vs non-verified

---

## Hypothesis testing ideas

You said you want hypothesis testing in the workflow, so add a few practical tests.

Examples:

- Is conversion rate different between mobile and desktop?
- Is average commission different between verified and non-verified leads?
- Do some traffic sources bring significantly higher-value users?
- Are some campaigns producing significantly worse ROAS?

Keep it practical. You do not need a huge stats thesis. Just run useful tests that support business decisions.

---

## ML tasks to include

## Task 1 — Conversion prediction

### Goal
Predict whether a lead or user will convert.

### Why it matters
Useful for scoring, prioritization, routing, and targeting.

### Possible features
- source
- campaign
- device
- age band
- region
- event counts
- recency
- verification flag
- page depth
- previous activity features

## Task 2 — High-value user or lead prediction

### Goal
Predict whether a converted lead or user will become high value.

### Why it matters
Strong for budget allocation and prioritization.

### Target examples
- top 20 percent by commission
- top 20 percent by revenue
- above-threshold expected value

## Task 3 — Revenue or commission prediction

### Goal
Predict expected value as a regression task.

This can be a second phase after classification.

---

## Modeling approach

Start simple, then improve.

### Baseline models

- logistic regression for classification
- linear regression for regression

### Stronger models

- random forest
- XGBoost
- LightGBM if you want

### Important modeling practices

- time-based split if there is time order
- avoid leakage
- use class imbalance handling if needed
- compare baseline vs stronger model
- perform error analysis
- inspect feature importance

---

## Threshold logic

This is one of the most important business parts.

Do not just say:

- model A has better AUC

Also answer:

- what score threshold should the business use?
- what happens to precision and recall at different thresholds?
- how does that affect profit?

### Example business threshold logic

If the model predicts high conversion probability:

- send to premium sales team
- increase budget on that campaign or segment
- prioritize follow-up

If model confidence is low:

- do not fully trust the model
- use fallback business rules
- route to standard workflow

---

## Experimentation and A/B testing layer

This should not be fake. Keep it tied to the real business decision.

### A/B testing idea

Test whether model-based prioritization improves business outcomes.

### Example experiment

#### Control group
Current manual or rules-based routing

#### Treatment group
Routing or budget prioritization based on model score

### Primary metrics
- conversion rate
- profit per lead
- revenue per lead

### Guardrail metrics
- CAC
- lead quality complaints
- response time
- over-concentration on one source

### Why this matters
It shows that you understand that a model is useful only if it improves real business outcomes.

---

## Project architecture

Keep the architecture simple and realistic.

### Flow

1. Data pulled from source files or BigQuery
2. Raw files stored locally or in S3
3. Cleaning and validation pipeline
4. Analytics table built
5. Notebook used for EDA and initial experiments
6. Feature pipeline created in Python scripts
7. Model training pipeline created
8. Best model saved and tracked
9. FastAPI app serves predictions
10. Docker container packages app
11. CI/CD builds and deploys
12. Monitoring checks input data, predictions, and API health

---

## Tools to use

Use one stable stack across the whole project.

## Data and analysis

- **SQL** for querying and joining data
- **Python** for the main project language
- **Pandas** or **Polars** for manipulation
- **Jupyter Notebook** for EDA and first experiments
- **Matplotlib / Plotly** for charts

## Data quality and validation

- **Pandera** or **Great Expectations** for checks
- optional: **Pydantic** for request validation in the API

## ML

- **scikit-learn** for baselines and pipelines
- **XGBoost** for stronger tabular models
- **MLflow** for experiment tracking and model registry

## Backend and serving

- **FastAPI** for prediction API
- **Pydantic** for request schemas

## Packaging and deployment

- **Docker** for containerization
- **GitHub Actions** for CI/CD
- **AWS S3** for artifacts or data
- **AWS App Runner**, **Lambda**, or a simple compute option for deployment
- **CloudWatch** for logs if using AWS

## Monitoring

- logging of requests and predictions
- simple drift checks
- latency tracking
- schema failure tracking

## UI

- **Streamlit** for a simple interface

---

## Suggested folder structure

```text
project/
├── README.md
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda_and_hypothesis_testing.ipynb
│   └── 03_modeling_experiments.ipynb
├── data/
│   ├── raw/
│   ├── staging/
│   └── mart/
├── src/
│   ├── data/
│   │   ├── extract.py
│   │   ├── clean.py
│   │   └── validate.py
│   ├── features/
│   │   └── build_features.py
│   ├── models/
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   └── predict.py
│   ├── pipelines/
│   │   └── run_pipeline.py
│   └── monitoring/
│       ├── drift.py
│       └── logging_utils.py
├── app/
│   └── main.py
├── tests/
├── configs/
├── architecture/
│   └── architecture.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/
    └── workflows/
```

---

## Suggested project phases

## Phase 1 — Data understanding and analytics layer

Goal:
Understand all tables, join logic, and commercial metrics.

Deliverables:
- data map
- clean joined analytics table
- first SQL queries
- first EDA notebook

## Phase 2 — Business analysis and hypothesis testing

Goal:
Answer commercial questions like a strong analyst.

Deliverables:
- conversion analysis
- revenue and commission analysis
- CAC and ROAS analysis
- practical hypothesis tests

## Phase 3 — ML experimentation

Goal:
Build and compare models for conversion and value prediction.

Deliverables:
- baseline model
- stronger model
- evaluation notebook
- threshold analysis

## Phase 4 — Pipelines and quality checks

Goal:
Move notebook logic into clean Python scripts.

Deliverables:
- extraction script
- cleaning script
- validation checks
- feature builder
- train pipeline
- inference pipeline

## Phase 5 — Serving and deployment

Goal:
Make the model usable.

Deliverables:
- FastAPI app
- Docker image
- deployment to AWS or temporary live demo
- Streamlit app if useful

## Phase 6 — Monitoring and documentation

Goal:
Make the project feel production-aware.

Deliverables:
- drift script
- prediction logging
- latency tracking
- architecture doc
- polished README

---

## Example first analytics outputs

These are the first business tables and charts you should build.

### Table 1 — Source performance

- traffic source
- users or leads
- conversions
- conversion rate
- revenue or commission
- average revenue or commission

### Table 2 — Campaign profitability

- date
- campaign
- spend
- conversions
- revenue
- profit
- ROAS

### Table 3 — Segment quality

- age band
- device
- region
- verified flag
- conversion rate
- commission or revenue

### Charts

- spend vs revenue over time
- ROAS by campaign
- conversion rate by source
- distribution of revenue or commission
- high-value segment comparison

---

## Example first model outputs

### Conversion model

Output:
Probability of conversion

Use case:
- prioritize follow-up
- score incoming leads
- rank channels or campaigns by likely outcome

### Value model

Output:
Expected revenue or commission

Use case:
- identify high-value leads
- support budget allocation
- improve CAC efficiency

---

## How to talk about this project in interviews

When describing the project, use this structure:

1. **Business problem**
   - the company spends on acquisition and wants profitable growth

2. **Data problem**
   - spend, lead outcomes, and revenue are split across different datasets

3. **Analytics work**
   - build one joined commercial view to measure conversion, CAC, ROAS, and profit

4. **ML work**
   - predict conversion and high-value leads

5. **Decision layer**
   - select thresholds based on business value

6. **Experimentation layer**
   - propose A/B test to validate impact

7. **Engineering layer**
   - package as API, deploy, monitor, and document

This makes you sound both commercial and technical.

---

## Strong practical starting plan

If starting fresh in a new conversation, use this sequence.

### Step 1
Pick the core dataset:
- your lead dataset, or
- theLook public dataset

### Step 2
Create a simple spend table with:
- date
- source
- campaign
- spend
- clicks
- impressions

### Step 3
Build one clean analytics table joined by:
- date
- traffic_source
- campaign

### Step 4
Do EDA first and answer:
- best source
- worst source
- best segment
- worst segment
- where profit comes from

### Step 5
Choose the first model target:
- conversion prediction

### Step 6
Build a baseline model, then a stronger model

### Step 7
Move notebook logic into scripts

### Step 8
Serve predictions through FastAPI

### Step 9
Containerize with Docker

### Step 10
Deploy briefly and add simple monitoring

---

## Final project outcome

By the end, this project should show that you can:

- frame a commercial problem clearly
- work with realistic, messy data
- build a joined analytics layer
- answer strong marketing and business questions
- run EDA and hypothesis testing
- build useful ML models
- choose thresholds based on business value
- think about experimentation properly
- package and deploy a model
- include monitoring and basic production thinking

That makes this project strong for both:

- data scientist roles
- ML engineer roles

---

## Reusable prompt for a new conversation

```text
I want to build Project 1: a Lead Acquisition Profitability System.

Goal:
Build an end-to-end ML and analytics project that connects acquisition spend to lead or user outcomes, predicts conversion and value, and helps optimize budget allocation.

I want the project to include:
- business framing
- dataset design and join logic
- SQL queries
- data cleaning and quality checks
- EDA
- hypothesis testing
- feature engineering
- ML modeling
- threshold logic
- A/B testing design
- Python pipelines
- FastAPI serving
- Docker
- CI/CD
- AWS deployment
- monitoring
- architecture documentation

Help me structure the project step by step, starting with the data model, the first SQL queries, and the first notebook plan.
```

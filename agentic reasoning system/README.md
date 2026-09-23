<div align="center">
  <h1>Agentic Reasoning System for Logic QA</h1>

  <p>
    <a href="#"><img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version"></a>
    <a href="#"><img src="https://img.shields.io/badge/AI-Agentic%20Reasoning-orange.svg" alt="Agentic AI"></a>
    <a href="#"><img src="https://img.shields.io/badge/Logic-Symbolic%20Solver-00A4EF.svg" alt="Symbolic Logic"></a>
    <a href="#"><img src="https://img.shields.io/badge/Data-CSV%20Processing-lightgrey.svg" alt="CSV Processing"></a>
  </p>

  <p><em>A modular, explainable system for multi-step logic question answering featuring subproblem decomposition, dynamic tool selection, and comprehensive reasoning traces.</em></p>
</div>

<hr>

<h2>Overview</h2>
<p>This project implements an advanced agentic reasoning pipeline designed to tackle complex logic-based question answering. By decomposing multifaceted problems into manageable subproblems, the system intelligently routes each task to the optimal solver—either a deterministic symbolic rule engine or a Large Language Model (LLM) stub. The result is a highly explainable, confidence-weighted prediction system backed by robust trace logging and consistency verification.</p>

<h2>Architecture Flow</h2>
<p>The system utilizes a multi-stage pipeline to ensure logical consistency and accurate answer prediction across diverse problem sets.</p>

<pre><code>
[ DATA INGESTION ]
 • Robust CSV/TSV Parsing
 • Training Pattern Mapping
        │
        ▼
[ PROBLEM DECOMPOSITION ]
 • Subproblem Extraction (parser.py)
        │
        ▼
[ DYNAMIC TOOL SELECTION ]
 • Heuristic Routing (tool_selector.py)
 ├──&gt; Symbolic Solver (Negations, Universals, Possibility)
 └──&gt; LLM Interface Stub (Semantic Reasoning)
        │
        ▼
[ REASONING &amp; VERIFICATION ]
 • Trace Generation (trace_generator.py)
 • Consistency Verification (verifier.py)
        │
        ▼
[ AGGREGATION &amp; PREDICTION ]
 • Training-Pattern Overrides
 • Confidence-Weighted Aggregation
 • Output Generation (output.csv)
</code></pre>

<hr>

<h2>Key Features</h2>
<ul>
  <li><strong>Intelligent Decomposition:</strong> Automatically breaks down complex logical premises into addressable subproblems.</li>
  <li><strong>Dynamic Tool Selection:</strong> Uses heuristic routing to choose between symbolic execution and LLM-based reasoning based on subproblem requirements.</li>
  <li><strong>Advanced Symbolic Solver:</strong> Specifically tuned to handle negations, universal quantifiers, and possibility cues.</li>
  <li><strong>Hybrid Aggregation:</strong> Combines training-pattern overrides with confidence-weighted scoring to generate final predictions.</li>
  <li><strong>Explainability &amp; Tracing:</strong> Generates highly detailed reasoning traces for each step and performs automated consistency verification.</li>
  <li><strong>Robust Data Handling:</strong> Features a fault-tolerant CSV loader capable of handling delimiter and formatting inconsistencies.</li>
</ul>

<hr>

<h2>Project Structure</h2>

<details>
<summary><strong>Click to expand: Repository Structure</strong></summary>
<br>
<pre><code>.
├── main.py                             # Core orchestration and aggregation logic
├── requirements.txt                    # Project dependencies
├── configs/
│   └── system_config.yaml              # System parameters and routing weights
├── modules/
│   ├── parser.py                       # Problem decomposition logic
│   ├── tool_selector.py                # Heuristic solver routing
│   ├── symbolic_solver.py              # Rule-based logic engine
│   ├── base_llm_interface.py           # LLM integration stub
│   ├── verifier.py                     # Trace and logic consistency checking
│   └── trace_generator.py              # Step-by-step reasoning logger
├── datasets/
│   ├── train.csv                       # Training data and pattern mapping
│   └── test.csv                        # Evaluation dataset
└── output.csv                          # Generated predictions and traces
</code></pre>
</details>

<hr>

<h2>Data Format Requirements</h2>

<p>The system expects input data in CSV format with the following core columns:</p>
<ul>
  <li><code>problemstatement</code>: The full text of the logical problem.</li>
  <li><code>topic</code>: The logical domain or category of the problem.</li>
  <li><code>answeroption1</code>, <code>answeroption2</code>, etc.: The available multiple-choice answers.</li>
  <li><code>correctoptionnumber</code>: The integer corresponding to the correct answer (Required in <code>train.csv</code> for pattern mapping; optional in <code>test.csv</code>).</li>
</ul>

<hr>

<h2>Getting Started</h2>

<h3>Prerequisites</h3>
<ul>
  <li>Python 3.8 or higher</li>
</ul>

<h3>Installation</h3>

<ol>
  <li>
    <strong>Clone the repository</strong>
<pre><code>git clone &lt;repository-url&gt;
cd agentic-reasoning-qa</code></pre>
  </li>
  <li>
    <strong>Install dependencies</strong>
<pre><code>pip install -r requirements.txt</code></pre>
  </li>
</ol>

<h3>Execution</h3>
<p>Run the main pipeline to process the datasets, generate predictions, and output the reasoning traces.</p>
<pre><code>python main.py</code></pre>

<hr>

<h2>Output Example</h2>
<p>The system generates an <code>output.csv</code> file containing the final predictions alongside the complete reasoning trace. Below is an example of the output structure:</p>

<table>
  <thead>
    <tr>
      <th>topic</th>
      <th>problem_statement</th>
      <th>solution</th>
      <th>correct option</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Quantifiers</td>
      <td>If all mammals breathe air, and whales are mammals, do whales...</td>
      <td><strong>Predicted option:</strong> 1 <br> <strong>Trace:</strong> Step 1: ... <br> <strong>Verification:</strong> True</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

<hr>

<h2>Customization &amp; Extension</h2>
<ul>
  <li><strong>Symbolic Rules:</strong> Tune keywords, quantifiers, and logical mappings within <code>modules/symbolic_solver.py</code>.</li>
  <li><strong>Heuristics:</strong> Extend or modify the logic routing conditions in <code>modules/tool_selector.py</code> to support new domains.</li>
  <li><strong>Scoring Mechanisms:</strong> Improve the confidence weighting functions and pattern mapping algorithms located in <code>main.py</code>.</li>
</ul>

<hr>

<div align="center">
  <p><i>Building modular, explainable pathways for multi-step artificial intelligence.</i></p>
</div>

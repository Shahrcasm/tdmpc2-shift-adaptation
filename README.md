# DA-TDMPC2 — Test-Time Task Embedding Adaptation for Neural World Models

**Course:** CSE 465 — Pattern Recognition and Neural Network  
**Faculty:** Dr. Mohammad Ashrafuzzaman Khan  
**Base Paper:** *TD-MPC2: Scalable, Robust World Models for Continuous Control* (Hansen et al., ICLR 2024)  
**Detailed Guide & Defense Q&A:** See [PROJECT_GUIDE.md](PROJECT_GUIDE.md)

---

## 1. Project Summary & Single Novelty

Pretrained neural world models like **TD-MPC2** learn to predict physical state transitions $(s_t, a_t) \to s_{t+1}$ across 30 continuous control tasks (`mt30-5M.pt`, containing **5,241,066 parameters**). However, when deployed under a **physical dynamics shift** (such as a robot carrying **1.5× heavier mass** or stepping on a **slippery floor**), the true physics changes, latent prediction error spikes, and control performance degrades.

Fine-tuning all 5.2 million neural network weights on a small test-time transition buffer is slow and causes catastrophic overfitting.

### Our Single Novelty: Test-Time Task Embedding Adaptation (`C2`)
Instead of retraining or fine-tuning the network, we:
1. **Freeze all 5,241,066 neural network weights** (encoder, dynamics, reward, policy prior, and Q-heads).
2. **Optimize only the 64-dimensional task embedding vector ($e$)** for the current task using standard PyTorch Adam gradient descent on the latent transition consistency loss:
   $$\mathcal{L}(e) = \frac{1}{K} \sum_{t=1}^{K} \| d(h(s_t, e), a_t, e) - h(s_{t+1}, e_0) \|^2$$
3. Because a physical shift is low-dimensional, updating only **64 parameters** ($0.0012\%$ of the model) acts as a strong regularizer and adapts in **0.27 seconds on a laptop CPU** ([`results/P2_adapt/demo_walker_walk_mass_1.5/summary.json`](results/P2_adapt/demo_walker_walk_mass_1.5/summary.json)).

---

## 2. Standard Pattern Recognition & Neural Network Pipeline

| Stage | Module / File | Description |
|---|---|---|
| **1. Data & Physical Shift Simulation** | [`src/datdmpc/envs/perturb.py`](src/datdmpc/envs/perturb.py) | Wraps DMControl / MuJoCo tasks with physical perturbations (`mass`, `friction`, `actuator`, `gravity`, `obs_noise`, `action_delay`) and collects $(s_t, a_t, r_t, s_{t+1})$ transitions. |
| **2. Data Preprocessing** | [`src/datdmpc/eval/harness.py`](src/datdmpc/eval/harness.py) | `SingleTaskMultitaskEnv` zero-pads task observations to 24 dimensions and truncates actions to the task's action space for the 30-task world model. |
| **3. Neural Network Architecture** | [`src/datdmpc/_upstream.py`](src/datdmpc/_upstream.py) & `DeviceAwareTDMPC2` | Pretrained TD-MPC2 world model (`Encoder` $h$, `Dynamics` $d$, `Reward` $R$, `Policy` $\pi$, `Q-Ensemble`) conditioned on a $30 \times 64$ task embedding table (`nn.Embedding(30, 64, max_norm=1)`). |
| **4. Pattern Prediction & Shift Error** | [`run_demo.py`](run_demo.py) | Measures one-step latent prediction Mean Squared Error (MSE) under nominal physics vs. shifted physics. |
| **5. Single Novelty (Embedding Adaptation)** | [`src/datdmpc/adapt/embedding.py`](src/datdmpc/adapt/embedding.py) | Freezes all network weights, masks gradients to the active task row `task_idx`, and runs Adam gradient descent on the 64-D embedding vector. |
| **6. Evaluation & Interactive UI** | [`streamlit_app.py`](streamlit_app.py) & [`scripts/eval.py`](scripts/eval.py) | Interactive Streamlit dashboard and CLI evaluation harness comparing Nominal vs. Shifted (Frozen) vs. Adapted (Ours). |

---

## 3. Verified Experimental Results (`walker-walk`, `mass:1.5`)

Measured via [`run_demo.py`](run_demo.py) on `checkpoints/mt30-5M.pt` and recorded in [`results/P2_adapt/demo_walker_walk_mass_1.5/summary.json`](results/P2_adapt/demo_walker_walk_mass_1.5/summary.json):

| Condition | Parameters Updated | Transition Prediction MSE | 5-Step Control Return | Wall-Clock Adaptation Time |
|---|---|---|---|---|
| **1. Nominal (`none`)** | `0` (Pretrained) | `0.000297` | `6.31` *(500-step full episode return: `506.97`, [`outputs/debug/mt30-5M__walker-walk__none__B0__seed0/summary.json`](outputs/debug/mt30-5M__walker-walk__none__B0__seed0/summary.json))* | `0.00 s` |
| **2. Shifted (`mass:1.5`, Frozen)** | `0` (Frozen) | `0.000537` (**+80.7% error spike**) | `5.61` | `0.00 s` |
| **3. Ours (`e_only` Adapted)** | **`64` numbers** (`0.0012%`) | **`0.000365`** (**-32.0% error reduction**; `0.000203` on fresh rollout) | **`6.99`** | **`0.27 s`** (`15` steps, `lr=0.002`) |

---

## 4. Quickstart: Running & Deploying the Demo

### A. Deploy to Streamlit Community Cloud (Run in Any Web Browser)
1. Push your branch to GitHub:
   ```powershell
   git push origin dev_shahriar
   ```
2. Open [share.streamlit.io](https://share.streamlit.io), click **"Create app"**, and select:
   - **Repository:** `Shahrcasm/tdmpc2-shift-adaptation`
   - **Branch:** `dev_shahriar`
   - **Main file path:** `streamlit_app.py`
3. Click **Deploy**. The app installs [`requirements.txt`](requirements.txt), automatically fetches `mt30-5M.pt` from Hugging Face on first run, and provides an interactive dashboard with live PyTorch adaptation in **< 1 second**.

### B. Local Setup & Terminal Demo (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e . --no-deps

# 1. Fetch and verify pretrained checkpoint (SHA-256 verified)
python scripts/get_checkpoints.py --models mt30-5M

# 2. Run the end-to-end CLI demo
python run_demo.py --steps 5 --grad-steps 15 --lr 0.002

# 3. Launch the interactive Streamlit UI locally
streamlit run streamlit_app.py

# 4. Run the full 66-test automated test suite
pytest -q
```

---

## 5. Team & Repository Governance

| Slot | Name | Student ID | Branch |
|---|---|---|---|
| **M1** | Md. Shahriar Rakib Rabbi | 2321937642 | `dev_shahriar` |
| **M2** | Md. Ishtiak Ahmed Moyen | 2131580642 | `dev_ishtiak` |
| **M3** | Md. Abdullah Talha | 2222614642 | `dev_talha` |

- **Presentation & Defense Guide:** [PROJECT_GUIDE.md](PROJECT_GUIDE.md)
- **Rules & File Ownership:** [AGENTS.md](AGENTS.md)
- **Status & Task Board:** [docs/STATUS.md](docs/STATUS.md)
- **Research Specification:** [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md)
- **Execution Manual:** [docs/RUNS.md](docs/RUNS.md)

---

## 6. Upstream Attribution & License

`third_party/tdmpc2/` is an unmodified copy of [nicklashansen/tdmpc2](https://github.com/nicklashansen/tdmpc2) at commit `e9f59321933cbc8e11a002b842adc7d4ffae8ff1` (MIT License, copyright Nicklas Hansen). Our code in `src/datdmpc/` extends upstream without modifying `third_party/` and is released under the [MIT License](LICENSE).

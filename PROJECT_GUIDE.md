# DA-TDMPC2: Domain Adaptation in Neural World Models (CSE 465)

**Course:** Pattern Recognition and Neural Network (CSE 465)  
**Faculty:** Dr. Mohammad Ashrafuzzaman Khan  
**Project:** Fast Test-Time Task Embedding Adaptation under Physical Dynamics Shift  
**Base Research Paper:** *TD-MPC2: Scalable, Robust World Models for Continuous Control* (Hansen et al., ICLR 2024)

---

## 1. Project Overview & The Core Problem

In robotics and physical control systems, neural networks are trained to recognize temporal dynamics patterns:
$$\text{Current State } (s_t) + \text{Action } (a_t) \xrightarrow{\text{Neural World Model}} \text{Predicted Next State } (\hat{s}_{t+1})$$

The state-of-the-art model **TD-MPC2** (ICLR 2024) trains a single 5.2-million-parameter multitask neural network to control 30 different physical tasks (`mt30-5M.pt`). However, it has a critical real-world limitation:
- **The Problem:** The neural network is trained and evaluated in a fixed, nominal simulator. When deployed under **physical dynamics shift**—such as a robot becoming **50% heavier** (`mass:1.5`) or walking on a **slippery surface** (`friction:0.5`)—the physical transition pattern changes, prediction error spikes, and control degrades.
- **Why Full Retraining Fails:** Fine-tuning all **5,241,066 neural network weights** on a small test-time sample causes severe **catastrophic overfitting**, forgets previously learned tasks, and is computationally too slow for real-time control.

---

## 2. Our Single Novelty: "Test-Time Task Embedding Adaptation"

Instead of modifying millions of network weights, we focus on **one simple, effective novelty**:

> **The Single Improvement:**  
> When a physical shift occurs, we **freeze all 5,241,066 neural network weights** and optimize **only the 64-dimensional learned task embedding vector ($e$)** for the current task using standard PyTorch gradient descent (backpropagation) on observed transition prediction errors.

### Why This Works Academically:
1. **Low-Dimensional Shift:** Physical changes (like mass or friction scaling) are low-dimensional changes. Updating 5.2M parameters introduces millions of unnecessary degrees of freedom. Updating **only 64 parameters** ($0.0012\%$ of the network) acts as a strong regularizer against overfitting.
2. **Real-Time CPU Speed:** 15 Adam gradient steps on the 64-dimensional embedding take **0.27 seconds on a laptop CPU** (`results/P2_adapt/demo_walker_walk_mass_1.5/summary.json`).
3. **Zero Catastrophic Forgetting:** Because all encoder, dynamics, reward, policy, and Q-network weights remain frozen, the rest of the multitask world model is never corrupted.

---

## 3. Standard Pattern Recognition & Neural Network Pipeline

The project follows the standard 6-stage pipeline taught in CSE 465:

```
[1. Data Collection]  --> Collect (s_t, a_t, s_{t+1}) transitions under nominal & shifted physics
        ↓
[2. Preprocessing]    --> Zero-padding observations to 24-D, action truncation, tensor batching
        ↓
[3. Neural Network]   --> Encoder h(s, e) -> Latent Dynamics d(z, a, e) -> Policy & Q-Heads
        ↓
[4. Pattern Recog.]   --> Predict next latent state; measure MSE spike under physical shift
        ↓
[5. OUR NOVELTY]      --> Freeze 5.2M weights; run 15 Adam steps on 64-D embedding 'e' (lr=0.002)
        ↓
[6. Evaluation]       --> Compare Transition MSE & Control Return: Nominal vs. Shifted vs. Adapted
```

---

## 4. Verified Experimental Results

All numbers below come from actual executions of [`run_demo.py`](run_demo.py) on `checkpoints/mt30-5M.pt` (`walker-walk` under `mass:1.5`, recorded in [`results/P2_adapt/demo_walker_walk_mass_1.5/summary.json`](results/P2_adapt/demo_walker_walk_mass_1.5/summary.json)):

| Condition | Parameters Updated | Transition Prediction MSE | 5-Step Control Return | Notes |
|---|---|---|---|---|
| **1. Nominal (Normal Physics)** | `0` (Pretrained) | `0.000297` | `6.31` | Full 500-step episode return = `506.97` (`outputs/debug/mt30-5M__walker-walk__none__B0__seed0/summary.json`) |
| **2. Shifted (`mass:1.5`, Frozen)** | `0` (Frozen) | `0.000537` (**+80.7% error spike**) | `5.61` | Unadapted model suffers large prediction mismatch |
| **3. Ours (`e_only` Adapted)** | **`64` numbers** (`0.0012%`) | **`0.000365`** (**-32.0% error drop**; `0.000203` on fresh rollout) | **`6.99`** | Converged in **0.27 seconds** on laptop CPU (`15` steps, `lr=0.002`) |

---

## 5. How to Run the Demo (3 Ways)

### Way 1: Streamlit Cloud Web App (No Local Setup Needed — Open in Any Browser)
1. Push your branch to GitHub:
   ```powershell
   git push origin dev_shahriar
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
3. Click **"Create app"** (or **"New app"**):
   - **Repository:** `Shahrcasm/tdmpc2-shift-adaptation`
   - **Branch:** `dev_shahriar`
   - **Main file path:** `streamlit_app.py`
4. Click **"Deploy!"**
   - Streamlit Cloud reads [`requirements.txt`](requirements.txt), automatically downloads and verifies `mt30-5M.pt` from Hugging Face on first boot, and gives you a permanent web link (`https://...streamlit.app`) you can open on any classroom computer.

### Way 2: Run the Streamlit Web UI Locally
```powershell
.\.venv\Scripts\Activate.ps1
pip install streamlit
streamlit run streamlit_app.py
```

### Way 3: Run the Terminal Demo Script
```powershell
.\.venv\Scripts\Activate.ps1
python run_demo.py --steps 5 --grad-steps 15 --lr 0.002
```

---

## 6. Defense Guide for Your Professor (Q&A)

### Q1: "What is your exact contribution over the TD-MPC2 paper?"
> *"The original TD-MPC2 paper (ICLR 2024) evaluates its pretrained multitask world model only in the nominal training simulator. When physical dynamics shift at test time—such as a 1.5x increase in body mass—latent transition prediction error spikes by +80.7%. Our contribution is a lightweight test-time adaptation method that freezes all 5,241,066 neural network weights and updates only the 64-dimensional task embedding vector via gradient descent on observed transitions."*

### Q2: "Why update only 64 numbers instead of fine-tuning the whole network?"
> *"Fine-tuning 5.2 million parameters on a small buffer of transitions causes severe overfitting and destroys the pretrained representations. Because physical shifts like mass or friction scaling are low-dimensional changes, restricting gradient updates to the 64-dimensional task embedding acts as a strong regularizer and adapts in 0.27 seconds on a CPU."*

### Q3: "What loss function do you optimize during adaptation?"
> *"We minimize the Mean Squared Error (MSE) latent transition consistency loss against the fixed nominal encoder target:
> $$\mathcal{L}(e) = \frac{1}{K} \sum_{t=1}^K \| d(h(s_t, e), a_t, e) - h(s_{t+1}, e_0) \|^2$$
> Fixing the target encoder at the initial nominal embedding $e_0$ prevents moving-target collapse while aligning the dynamics prediction with the shifted environment."*

### Q4: "How does this connect to Pattern Recognition and Neural Networks?"
> *"The world model is a neural sequence predictor that recognizes the input-output pattern $(s_t, a_t) \to s_{t+1}$. A physical perturbation creates an out-of-distribution domain shift. Our method performs representation-space adaptation by moving the 64-dimensional task embedding in latent space to match the new physical pattern."*
